// Follow one competitor through a folder of frames: seed = human nearest seedX (or rightmost if seedX < 0),
// then each frame: VNTrackObjectRequest prediction, snapped to the best-overlapping detected human.
// usage: swift track_gab.swift <framesDir> <seedX|-1> <out.json>
import AppKit
import Vision

let a = CommandLine.arguments
let dir = a[1], seedX = Double(a[2])!, outPath = a[3]
let files = try! FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".jpg") }.sorted()
func load(_ f: String) -> CGImage {
    let s = CGImageSourceCreateWithURL(URL(fileURLWithPath: dir + "/" + f) as CFURL, nil)!
    return CGImageSourceCreateImageAtIndex(s, 0, nil)!
}
func humans(_ img: CGImage) -> [CGRect] {
    let r = VNDetectHumanRectanglesRequest(); r.upperBodyOnly = false
    try? VNImageRequestHandler(cgImage: img).perform([r])
    return (r.results ?? []).map { $0.boundingBox }.filter { $0.height > 0.25 }   // ignore the audience
}
func iou(_ p: CGRect, _ q: CGRect) -> Double {
    let i = p.intersection(q); if i.isNull { return 0 }
    return Double(i.width * i.height) / Double(p.width * p.height + q.width * q.height - i.width * i.height)
}
let seq = VNSequenceRequestHandler()
var obs: VNDetectedObjectObservation? = nil
var out: [[String: Double]] = []
var last: CGRect? = nil
for (k, f) in files.enumerated() {
    let img = load(f)
    let hs = humans(img)
    var box: CGRect? = nil
    if obs == nil {
        box = seedX < 0 ? hs.max { $0.midX < $1.midX } : hs.min { abs(Double($0.midX) - seedX) < abs(Double($1.midX) - seedX) }
    } else {
        let req = VNTrackObjectRequest(detectedObjectObservation: obs!); req.trackingLevel = .accurate
        try? seq.perform([req], on: img)
        if let r = req.results?.first as? VNDetectedObjectObservation {
            let pred = r.boundingBox
            let best = hs.max { iou($0, pred) < iou($1, pred) }
            if let b = best, iou(b, pred) > 0.35 { box = b } else { box = pred }
        }
    }
    if let b = box {
        // re-seed the tracker on the snapped box so drift doesn't accumulate
        obs = VNDetectedObjectObservation(boundingBox: b); last = b
    }
    let b = box ?? last ?? .zero
    out.append(["k": Double(k), "x": Double(b.midX), "top": Double(1 - b.maxY), "bottom": Double(1 - b.minY), "w": Double(b.width), "n": Double(hs.count)])
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: outPath))
print("frames", out.count)
