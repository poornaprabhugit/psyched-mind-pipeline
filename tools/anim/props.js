// ================= long-video framework =================
let CH=0, WORDS=[], DUR=0, TRICKS_BEFORE=0;
const norm=s=>s.toLowerCase().replace(/[^a-z0-9$%-]/g,'');
// time of the n-th occurrence of a word (or first word of a phrase)
function A(phrase,occ=1){const ps=phrase.split(' ').map(norm);let c=0;
  for(let i=0;i<WORDS.length;i++){let ok=true;for(let j=0;j<ps.length;j++){if(!WORDS[i+j]||norm(WORDS[i+j].w)!==ps[j]){ok=false;break;}}
    if(ok){c++;if(c===occ)return WORDS[i].start;}}
  console.log('MISSING',CH,phrase);return 1e9;}
const L=(t,a,d=0.4)=>eo(cl((t-a)/d));          // ease-in from time a over d seconds
const between=(t,a,b)=>t>=a&&t<b;
function sky(night){const g=ctx.createLinearGradient(0,0,0,H);
  if(night){g.addColorStop(0,'#0E0C26');g.addColorStop(1,'#17143A');}else{g.addColorStop(0,C.bg2);g.addColorStop(1,C.bg);}
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.fillStyle='rgba(255,255,255,0.05)';ctx.fillRect(0,GROUND,W,6);}
function chapterLabel(txt_){ctx.save();ctx.globalAlpha=0.75;ctx.font=`bold 30px ${F}`;const w=ctx.measureText(txt_).width;
  ctx.fillStyle='rgba(255,255,255,0.08)';rr(40,34,w+44,56,28);ctx.fill();txt(txt_,62,63,30,C.ink,'left','bold');ctx.restore();}
let COUNTER=null;function counter(n,pop){COUNTER=[n,pop];}
function drawCounter(n,pop){ctx.save();const x=W-250,y=36;ctx.translate(x+105,y+30);const s=1+0.25*pop;ctx.scale(s,s);ctx.translate(-(x+105),-(y+30));
  ctx.fillStyle='rgba(255,255,255,0.1)';rr(x,y,210,60,30);ctx.fill();txt('TRICKS',x+70,y+31,24,C.dim,'center','bold');
  txt(n+'/8',x+160,y+31,32,pop>0.01?C.yel:C.ink,'center','900');ctx.restore();}
function bigNote(x,y,rot,s,text,col='#FFE27A'){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);
  ctx.fillStyle=col;ctx.fillRect(-90,-70,180,140);ctx.fillStyle='rgba(0,0,0,0.08)';ctx.fillRect(-90,-70,180,22);
  ctx.font=`900 30px ${F}`;ctx.fillStyle='#3A2A10';ctx.textAlign='center';ctx.textBaseline='middle';
  text.split('\n').forEach((l,i,a)=>ctx.fillText(l,0,10+(i-(a.length-1)/2)*36));ctx.restore();}
function wallet(x,y,s,open=0,bills=0){ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  for(let i=0;i<bills;i++){bill(-10+i*6,-50-i*5,-0.1+i*0.05,0.8);}
  ctx.fillStyle='#8A5A3B';rr(-110,-60,220,130,16);ctx.fill();ctx.fillStyle='#6b4229';
  ctx.save();ctx.translate(0,-60);ctx.rotate(-1.3*open);rr(-110,-90,220,90,16);ctx.fill();ctx.restore();
  ctx.fillStyle='#C9A27E';ctx.beginPath();ctx.arc(80,5,10,0,7);ctx.fill();ctx.restore();}
function cup(x,y,s,steam=0){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='#F6F1E7';
  ctx.beginPath();ctx.moveTo(-40,-60);ctx.lineTo(40,-60);ctx.lineTo(30,30);ctx.lineTo(-30,30);ctx.closePath();ctx.fill();
  ctx.fillStyle='#8A5A3B';ctx.fillRect(-42,-72,84,16);ctx.fillStyle=C.cor;ctx.fillRect(-36,-25,72,20);
  if(steam>0){ctx.strokeStyle='rgba(255,255,255,0.5)';ctx.lineWidth=5;ctx.lineCap='round';for(let i=-1;i<=1;i++){ctx.beginPath();
    for(let k=0;k<=10;k++){const yy=-80-k*6;const xx=i*18+Math.sin(k*0.8+steam*4+i)*6;k?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy);}ctx.stroke();}}
  ctx.restore();}
function stampCard(x,y,s,slots,filled,hl=0,label){ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  const cols=5,rows=Math.ceil(slots/cols),w=cols*70+40,h=rows*70+90;
  ctx.fillStyle='#FFF6E8';rr(-w/2,-h/2,w,h,20);ctx.fill();if(label)txt(label,0,-h/2+34,30,'#5A3A20','center','900');
  for(let i=0;i<slots;i++){const r=Math.floor(i/cols),c=i%cols;const cx=-w/2+55+c*70,cy=-h/2+90+r*70;
    ctx.strokeStyle='#C9A27E';ctx.lineWidth=4;ctx.beginPath();ctx.arc(cx,cy,24,0,7);ctx.stroke();
    if(i<filled){ctx.fillStyle=C.cor;ctx.beginPath();ctx.arc(cx,cy,20,0,7);ctx.fill();txt('★',cx,cy+2,24,'#fff');}
    else if(hl>0){ctx.fillStyle=`rgba(255,201,77,${0.35*hl})`;ctx.beginPath();ctx.arc(cx,cy,20,0,7);ctx.fill();}}
  ctx.restore();}
function sparkle(x,y,s,t){ctx.save();ctx.translate(x,y);ctx.rotate(t*2);ctx.scale(s*(0.8+0.2*Math.sin(t*9)),s*(0.8+0.2*Math.sin(t*9)));
  ctx.fillStyle=C.yel;ctx.beginPath();for(let i=0;i<8;i++){const r=i%2?10:30,a=i*Math.PI/4;ctx.lineTo(Math.cos(a)*r,Math.sin(a)*r);}ctx.closePath();ctx.fill();ctx.restore();}
function hbar(x,y,w,frac,col,label,val,k){txt(label,x,y-34,30,C.ink,'left','bold');
  ctx.fillStyle='rgba(255,255,255,0.1)';rr(x,y,w,44,22);ctx.fill();ctx.fillStyle=col;rr(x,y,Math.max(44,w*frac*k),44,22);ctx.fill();
  if(k>0.2)txt(val,x+Math.max(44,w*frac*k)+20,y+23,32,col,'left','900');}
function panel(x,y,w,h){ctx.fillStyle='rgba(255,255,255,0.06)';rr(x,y,w,h,30);ctx.fill();}
function title(t0,t,text,sub,hold=4.5){const k=Math.min(L(t,t0,0.5),1-L(t,t0+hold,0.5));if(k<=0)return;ctx.save();ctx.globalAlpha=k;
  ctx.fillStyle='rgba(10,8,30,0.82)';ctx.fillRect(0,0,W,H);ctx.translate(W/2,H/2-30);ctx.scale(mix(0.9,1,k),mix(0.9,1,k));
  txt(text,0,0,70,C.ink,'center','900');if(sub)txt(sub,0,90,40,C.yel,'center','bold');ctx.restore();}


// ---------- extra props ----------
function heartEyes(x,y,s){for(const d of [-1,1]){ctx.save();ctx.translate(x+d*28*s,y-222*s);ctx.scale(s*1.1,s*1.1);ctx.fillStyle=C.cor;
  ctx.beginPath();ctx.moveTo(0,10);ctx.bezierCurveTo(-26,-8,-12,-26,0,-12);ctx.bezierCurveTo(12,-26,26,-8,0,10);ctx.fill();ctx.restore();}}
function bubble(x,y,w,h,tailx,taily){ctx.fillStyle='#fff';rr(x,y,w,h,40);ctx.fill();ctx.beginPath();ctx.arc(tailx,taily,14,0,7);ctx.arc(tailx-30,taily+40,9,0,7);ctx.fill();}
function gymBuilding(x){ctx.fillStyle='#3A3378';rr(x,420,520,480,16);ctx.fill();ctx.fillStyle=C.cor;rr(x-20,380,560,80,16);ctx.fill();
  txt('GYM',x+260,422,50,'#fff','center','900');ctx.fillStyle='#1a1630';rr(x+190,700,140,200,10);ctx.fill();
  ctx.fillStyle='#5a4fb0';rr(x+150,890,220,14,6);ctx.fill();}
function dumbbell(x,y,s,rot=0){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);ctx.fillStyle='#555';ctx.fillRect(-60,-6,120,12);
  ctx.fillStyle='#222';rr(-80,-30,24,60,6);ctx.fill();rr(56,-30,24,60,6);ctx.fill();ctx.restore();}
function people(x,y,cols,rows,lit,col,size=34,gap=12){for(let i=0;i<cols*rows;i++){const r=Math.floor(i/cols),c=i%cols;
  ctx.fillStyle=i<lit?col:'rgba(255,255,255,0.15)';const px=x+c*(size+gap),py=y+r*(size+gap);
  ctx.beginPath();ctx.arc(px+size/2,py+size*0.28,size*0.22,0,7);ctx.fill();rr(px+size*0.18,py+size*0.5,size*0.64,size*0.5,size*0.25);ctx.fill();}}
function card(x,y,w,h,col){ctx.fillStyle=col||'rgba(255,255,255,0.08)';rr(x,y,w,h,24);ctx.fill();}
function phone(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='#111';rr(-230,-400,460,800,50);ctx.fill();
  ctx.fillStyle='#F6F1E7';rr(-205,-370,410,740,30);ctx.fill();ctx.restore();}
function tripCard(x,y,s,name,price,col,heart){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle=col;rr(-170,-110,340,220,24);ctx.fill();
  txt(name,0,-50,44,'#fff','center','900');txt(price,0,30,64,'#fff','center','900');if(heart){ctx.fillStyle='#fff';txt('♥ more fun',0,86,30,'#fff','center','bold');}ctx.restore();}
function jacket(x,y,s,col='#3DB2DC'){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle=col;
  ctx.beginPath();ctx.moveTo(-60,-120);ctx.lineTo(60,-120);ctx.lineTo(120,-60);ctx.lineTo(95,-20);ctx.lineTo(70,-50);ctx.lineTo(70,120);ctx.lineTo(-70,120);ctx.lineTo(-70,-50);ctx.lineTo(-95,-20);ctx.lineTo(-120,-60);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(0,0,0,0.25)';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(0,-120);ctx.lineTo(0,120);ctx.stroke();
  ctx.fillStyle='#ddd';ctx.beginPath();ctx.arc(0,-150,14,Math.PI,0);ctx.lineWidth=5;ctx.strokeStyle='#ccc';ctx.stroke();ctx.restore();}
function snowCloud(x,y,t){ctx.fillStyle='#B9B4E0';for(const [dx,r] of [[-40,34],[0,46],[44,34]]){ctx.beginPath();ctx.arc(x+dx,y,r,0,7);ctx.fill();}
  ctx.fillStyle='#fff';for(let i=0;i<6;i++){const fy=(t*120+i*37)%160;ctx.beginPath();ctx.arc(x-50+i*20,y+40+fy,5,0,7);ctx.fill();}}
function badge(x,y,text,col,k){if(k<=0)return;ctx.save();ctx.translate(x,y);ctx.rotate(-0.06);ctx.scale(back(k),back(k));ctx.font=`900 44px ${F}`;
  const w=ctx.measureText(text).width;ctx.fillStyle=col;rr(-w/2-30,-44,w+60,88,44);ctx.fill();txt(text,0,2,44,'#17143A','center','900');ctx.restore();}
function cnt(t,n,tT){counter(t>tT?n:n-1,t>tT?Math.max(0,1-(t-tT)/0.6):0);}


function coin(x,y,s,rot=0){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);ctx.fillStyle='#C9CDD6';ctx.beginPath();ctx.arc(0,0,40,0,7);ctx.fill();
  ctx.strokeStyle='#9AA0AC';ctx.lineWidth=6;ctx.beginPath();ctx.arc(0,0,32,0,7);ctx.stroke();txt('25¢',0,2,24,'#555','center','900');ctx.restore();}
function candyMachine(x,y){ctx.fillStyle=C.cor;rr(x-90,y-120,180,330,20);ctx.fill();ctx.fillStyle='rgba(255,255,255,0.85)';ctx.beginPath();ctx.arc(x,y-200,130,0,7);ctx.fill();
  const cs=[C.yel,C.grn,C.blu,C.pnk];for(let i=0;i<18;i++){ctx.fillStyle=cs[i%4];ctx.beginPath();ctx.arc(x-80+(i%6)*32,y-150-Math.floor(i/6)*34,14,0,7);ctx.fill();}
  ctx.fillStyle='#1a1630';rr(x-30,y+90,60,50,8);ctx.fill();ctx.fillStyle='#ddd';rr(x+30,y-60,20,50,6);ctx.fill();}
function padlock(x,y,s){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.strokeStyle='#E8B13A';ctx.lineWidth=10;ctx.beginPath();ctx.arc(0,-20,24,Math.PI,0);ctx.stroke();
  ctx.fillStyle='#E8B13A';rr(-36,-20,72,60,10);ctx.fill();ctx.fillStyle='#7a5a10';ctx.beginPath();ctx.arc(0,6,8,0,7);ctx.fill();ctx.restore();}
function jar(x,y,s,label,fill,col=C.grn,price){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='rgba(255,255,255,0.18)';rr(-80,-120,160,220,30);ctx.fill();
  ctx.fillStyle=col;const h=200*fill;rr(-70,90-h,140,h,22);ctx.fill();ctx.fillStyle='#8F8AB8';rr(-90,-140,180,30,10);ctx.fill();
  txt(label,0,150,34,C.ink,'center','900');if(price)tag(70,-140,0.15,0.8,price,C.yel);ctx.restore();}
function mug(x,y,s,crown=0){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='#F6F1E7';rr(-70,-90,140,170,20);ctx.fill();
  ctx.strokeStyle='#F6F1E7';ctx.lineWidth=18;ctx.beginPath();ctx.arc(80,-5,38,-Math.PI/2,Math.PI/2);ctx.stroke();ctx.fillStyle=C.blu;txt('♥',0,0,60,C.cor,'center','900');
  if(crown>0){ctx.save();ctx.translate(0,-130);ctx.scale(crown,crown);ctx.fillStyle=C.gold;ctx.beginPath();ctx.moveTo(-50,20);ctx.lineTo(-50,-20);ctx.lineTo(-25,5);ctx.lineTo(0,-30);ctx.lineTo(25,5);ctx.lineTo(50,-20);ctx.lineTo(50,20);ctx.closePath();ctx.fill();ctx.restore();
    ctx.strokeStyle=`rgba(255,201,77,${crown*0.8})`;ctx.lineWidth=6;ctx.beginPath();ctx.ellipse(0,-185,60,14,0,0,7);ctx.stroke();}
  ctx.restore();}
function moth(x,y,s,t){const fl=Math.abs(Math.sin(t*28));ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='#CFC6B8';
  ctx.beginPath();ctx.ellipse(-9,0,12,6+fl*6,0.5,0,7);ctx.ellipse(9,0,12,6+fl*6,-0.5,0,7);ctx.fill();ctx.fillStyle='#6E6556';ctx.beginPath();ctx.ellipse(0,0,4,9,0,0,7);ctx.fill();ctx.restore();}
function pockets(x,s,t,t0){const pk=lin(t,t0,t0+0.2);if(pk<=0)return;ctx.save();ctx.fillStyle='#F6F1E7';
  [-1,1].forEach(d=>{ctx.save();ctx.translate(x+d*76*s,GROUND-100*s);ctx.rotate(d*(0.3+Math.sin(t*12)*0.1));ctx.scale(back(pk),back(pk));
    ctx.beginPath();ctx.moveTo(0,-30);ctx.lineTo(d*62,-18);ctx.lineTo(d*55,36);ctx.lineTo(0,26);ctx.closePath();ctx.fill();ctx.strokeStyle='#C9666B';ctx.lineWidth=5;ctx.stroke();ctx.restore();});ctx.restore();}


// ================= HUMOR LAYER =================
function comic(x,y,word,k,col=C.yel,size=80,rot=-0.12){if(k<=0||k>=1)return;const s=back(cl(k*3));ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);
  ctx.globalAlpha=k>0.8?(1-k)*5:1;ctx.font=`900 ${size}px ${F}`;ctx.lineWidth=12;ctx.strokeStyle='#17143A';ctx.lineJoin='round';ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.strokeText(word,0,0);ctx.fillStyle=col;ctx.fillText(word,0,0);ctx.restore();}
function dizzy(x,y,t){for(let i=0;i<3;i++){const a=t*5+i*2.1;txt('★',x+Math.cos(a)*70,y+Math.sin(a)*22,40,C.yel,'center','900');}}
function wings(x,y,t,s=1){const f=Math.sin(t*30)*0.6;ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='#F6F1E7';
  for(const d of [-1,1]){ctx.save();ctx.scale(d,1);ctx.rotate(-0.4+f);ctx.beginPath();ctx.ellipse(40,-10,40,16,-0.5,0,7);ctx.fill();ctx.restore();}ctx.restore();}
function jitterLines(x,y,t){ctx.strokeStyle=C.yel;ctx.lineWidth=5;for(const d of [-1,1]){ctx.beginPath();for(let k=0;k<5;k++){const xx=x+d*(140+k*6)+(k%2?8:-8),yy=y-60+k*30;k?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy);}ctx.stroke();}}
function floatHearts(x,y,t,t0){for(let i=0;i<4;i++){const k=((t-t0)*0.6+i*0.25)%1;txt('♥',x+Math.sin(k*8+i)*40-60+i*40,y-k*260,40+20*(1-k),C.cor,'center','900');}}
function runningWallet(x,t){ctx.save();ctx.strokeStyle=C.ink;ctx.lineWidth=8;ctx.lineCap='round';const st=Math.sin(t*20);
  ctx.beginPath();ctx.moveTo(x-30,870);ctx.lineTo(x-30+st*20,900);ctx.moveTo(x+30,870);ctx.lineTo(x+30-st*20,900);ctx.stroke();ctx.restore();wallet(x,820,0.45,0,0);}
function tear(x,y,t,t0){const k=((t-t0)*0.8)%1;ctx.fillStyle='#7FD3FF';ctx.beginPath();ctx.ellipse(x,y+k*60,7,10,0,0,7);ctx.fill();}

