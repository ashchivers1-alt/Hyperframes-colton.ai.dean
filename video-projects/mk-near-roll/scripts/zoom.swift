// Slow-mo v2: tracked punch-in plate + overlay (arrow + "ME" label over my kart, circle on the lifted wheels).
// usage: swift zoom.swift <trackDir> <framesDir> <plateOutDir> <overlayOutDir>
import AppKit
import CoreImage
import CoreImage.CIFilterBuiltins

let trackDir = CommandLine.arguments[1], framesDir = CommandLine.arguments[2], plateDir = CommandLine.arguments[3], outDir = CommandLine.arguments[4]
for d in [plateDir, outDir] { try? FileManager.default.createDirectory(atPath: d, withIntermediateDirectories: true) }
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

// ---------- kart position per frame (from smoothed cut-out, falls back to tracker box) ----------
let ARROW_IN = 516, ARROW_OUT = 680
var kRaw = [Int: (Double, Double)]()          // (centre x, top y) source px, top-left origin
for n in FIRST...LAST {
    guard let b = box[n] else { continue }
    if n >= ARROW_IN - 8, n <= ARROW_OUT + 8, let m = smoothMask(n), let (x0, y0, x1, _) = maskBounds(m) {
        kRaw[n] = ((x0 + x1) / 2, y0)
    } else { kRaw[n] = (b.x + b.w / 2, b.y) }
}
func kart(_ n: Int, _ k: Int = 5) -> (Double, Double)? {
    var ax = 0.0, ay = 0.0, c = 0.0
    for j in (n - k)...(n + k) { if let p = kRaw[j] { ax += p.0; ay += p.1; c += 1 } }
    return c > 0 ? (ax / c, ay / c) : nil
}
// ---------- zoom path ----------
let ZMAX = 1.7
func ease(_ t: Double) -> Double { let u = min(1, max(0, t)); return u * u * (3 - 2 * u) }
func zoom(_ n: Int) -> Double {
    let up = ease(Double(n - 520) / 36.0), down = ease(Double(n - 660) / 27.0)
    return 1 + (ZMAX - 1) * up * (1 - down)
}
// smoothed kart centre for camera (heavier smoothing than the arrow)
func camTarget(_ n: Int) -> (Double, Double) {
    var ax = 0.0, ay = 0.0, c = 0.0
    for j in (n - 10)...(n + 10) { if let b = box[j] { ax += b.x + b.w / 2; ay += b.y + b.h / 2; c += 1 } }
    return c > 0 ? (ax / c, ay / c) : (SW / 2, SH / 2)
}
struct View { var x0, y0, w, h: Double }      // crop in source px, top-left origin
func view(_ n: Int) -> View {
    let z = zoom(n), w = SW / z, h = SH / z
    let wgt = (z - 1) / (ZMAX - 1)
    let t = camTarget(n)
    var cx = SW / 2 * (1 - wgt) + t.0 * wgt, cy = SH / 2 * (1 - wgt) + t.1 * wgt
    cx = min(max(cx, w / 2), SW - w / 2); cy = min(max(cy, h / 2), SH - h / 2)
    return View(x0: cx - w / 2, y0: cy - h / 2, w: w, h: h)
}
let canvas = CGRect(x: 0, y: 0, width: VW, height: VH)
let fgH = SH * s
func save(_ cg: CGImage, _ path: String) {
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, "public.png" as CFString, 1, nil)!
    CGImageDestinationAddImage(d, cg, nil); CGImageDestinationFinalize(d)
}
let red = NSColor(red: 1, green: 0.15, blue: 0.1, alpha: 1)
for n in FIRST...LAST {
    // ---- plate: blurred fill + punched-in picture ----
    let src = CIImage(contentsOf: URL(fileURLWithPath: String(format: "%@/f%04d.png", framesDir, n)))!
    let bs = VH / SH
    var bg = src.transformed(by: CGAffineTransform(scaleX: bs, y: bs))
    bg = bg.transformed(by: CGAffineTransform(translationX: -(SW * bs - VW) / 2, y: 0))
    let bl = CIFilter.gaussianBlur(); bl.inputImage = bg.clampedToExtent(); bl.radius = 30
    let cc = CIFilter.colorControls(); cc.inputImage = bl.outputImage!.cropped(to: canvas); cc.brightness = -0.12; cc.saturation = 0.85
    let v = view(n), k = VW / v.w
    var fg = src.cropped(to: CGRect(x: v.x0, y: SH - v.y0 - v.h, width: v.w, height: v.h))
    fg = fg.transformed(by: CGAffineTransform(translationX: -v.x0, y: -(SH - v.y0 - v.h)))
    let ls = CIFilter.lanczosScaleTransform(); ls.inputImage = fg; ls.scale = Float(k); ls.aspectRatio = 1
    let fgS = ls.outputImage!.transformed(by: CGAffineTransform(translationX: 0, y: (VH - fgH) / 2)).cropped(to: CGRect(x: 0, y: (VH - fgH) / 2, width: VW, height: fgH))
    let plate = fgS.composited(over: cc.outputImage!.cropped(to: canvas))
    save(ctx.createCGImage(plate, from: canvas)!, String(format: "%@/p%04d.png", plateDir, n))

    // ---- overlay ----
    let cgc = CGContext(data: nil, width: Int(VW), height: Int(VH), bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    cgc.translateBy(x: 0, y: VH); cgc.scaleBy(x: 1, y: -1)        // top-left origin
    let fgTop0 = (VH - fgH) / 2
    func reel(_ x: Double, _ y: Double) -> CGPoint { CGPoint(x: (x - v.x0) * k, y: fgTop0 + (y - v.y0) * k) }
    let aA = ramp(n, ARROW_IN, ARROW_OUT, 6)
    if aA > 0, let kp = kart(n) {
        var p = reel(kp.0, kp.1)
        p.x = min(max(p.x, 110), VW - 110)
        let bob = 9 * sin(Double(n - ARROW_IN) * 0.32)
        let tip = CGPoint(x: p.x, y: p.y - 14 - bob), top = CGPoint(x: p.x, y: tip.y - 78)
        cgc.setAlpha(aA)
        cgc.setShadow(offset: .zero, blur: 10, color: NSColor.black.withAlphaComponent(0.85).cgColor)
        let path = CGMutablePath()
        path.move(to: tip); path.addLine(to: CGPoint(x: tip.x - 30, y: tip.y - 34)); path.addLine(to: CGPoint(x: tip.x - 11, y: tip.y - 34))
        path.addLine(to: CGPoint(x: top.x - 11, y: top.y)); path.addLine(to: CGPoint(x: top.x + 11, y: top.y))
        path.addLine(to: CGPoint(x: tip.x + 11, y: tip.y - 34)); path.addLine(to: CGPoint(x: tip.x + 30, y: tip.y - 34)); path.closeSubpath()
        cgc.addPath(path); cgc.setFillColor(red.cgColor); cgc.fillPath()
        cgc.setShadow(offset: .zero, blur: 0, color: nil)
        cgc.addPath(path); cgc.setStrokeColor(NSColor.white.cgColor); cgc.setLineWidth(5); cgc.setLineJoin(.round); cgc.strokePath()
        // label
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current = NSGraphicsContext(cgContext: cgc, flipped: true)
        let font = NSFont.systemFont(ofSize: 64, weight: .black)
        let txt = NSAttributedString(string: "ME 🤡", attributes: [.font: font, .foregroundColor: NSColor.white,
            .strokeColor: NSColor.black, .strokeWidth: -6.0])
        let sz = txt.size()
        let sh = NSShadow(); sh.shadowBlurRadius = 10; sh.shadowColor = NSColor.black.withAlphaComponent(0.8)
        sh.set()
        txt.draw(at: CGPoint(x: top.x - sz.width / 2, y: top.y - sz.height - 2))
        NSGraphicsContext.restoreGraphicsState()
        cgc.setAlpha(1)
    }
    // wheel-lift circle (no arrow)
    let la = ramp(n, LIFT_IN, LIFT_OUT, 4)
    if la > 0, let lb = liftAnchor[n] ?? { let b = smoothed(n); return (b.x + b.w * 0.86, b.y + b.h * 0.80) }() as (Double, Double)? {
        let c = reel(lb.0, lb.1)
        let b = smoothed(n)
        let t = Double(n - LIFT_IN)
        let r = b.h * k * 0.24 * (t < 5 ? 1.5 - 0.5 * (t / 5) : 1.0 + 0.04 * sin(t * 0.6))
        let ring = CGRect(x: c.x - r, y: c.y - r * 0.8, width: 2 * r, height: 1.6 * r)
        cgc.setAlpha(la)
        cgc.setShadow(offset: .zero, blur: 10, color: NSColor.black.withAlphaComponent(0.8).cgColor)
        cgc.setStrokeColor(NSColor.white.cgColor); cgc.setLineWidth(11); cgc.strokeEllipse(in: ring)
        cgc.setStrokeColor(red.cgColor); cgc.setLineWidth(6); cgc.strokeEllipse(in: ring)
        cgc.setAlpha(1)
    }
    save(cgc.makeImage()!, String(format: "%@/o%04d.png", outDir, n))
}
print("done")
