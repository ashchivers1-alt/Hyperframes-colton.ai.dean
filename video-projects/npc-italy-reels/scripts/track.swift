// Face (fallback: upper body) centre per sampled frame. usage: track <frameDir> <out.json>
// Frames are f0001.jpg... ; writes [{"x":cx,"y":cy,"h":faceH,"ok":1}] normalised 0-1 (y from top).
import AppKit
import Vision
let a = CommandLine.arguments
let files = try! FileManager.default.contentsOfDirectory(atPath: a[1]).filter { $0.hasSuffix(".jpg") }.sorted()
var out: [[String: Double]] = []
for f in files {
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1] + "/" + f) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    let fr = VNDetectFaceRectanglesRequest(), hr = VNDetectHumanRectanglesRequest(); hr.upperBodyOnly = true
    try? VNImageRequestHandler(cgImage: img).perform([fr, hr])
    var r: [String: Double] = ["ok": 0]
    if let b = fr.results?.max(by: { $0.boundingBox.height < $1.boundingBox.height })?.boundingBox, b.height > 0.05 {
        r = ["x": Double(b.midX), "y": Double(1 - b.midY), "h": Double(b.height), "ok": 1]
    } else if let b = hr.results?.max(by: { $0.boundingBox.height < $1.boundingBox.height })?.boundingBox {
        r = ["x": Double(b.midX), "y": Double(1 - b.maxY + b.height * 0.15), "h": Double(b.height * 0.3), "ok": 2]
    }
    out.append(r)
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[2]))
print(a[1], files.count, out.filter { $0["ok"] != 0 }.count)
