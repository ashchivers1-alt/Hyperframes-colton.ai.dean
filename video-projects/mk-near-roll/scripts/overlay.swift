// Render the slow-mo overlay (1080x1920 RGBA PNG per slow-mo frame):
//  - neon outline + glow hugging the tracked kart (masks smoothed over neighbouring frames)
//  - circle + arrow on the lifted wheels during the near-roll
// usage: swift overlay.swift <trackDir> <outDir>
import AppKit
import CoreImage
import CoreImage.CIFilterBuiltins

let trackDir = CommandLine.arguments[1], outDir = CommandLine.arguments[2]
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
let SW = 1206.0, SH = 678.0                    // source frame
let VW = 1080.0, VH = 1920.0                   // reel canvas
let s = VW / SW                                // fit full source width
let fgTop = (VH - SH * s) / 2                  // top of the fitted frame (from top)
let FIRST = 475, LAST = 687
let OUT_IN = 516, OUT_OUT = 678                // outline active range (source frames)
let LIFT_IN = 632, LIFT_OUT = 670              // wheel-lift callout range

struct Box { var x, y, w, h, score: Double }
let raw = try! JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: trackDir + "/track.json"))) as! [[String: Any]]
var box = [Int: Box]()
for r in raw { box[r["n"] as! Int] = Box(x: r["x"] as! Double, y: r["y"] as! Double, w: r["w"] as! Double, h: r["h"] as! Double, score: r["mask_score"] as! Double) }
func smoothed(_ n: Int, _ k: Int = 4) -> Box {
    var acc = Box(x: 0, y: 0, w: 0, h: 0, score: 0); var c = 0.0
    for j in (n - k)...(n + k) { if let b = box[j] { acc.x += b.x; acc.y += b.y; acc.w += b.w; acc.h += b.h; c += 1 } }
    return Box(x: acc.x / c, y: acc.y / c, w: acc.w / c, h: acc.h / c, score: 0)
}
let ctx = CIContext()
func mask(_ n: Int) -> CIImage? {
    let u = URL(fileURLWithPath: String(format: "%@/m%04d.png", trackDir, n))
    return CIImage(contentsOf: u)
}
// temporally smoothed, motion-aligned mask for frame n (source pixel space, CI coords)
func smoothMask(_ n: Int) -> CIImage? {
    guard let bn = box[n] else { return nil }
    var parts: [(CIImage, Double)] = []
    for j in (n - 5)...(n + 5) {
        guard let bj = box[j], bj.score > 0.3, let m = mask(j) else { continue }
        // shift neighbour mask so its box centre sits on this frame's box centre
        let dx = (bn.x + bn.w / 2) - (bj.x + bj.w / 2), dy = (bn.y + bn.h / 2) - (bj.y + bj.h / 2)
        parts.append((m.transformed(by: CGAffineTransform(translationX: dx, y: -dy)), 1.0 / (1.0 + Double(abs(j - n)))))
    }
    guard !parts.isEmpty else { return nil }
    let wsum = parts.reduce(0) { $0 + $1.1 }
    let rect = CGRect(x: 0, y: 0, width: SW, height: SH)
    var acc = CIImage(color: .black).cropped(to: rect)
    for (m, w) in parts {
        let k = w / wsum                       // normalised weights: the sum never exceeds 1
        let f = CIFilter.colorMatrix(); f.inputImage = m
        f.rVector = CIVector(x: k, y: 0, z: 0, w: 0); f.gVector = CIVector(x: 0, y: k, z: 0, w: 0); f.bVector = CIVector(x: 0, y: 0, z: k, w: 0)
        let add = CIFilter.linearDodgeBlendMode(); add.inputImage = f.outputImage!.composited(over: CIImage(color: .black).cropped(to: rect)); add.backgroundImage = acc
        acc = add.outputImage!.cropped(to: rect)
    }
    // threshold around 0.5 with a soft knee
    let g = 7.0
    let f = CIFilter.colorMatrix(); f.inputImage = acc
    f.rVector = CIVector(x: g, y: 0, z: 0, w: 0); f.gVector = CIVector(x: 0, y: g, z: 0, w: 0); f.bVector = CIVector(x: 0, y: 0, z: g, w: 0)
    f.biasVector = CIVector(x: -0.5 * g + 0.5, y: -0.5 * g + 0.5, z: -0.5 * g + 0.5, w: 0)
    let c = CIFilter.colorClamp(); c.inputImage = f.outputImage
    let b = CIFilter.gaussianBlur(); b.inputImage = c.outputImage!.clampedToExtent(); b.radius = 0.8
    return b.outputImage!.cropped(to: rect)
}
func opaque(_ i: CIImage) -> CIImage {
    let f = CIFilter.colorMatrix(); f.inputImage = i
    f.aVector = CIVector(x: 0, y: 0, z: 0, w: 0); f.biasVector = CIVector(x: 0, y: 0, z: 0, w: 1)
    return f.outputImage!
}
// mask extent in source px (top-left origin): returns (minX, minY, maxX, maxY) of pixels > 0.5
func maskBounds(_ m: CIImage) -> (Double, Double, Double, Double)? {
    guard let cgm = ctx.createCGImage(m, from: CGRect(x: 0, y: 0, width: SW, height: SH), format: .L8, colorSpace: CGColorSpaceCreateDeviceGray()) else { return nil }
    let w = cgm.width, h = cgm.height
    var buf = [UInt8](repeating: 0, count: w * h)
    let c = CGContext(data: &buf, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w, space: CGColorSpaceCreateDeviceGray(), bitmapInfo: 0)!
    c.draw(cgm, in: CGRect(x: 0, y: 0, width: w, height: h))
    var x0 = w, y0 = h, x1 = -1, y1 = -1
    for y in 0..<h { for x in 0..<w where buf[y * w + x] > 128 { x0 = min(x0, x); x1 = max(x1, x); y0 = min(y0, y); y1 = max(y1, y) } }
    return x1 < 0 ? nil : (Double(x0), Double(y0), Double(x1), Double(y1))
}
func ramp(_ n: Int, _ a: Int, _ b: Int, _ f: Int = 6) -> Double {
    if n < a || n > b { return 0 }
    return min(1, Double(n - a + 1) / Double(f), Double(b - n + 1) / Double(f))
}
// lift anchor per frame from the smoothed cut-out: right end of the kart, lower third; then smoothed over time
var liftRaw = [Int: (Double, Double)]()
for n in (LIFT_IN - 6)...(LIFT_OUT + 6) {
    if let m = smoothMask(n), let (x0, y0, x1, y1) = maskBounds(m) {
        liftRaw[n] = (x1 - (x1 - x0) * 0.13, y0 + (y1 - y0) * 0.74)
    }
}
var liftAnchor = [Int: (Double, Double)]()
for n in LIFT_IN...LIFT_OUT {
    var ax = 0.0, ay = 0.0, c = 0.0
    for j in (n - 4)...(n + 4) { if let p = liftRaw[j] { ax += p.0; ay += p.1; c += 1 } }
    if c > 0 { liftAnchor[n] = (ax / c, ay / c) }
}
let yellow = CIColor(red: 1.0, green: 0.92, blue: 0.0)
let canvas = CGRect(x: 0, y: 0, width: VW, height: VH)
let fgRect = CGRect(x: 0, y: VH - fgTop - SH * s, width: VW, height: SH * s)   // fitted picture area (CI coords)
let toReel = CGAffineTransform(scaleX: s, y: s).concatenating(CGAffineTransform(translationX: 0, y: VH - fgTop - SH * s))

for n in FIRST...LAST {
    var out = CIImage(color: .clear).cropped(to: canvas)
    let a = ramp(n, OUT_IN, OUT_OUT)
    if a > 0, let m = smoothMask(n) {
        let mr = m.transformed(by: toReel).cropped(to: canvas)
        // ring = dilated mask minus mask
        let dil = CIFilter.morphologyMaximum(); dil.inputImage = mr.clampedToExtent(); dil.radius = 4
        let sub = CIFilter.subtractBlendMode(); sub.inputImage = opaque(mr); sub.backgroundImage = opaque(dil.outputImage!.cropped(to: canvas))
        let ring = opaque(sub.outputImage!).cropped(to: canvas)
        let glowB = CIFilter.gaussianBlur(); glowB.inputImage = ring.clampedToExtent(); glowB.radius = 9
        let glow = opaque(glowB.outputImage!).cropped(to: canvas)
        func colourise(_ m: CIImage, _ alpha: Double) -> CIImage {
            let bw = CIFilter.blendWithMask(); bw.inputImage = CIImage(color: yellow).cropped(to: canvas)
            bw.backgroundImage = CIImage(color: .clear).cropped(to: canvas)
            let am = CIFilter.colorMatrix(); am.inputImage = m
            am.rVector = CIVector(x: alpha, y: 0, z: 0, w: 0); am.gVector = CIVector(x: 0, y: alpha, z: 0, w: 0); am.bVector = CIVector(x: 0, y: 0, z: alpha, w: 0)
            bw.maskImage = am.outputImage
            return bw.outputImage!.cropped(to: canvas)
        }
        out = colourise(ring, a).cropped(to: fgRect).composited(over: colourise(glow, 1.6 * a).cropped(to: fgRect).composited(over: out))
    }
    // wheel-lift callout (drawn with CoreGraphics on top)
    let la = ramp(n, LIFT_IN, LIFT_OUT, 4)
    var cg = ctx.createCGImage(out, from: canvas)!
    if la > 0, let _ = box[n] {
        let b = smoothed(n)
        var cxS = b.x + b.w * 0.86, cyS = b.y + b.h * 0.80        // lifted right-hand wheels (source px, top-left origin)
        if let lb = liftAnchor[n] { cxS = lb.0; cyS = lb.1 }
        let cx = cxS * s, cy = fgTop + cyS * s                      // reel px, top-left origin
        let r0 = b.h * s * 0.26
        let t = Double(n - LIFT_IN)
        let pop = t < 5 ? 1.5 - 0.5 * (t / 5) : 1.0 + 0.04 * sin(t * 0.6)
        let r = r0 * pop
        let rep = NSBitmapImageRep(cgImage: cg)
        let g = NSGraphicsContext(bitmapImageRep: rep)!
        NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = g
        let c = g.cgContext
        c.translateBy(x: 0, y: VH); c.scaleBy(x: 1, y: -1)           // top-left origin
        c.setAlpha(la)
        c.setShadow(offset: .zero, blur: 10, color: NSColor.black.withAlphaComponent(0.8).cgColor)
        let ring = CGRect(x: cx - r, y: cy - r * 0.8, width: 2 * r, height: 1.6 * r)
        c.setStrokeColor(NSColor.white.cgColor); c.setLineWidth(11); c.strokeEllipse(in: ring)
        c.setStrokeColor(NSColor(red: 1, green: 0.15, blue: 0.1, alpha: 1).cgColor); c.setLineWidth(6); c.strokeEllipse(in: ring)
        // arrow from lower-right pointing at the ring
        let tip = CGPoint(x: cx + r * 0.78, y: cy + r * 0.62)
        let tail = CGPoint(x: tip.x + 95, y: tip.y + 120)
        let ang = atan2(tip.y - tail.y, tip.x - tail.x)
        func head(_ p: CGPoint, _ len: Double, _ spread: Double) -> [CGPoint] {
            [CGPoint(x: p.x - len * cos(ang - spread), y: p.y - len * sin(ang - spread)), p,
             CGPoint(x: p.x - len * cos(ang + spread), y: p.y - len * sin(ang + spread))]
        }
        for (col, w) in [(NSColor.white, 16.0), (NSColor(red: 1, green: 0.15, blue: 0.1, alpha: 1), 9.0)] {
            c.setStrokeColor(col.cgColor); c.setLineWidth(w); c.setLineCap(.round); c.setLineJoin(.round)
            c.move(to: tail); c.addLine(to: tip); c.strokePath()
            c.addLines(between: head(tip, 34, 0.5)); c.strokePath()
        }
        NSGraphicsContext.restoreGraphicsState()
        cg = rep.cgImage!
    }
    let url = URL(fileURLWithPath: String(format: "%@/o%04d.png", outDir, n))
    let dest = CGImageDestinationCreateWithURL(url as CFURL, "public.png" as CFString, 1, nil)!
    CGImageDestinationAddImage(dest, cg, nil); CGImageDestinationFinalize(dest)
}
print("done")
