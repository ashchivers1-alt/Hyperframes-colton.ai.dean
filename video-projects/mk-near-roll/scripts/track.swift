// Track the red kart with VNTrackObjectRequest (forward + backward from a seed frame),
// then cut it out per frame with VNGenerateForegroundInstanceMaskRequest restricted to the tracked box.
// usage: swift track.swift <framesDir> <outDir> <seedFrame> <x> <y> <w> <h> <first> <last>
// box in pixel coords, origin top-left. Writes <outDir>/m%04d.png masks + track.json
import AppKit
import CoreImage
import Vision

let a = CommandLine.arguments
let framesDir = a[1], outDir = a[2]
let seed = Int(a[3])!
let W = 1206.0, H = 678.0
let sx = Double(a[4])!, sy = Double(a[5])!, sw = Double(a[6])!, sh = Double(a[7])!
let first = Int(a[8])!, last = Int(a[9])!
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)

func cg(_ n: Int) -> CGImage {
    let url = URL(fileURLWithPath: String(format: "%@/f%04d.png", framesDir, n))
    let src = CGImageSourceCreateWithURL(url as CFURL, nil)!
    return CGImageSourceCreateImageAtIndex(src, 0, nil)!
}
// Vision normalised rect (origin bottom-left) <-> pixel rect (origin top-left)
func toNorm(_ x: Double, _ y: Double, _ w: Double, _ h: Double) -> CGRect {
    CGRect(x: x / W, y: 1 - (y + h) / H, width: w / W, height: h / H)
}
func toPix(_ r: CGRect) -> [Double] {
    [Double(r.minX) * W, (1 - Double(r.maxY)) * H, Double(r.width) * W, Double(r.height) * H]
}

var boxes: [Int: [Double]] = [:]
var conf: [Int: Double] = [:]
func run(_ order: [Int]) {
    let handler = VNSequenceRequestHandler()
    var obs = VNDetectedObjectObservation(boundingBox: toNorm(sx, sy, sw, sh))
    for n in order {
        let req = VNTrackObjectRequest(detectedObjectObservation: obs)
        req.trackingLevel = .accurate
        try? handler.perform([req], on: cg(n))
        if let r = req.results?.first as? VNDetectedObjectObservation {
            obs = r
            boxes[n] = toPix(r.boundingBox); conf[n] = Double(r.confidence)
        }
    }
}
run(Array(seed...last))
run(Array((first...seed).reversed()))

// per-frame cut-out: run the foreground-instance model on a crop around the tracked box
let ctx = CIContext()
for n in first...last {
    guard let b = boxes[n] else { continue }
    let full = cg(n)
    let pad = 0.3
    let cx0 = max(0, b[0] - b[2] * pad), cy0 = max(0, b[1] - b[3] * pad)
    let cx1 = min(W, b[0] + b[2] * (1 + pad)), cy1 = min(H, b[1] + b[3] * (1 + pad))
    let crop = full.cropping(to: CGRect(x: cx0, y: cy0, width: cx1 - cx0, height: cy1 - cy0))!
    let cw = Double(crop.width), ch = Double(crop.height)
    let req = VNGenerateForegroundInstanceMaskRequest()
    let h = VNImageRequestHandler(cgImage: crop)
    try? h.perform([req])
    var score = 0.0
    var out = CIImage(color: .black).cropped(to: CGRect(x: 0, y: 0, width: W, height: H))
    if let res = req.results?.first {
        // keep instances whose pixels mostly sit inside the tracked box (in crop coords)
        let bx0 = b[0] - cx0, bx1 = bx0 + b[2], by0 = b[1] - cy0, by1 = by0 + b[3]
        let lm = res.instanceMask
        CVPixelBufferLockBaseAddress(lm, .readOnly)
        let mw = CVPixelBufferGetWidth(lm), mh = CVPixelBufferGetHeight(lm), rb = CVPixelBufferGetBytesPerRow(lm)
        let base = CVPixelBufferGetBaseAddress(lm)!.assumingMemoryBound(to: UInt8.self)
        var inside = [Int: Int](), total = [Int: Int]()
        for y in 0..<mh { for x in 0..<mw {
            let v = Int(base[y * rb + x]); if v == 0 { continue }
            total[v, default: 0] += 1
            let px = Double(x) / Double(mw) * cw, py = Double(y) / Double(mh) * ch
            if px >= bx0 && px <= bx1 && py >= by0 && py <= by1 { inside[v, default: 0] += 1 }
        }}
        CVPixelBufferUnlockBaseAddress(lm, .readOnly)
        let boxPix = (b[2] * b[3]) / (cw * ch) * Double(mw * mh)
        var keep = IndexSet(); var covered = 0
        for (k, t) in total where Double(inside[k] ?? 0) / Double(t) > 0.7 { keep.insert(k); covered += inside[k] ?? 0 }
        score = Double(covered) / boxPix
        if !keep.isEmpty, let mb = try? res.generateScaledMaskForImage(forInstances: keep, from: h) {
            let m = CIImage(cvPixelBuffer: mb).transformed(by: CGAffineTransform(translationX: cx0, y: H - cy1))
            out = m.composited(over: out)
        }
    }
    let url = URL(fileURLWithPath: String(format: "%@/m%04d.png", outDir, n))
    try? ctx.writePNGRepresentation(of: out.cropped(to: CGRect(x: 0, y: 0, width: W, height: H)), to: url, format: .L8, colorSpace: CGColorSpaceCreateDeviceGray())
    boxes[n]!.append(score)
}
let json = (first...last).compactMap { n -> [String: Any]? in
    guard let b = boxes[n] else { return nil }
    return ["n": n, "x": b[0], "y": b[1], "w": b[2], "h": b[3], "conf": conf[n] ?? 0, "mask_score": b.count > 4 ? b[4] : 0]
}
let data = try! JSONSerialization.data(withJSONObject: json, options: [.prettyPrinted])
try! data.write(to: URL(fileURLWithPath: outDir + "/track.json"))
print("tracked", boxes.count, "frames")
