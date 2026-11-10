// Tracked "GABRIELLA" arrow + name over competitor 352 on stage (RGBA PNG per timeline frame; laid out in 1920x1080 coords, drawn at SC x).
// usage: gab_label <stageDir> <outDir>   (stageDir holds h37.json..h43.json: track + matte head top)
// The tag always hangs a clear gap above her head (never over her face/hair).
import AppKit
let a = CommandLine.arguments; let sd = a[1], od = a[2]
try? FileManager.default.createDirectory(atPath: od, withIntermediateDirectories: true)
let W = 1920.0, H = 1080.0, SC = 2.0   // SC = 2 -> 3840x2160 UHD
let red = NSColor(red: 0.85, green: 0.02, blue: 0.035, alpha: 1)
var idx = 0
var minTop = 9999.0
for item in 37...43 {
    let d = try! JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: "\(sd)/h\(item).json"))) as! [[String: Double]]
    // heavy temporal smoothing so the marker glides
    func sm(_ k: Int, _ key: String, _ r: Int = 6) -> Double {
        var s = 0.0, c = 0.0
        for j in max(0, k - r)...min(d.count - 1, k + r) { s += d[j][key]!; c += 1 }
        return s / c
    }
    // head top: fill matte misses from neighbours, take the highest point over ±10 frames (so motion
    // never pulls the tag down into her head), then smooth
    var hd = d.map { $0["head"]! }
    // drop single-frame spikes (a neighbour's arm / the judge leaking into the column band)
    let raw = hd
    for k in 0..<hd.count where raw[k] >= 0 {
        let nb = raw[max(0, k - 5)...min(raw.count - 1, k + 5)].filter { $0 >= 0 }.sorted()
        if raw[k] < nb[nb.count / 2] - 0.08 { hd[k] = -1 }
    }
    for k in 0..<hd.count where hd[k] < 0 {
        let prev = (0..<k).reversed().first { hd[$0] >= 0 }, next = (k..<hd.count).first { hd[$0] >= 0 }
        hd[k] = prev.map { hd[$0] } ?? next.map { hd[$0] } ?? d[k]["top"]!
    }
    let hmin = (0..<hd.count).map { k in hd[max(0, k - 10)...min(hd.count - 1, k + 10)].min()! }
    func head(_ k: Int) -> Double {
        let r = max(0, k - 6)...min(hd.count - 1, k + 6)
        return min(hmin[k], r.map { hmin[$0] }.reduce(0, +) / Double(r.count))
    }
    for k in 0..<d.count {
        let ctx = CGContext(data: nil, width: Int(W * SC), height: Int(H * SC), bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
        ctx.translateBy(x: 0, y: H * SC); ctx.scaleBy(x: SC, y: -SC)
        // fade in on the first clip, out on the last; quick re-entry on each cut
        let fin = item == 37 ? min(1, Double(k) / 10) : min(1, Double(k) / 4)
        let fout = item == 43 ? min(1, Double(d.count - 1 - k) / 10) : 1
        let alpha = fin * fout
        let cx = sm(k, "x") * W, top = head(k) * H
        let bob = 3 * (1 - cos(Double(idx) * 0.18))   // bobs upward only, away from her head
        let tip = CGPoint(x: cx, y: top - 26 - bob)
        ctx.setAlpha(alpha)
        ctx.setShadow(offset: .zero, blur: 10, color: NSColor.black.withAlphaComponent(0.85).cgColor)
        let p = CGMutablePath()
        p.move(to: tip); p.addLine(to: CGPoint(x: tip.x - 20, y: tip.y - 26)); p.addLine(to: CGPoint(x: tip.x + 20, y: tip.y - 26)); p.closeSubpath()
        ctx.addPath(p); ctx.setFillColor(red.cgColor); ctx.fillPath()
        // label: GABRIELLA (and MOVED pill on the first post-swap clip)
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current = NSGraphicsContext(cgContext: ctx, flipped: true)
        let font = NSFont(name: "Bebas Neue", size: 50) ?? NSFont.systemFont(ofSize: 40, weight: .heavy)
        let txt = NSAttributedString(string: "GABRIELLA", attributes: [.font: font, .foregroundColor: NSColor.white, .kern: 1.5])
        let sz = txt.size()
        let lx = min(max(tip.x - sz.width / 2 - 14, 20), W - sz.width - 48), ly = tip.y - 26 - sz.height - 12
        let bg = NSBezierPath(roundedRect: NSRect(x: lx, y: ly, width: sz.width + 28, height: sz.height + 8), xRadius: 4, yRadius: 4)
        NSColor(white: 0.04, alpha: 0.78).setFill(); bg.fill()
        red.setFill(); NSRect(x: lx, y: ly + sz.height + 4, width: sz.width + 28, height: 4).fill()
        txt.draw(at: NSPoint(x: lx + 14, y: ly + 5))
        minTop = min(minTop, ly)
        if item == 41 && k < 110 {
            // beside the name (not stacked above) so it never pushes the tag down toward her head
            let mf = NSFont.systemFont(ofSize: 24, weight: .heavy)
            let mt = NSAttributedString(string: "← MOVED HERE", attributes: [.font: mf, .foregroundColor: NSColor.white, .kern: 2])
            let ms = mt.size(); let mx = lx + sz.width + 28 + 10, my = ly + (sz.height + 8 - ms.height - 6) / 2
            let pill = NSBezierPath(roundedRect: NSRect(x: mx, y: my, width: ms.width + 20, height: ms.height + 6), xRadius: 4, yRadius: 4)
            red.setFill(); pill.fill(); mt.draw(at: NSPoint(x: mx + 10, y: my + 3))
        }
        NSGraphicsContext.restoreGraphicsState()
        let img = ctx.makeImage()!
        let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: String(format: "%@/o%05d.png", od, idx)) as CFURL, "public.png" as CFString, 1, nil)!
        CGImageDestinationAddImage(dst, img, nil); CGImageDestinationFinalize(dst)
        idx += 1
    }
}
print("frames", idx, "min tag top px", minTop)
