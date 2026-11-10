import wave, array, json, sys, math
w = wave.open('edit16k.wav'); SR = w.getframerate()
def rms(t, win=0.02):
    w.setpos(int(t*SR)); a = array.array('h', w.readframes(int(win*SR)))
    return math.sqrt(sum(x*x for x in a)/len(a)) if a else 0
def quiet(t, lo, hi, step=0.01):
    best = min((rms(lo+i*step), lo+i*step) for i in range(int((hi-lo)/step)+1))
    return best
W = json.load(open('words.json'))
def nb(t):  # words around t
    i = min(range(len(W)), key=lambda k: abs(W[k]['start']-t))
    return ' '.join(f"{W[k]['text']}@{W[k]['start']:.2f}" for k in range(max(0,i-2), min(len(W), i+3)))
for t in map(float, sys.argv[1:]):
    r, q = quiet(t, t-0.3, t+0.3)
    print(f'{t:8.2f} -> quiet {q:8.2f} rms {r:6.0f} | {nb(t)}')
