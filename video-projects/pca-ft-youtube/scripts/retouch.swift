// Subtle under-eye retouch for a talking-head clip.
//   retouch detect <in.mov> <eyes.json>                  per-frame eye landmarks (pixels, y from top) or null
//   retouch render <in.mov> <eyes_smooth.json> <out.mov> [strength 0-1] [startSec] [durSec] [maskOnly]
// Render: under each eye a feathered ellipse; inside it the low frequencies are lifted toward the
// surrounding cheek tone and the purple cast is pulled out, while fine skin texture is kept.
import AVFoundation
import CoreImage
import Vision

let a = CommandLine.arguments
let mode = a[1]
let asset = AVURLAsset(url: URL(fileURLWithPath: a[2]))
let track = asset.tracks(withMediaType: .video)[0]
let size = track.naturalSize.applying(track.preferredTransform)
let W = abs(size.width), H = abs(size.height)
let fps = track.nominalFrameRate

// reads through a video composition: applies the rotation and tone-maps iPhone HLG to SDR Rec.709
let vcomp: AVVideoComposition = {
    let vc = AVMutableVideoComposition(propertiesOf: asset)
    vc.colorPrimaries = AVVideoColorPrimaries_ITU_R_709_2
    vc.colorTransferFunction = AVVideoTransferFunction_ITU_R_709_2
    vc.colorYCbCrMatrix = AVVideoYCbCrMatrix_ITU_R_709_2
    return vc
}()
func reader(start: Double = 0, dur: Double = 0) -> (AVAssetReader, AVAssetReaderOutput) {
    let r = try! AVAssetReader(asset: asset)
    if dur > 0 { r.timeRange = CMTimeRange(start: CMTime(seconds: start, preferredTimescale: 600), duration: CMTime(seconds: dur, preferredTimescale: 600)) }
    let o = AVAssetReaderVideoCompositionOutput(videoTracks: [track], videoSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
    o.videoComposition = vcomp
    o.alwaysCopiesSampleData = false
    r.add(o); r.startReading(); return (r, o)
}

if mode == "detect" {
    let (r, o) = reader()
    var out: [Any] = []
    let k = 1280.0 / Double(W)
    while true { let more: Bool = autoreleasepool {
        guard let sb = o.copyNextSampleBuffer(), let pb = CMSampleBufferGetImageBuffer(sb) else { return false }
        let img = CIImage(cvPixelBuffer: pb).transformed(by: CGAffineTransform(scaleX: k, y: k))
        let req = VNDetectFaceLandmarksRequest()
        try? VNImageRequestHandler(ciImage: img).perform([req])
        let iw = img.extent.width, ih = img.extent.height
        // largest face
        if let f = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }), let lm = f.landmarks,
           let le = lm.leftEye, let re = lm.rightEye {
            func eye(_ e: VNFaceLandmarkRegion2D) -> [Double] {
                let p = e.pointsInImage(imageSize: CGSize(width: iw, height: ih))
                let cx = p.map { $0.x }.reduce(0, +) / CGFloat(p.count), cy = p.map { $0.y }.reduce(0, +) / CGFloat(p.count)
                let xs = p.map { $0.x }, w = (xs.max()! - xs.min()!)
                return [Double(cx) / k, Double(ih - cy) / k, Double(w) / k]
            }
            let l = eye(le), rr = eye(re)
            out.append(l + rr + [Double(f.confidence)])
        } else { out.append(NSNull()) }
        if out.count % 600 == 0 { print("frame", out.count) }
        return true }
        if !more { break } }
    try! JSONSerialization.data(withJSONObject: ["fps": fps, "w": W, "h": H, "eyes": out]).write(to: URL(fileURLWithPath: a[3]))
    print("detected", out.count, "reader status", r.status.rawValue, r.error as Any)
    exit(0)
}

// ---------------------------------------------------------------- render
let J = try! JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: a[3]))) as! [String: Any]
let eyes = J["eyes"] as! [Any]
let strength = a.count > 5 ? Double(a[5])! : 0.55
let start = a.count > 6 ? Double(a[6])! : 0, dur = a.count > 7 ? Double(a[7])! : 0
let maskOnly = a.count > 8 && a[8] == "mask"
let (r, o) = reader(start: start, dur: dur)
let outURL = URL(fileURLWithPath: a[4]); try? FileManager.default.removeItem(at: outURL)
let w = try! AVAssetWriter(outputURL: outURL, fileType: .mov)
let vin = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.hevc, AVVideoWidthKey: W, AVVideoHeightKey: H,
    AVVideoColorPropertiesKey: [AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
                                AVVideoTransferFunctionKey: AVVideoTransferFunction_ITU_R_709_2,
                                AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2],
    AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 90_000_000, AVVideoExpectedSourceFrameRateKey: fps]])
vin.expectsMediaDataInRealTime = false
let ad = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: vin, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA, kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H])
w.add(vin); w.startWriting(); w.startSession(atSourceTime: .zero)
let cs = CGColorSpace(name: CGColorSpace.itur_709)!
let ctx = CIContext(options: [.workingColorSpace: cs, .outputColorSpace: cs])
let full = CGRect(x: 0, y: 0, width: W, height: H)

// one under-eye ellipse: eye centre (cx, cy from top), eye width ew, roll angle of the eye line
func ellipse(_ cx: Double, _ cy: Double, _ ew: Double, _ ang: Double) -> CIImage {
    let down = 0.68 * ew                       // centre of the bag below the eye centre
    let ux = -sin(ang), uy = cos(ang)          // "down" in image coords (y from top)
    let ex = cx + ux * down, ey = cy + uy * down
    let g = CIFilter(name: "CIRadialGradient", parameters: [
        "inputCenter": CIVector(x: 0, y: 0), "inputRadius0": 0.25, "inputRadius1": 1.0,
        "inputColor0": CIColor(red: 1, green: 1, blue: 1), "inputColor1": CIColor(red: 0, green: 0, blue: 0)])!.outputImage!
    // unit circle -> ellipse 0.78ew wide x 0.36ew tall, rotated, moved (CI y is from bottom)
    let t = CGAffineTransform(scaleX: 0.80 * ew, y: 0.40 * ew)
        .concatenating(CGAffineTransform(rotationAngle: -ang))
        .concatenating(CGAffineTransform(translationX: ex, y: Double(H) - ey))
    return g.transformed(by: t)
}

var i = Int((start * Double(fps)).rounded())
var n = 0
while true { let more: Bool = autoreleasepool {
    guard let sb = o.copyNextSampleBuffer(), let pb = CMSampleBufferGetImageBuffer(sb) else { return false }
    let src = CIImage(cvPixelBuffer: pb)
    var outImg = src
    if i < eyes.count, let e = eyes[i] as? [Double], e.count >= 7, e[6] > 0.01 {
        let ang = atan2(e[4] - e[1], e[3] - e[0]) // image coords, y down
        let ang2 = ang > .pi / 2 ? ang - .pi : (ang < -.pi / 2 ? ang + .pi : ang)
        let m1 = ellipse(e[0], e[1], e[2], ang2), m2 = ellipse(e[3], e[4], e[5], ang2)
        let mask = m1.applyingFilter("CIMaximumCompositing", parameters: [kCIInputBackgroundImageKey: m2])
            .cropped(to: full)
            .applyingFilter("CIColorMatrix", parameters: ["inputRVector": CIVector(x: strength * e[6], y: 0, z: 0, w: 0),
                                                         "inputGVector": CIVector(x: 0, y: strength * e[6], z: 0, w: 0),
                                                         "inputBVector": CIVector(x: 0, y: 0, z: strength * e[6], w: 0)])
        let ew = (e[2] + e[5]) / 2
        // low-pass of the frame; lift it (fills the shadow) and pull the cool/purple cast out
        let lowR = 0.18 * ew, texR = 0.05 * ew
        let low = src.clampedToExtent().applyingFilter("CIGaussianBlur", parameters: ["inputRadius": lowR]).cropped(to: full)
        let fine = src.clampedToExtent().applyingFilter("CIGaussianBlur", parameters: ["inputRadius": texR]).cropped(to: full)
        let lifted = low.applyingFilter("CIExposureAdjust", parameters: ["inputEV": 0.42])
            .applyingFilter("CITemperatureAndTint", parameters: ["inputNeutral": CIVector(x: 6500, y: 0), "inputTargetNeutral": CIVector(x: 6200, y: -6)])
            .applyingFilter("CIColorControls", parameters: ["inputSaturation": 0.92])
        // frequency separation: src = low + mid + fine.  result = src + (lifted - low) - 0.5 * (fine - low)
        // -> shadow filled, the crease (mid band) halved, pores / fine texture untouched
        func scale(_ im: CIImage, _ k: Double) -> CIImage {
            im.applyingFilter("CIColorMatrix", parameters: ["inputRVector": CIVector(x: k, y: 0, z: 0, w: 0), "inputGVector": CIVector(x: 0, y: k, z: 0, w: 0),
                                                           "inputBVector": CIVector(x: 0, y: 0, z: k, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 0),
                                                           "inputBiasVector": CIVector(x: 0, y: 0, z: 0, w: 0)])
        }
        func add(_ x: CIImage, _ y: CIImage) -> CIImage { x.applyingFilter("CIAdditionCompositing", parameters: [kCIInputBackgroundImageKey: y]) }
        let lowN = scale(low, -1)
        let delta = add(lifted, lowN)                          // lifted - low
        let mid = add(fine, lowN)                              // fine - low
        let res = add(add(src, delta), scale(mid, -0.5)).applyingFilter("CIColorClamp").cropped(to: full)
            .applyingFilter("CIColorMatrix", parameters: ["inputAVector": CIVector(x: 0, y: 0, z: 0, w: 0), "inputBiasVector": CIVector(x: 0, y: 0, z: 0, w: 1)])
        outImg = maskOnly ? mask : res.applyingFilter("CIBlendWithMask", parameters: [kCIInputBackgroundImageKey: src, kCIInputMaskImageKey: mask])
    }
    while !vin.isReadyForMoreMediaData { usleep(2000) }
    var ob: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, ad.pixelBufferPool!, &ob)
    ctx.render(outImg.cropped(to: full), to: ob!, bounds: full, colorSpace: cs)
    ad.append(ob!, withPresentationTime: CMTime(value: CMTimeValue(n), timescale: CMTimeScale(fps.rounded())))
    i += 1; n += 1
    if n % 600 == 0 { print("rendered", n) }
    return true }
    if !more { break } }
vin.markAsFinished()
let sem = DispatchSemaphore(value: 0)
w.finishWriting { sem.signal() }; sem.wait()
print("done", n, w.status.rawValue, w.error as Any)
