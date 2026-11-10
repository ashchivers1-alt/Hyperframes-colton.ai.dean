// Locate competitor 352 (Gabriella) per output frame in each stage segment.
// Human rectangles every frame; OCR for the "352" hip tag every 3rd frame (re-anchors the pick).
// usage: swift find352.swift <src.mov> <segments.json> <out.json>
// segments.json: [{"item":38,"src_start":9.88,"src_end":29.13,"frames":462}]  (times in seconds)
import AVFoundation
import Vision
import CoreImage

let a = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: a[1]))
let segs = try! JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: a[2]))) as! [[String: Any]]
let gen = AVAssetImageGenerator(asset: asset)
gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = .zero
gen.appliesPreferredTrackTransform = true
gen.maximumSize = CGSize(width: 3840, height: 2160)
let FPS = 24000.0 / 1001.0
var out: [[String: Any]] = []

func ocr(_ img: CGImage) -> [(String, CGRect)] {
    let r = VNRecognizeTextRequest(); r.recognitionLevel = .accurate; r.usesLanguageCorrection = false
    r.minimumTextHeight = 0.008
    try? VNImageRequestHandler(cgImage: img).perform([r])
    var res: [(String, CGRect)] = []
    for o in r.results ?? [] {
        for c in o.topCandidates(3) where c.string.contains("352") {
            if let box = try? c.boundingBox(for: c.string.range(of: "352")!) { res.append(("352", box.boundingBox)) }
        }
    }
    return res
}
func humans(_ img: CGImage) -> [CGRect] {
    let r = VNDetectHumanRectanglesRequest(); r.upperBodyOnly = false
    try? VNImageRequestHandler(cgImage: img).perform([r])
    return (r.results ?? []).map { $0.boundingBox }
}
for s in segs {
    let item = s["item"] as! Int, t0 = s["src_start"] as! Double, n = s["frames"] as! Int
    var prev: CGRect? = nil
    var lastTag = -999
    for k in 0..<n {
        let t = t0 + Double(k) / FPS
        guard let img = try? gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 6000), actualTime: nil) else { continue }
        let hs = humans(img)
        var tag: CGRect? = nil
        if k % 3 == 0 { tag = ocr(img).first?.1 }
        var pick: CGRect? = nil
        if let tg = tag {
            let c = CGPoint(x: tg.midX, y: tg.midY)
            pick = hs.filter { $0.insetBy(dx: -$0.width * 0.15, dy: 0).contains(c) }.min { abs($0.midX - c.x) < abs($1.midX - c.x) }
            if pick != nil { lastTag = k }
        }
        if pick == nil, let p = prev {
            pick = hs.min { hypot($0.midX - p.midX, $0.midY - p.midY) < hypot($1.midX - p.midX, $1.midY - p.midY) }
            if let q = pick, hypot(q.midX - p.midX, q.midY - p.midY) > 0.12 { pick = nil }
        }
        if let p = pick { prev = p }
        var rec: [String: Any] = ["item": item, "k": k, "tag": tag != nil, "since_tag": k - lastTag]
        if let p = pick ?? prev { rec["x"] = p.midX; rec["top"] = 1 - p.maxY; rec["w"] = p.width; rec["h"] = p.height; rec["held"] = pick == nil }
        out.append(rec)
    }
    print("item", item, "done"); fflush(stdout)
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[3]))
