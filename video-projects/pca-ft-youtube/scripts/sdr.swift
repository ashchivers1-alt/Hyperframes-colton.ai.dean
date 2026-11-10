// iPhone HLG -> SDR Rec.709 (Apple tone-map), rotation applied, full res. usage: sdr <in.mov> <out.mov>
import AVFoundation
let a = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: a[1]))
let sem = DispatchSemaphore(value: 0)
Task {
    let vc = try! await AVMutableVideoComposition.videoComposition(withPropertiesOf: asset)
    vc.colorPrimaries = AVVideoColorPrimaries_ITU_R_709_2
    vc.colorTransferFunction = AVVideoTransferFunction_ITU_R_709_2
    vc.colorYCbCrMatrix = AVVideoYCbCrMatrix_ITU_R_709_2
    let ex = AVAssetExportSession(asset: asset, presetName: AVAssetExportPresetHEVCHighestQuality)!
    ex.videoComposition = vc
    try? FileManager.default.removeItem(atPath: a[2])
    do { try await ex.export(to: URL(fileURLWithPath: a[2]), as: .mov); print("ok", a[2]) } catch { print("FAIL", error) }
    sem.signal()
}
sem.wait()
