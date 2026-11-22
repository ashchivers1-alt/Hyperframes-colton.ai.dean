"""Robust Video Matting over a video -> grayscale matte video (white = person).
Usage: python3 -I run_rvm.py <model.onnx> <in.mp4> <out_matte.mp4> [max_frames]
"""
import sys, subprocess, numpy as np, onnxruntime as ort

model, src, out = sys.argv[1:4]
maxf = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
W, H = 1080, 1920
sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
ds = np.array([0.25], np.float32)

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", "30",
                        "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
n = 0
while n < maxf:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) / 255.0
    x = img.transpose(2, 0, 1)[None]
    fgr, pha, *rec = sess.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": ds})
    a = (np.clip(pha[0, 0], 0, 1) * 255).astype(np.uint8)
    enc.stdin.write(a.tobytes())
    n += 1
    if n % 100 == 0:
        print(n, flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
print("frames", n)
