"""Subtle under-eye touch-up (natural): lifts dark under-eye shadow toward the surrounding
cheek tone and lightly softens texture. Face Mesh landmarks, temporally smoothed.
Usage: python undereye.py in.mp4 out.mp4 [strength=0.6] [--frames a,b,c --png outdir]
"""
import sys, subprocess, numpy as np, cv2, mediapipe as mp

src, dst = sys.argv[1], sys.argv[2]
STRENGTH = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else 0.6
test_frames = None
if "--frames" in sys.argv:
    test_frames = set(int(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(","))
    png_dir = sys.argv[sys.argv.index("--png") + 1]

W, H = 1080, 1920
# lower-lid landmark chains (outer -> inner corner), per eye
LIDS = [[33, 7, 163, 144, 145, 153, 154, 155, 133], [263, 249, 390, 373, 374, 380, 381, 382, 362]]

fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True,
                                     min_detection_confidence=0.5, min_tracking_confidence=0.5)

def eye_mask(pts):
    """Feathered crescent under one eye. pts: (9,2) lower lid, outer->inner."""
    width = np.linalg.norm(pts[0] - pts[-1])
    down = np.array([0, 1.0])
    top = pts + down * width * 0.07           # start just below the lashes
    depth = width * np.array([0.30, 0.42, 0.50, 0.55, 0.56, 0.55, 0.48, 0.38, 0.26])[:, None]
    bottom = (pts + down * (width * 0.07 + depth))[::-1]
    poly = np.concatenate([top, bottom]).astype(np.int32)
    m = np.zeros((H, W), np.float32)
    cv2.fillPoly(m, [poly], 1.0)
    k = int(width * 0.35) | 1
    return cv2.GaussianBlur(m, (k, k), width * 0.12), width

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
enc = None
if test_frames is None:
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
                            "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst], stdin=subprocess.PIPE)

smooth = None
n = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    small = cv2.resize(img, (540, 960))
    res = fm.process(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
    out = img
    if res.multi_face_landmarks:
        lm = res.multi_face_landmarks[0].landmark
        cur = np.array([[[lm[i].x * W, lm[i].y * H] for i in chain] for chain in LIDS])
        # temporal smoothing (reset on big jumps = cuts)
        if smooth is None or np.abs(cur - smooth).max() > 60:
            smooth = cur
        else:
            smooth = smooth * 0.6 + cur * 0.4
        mask = np.zeros((H, W), np.float32)
        widths = []
        for e in range(2):
            m, w = eye_mask(smooth[e]); mask = np.maximum(mask, m); widths.append(w)
        if mask.max() > 0:
            ys, xs = np.where(mask > 0.01)
            y0, y1 = max(0, ys.min() - 60), min(H, ys.max() + 60)
            x0, x1 = max(0, xs.min() - 60), min(W, xs.max() + 60)
            roi = img[y0:y1, x0:x1].astype(np.float32)
            mk = mask[y0:y1, x0:x1][..., None] * STRENGTH
            lab = cv2.cvtColor(roi.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
            wavg = np.mean(widths)
            # surrounding tone: wide blur; lift only where darker than surroundings
            ref = cv2.GaussianBlur(lab, (0, 0), wavg * 0.45)
            L = lab[..., 0]
            lift = np.clip(ref[..., 0] - L, 0, None)
            lab2 = lab.copy()
            lab2[..., 0] = L + lift * 0.85 + 2.0
            # pull a/b (purple/brown cast) toward surrounding skin
            lab2[..., 1:] = lab[..., 1:] * 0.55 + ref[..., 1:] * 0.45
            fixed = cv2.cvtColor(np.clip(lab2, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
            # light texture softening, keep fine detail (frequency split)
            soft = cv2.bilateralFilter(fixed.astype(np.uint8), 9, 22, 7).astype(np.float32)
            detail = fixed - cv2.GaussianBlur(fixed, (0, 0), 1.2)
            fixed = soft * 0.5 + fixed * 0.5 + detail * 0.35
            roi = roi * (1 - mk) + fixed * mk
            out = img.copy(); out[y0:y1, x0:x1] = np.clip(roi, 0, 255).astype(np.uint8)
    if test_frames is not None:
        if n in test_frames:
            cv2.imwrite(f"{png_dir}/after-{n}.png", out); cv2.imwrite(f"{png_dir}/before-{n}.png", img)
        if n >= max(test_frames):
            break
    else:
        enc.stdin.write(out.tobytes())
    n += 1
    if n % 200 == 0:
        print(n, flush=True)
dec.kill()
if enc:
    enc.stdin.close(); enc.wait()
print("frames", n)
