// prints t, dx (px at 480w) between consecutive frames sampled at 10fps
import AVFoundation; import Vision; import CoreImage
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let asset = AVURLAsset(url: url)
let gen = AVAssetImageGenerator(asset: asset)
gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = .zero
gen.maximumSize = CGSize(width: 480, height: 270)
let dur = CMTimeGetSeconds(asset.duration)
var prev: CGImage? = nil
var t = 0.0
while t < dur - 0.05 {
    let img = try! gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil)
    // horizon band only (middle third) to avoid the bodywork
    let band = img.cropping(to: CGRect(x: 0, y: 70, width: 480, height: 110))!
    if let p = prev {
        let req = VNTranslationalImageRegistrationRequest(targetedCGImage: band)
        try! VNImageRequestHandler(cgImage: p).perform([req])
        let tx = (req.results?.first as? VNImageTranslationAlignmentObservation)?.alignmentTransform.tx ?? .nan
        print(String(format: "%.1f %.1f", t, tx))
    }
    prev = band; t += 0.1
}
