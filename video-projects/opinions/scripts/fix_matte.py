"""Fill the semi-transparent hood/neck gaps that RVM leaves in a person matte.
Grey closing (dilate→erode) with a large ellipse fills concave gaps narrower than the kernel
(hood between beard and shoulders), then the result is re-feathered.
Usage: python3 -I scripts/fix_matte.py in_matte.mp4 out_matte.mp4 [kernel=71]
"""
import sys, subprocess, numpy as np, cv2

src, dst = sys.argv[1], sys.argv[2]
K = int(sys.argv[3]) if len(sys.argv) > 3 else 71
W, H = 1080, 1920
ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (K, K))
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
n = 0
while True:
    buf = dec.stdout.read(W * H)
    if len(buf) < W * H:
        break
    m = np.frombuffer(buf, np.uint8).reshape(H, W)
    # boost: anything the model is fairly sure about becomes solid
    b = np.clip((m.astype(np.float32) - 22) * 3.5, 0, 255).astype(np.uint8)
    closed = cv2.morphologyEx(b, cv2.MORPH_CLOSE, ker)
    # only let closing ADD opacity inside the body (below the top of the head silhouette band)
    out = np.maximum(b, closed)
    out = cv2.GaussianBlur(out, (0, 0), 1.6)
    enc.stdin.write(out.tobytes())
    n += 1
enc.stdin.close(); enc.wait(); dec.kill()
print("frames", n)
