// Leg joints of the largest person per sampled frame. usage: pose <frameDir> <out.json>
// writes [{"lHip":[x,y,c],"lKnee":..,"lAnkle":..,"rHip":..,"rKnee":..,"rAnkle":..}] normalised 0-1 (y from top), {} when no person.
import AppKit
import Vision
let a = CommandLine.arguments
let files = try! FileManager.default.contentsOfDirectory(atPath: a[1]).filter { $0.hasSuffix(".jpg") }.sorted()
let names: [(String, VNHumanBodyPoseObservation.JointName)] = [("lHip", .leftHip), ("lKnee", .leftKnee), ("lAnkle", .leftAnkle),
                                                              ("rHip", .rightHip), ("rKnee", .rightKnee), ("rAnkle", .rightAnkle)]
var out: [[String: [Double]]] = []
for f in files {
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1] + "/" + f) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    let req = VNDetectHumanBodyPoseRequest()
    try? VNImageRequestHandler(cgImage: img).perform([req])
    var best: [String: [Double]] = [:]; var bestN = 0
    for ob in req.results ?? [] {
        let pts = (try? ob.recognizedPoints(.all)) ?? [:]
        var d: [String: [Double]] = [:]
        for (k, j) in names { if let p = pts[j], p.confidence > 0.1 { d[k] = [Double(p.location.x), Double(1 - p.location.y), Double(p.confidence)] } }
        if d.count > bestN { best = d; bestN = d.count }
    }
    out.append(best)
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[2]))
print(a[1], files.count)
