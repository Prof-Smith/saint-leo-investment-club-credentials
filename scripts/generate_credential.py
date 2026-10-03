#!/usr/bin/env python3
import csv, os, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode
BASE_URL=os.getenv('BASE_URL','https://USERNAME.github.io/REPOSITORY').rstrip('/')
TITLES={'EXP':'Finance Explorer','NET':'Investment Networker','CMS':'Capital Markets Scholar','LIF':'Leo Investment Fellow'}
SLUGS={'EXP':'finance-explorer','NET':'investment-networker','CMS':'capital-markets-scholar','LIF':'leo-investment-fellow'}
BADGES={'EXP':'finance-explorer-master-v5.png','NET':'investment-networker-master-v5.png','CMS':'capital-markets-scholar-master-v5.png','LIF':'leo-investment-fellow-master-v5.png'}
ID_RE=re.compile(r'^SLIC-(EXP|NET|CMS|LIF)-\d{4}-\d{3}$')
root=Path(__file__).resolve().parents[1]
template=(root/'templates/credential-template.html').read_text(encoding='utf-8')
issued=root/'assets'/'issued'; issued.mkdir(parents=True,exist_ok=True)
def font(size,bold=False):
 p='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 return ImageFont.truetype(p,size) if Path(p).exists() else ImageFont.load_default()
def fit(draw,text,w,start,minimum,bold=True):
 for n in range(start,minimum-1,-1):
  f=font(n,bold)
  if draw.textbbox((0,0),text,font=f)[2] <= w:return f
 return font(minimum,bold)
def make_badge(master,out_path,cid,issue_date,url):
 im=Image.open(master).convert('RGBA').resize((1200,1200),Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(im); green=(3,54,41,255); gold=(224,178,54,255); white=(255,255,255,255)
 # Replace only the existing credential fields. No new external panel.
 d.rounded_rectangle((260,862,585,1012),radius=8,fill=green,outline=gold,width=3)
 d.text((278,878),'Credential ID:',font=font(17,True),fill=gold)
 d.text((278,904),cid,font=fit(d,cid,285,24,16,True),fill=white)
 d.line((278,940,565,940),fill=gold,width=2)
 d.text((278,949),'Issued:',font=font(16,True),fill=gold)
 d.text((278,975),issue_date,font=fit(d,issue_date,285,22,15,False),fill=white)
 # Replace only the existing QR field.
 qr=qrcode.QRCode(version=None,error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=3,border=4)
 qr.add_data(url); qr.make(fit=True)
 qrim=qr.make_image(fill_color='black',back_color='white').convert('RGBA')
 d.rounded_rectangle((600,852,777,1025),radius=8,fill=white,outline=gold,width=3)
 im.alpha_composite(qrim,(615,860))
 d.rectangle((615,1000,762,1018),fill=white)
 cap='SCAN TO VERIFY'; f=fit(d,cap,134,15,11,True); bb=d.textbbox((0,0),cap,font=f)
 d.text((688-(bb[2]-bb[0])/2,1001),cap,font=f,fill=(0,0,0,255))
 im.save(out_path,optimize=True)
with open(sys.argv[1],newline='',encoding='utf-8') as f:
 for row in csv.DictReader(f):
  typ=row['credential_type'].strip().upper(); cid=row['credential_id'].strip().upper()
  if typ not in TITLES or not ID_RE.fullmatch(cid) or cid.split('-')[1]!=typ:raise ValueError(f'Invalid credential type/ID: {typ}/{cid}')
  url=f'{BASE_URL}/credentials/{cid}.html'; fn=f'{cid}-v7.png'
  make_badge(root/'assets'/'badges'/BADGES[typ],issued/fn,cid,row['issue_date'],url)
  html=template
  vals={'{{CREDENTIAL_TITLE}}':TITLES[typ],'{{CREDENTIAL_ID}}':cid,'{{PUBLIC_NAME}}':row['public_name'],'{{ISSUE_DATE}}':row['issue_date'],'{{STATUS}}':row['status'],'{{CRITERIA_URL}}':f'../criteria/{SLUGS[typ]}.html','{{BADGE_URL}}':f'../assets/issued/{fn}'}
  for k,v in vals.items():html=html.replace(k,v)
  (root/'credentials'/f'{cid}.html').write_text(html,encoding='utf-8')
