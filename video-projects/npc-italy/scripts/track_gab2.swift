// Pure appearance tracker from a hand-placed seed box (normalized, top-left origin): cx top bottom w
// usage: track_gab2 <framesDir> <cx> <top> <bottom> <w> <out.json>
import AppKit
import Vision
let a = CommandLine.arguments
let dir = a[1]; let cx = Double(a[2])!, top = Double(a[3])!, bot = Double(a[4])!, w = Double(a[5])!
let files = try! FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".jpg") }.sorted()
func load(_ f: String) -> CGImage {
    let s = CGImageSourceCreateWithURL(URL(fileURLWithPath: dir + "/" + f) as CFURL, nil)!
    return CGImageSourceCreateImageAtIndex(s, 0, nil)!
}
let seq = VNSequenceRequestHandler()
var obs = VNDetectedObjectObservation(boundingBox: CGRect(x: cx - w / 2, y: 1 - bot, width: w, height: bot - top))
var out: [[String: Double]] = []
for (k, f) in files.enumerated() {
    var b = obs.boundingBox, conf = 1.0
    if k > 0 {
        let req = VNTrackObjectRequest(detectedObjectObservation: obs); req.trackingLevel = .accurate
        try? seq.perform([req], on: load(f))
        if let r = req.results?.first as? VNDetectedObjectObservation { obs = r; b = r.boundingBox; conf = Double(r.confidence) }
    }
    out.append(["k": Double(k), "x": Double(b.midX), "top": Double(1 - b.maxY), "bottom": Double(1 - b.minY), "w": Double(b.width), "conf": conf])
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[6]))
print("frames", out.count)
