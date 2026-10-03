#!/usr/bin/env python3
import csv, os, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode
BASE_URL=os.getenv('BASE_URL','https://USERNAME.github.io/REPOSITORY').rstrip('/')
TITLES={'EXP':'Finance Explorer','NET':'Investment Networker','CMS':'Capital Markets Scholar','LIF':'Leo Investment Fellow'}
SLUGS={'EXP':'finance-explorer','NET':'investment-networker','CMS':'capital-markets-scholar','LIF':'leo-investment-fellow'}
BADGES={'EXP':'finance-explorer-clean-v10.png','NET':'investment-networker-clean-v10.png','CMS':'capital-markets-scholar-clean-v10.png','LIF':'leo-investment-fellow-clean-v10.png'}
ID_RE=re.compile(r'^SLIC-(EXP|NET|CMS|LIF)-\d{4}-\d{3}$')
root=Path(__file__).resolve().parents[1]; template=(root/'templates/credential-template.html').read_text(encoding='utf-8'); issued=root/'assets/issued'; issued.mkdir(exist_ok=True)
def fnt(n,b=False):
 p='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if b else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; return ImageFont.truetype(p,n)
def fit(d,t,w,s,m,b=True):
 for n in range(s,m-1,-1):
  f=fnt(n,b)
  if d.textbbox((0,0),t,font=f)[2] <= w:return f
 return fnt(m,b)
def make(master,out,cid,date,url):
 im=Image.open(master).convert('RGBA'); d=ImageDraw.Draw(im); gold=(232,190,70,255); white=(255,255,255,255)
 # data sits entirely inside rebuilt footer strip
 d.text((225,805),'CREDENTIAL ID',font=fnt(22,True),fill=gold)
 d.text((225,840),cid,font=fit(d,cid,430,37,23,True),fill=white)
 d.text((225,910),'ISSUE DATE',font=fnt(21,True),fill=gold)
 d.text((225,945),date,font=fit(d,date,430,31,20,False),fill=white)
 qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=3,border=4); qr.add_data(url); qr.make(fit=True)
 q=qr.make_image(fill_color='black',back_color='white').convert('RGBA'); qw,qh=q.size
 box=(745,792,955,982); d.rounded_rectangle(box,radius=13,fill='white',outline=gold,width=4)
 im.alpha_composite(q,(850-qw//2,800))
 d.rectangle((760,946,940,974),fill='white')
 cap='SCAN TO VERIFY'; cf=fit(d,cap,168,17,12,True); bb=d.textbbox((0,0),cap,font=cf); d.text((850-(bb[2]-bb[0])/2,950),cap,font=cf,fill='black')
 im.save(out,optimize=True)
with open(sys.argv[1],newline='',encoding='utf-8') as f:
 for row in csv.DictReader(f):
  typ=row['credential_type'].strip().upper(); cid=row['credential_id'].strip().upper()
  if typ not in TITLES or not ID_RE.fullmatch(cid) or cid.split('-')[1]!=typ: raise ValueError(cid)
  url=f'{BASE_URL}/credentials/{cid}.html'; fn=f'{cid}-v10.png'; make(root/'assets/badges'/BADGES[typ],issued/fn,cid,row['issue_date'],url)
  html=template
  vals={'{{CREDENTIAL_TITLE}}':TITLES[typ],'{{CREDENTIAL_ID}}':cid,'{{PUBLIC_NAME}}':row['public_name'],'{{ISSUE_DATE}}':row['issue_date'],'{{STATUS}}':row['status'],'{{CRITERIA_URL}}':f'../criteria/{SLUGS[typ]}.html','{{BADGE_URL}}':f'../assets/issued/{fn}'}
  for k,v in vals.items(): html=html.replace(k,v)
  (root/'credentials'/f'{cid}.html').write_text(html,encoding='utf-8')
