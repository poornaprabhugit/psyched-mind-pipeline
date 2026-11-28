window.TALK=0;
const GROUND=900;
const W=1920,H=1080;
const cv=document.getElementById('c'), ctx=cv.getContext('2d');
const C={bg:'#17143A',bg2:'#221E52',ink:'#F6F1E7',dim:'#8F8AB8',yel:'#FFC94D',cor:'#FF6B6B',grn:'#3DDC97',blu:'#7C83FD',pnk:'#FF9EC7',brn:'#8A5A3B',gold:'#E8B13A'};
const F='"DejaVu Sans", "Liberation Sans", Arial, sans-serif';

// ---------- easing / helpers ----------
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lin=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3);
const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back=x=>{const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const mix=(a,b,k)=>a+(b-a)*k;
function rr(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r);}
function txt(s,x,y,size,col,align='center',weight='bold'){ctx.font=`${weight} ${size}px ${F}`;ctx.fillStyle=col;ctx.textAlign=align;ctx.textBaseline='middle';ctx.fillText(s,x,y);}
function bg(){
  const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,C.bg2);g.addColorStop(1,C.bg);
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  // soft floor
  ctx.fillStyle='rgba(255,255,255,0.05)';ctx.fillRect(0,GROUND,W,6);
}

// ---------- the character: "Pip", an original round bean ----------
// opts: x,y (feet center), s scale, col, mood ('happy','sad','shock','meh','calm'), arms [lAngle,rAngle], walk phase, blink, look (-1..1)
window.NOW=0;window.BEATS=[];window.MAIN_DRAWN=false;
function gestureArms(o){ // acting along with the voice on emphasis words
  const idle=!o.arms||(Math.abs(o.arms[0]-0.35)<0.01&&Math.abs(o.arms[1]+0.35)<0.01);
  if(!idle||o.walk!=null||(o.s||1)<0.5)return null;
  let b=null;for(const x of BEATS){if(x.t<=NOW&&NOW-x.t<1.1)b=x;}
  if(!b)return null;const k=Math.sin(Math.PI*cl((NOW-b.t)/1.1));
  const P={point:[0.35,-1.9],up:[2.0,-2.0],nod:[0.35,-0.35],shrug:[1.7,-1.7],count:[0.35,-2.7]}[b.kind];
  return {arms:[mix(0.35,P[0],k),mix(-0.35,P[1],k)],nod:b.kind==='nod'?Math.sin((NOW-b.t)*14)*0.06*k:0,hop:b.kind==='up'?k*14:0,kind:b.kind};}
function pip(o){
  if((o.s||1)>=1)MAIN_DRAWN=true;
  const g=gestureArms(o);if(g)o=Object.assign({},o,{arms:g.arms});
  if(o.blink==null||o.blink===false){o=Object.assign({},o,{blink:((NOW+o.x*0.0137)%3.6)<0.09});}
  const s=o.s||1, col=o.col||C.blu;
  const br=o.walk==null?Math.sin(NOW*2.4+o.x*0.01):0, sway=o.walk==null?Math.sin(NOW*1.1+o.x*0.02)*0.025:0;
  ctx.save();ctx.translate(o.x,o.y-(g?g.hop:0));ctx.rotate(sway+(g?g.nod:0));ctx.scale(s*(o.flip?-1:1)*(1-0.012*br),s*(1+0.018*br));
  const step=o.walk!=null?Math.sin(o.walk*Math.PI*2):0;
  const bob=o.walk!=null?Math.abs(Math.sin(o.walk*Math.PI*2))*6:0;
  // legs
  ctx.strokeStyle=C.ink;ctx.lineWidth=14;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(-28,-70);ctx.lineTo(-28+step*18,0);ctx.moveTo(28,-70);ctx.lineTo(28-step*18,0);ctx.stroke();
  ctx.translate(0,-bob);
  // arms
  const arm=(sx,ang)=>{ctx.beginPath();ctx.moveTo(sx,-170);ctx.lineTo(sx+Math.sin(ang)*85,-170+Math.cos(ang)*85);ctx.stroke();
    ctx.fillStyle=C.ink;ctx.beginPath();ctx.arc(sx+Math.sin(ang)*85,-170+Math.cos(ang)*85,11,0,7);ctx.fill();};
  const a=o.arms||[0.35,-0.35];
  arm(-70,-a[0]);arm(70,-a[1]);
  // body
  ctx.fillStyle=col;rr(-80,-300,160,240,80);ctx.fill();
  ctx.fillStyle='rgba(255,255,255,0.18)';rr(-58,-280,40,90,20);ctx.fill();
  // face
  const lk=(o.look||0)*10;
  const bl=o.blink?0.12:1;
  ctx.fillStyle='#fff';
  const ey=-220;
  const er=o.mood==='shock'?24:20;
  ctx.beginPath();ctx.ellipse(-28+lk,ey,er,er*bl,0,0,7);ctx.ellipse(28+lk,ey,er,er*bl,0,0,7);ctx.fill();
  ctx.fillStyle='#1a1630';
  ctx.beginPath();ctx.ellipse(-26+lk*1.4,ey+2,10,10*bl,0,0,7);ctx.ellipse(30+lk*1.4,ey+2,10,10*bl,0,0,7);ctx.fill();
  ctx.strokeStyle='#1a1630';ctx.lineWidth=7;
  if(o.palm){ctx.strokeStyle=C.ink;ctx.lineWidth=14;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(70,-170);ctx.lineTo(18,-226);ctx.stroke();
    ctx.fillStyle=C.ink;ctx.beginPath();ctx.ellipse(10,-228,20,15,-0.6,0,7);ctx.fill();}
  const m=o.mood||'calm';ctx.beginPath();
  if(o.talk>0.06){ctx.fillStyle='#1a1630';ctx.beginPath();ctx.ellipse(lk,-176,13+o.talk*5,3+o.talk*17,0,0,7);ctx.fill();
    ctx.fillStyle='#FF7F9A';ctx.beginPath();ctx.ellipse(lk,-176+(3+o.talk*17)*0.45,7+o.talk*3,1.5+o.talk*5,0,0,7);ctx.fill();ctx.restore();return;}
  if(m==='happy'){ctx.arc(lk,-185,22,0.15*Math.PI,0.85*Math.PI);ctx.stroke();}
  else if(m==='sad'){ctx.arc(lk,-160,20,1.2*Math.PI,1.8*Math.PI);ctx.stroke();
    ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(-48+lk,-252);ctx.lineTo(-14+lk,-246);ctx.moveTo(48+lk,-252);ctx.lineTo(14+lk,-246);ctx.stroke();}
  else if(m==='shock'){ctx.fillStyle='#1a1630';ctx.beginPath();ctx.ellipse(lk,-170,12,16,0,0,7);ctx.fill();}
  else if(m==='meh'){ctx.moveTo(-16+lk,-172);ctx.lineTo(18+lk,-176);ctx.stroke();
    ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(-46+lk,-250);ctx.lineTo(-12+lk,-250);ctx.moveTo(46+lk,-254);ctx.lineTo(12+lk,-248);ctx.stroke();}
  else {ctx.arc(lk,-180,14,0.2*Math.PI,0.8*Math.PI);ctx.stroke();}
  ctx.restore();
}

// ---------- props ----------
function bill(x,y,rot,s=1,label='$10'){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);
  ctx.fillStyle=C.grn;rr(-90,-48,180,96,12);ctx.fill();ctx.strokeStyle='#1d7a52';ctx.lineWidth=6;rr(-78,-36,156,72,8);ctx.stroke();
  txt(label,0,2,46,'#0f3b28');ctx.restore();}
function ticket(x,y,rot,s=1,label='$10'){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);
  ctx.fillStyle=C.yel;ctx.beginPath();ctx.moveTo(-100,-50);ctx.lineTo(100,-50);ctx.lineTo(100,-14);ctx.arc(100,0,14,-Math.PI/2,Math.PI/2,true);ctx.lineTo(100,50);ctx.lineTo(-100,50);ctx.lineTo(-100,14);ctx.arc(-100,0,14,Math.PI/2,-Math.PI/2,true);ctx.closePath();ctx.fill();
  ctx.setLineDash([8,8]);ctx.strokeStyle='#a87b12';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(40,-42);ctx.lineTo(40,42);ctx.stroke();ctx.setLineDash([]);
  txt('SHOW',-30,-14,26,'#5a3f05');txt(label,-30,22,34,'#5a3f05');ctx.restore();}
function tag(x,y,rot,s,label,col=C.ink,fg='#1a1630'){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);
  ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(-70,-44);ctx.lineTo(70,-44);ctx.lineTo(70,44);ctx.lineTo(-70,44);ctx.lineTo(-100,0);ctx.closePath();ctx.fill();
  ctx.fillStyle=C.bg;ctx.beginPath();ctx.arc(-72,0,9,0,7);ctx.fill();
  txt(label,8,3,44,fg);ctx.restore();}
function mark(x,y,ok,k){if(k<=0)return;ctx.save();ctx.translate(x,y);ctx.scale(back(k),back(k));
  ctx.fillStyle=ok?C.grn:C.cor;ctx.beginPath();ctx.arc(0,0,48,0,7);ctx.fill();
  ctx.strokeStyle='#fff';ctx.lineWidth=12;ctx.lineCap='round';ctx.beginPath();
  if(ok){ctx.moveTo(-20,2);ctx.lineTo(-5,18);ctx.lineTo(22,-16);}else{ctx.moveTo(-17,-17);ctx.lineTo(17,17);ctx.moveTo(17,-17);ctx.lineTo(-17,17);}
  ctx.stroke();ctx.restore();}
function booth(x,y,s=1){ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  ctx.fillStyle='#3a3378';rr(-90,-260,180,260,14);ctx.fill();ctx.fillStyle=C.cor;rr(-105,-300,210,60,14);ctx.fill();
  txt('TICKETS',0,-270,30,'#fff');ctx.fillStyle='#1a1630';rr(-55,-200,110,80,10);ctx.fill();ctx.restore();}
function truffle(x,y,s=1,sad=0){ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  ctx.fillStyle=C.gold;ctx.beginPath();ctx.moveTo(-70,-20);ctx.lineTo(-120,-60);ctx.lineTo(-115,30);ctx.closePath();ctx.fill();
  ctx.beginPath();ctx.moveTo(70,-20);ctx.lineTo(120,-60);ctx.lineTo(115,30);ctx.closePath();ctx.fill();
  const g=ctx.createRadialGradient(-25,-30,10,0,0,90);g.addColorStop(0,'#FFE08A');g.addColorStop(1,'#C98A14');
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,0,80,0,7);ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,.5)';ctx.lineWidth=4;for(let i=-2;i<=2;i++){ctx.beginPath();ctx.moveTo(i*22-10,-70);ctx.lineTo(i*22+10,70);ctx.stroke();}
  // tiny face
  ctx.fillStyle='#5a3f05';ctx.beginPath();ctx.arc(-22,-6,7,0,7);ctx.arc(22,-6,7,0,7);ctx.fill();
  ctx.strokeStyle='#5a3f05';ctx.lineWidth=5;ctx.beginPath();
  if(sad>.5)ctx.arc(0,34,14,1.2*Math.PI,1.8*Math.PI);else ctx.arc(0,14,14,0.2*Math.PI,0.8*Math.PI);ctx.stroke();
  ctx.restore();}
function choc(x,y,s=1,happy=0){ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  ctx.fillStyle=C.brn;rr(-75,-60,150,120,12);ctx.fill();ctx.fillStyle='#6b4229';
  for(let i=0;i<3;i++)for(let j=0;j<2;j++){rr(-62+i*44,-48+j*52,36,44,6);ctx.fill();}
  ctx.fillStyle='#f4e3d0';ctx.beginPath();ctx.arc(-20,-4,7,0,7);ctx.arc(20,-4,7,0,7);ctx.fill();
  ctx.strokeStyle='#f4e3d0';ctx.lineWidth=5;ctx.beginPath();ctx.arc(0,12,12+happy*4,0.2*Math.PI,0.8*Math.PI);ctx.stroke();
  ctx.restore();}
function stamp(x,y,word,k,col=C.cor,size=110,rot=-0.18){if(k<=0)return;const sc=mix(2.2,1,eo(cl(k*1.6)));
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(sc,sc);ctx.globalAlpha=cl(k*3);
  ctx.font=`900 ${size}px ${F}`;const w=ctx.measureText(word).width;
  ctx.strokeStyle=col;ctx.lineWidth=10;rr(-w/2-28,-size*0.62,w+56,size*1.24,18);ctx.stroke();
  txt(word,0,4,size,col,'center','900');ctx.restore();}
function grid(x,y,n,col,k,cols=10,size=46,gap=14){ // 100 dots, first n lit
  for(let i=0;i<100;i++){const r=Math.floor(i/cols),c=i%cols;
    const lit=i<n*cl(k*1.05);
    ctx.fillStyle=lit?col:'rgba(255,255,255,0.12)';
    const px=x+c*(size+gap),py=y+r*(size+gap);
    ctx.beginPath();ctx.arc(px+size/2,py+size*0.28,size*0.22,0,7);ctx.fill();
    rr(px+size*0.18,py+size*0.5,size*0.64,size*0.5,size*0.25);ctx.fill();}}

