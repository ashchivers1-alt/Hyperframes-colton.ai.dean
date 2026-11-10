import wave, array, math, sys
w = wave.open('edit16k.wav'); SR = w.getframerate()
def rms(t, win=0.02):
    w.setpos(int(t*SR)); a = array.array('h', w.readframes(int(win*SR))); return math.sqrt(sum(x*x for x in a)/len(a))
for t in map(float, sys.argv[1:]):
    print(f'== {t}')
    for i in range(-20, 21, 1):
        x = t + i*0.02; r = rms(x)
        print(f'{x:8.2f} {r:6.0f} ' + '#'*int(r/150))
