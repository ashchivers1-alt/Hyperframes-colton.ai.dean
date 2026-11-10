// Subject lift with Apple's built-in Vision framework (macOS 14+, no model download).
// Usage: swift scripts/lift_subject.swift <in.jpg> <out_prefix>
// Writes <out_prefix>-<n>.png per detected instance (RGBA cut-out, full image size)
// and <out_prefix>-all.png with every instance combined.
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let input = URL(fileURLWithPath: args[1]), prefix = args[2]
guard let img = CIImage(contentsOf: input) else { fatalError("cannot read input") }
let req = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: img)
try handler.perform([req])
guard let obs = req.results?.first else { fatalError("no subject found") }
let ctx = CIContext()

func write(_ set: IndexSet, _ name: String) throws {
    let buf = try obs.generateMaskedImage(ofInstances: set, from: handler, croppedToInstancesExtent: false)
    let ci = CIImage(cvPixelBuffer: buf)
    guard let cg = ctx.createCGImage(ci, from: ci.extent),
          let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: name) as CFURL, UTType.png.identifier as CFString, 1, nil) else { fatalError("write \(name)") }
    CGImageDestinationAddImage(dst, cg, nil)
    CGImageDestinationFinalize(dst)
    print(name)
}
for i in obs.allInstances { try write(IndexSet(integer: i), "\(prefix)-\(i).png") }
try write(obs.allInstances, "\(prefix)-all.png")
