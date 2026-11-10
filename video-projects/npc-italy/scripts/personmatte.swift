// Vision person segmentation per frame -> grayscale PNG mattes. usage: personmatte <inDir> <outDir>
import AppKit; import Vision; import CoreImage
let a = CommandLine.arguments; let inD = a[1], outD = a[2]
try? FileManager.default.createDirectory(atPath: outD, withIntermediateDirectories: true)
let ctx = CIContext()
let files = try! FileManager.default.contentsOfDirectory(atPath: inD).filter { $0.hasSuffix(".jpg") }.sorted()
let req = VNGeneratePersonSegmentationRequest(); req.qualityLevel = .accurate; req.outputPixelFormat = kCVPixelFormatType_OneComponent8
for f in files {
    let s = CGImageSourceCreateWithURL(URL(fileURLWithPath: inD + "/" + f) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(s, 0, nil)!
    try? VNImageRequestHandler(cgImage: img).perform([req])
    guard let pb = req.results?.first?.pixelBuffer else { continue }
    var m = CIImage(cvPixelBuffer: pb)
    m = m.transformed(by: CGAffineTransform(scaleX: CGFloat(img.width) / m.extent.width, y: CGFloat(img.height) / m.extent.height))
    try? ctx.writePNGRepresentation(of: m, to: URL(fileURLWithPath: outD + "/" + f.replacingOccurrences(of: ".jpg", with: ".png")), format: .L8, colorSpace: CGColorSpaceCreateDeviceGray())
}
print("mattes", files.count)
