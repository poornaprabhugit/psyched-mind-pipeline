// ===== 28 Nov batch · 7 animated Shorts =====
function devil(x,y,s,t){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle=C.cor;rr(-30,-50,60,90,30);ctx.fill();
  ctx.beginPath();ctx.moveTo(-24,-40);ctx.lineTo(-34,-70);ctx.lineTo(-10,-48);ctx.moveTo(24,-40);ctx.lineTo(34,-70);ctx.lineTo(10,-48);ctx.fill();
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(-10,-20,7,0,7);ctx.arc(10,-20,7,0,7);ctx.fill();ctx.fillStyle='#1a1630';ctx.beginPath();ctx.arc(-9,-19,3,0,7);ctx.arc(11,-19,3,0,7);ctx.fill();
  ctx.strokeStyle='#1a1630';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,-4,9,0.1*Math.PI,0.9*Math.PI);ctx.stroke();ctx.restore();}
function halo(x,y,k){if(k<=0)return;ctx.save();ctx.globalAlpha=k;ctx.strokeStyle=C.yel;ctx.lineWidth=8;ctx.beginPath();ctx.ellipse(x,y,70,18,0,0,7);ctx.stroke();ctx.restore();}
function bigNum(x,y,v,col,label){txt(v,x,y,130,col,'center','900');if(label)txt(label,x,y+90,40,C.ink,'center','bold');}
function vbar(x,base,w,h,col,label,val,k){ctx.fillStyle='rgba(255,255,255,0.1)';rr(x-w/2,base-500,w,500,20);ctx.fill();ctx.fillStyle=col;rr(x-w/2,base-h*k,w,h*k,20);ctx.fill();
  txt(label,x,base+50,38,C.ink,'center','900');if(k>0.2)txt(val,x,base-h*k-60,80,col,'center','900');}
function beer(x,y,s,col){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='rgba(255,255,255,0.25)';ctx.beginPath();ctx.moveTo(-40,-110);ctx.lineTo(40,-110);ctx.lineTo(32,40);ctx.lineTo(-32,40);ctx.closePath();ctx.fill();
  ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(-36,-80);ctx.lineTo(36,-80);ctx.lineTo(30,36);ctx.lineTo(-30,36);ctx.closePath();ctx.fill();ctx.fillStyle='#FFF8E8';rr(-40,-112,80,34,16);ctx.fill();ctx.restore();}
function calendarPage(x,y,s,day,label){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle='#F6F1E7';rr(-120,-140,240,280,18);ctx.fill();ctx.fillStyle=C.cor;rr(-120,-140,240,70,18);ctx.fill();ctx.fillRect(-120,-90,240,20);
  txt(label||'DAY',0,-104,34,'#fff','center','900');txt(String(day),0,40,110,'#17143A','center','900');ctx.restore();}
function confetti(x,y,t,t0){const k=t-t0;if(k<0||k>2.5)return;const cs=[C.yel,C.cor,C.grn,C.blu,C.pnk];for(let i=0;i<30;i++){const a=i*2.39,v=380+(i%5)*60;
  const px=x+Math.cos(a)*v*k*0.8,py=y-Math.sin(a)*v*k*0.8+500*k*k*0.5;ctx.fillStyle=cs[i%5];ctx.save();ctx.translate(px,py);ctx.rotate(k*8+i);ctx.fillRect(-8,-4,16,8);ctx.restore();}}
function sweat(x,y,t){for(let i=0;i<2;i++){const k=((t*1.5)+i*0.5)%1;ctx.fillStyle='#7FD3FF';ctx.beginPath();ctx.ellipse(x+i*30,y+k*60,8,12,0,0,7);ctx.fill();}}
function tabs(x,y,n,t){for(let i=0;i<n;i++){ctx.fillStyle=i%2?'#E8E4F7':'#F6F1E7';rr(x-180+i*14,y-140+i*10,300,200,12);ctx.fill();}txt('JOB OFFER',x-30+n*14,y-60+n*10,26,'#17143A','center','900');}

// ---------- Q01 wallet ----------
SH.q01={hook:'Found a wallet with cash. Return it?',
 draw(t){const tR=A('researchers turned'),tE=A('empty ones'),t40=A('forty percent'),tM=A('with money inside'),t51=A('fifty-one'),tMost=A('most people guessed');
  if(t<tR){street();ctx.fillStyle='#3A3378';rr(760,880,240,300,14);ctx.fill();txt('LOST &',880,940,40,'#fff','center','900');txt('FOUND',880,990,40,'#fff','center','900');
    const pick=L(t,0.5,0.4);const walk=L(t,2.3,1.0);const px=mix(330,620,walk);
    if(pick<1)wallet(420,1150,0.6,0,2);else wallet(px+150,980,0.55,0,2);
    pip({x:px,y:GROUND,s:1.4,col:C.blu,mood:t<0.5?'calm':(t<1.2?'shock':(t<2.3?'meh':'happy')),arms:t>0.5?[0.35,-1.4]:[0.35,-0.35],look:t<0.5?-0.6:0.6,walk:walk>0&&walk<1?t*1.7:null});
    halo(px,GROUND-420*1.4+60,L(t,2.2,0.3));}
  else if(t<tE){sky(false);txt('Researchers turned in',W/2,470,50,C.ink,'center','900');txt('17,000+ “lost” wallets',W/2,540,60,C.yel,'center','900');
    ctx.fillStyle='#2C2766';ctx.beginPath();ctx.ellipse(W/2,880,420,230,0,0,7);ctx.fill();
    const k=L(t,A('forty countries'),1.2);for(let i=0;i<40;i++){if(i/40>k)break;const a=i*2.4,r=60+(i*53)%330;ctx.fillStyle=C.cor;ctx.beginPath();ctx.arc(W/2+Math.cos(a)*r,880+Math.sin(a)*r*0.5,10,0,7);ctx.fill();}
    txt(Math.round(40*k)+' countries',W/2,1180,56,C.ink,'center','900');}
  else if(t<tMost){sky(false);vbar(340,1150,240,0.4*800,C.dim,'empty',Math.round(40*L(t,t40,0.6))+'%',L(t,t40,0.6));wallet(340,560,0.5,0,0);
    if(t>tM){vbar(740,1150,240,0.51*800,C.grn,'with money',Math.round(51*L(t,t51,0.6))+'%',L(t,t51,0.6));wallet(740,560,0.5,0,3);}
    txt('came back',W/2,480,56,C.ink,'center','900');}
  else {street();const cols=[C.pnk,C.yel,'#5FD3F3'];cols.forEach((c,i)=>{pip({x:220+i*220,y:GROUND,s:0.9,col:c,mood:t>tMost+1.1?'shock':'calm',look:0.3});});
    bubble(150,520,640,180,300,720);txt('Cash = fewer come back',470,610,40,'#17143A','center','900');stamp(470,610,'WRONG',L(t,tMost+0.9,0.4),C.cor,80,-0.12);
    pip({x:880,y:GROUND,s:1.2,col:C.blu,mood:'happy',look:-0.5});halo(880,GROUND-420*1.2+50,1);}},
 gag(t){if(t>1.1&&t<2.2){const k=L(t,1.1,0.3);devil(560,640-20*Math.sin(t*6),0.9*k,t);comic(560,520,'keep it?',(t-1.1)/1.1,C.cor,46);}
   if(t>2.1&&t<2.6)comic(560,640,'POOF',(t-2.1)/0.5,'#fff',60);},
 cam(){return [[1.0,1.3,1.25,450,800]];},
 sfx(){return [[0.5,'pop'],[1.1,'boing'],[2.15,'pop'],[2.3,'ding'],[A('most people guessed')+0.9,'wah']];}};

// ---------- Q04 planning ----------
SH.q04={hook:'Your paper: done in 34 days, or 56?',
 draw(t){const tS=A('students guessed'),tAvg=A('average guess'),tReal=A('real time'),t56=A('fifty-six'),tFew=A('fewer than one'),tHalf=A('about half');
  if(t<tFew){sky(false);ctx.fillStyle='#3A3378';rr(150,900,780,40,12);ctx.fill();ctx.fillRect(200,940,24,240);ctx.fillRect(860,940,24,240);
    ctx.fillStyle='#F6F1E7';for(let i=0;i<5;i++)rr(560-i*4,830-i*14,220,30,4),ctx.fill();
    const flip=t>tReal?L(t,tReal,1.6):0;const day=t<tAvg?'?':(t<tReal?34:Math.round(mix(34,56,flip)));
    calendarPage(780,560,1.1,day,t<tReal?'MY GUESS':'REAL');
    if(t>tReal&&flip<1){for(let i=0;i<3;i++){const k=((t*6)+i*0.33)%1;ctx.save();ctx.globalAlpha=1-k;ctx.translate(780+k*200,560-k*300);ctx.rotate(k*3);ctx.fillStyle='#F6F1E7';rr(-90,-110,180,220,14);ctx.fill();ctx.restore();}}
    const beard=L(t,tReal,2);pip({x:400,y:GROUND,s:1.4,col:C.blu,mood:t<tReal?'happy':(beard>0.6?'meh':'shock'),arms:t<tReal?[0.35,-2.6]:[0.35,-0.35],look:0.6});
    if(beard>0){ctx.fillStyle='#E9E4F2';ctx.beginPath();ctx.ellipse(400,GROUND-170*1.4,70,40+beard*90,0,0,Math.PI);ctx.fill();}
    if(t>tAvg&&t<tReal)badge(780,860,'guess: 34 days',C.yel,L(t,tAvg,0.3));if(t>t56)badge(780,860,'real: 56 days',C.cor,L(t,t56,0.3));}
  else {sky(false);txt('Finished on time',W/2,470,58,C.ink,'center','900');
    for(let i=0;i<3;i++){const ok=i===0;pip({x:240+i*300,y:900,s:0.85,col:ok?C.grn:C.dim,mood:ok?'happy':'sad',look:0});mark(240+i*300,480+50,ok,L(t,tFew+i*0.2,0.3));}
    txt('fewer than 1 in 3',W/2,1000,60,C.yel,'center','900');
    if(t>tHalf){badge(W/2,1130,'about half missed even their worst-case date',C.cor,L(t,tHalf,0.3));}}},
 gag(t){const tR=A('real time');if(t>tR+0.3&&t<A('fewer than one'))comic(560,680,'*sigh*',((t-tR-0.3)%1.8)/1.2,C.dim,48);},
 cam(){return [[A('real time')+0.8,1.6,1.25,450,780]];},
 sfx(){const r=A('real time');return [[A('average guess'),'pop'],[r,'whoosh'],[r+0.4,'brr'],[A('fewer than one'),'wah']];}};

// ---------- Q06 train ----------
SH.q06={hook:'Talk to the stranger, or sit alone?',
 draw(t){const tT=A('train commuters'),tO=A('other commuters predicted'),tW=A("it wasnt"),tTalk=A('the talkers had'),tWe=A('we just expect');
  sky(false);ctx.fillStyle='#2C2766';rr(60,420,960,420,30);ctx.fill();
  ctx.save();ctx.beginPath();rr(100,460,880,260,20);ctx.clip();ctx.fillStyle='#3B3A7A';ctx.fillRect(100,460,880,260);
  for(let i=0;i<8;i++){const x=((i*170-t*260)%1360+1360)%1360-160;ctx.fillStyle='#4C4A9A';ctx.fillRect(x,520+((i*41)%120),120,200);}ctx.restore();
  ctx.fillStyle='#3A3378';rr(120,1000,840,180,30);ctx.fill();
  const hi=t>tT+0.6;const glance=t<tT+0.6?Math.sin(t*2.6):0;
  pip({x:380,y:GROUND,s:1.25,col:C.blu,mood:hi?'happy':'calm',arms:[0.35,-0.35],look:hi?0.8:(glance>0?0.8:-0.8)});
  pip({x:700,y:GROUND,s:1.25,col:C.yel,mood:hi?'happy':'calm',arms:[0.35,-0.35],look:hi?-0.8:(glance>0?-0.8:0.8)});
  if(hi&&t<tO){bubble(170,300,300,130,330,440);txt('Hi!',320,365,56,'#17143A','center','900');}
  if(t>tO&&t<tWe){card(120,300,840,150,'rgba(10,8,30,0.85)');txt('Prediction: quiet ride = nicer',W/2,375,46,C.ink,'center','900');stamp(W/2,375,'NOPE',L(t,tW,0.4),C.cor,70,-0.1);
    if(t>tTalk)badge(W/2,520,'talkers: more pleasant trip',C.grn,L(t,tTalk,0.3));}
  if(t>tWe)txt('we just expect awkward',W/2,370,52,C.yel,'center','900');},
 gag(t){const tT=A('train commuters');if(t<tT+0.6){const ph=Math.sin(t*2.6);if(Math.abs(ph)>0.97)comic(540,700,'…',0.3,C.ink,70);}
   if(t>tT+0.6&&t<tT+2.5){for(let i=0;i<3;i++)txt('♪',380+i*140,640-((t*80+i*40)%160),50,C.yel,'center','900');}},
 cam(){return [[0.2,2.5,1.2,540,880]];},
 sfx(){const tT=A('train commuters');return [[0.9,'pop'],[2.1,'pop'],[tT+0.6,'ding'],[A("it wasnt"),'thud']];}};

// ---------- Q08 old friend ----------
SH.q08={hook:'Text an old friend after a long time?',
 draw(t){const tStudy=A('in study after study'),tThen=A('then senders guessed'),tAgain=A('again and again'),tLow=A('too low');
  if(t<tThen){sky(false);const sent=t>tStudy+0.2;
    pip({x:300,y:GROUND,s:1.3,col:C.blu,mood:sent?'happy':'shock',arms:[0.35,-1.4],look:0.6});phone(560,780,0.55);
    ctx.fillStyle=C.blu;rr(450,640,230,110,20);ctx.fill();txt('Hey! Been a',565,675,28,'#fff','center','900');txt('while!',565,715,28,'#fff','center','900');
    ctx.fillStyle=sent?C.grn:C.cor;rr(500,880,130,60,30);ctx.fill();txt(sent?'SENT':'SEND',565,911,30,'#fff','center','900');
    if(sent){pip({x:860,y:GROUND,s:1.0,col:C.pnk,mood:'happy',arms:[2.0,-2.0],look:-0.5});}}
  else {sky(false);txt('How much the note was appreciated',W/2,470,44,C.ink,'center','900');
    const k=L(t,tThen+0.6,0.7);vbar(340,1150,240,320,C.dim,'sender’s guess','',k);if(t>tAgain)vbar(740,1150,240,430,C.grn,'real','',L(t,tAgain,0.7));
    stamp(W/2,620,'TOO LOW',L(t,tLow,0.4),C.cor,80,-0.1);}},
 gag(t){const tS=A('in study after study');if(t<tS+0.2)sweat(360,GROUND-330*1.3,t);if(t>tS+0.2&&t<A('then senders guessed'))confetti(860,800,t,tS+0.3);
   if(t>tS+0.3&&t<tS+1.5)comic(860,620,'YAY!',(t-tS-0.3)/1.2,C.yel,70);},
 cam(){return [[0.3,1.8,1.3,470,800]];},
 sfx(){const tS=A('in study after study');return [[0.6,'buzz'],[tS+0.2,'ding'],[tS+0.3,'boing'],[A('too low'),'thud']];}};

// ---------- Q09 experience vs thing ----------
SH.q09={hook:'Concert ticket vs new jacket?',
 draw(t){const tOver=A('over twelve hundred'),tOwn=A('bought to own'),tDo=A('bought to do'),tWhich=A('which made them happier'),t57=A('fifty-seven'),t34=A('thirty-four');
  if(t<tOver||(t>tOwn&&t<tWhich)){sky(false);card(60,420,460,760);card(560,420,460,760);txt('A THING',290,480,40,C.dim,'center','900');txt('AN EXPERIENCE',790,480,40,C.dim,'center','900');
    jacket(290,760,1.1);
    for(let i=0;i<5;i++){ctx.fillStyle=[C.yel,C.pnk,'#5FD3F3',C.grn,C.cor][i];ctx.globalAlpha=0.5+0.5*Math.sin(t*4+i);ctx.beginPath();ctx.moveTo(620+i*90,520);ctx.lineTo(600+i*90,1000);ctx.lineTo(660+i*90,1000);ctx.fill();ctx.globalAlpha=1;}
    const dance=Math.sin(t*8)*0.5;pip({x:790,y:1120,s:0.95,col:C.blu,mood:'happy',arms:[1.6+dance,-1.6+dance],look:0});}
  else if(t<tOwn){sky(false);txt('1,263 Americans',W/2,480,64,C.yel,'center','900');txt('thought of two purchases',W/2,560,44,C.ink,'center','bold');people(150,660,12,10,Math.round(120*L(t,tOver,1.2)),C.blu,52,12);}
  else {sky(false);txt('Which made you happier?',W/2,470,54,C.ink,'center','900');
    vbar(340,1150,240,0.34*800,C.dim,'the thing',Math.round(34*L(t,t34,0.6))+'%',t>t34?L(t,t34,0.6):0);vbar(740,1150,240,0.57*800,C.grn,'the experience',Math.round(57*L(t,t57,0.6))+'%',L(t,t57,0.6));}},
 gag(t){const tOver=A('over twelve hundred');const show=t<tOver||(t>A('bought to own')&&t<A('which made them happier'));if(!show)return;
   const k=L(t,0.8,2.5);ctx.save();ctx.globalAlpha=0.6*k;ctx.fillStyle='#8F8AB8';for(let i=0;i<14;i++)ctx.fillRect(200+((i*37)%180),620+((i*53)%300),6,6);ctx.restore();
   if(k>0.3){const sy=mix(440,640,L(t,1.6,0.8));ctx.strokeStyle='#ddd';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(360,440);ctx.lineTo(360,sy);ctx.stroke();ctx.fillStyle='#111';ctx.beginPath();ctx.arc(360,sy,12,0,7);ctx.fill();
     ctx.strokeStyle='#111';ctx.lineWidth=3;for(let i=0;i<4;i++){ctx.beginPath();ctx.moveTo(348,sy-6+i*4);ctx.lineTo(334,sy-12+i*8);ctx.moveTo(372,sy-6+i*4);ctx.lineTo(386,sy-12+i*8);ctx.stroke();}}
   comic(290,1060,'dusty…',(t-2.2)/1.6,C.dim,44);},
 cam(){return [[1.4,2.2,1.25,300,760]];},
 sfx(){return [[1.6,'slide'],[A('fifty-seven'),'ding']];}};

// ---------- Q12 ordering ----------
SH.q12={hook:'Friend orders your pick first. Switch?',
 draw(t){const tBar=A('a bar offered'),tSome=A('some tables'),tPriv=A('others chose in private'),tOut=A('out loud people picked'),tLess=A('liked it less'),tMany=A('many wished');
  sky(true);ctx.fillStyle='#3A3378';rr(100,1000,880,40,14);ctx.fill();
  const cols=['#E8B13A','#5A2E1A','#F3D27A','#B8452E'];const names=['Amber','Dark','Pale','Red'];
  if(t<tSome||t>tPriv&&t<tOut){cols.forEach((c,i)=>beer(240+i*200,900,1,c));txt('4 free samples',W/2,470,56,C.yel,'center','900');
    if(t>tPriv){card(260,520,560,200,'#F6F1E7');txt('MENU (private)',W/2,570,34,'#17143A','center','900');txt('☑ Amber  ☐ Dark  ☐ Pale  ☐ Red',W/2,640,34,'#17143A','center','bold');}
    return;}
  const fr=[C.pnk,C.yel,'#5FD3F3'];fr.forEach((c,i)=>{pip({x:200+i*200,y:GROUND,s:0.85,col:c,mood:'happy',look:0.3});if(t>tSome+i*0.5&&t<tOut+0.5){bubble(120+i*200,470+i*20,170,90,210+i*200,580);txt(names[i]+'!',205+i*200,515+i*20,32,'#17143A','center','900');}
    if(t>tOut)beer(200+i*200,960,0.7,cols[i]);});
  const sw=t>tSome+1.6;pip({x:850,y:GROUND,s:1.0,col:C.blu,mood:t>tLess?'sad':(sw?'meh':'calm'),look:t>tMany?-0.9:-0.3});
  if(t>tSome+1.0&&t<tSome+1.6){bubble(720,440,260,100,800,560);txt('Amber…',850,490,34,'#17143A','center','900');}
  if(sw&&t<tOut+0.5){bubble(720,440,260,100,800,560);txt('Red!',850,490,40,'#17143A','center','900');}
  if(t>tOut)beer(850+60,960,0.7,cols[3]);},
 gag(t){const tL=A('liked it less'),tM=A('many wished');comic(850,640,'bleh',(t-tL)/1.0,C.grn,56);
   if(t>tM){const k=L(t,tM+0.6,0.6);comic(500,640,'mine!',(t-tM-0.6)/1.0,C.pnk,50);}},
 cam(){return [[A('many wished'),1.8,1.25,700,880]];},
 sfx(){return [[A('liked it less'),'wah'],[A('many wished')+0.6,'slide']];}};

// ---------- Q13 best vs good enough ----------
SH.q13={hook:'Best job or good-enough job?',
 draw(t){const tAm=A('american students'),tSome=A('some aimed'),tOth=A('others good enough'),tBest=A('the best-seekers'),t20=A('twenty percent'),tBut=A('but they felt');
  sky(false);card(50,420,470,780);card(560,420,470,780);txt('“THE BEST”',285,480,40,C.cor,'center','900');txt('“GOOD ENOUGH”',795,480,40,C.grn,'center','900');
  tabs(285,760,Math.min(12,Math.floor(L(t,tSome,2.5)*12)+1),t);
  pip({x:285,y:1150,s:0.85,col:C.blu,mood:t>tBut?'shock':'calm',look:0.2,arms:[0.35,-1.3]});
  ctx.strokeStyle='#F6F1E7';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(640,700);ctx.quadraticCurveTo(795,820,950,700);ctx.stroke();ctx.fillStyle='#2BB3A3';ctx.beginPath();ctx.moveTo(640,700);ctx.quadraticCurveTo(795,860,950,700);ctx.quadraticCurveTo(795,800,640,700);ctx.fill();
  pip({x:795,y:860,s:0.6,col:C.yel,mood:'happy',look:0});
  if(t>t20)badge(285,580,'+20% pay',C.yel,L(t,t20,0.3));
  if(t>tBut){snowCloud(285,560,t);badge(285,1120,'more stressed',C.cor,L(t,tBut,0.3));badge(795,1120,'happier with the job',C.grn,L(t,tBut+0.6,0.3));}},
 gag(t){const tB=A('but they felt');if(t>A('some aimed')+1&&t<tB+0.2){const tw=Math.sin(t*40)>0.6;if(tw)comic(285,880,'twitch',0.3,C.cor,38);}
   txt('z',870-((t*30)%40),760-((t*40)%80),36,C.ink,'center','900');},
 cam(){return [[A('but they felt')+0.4,1.8,1.2,285,800]];},
 sfx(){return [[A('twenty percent'),'ding'],[A('but they felt'),'thud']];}};
