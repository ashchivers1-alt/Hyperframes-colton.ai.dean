// write 480x270 gray mask frames (30fps) for segment, rectangle boxes interpolated between keys, padded
const K=JSON.parse(require('fs').readFileSync('keys.json'))[process.argv[2]]; const t0=K[0][0], t1=K[K.length-1][0];
const W=480,H=270,N=Math.round((t1-t0)*30), out=require('fs').createWriteStream(process.argv[3]);
function box(t){ for(let i=0;i<K.length-1;i++){const [a,ba]=K[i],[b,bb]=K[i+1]; if(t>=a&&t<=b){const u=(t-a)/(b-a); return ba.map((v,j)=>v+(bb[j]-v)*u);} } return K[K.length-1][1]; }
for(let n=0;n<N;n++){ const [x0,y0,x1,y1]=box(t0+n/30), px=(x1-x0)*0.2+8, py=(y1-y0)*0.2+8; const f=Buffer.alloc(W*H);
  for(let y=Math.max(0,Math.floor(y0-py));y<Math.min(H,Math.ceil(y1+py));y++) for(let x=Math.max(0,Math.floor(x0-px));x<Math.min(W,Math.ceil(x1+px));x++) f[y*W+x]=255;
  out.write(f);} out.end(); console.log(process.argv[2], t0, t1, N);
