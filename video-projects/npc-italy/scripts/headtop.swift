// Per-frame head top for the tracked competitor: person-segmentation matte, topmost person row
// inside a narrow column band around the tracked centre. Adds "head" (0-1, from top) to each record.
// usage: headtop <frameDir> <track.json> <out.json>
import AppKit
import Vision

let a = CommandLine.arguments
let dir = a[1]
var d = try! JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: a[2]))) as! [[String: Double]]
for k in 0..<d.count {
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: String(format: "%@/f%04d.jpg", dir, k + 1)) as CFURL, nil)!
    let full = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    // segment a crop around her so small (wide-shot) figures still get a usable matte
    let FW = Double(full.width), FH = Double(full.height)
    let cx = d[k]["x"]!, cw = 0.16, cy0 = max(0, d[k]["top"]! - 0.18), cy1 = min(1, d[k]["bottom"]! + 0.02)
    let cr = CGRect(x: max(0, cx - cw / 2) * FW, y: cy0 * FH, width: cw * FW, height: (cy1 - cy0) * FH).integral
    let img = full.cropping(to: cr)!
    let req = VNGeneratePersonSegmentationRequest(); req.qualityLevel = .accurate
    req.outputPixelFormat = kCVPixelFormatType_OneComponent8
    try? VNImageRequestHandler(cgImage: img).perform([req])
    var head = -1.0
    if let pb = req.results?.first?.pixelBuffer {
        CVPixelBufferLockBaseAddress(pb, .readOnly)
        let mw = CVPixelBufferGetWidth(pb), mh = CVPixelBufferGetHeight(pb), rb = CVPixelBufferGetBytesPerRow(pb)
        let p = CVPixelBufferGetBaseAddress(pb)!.assumingMemoryBound(to: UInt8.self)
        // map full-frame coords into the crop's matte
        let fx = { (v: Double) in (v * FW - Double(cr.minX)) / Double(cr.width) * Double(mw) }
        let x = d[k]["x"]!, w = max(d[k]["w"]!, 0.04)
        let x0 = max(0, Int(fx(x - w * 0.3))), x1 = min(mw - 1, Int(fx(x + w * 0.3)))
        let yMax = Int((min(0.95, d[k]["bottom"]!) * FH - Double(cr.minY)) / Double(cr.height) * Double(mh))
        for y in 0..<yMax {
            var c = 0
            for xx in x0...x1 where p[y * rb + xx] > 128 { c += 1 }
            if c >= 2 { head = (Double(cr.minY) + Double(y) / Double(mh) * Double(cr.height)) / FH; break }
        }
        CVPixelBufferUnlockBaseAddress(pb, .readOnly)
    }
    d[k]["head"] = head
}
try! JSONSerialization.data(withJSONObject: d).write(to: URL(fileURLWithPath: a[3]))
print("frames", d.count)
