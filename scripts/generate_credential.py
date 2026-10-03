#!/usr/bin/env python3
"""Generate unique credential pages and issued badge PNGs from an approved CSV.

Usage:
  BASE_URL="https://prof-smith.github.io/saint-leo-investment-club-credentials" \
  python scripts/generate_credential.py sample-data/approved-credential.csv

Each output badge contains the row's credential ID and issue date. Its QR code
encodes that credential's unique public verification URL.
"""
import csv, os, sys, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode

BASE_URL=os.getenv('BASE_URL','https://USERNAME.github.io/REPOSITORY').rstrip('/')
TITLES={'EXP':'Finance Explorer','NET':'Investment Networker','CMS':'Capital Markets Scholar','LIF':'Leo Investment Fellow'}
SLUGS={'EXP':'finance-explorer','NET':'investment-networker','CMS':'capital-markets-scholar','LIF':'leo-investment-fellow'}
BADGES={'EXP':'finance-explorer-master.png','NET':'investment-networker-master.png','CMS':'capital-markets-scholar-master.png','LIF':'leo-investment-fellow-master.png'}
ID_RE=re.compile(r'^SLIC-(EXP|NET|CMS|LIF)-\d{4}-\d{3}$')
root=Path(__file__).resolve().parents[1]
template=(root/'templates/credential-template.html').read_text(encoding='utf-8')
issued=root/'assets'/'issued'; issued.mkdir(parents=True,exist_ok=True)

def font(size,bold=False):
    names=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for n in names:
        if Path(n).exists(): return ImageFont.truetype(n,size)
    return ImageFont.load_default()

def fit_text(draw,text,max_width,start=38,min_size=20,bold=True):
    for size in range(start,min_size-1,-1):
        f=font(size,bold)
        if draw.textbbox((0,0),text,font=f)[2] <= max_width: return f
    return font(min_size,bold)

def make_issued_badge(master_path,out_path,cid,issue_date,url):
    im=Image.open(master_path).convert('RGBA').resize((1200,1200),Image.Resampling.LANCZOS)
    d=ImageDraw.Draw(im)
    green=(4,55,42,255); gold=(221,178,63,255); white=(255,255,255,255)

    # Credential data is integrated into the lower portion of the circular badge.
    # The panels stay above the lower ring so nothing appears detached from the badge.
    d.rounded_rectangle((150,835,610,1045),radius=24,fill=green,outline=gold,width=4)
    d.text((180,855),'Credential ID:',font=font(27),fill=white)
    d.text((180,892),cid,font=fit_text(d,cid,395,37,23),fill=white)
    d.line((180,940,580,940),fill=gold,width=3)
    d.text((180,953),'Issued:',font=font(26),fill=white)
    d.text((180,989),issue_date,font=fit_text(d,issue_date,395,33,21),fill=white)

    qr=qrcode.QRCode(version=None,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4)
    qr.add_data(url); qr.make(fit=True)
    qrim=qr.make_image(fill_color='black',back_color='white').convert('RGBA').resize((168,168),Image.Resampling.NEAREST)
    d.rounded_rectangle((635,832,855,1052),radius=20,fill=white,outline=gold,width=4)
    im.alpha_composite(qrim,(661,845))

    caption='SCAN TO VERIFY'
    d.rounded_rectangle((650,1018,840,1043),radius=8,fill=white)
    cf=fit_text(d,caption,178,22,16)
    bb=d.textbbox((0,0),caption,font=cf)
    d.text((745-(bb[2]-bb[0])/2,1019),caption,font=cf,fill=(0,0,0,255))
    im.save(out_path,optimize=True)

with open(sys.argv[1],newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        typ=row['credential_type'].strip().upper(); cid=row['credential_id'].strip().upper()
        if typ not in TITLES: raise ValueError(f'Unknown credential type: {typ}')
        if not ID_RE.fullmatch(cid) or cid.split('-')[1] != typ: raise ValueError(f'Invalid credential ID/type: {cid}/{typ}')
        verification_url=f'{BASE_URL}/credentials/{cid}.html'
        badge_rel=f'../assets/issued/{cid}.png?v=4'
        make_issued_badge(root/'assets'/'badges'/BADGES[typ],issued/f'{cid}.png',cid,row['issue_date'],verification_url)
        html=template
        values={'{{CREDENTIAL_TITLE}}':TITLES[typ],'{{CREDENTIAL_ID}}':cid,'{{PUBLIC_NAME}}':row['public_name'],'{{ISSUE_DATE}}':row['issue_date'],'{{STATUS}}':row['status'],'{{CRITERIA_URL}}':f'../criteria/{SLUGS[typ]}.html','{{BADGE_URL}}':badge_rel}
        for k,v in values.items(): html=html.replace(k,v)
        (root/'credentials'/f'{cid}.html').write_text(html,encoding='utf-8')
        print(f'Created {verification_url}')
        print(f'Created assets/issued/{cid}.png')
