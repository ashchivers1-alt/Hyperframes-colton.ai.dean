// Person cut-out: matte.swift <in.jpg> <out.png>  (accurate Vision person segmentation, alpha from mask)
import AppKit
import Vision
import CoreImage
let a = CommandLine.arguments
let ci = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let req = VNGeneratePersonSegmentationRequest(); req.qualityLevel = .accurate; req.outputPixelFormat = kCVPixelFormatType_OneComponent8
try! VNImageRequestHandler(ciImage: ci).perform([req])
var mask = CIImage(cvPixelBuffer: req.results!.first!.pixelBuffer)
mask = mask.transformed(by: CGAffineTransform(scaleX: ci.extent.width / mask.extent.width, y: ci.extent.height / mask.extent.height))
let out = ci.applyingFilter("CIBlendWithMask", parameters: ["inputBackgroundImage": CIImage.empty(), "inputMaskImage": mask])
let ctx = CIContext()
try! ctx.writePNGRepresentation(of: out, to: URL(fileURLWithPath: a[2]), format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!)
