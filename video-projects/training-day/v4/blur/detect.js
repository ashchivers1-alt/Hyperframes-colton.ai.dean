// read rgb24 480x270 frames at 10fps from stdin; print per-frame bbox of red-label pixels (grid-cluster)
const W=480,H=270,FS=W*H*3; let buf=Buffer.alloc(0), n=0; const out=[];
process.stdin.on('data',d=>{buf=Buffer.concat([buf,d]); while(buf.length>=FS){proc(buf.subarray(0,FS)); buf=buf.subarray(FS);} });
process.stdin.on('end',()=>{require('fs').writeFileSync(process.argv[2],JSON.stringify(out));});
function proc(f){
  const G=10, gw=W/G, gh=Math.ceil(H/G), cnt=new Array(gw*gh).fill(0);
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=(y*W+x)*3,r=f[i],g=f[i+1],b=f[i+2];
    if(r>140 && r-g>90 && r-b>60 && g<110) cnt[Math.floor(y/G)*gw+Math.floor(x/G)]++;}
  // cells with >=6 red px; flood-fill clusters (8-neigh, allow 1-cell gaps via dilation)
  const on=cnt.map(c=>c>=6), seen=new Array(on.length).fill(false); let best=null;
  for(let s=0;s<on.length;s++){ if(!on[s]||seen[s])continue; const st=[s]; seen[s]=true; let m={x0:1e9,y0:1e9,x1:-1,y1:-1,px:0};
    while(st.length){const c=st.pop(),cx=c%gw,cy=(c-cx)/gw; m.x0=Math.min(m.x0,cx);m.y0=Math.min(m.y0,cy);m.x1=Math.max(m.x1,cx);m.y1=Math.max(m.y1,cy);m.px+=cnt[c];
      for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++){const nx=cx+dx,ny=cy+dy; if(nx<0||ny<0||nx>=gw||ny>=gh)continue; const k=ny*gw+nx; if(on[k]&&!seen[k]){seen[k]=true;st.push(k);}}}
    if(!best||m.px>best.px)best=m; }
  out.push(best&&best.px>=25?[n,best.x0*G,best.y0*G,(best.x1+1)*G,(best.y1+1)*G,best.px]:[n,null]); n++;
}
