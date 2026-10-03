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
    path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(path,size) if Path(path).exists() else ImageFont.load_default()

def fit(draw,text,max_width,start,min_size,bold=True):
    for size in range(start,min_size-1,-1):
        f=font(size,bold)
        if draw.textbbox((0,0),text,font=f)[2] <= max_width: return f
    return font(min_size,bold)

def make_badge(master,out_path,cid,issue_date,url):
    im=Image.open(master).convert('RGBA').resize((1200,1200),Image.Resampling.LANCZOS)
    d=ImageDraw.Draw(im)
    green=(3,54,41,255); gold=(224,178,54,255); white=(255,255,255,255)

    # One unified panel completely inside the circular badge. It covers the
    # original placeholder ID/QR area and prevents any detached overlay.
    panel=(205,805,940,1035)
    d.rounded_rectangle(panel,radius=28,fill=green,outline=gold,width=5)

    # Left: credential details.
    d.text((240,835),'Credential ID',font=font(25,True),fill=gold)
    d.text((240,872),cid,font=fit(d,cid,410,38,24,True),fill=white)
    d.line((240,920,675,920),fill=gold,width=3)
    d.text((240,938),'Issue date',font=font(25,True),fill=gold)
    d.text((240,975),issue_date,font=fit(d,issue_date,410,34,22,False),fill=white)

    # Right: unique QR with full quiet zone; entirely inside the unified panel.
    qr=qrcode.QRCode(version=None,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4)
    qr.add_data(url); qr.make(fit=True)
    qrim=qr.make_image(fill_color='black',back_color='white').convert('RGBA').resize((156,156),Image.Resampling.NEAREST)
    d.rounded_rectangle((720,821,910,1021),radius=16,fill=white,outline=gold,width=3)
    im.alpha_composite(qrim,(737,831))
    caption='SCAN TO VERIFY'; cf=fit(d,caption,166,19,14,True)
    bb=d.textbbox((0,0),caption,font=cf)
    d.rectangle((730,982,900,1014),fill=white)
    d.text((815-(bb[2]-bb[0])/2,988),caption,font=cf,fill=(0,0,0,255))
    im.save(out_path,optimize=True)

with open(sys.argv[1],newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        typ=row['credential_type'].strip().upper(); cid=row['credential_id'].strip().upper()
        if typ not in TITLES or not ID_RE.fullmatch(cid) or cid.split('-')[1] != typ:
            raise ValueError(f'Invalid credential type/ID: {typ}/{cid}')
        url=f'{BASE_URL}/credentials/{cid}.html'
        filename=f'{cid}-v5.png'
        make_badge(root/'assets'/'badges'/BADGES[typ],issued/filename,cid,row['issue_date'],url)
        html=template
        vals={'{{CREDENTIAL_TITLE}}':TITLES[typ],'{{CREDENTIAL_ID}}':cid,'{{PUBLIC_NAME}}':row['public_name'],'{{ISSUE_DATE}}':row['issue_date'],'{{STATUS}}':row['status'],'{{CRITERIA_URL}}':f'../criteria/{SLUGS[typ]}.html','{{BADGE_URL}}':f'../assets/issued/{filename}'}
        for k,v in vals.items(): html=html.replace(k,v)
        (root/'credentials'/f'{cid}.html').write_text(html,encoding='utf-8')
        print(url)
