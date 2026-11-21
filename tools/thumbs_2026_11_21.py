from PIL import Image, ImageDraw, ImageFont, ImageFilter
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def base(p, box):
    im=Image.open(p).convert('RGB').crop(box).resize((1280,720), Image.LANCZOS)
    return im
def text(im, lines, x, y, size, fill=(255,230,0), bg=None, anchor='la'):
    d=ImageDraw.Draw(im); f=ImageFont.truetype(FB,size)
    for i,l in enumerate(lines):
        yy=y+i*int(size*1.08)
        if bg:
            bb=d.textbbox((x,yy),l,font=f,anchor=anchor); d.rectangle((bb[0]-18,bb[1]-10,bb[2]+18,bb[3]+14),fill=bg)
        d.text((x,yy),l,font=f,fill=fill,anchor=anchor,stroke_width=0 if bg else 8,stroke_fill=(0,0,0))
    return im
def shade(im, side='right', strength=170):
    ov=Image.new('L',im.size,0); d=ImageDraw.Draw(ov)
    for x in range(im.width):
        a = int(strength*max(0,(x-im.width*0.4)/(im.width*0.6))) if side=='right' else int(strength*max(0,(im.width*0.6-x)/(im.width*0.6)))
        d.line((x,0,x,im.height),fill=a)
    dark=Image.new('RGB',im.size,(17,17,20)); return Image.composite(dark,im,ov)
# A: puzzled person, "FORGOT WHY?"
a=base('/tmp/claude-0/th_78.png',(60,0,1660,900)); a=shade(a,'left'); a=text(a,["FORGOT","WHY?"],50,200,150); a.save('/home/claude/deliver/long/Thumb A – Forgot why.jpg',quality=92)
# B: meeting, "WHAT WAS HER NAME?"
b=base('/tmp/claude-0/th_180.png',(0,0,1600,900)); b=shade(b,'left'); b=text(b,["WHAT WAS","HIS NAME?"],50,200,128,fill=(17,17,20),bg=(255,230,0)); b.save('/home/claude/deliver/long/Thumb B – His name.jpg',quality=92)
# C: hands on head, "ON PURPOSE"
c=base('/tmp/claude-0/th_24.png',(160,0,1760,900)); c=shade(c,'right',200); c=text(c,["ON","PURPOSE"],1240,230,150,fill=(17,17,20),bg=(255,230,0),anchor='ra'); c.save('/home/claude/deliver/long/Thumb C – On purpose.jpg',quality=92)
