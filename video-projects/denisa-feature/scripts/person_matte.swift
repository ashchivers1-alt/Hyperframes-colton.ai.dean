// Person matte with Apple's built-in Vision framework (no model download).
// Usage: swift scripts/person_matte.swift <src_png_dir> <out_mask_dir>
// Writes one grayscale PNG per input frame (white = person), same size as the input.
// One request object is reused across frames so Vision can keep its temporal state.
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let srcDir = URL(fileURLWithPath: args[1]), outDir = URL(fileURLWithPath: args[2])
let files = try FileManager.default.contentsOfDirectory(atPath: srcDir.path).filter { $0.hasSuffix(".png") }.sorted()
let ctx = CIContext()
let request = VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate
request.outputPixelFormat = kCVPixelFormatType_OneComponent8

for (i, name) in files.enumerated() {
    let url = srcDir.appendingPathComponent(name)
    guard let img = CIImage(contentsOf: url) else { fatalError("cannot read \(name)") }
    try VNImageRequestHandler(ciImage: img).perform([request])
    guard let buf = request.results?.first?.pixelBuffer else { fatalError("no mask for \(name)") }
    var mask = CIImage(cvPixelBuffer: buf)
    let sx = img.extent.width / mask.extent.width, sy = img.extent.height / mask.extent.height
    mask = mask.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
    let out = outDir.appendingPathComponent(name)
    guard let cg = ctx.createCGImage(mask, from: img.extent, format: .L8, colorSpace: CGColorSpaceCreateDeviceGray()),
          let dst = CGImageDestinationCreateWithURL(out as CFURL, UTType.png.identifier as CFString, 1, nil) else { fatalError("write \(name)") }
    CGImageDestinationAddImage(dst, cg, nil)
    CGImageDestinationFinalize(dst)
    if (i + 1) % 50 == 0 { print(i + 1) }
}
print("frames", files.count)
