// All faces + upper bodies per sampled frame. usage: track <frameDir> <out.json>
// writes [{"faces":[[cx,cy,h]...],"bodies":[[cx,top,h]...]}] normalised 0-1 (y from top).
import AppKit
import Vision
let a = CommandLine.arguments
let files = try! FileManager.default.contentsOfDirectory(atPath: a[1]).filter { $0.hasSuffix(".jpg") }.sorted()
var out: [[String: [[Double]]]] = []
for f in files {
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1] + "/" + f) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    let fr = VNDetectFaceRectanglesRequest(), hr = VNDetectHumanRectanglesRequest(); hr.upperBodyOnly = false
    try? VNImageRequestHandler(cgImage: img).perform([fr, hr])
    let faces = (fr.results ?? []).filter { $0.boundingBox.height > 0.04 }.map { [Double($0.boundingBox.midX), Double(1 - $0.boundingBox.midY), Double($0.boundingBox.height)] }
    let bodies = (hr.results ?? []).map { [Double($0.boundingBox.midX), Double(1 - $0.boundingBox.maxY), Double($0.boundingBox.height)] }
    out.append(["faces": faces, "bodies": bodies])
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[2]))
print(a[1], files.count)
