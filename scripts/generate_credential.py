#!/usr/bin/env python3
import csv, os, re, sys
from pathlib import Path
import qrcode
BASE_URL=os.getenv('BASE_URL','https://USERNAME.github.io/REPOSITORY').rstrip('/')
TITLES={'EXP':'Finance Explorer','NET':'Investment Networker','CMS':'Capital Markets Scholar','LIF':'Leo Investment Fellow'}
SLUGS={'EXP':'finance-explorer','NET':'investment-networker','CMS':'capital-markets-scholar','LIF':'leo-investment-fellow'}
BADGES={'EXP':'finance-explorer-display-v25.png','NET':'investment-networker-display-v25.png','CMS':'capital-markets-scholar-display-v31.jpg','LIF':'leo-investment-fellow-display-v31.jpg'}
ID_RE=re.compile(r'^SLIC-(EXP|NET|CMS|LIF)-\d{4}-\d{3}$')
root=Path(__file__).resolve().parents[1]; template=(root/'templates/credential-template.html').read_text(encoding='utf-8'); qrdir=root/'assets/qr'; qrdir.mkdir(exist_ok=True)
with open(sys.argv[1],newline='',encoding='utf-8') as f:
 for row in csv.DictReader(f):
  typ=row['credential_type'].strip().upper(); cid=row['credential_id'].strip().upper()
  if typ not in TITLES or not ID_RE.fullmatch(cid) or cid.split('-')[1]!=typ: raise ValueError(cid)
  url=f'{BASE_URL}/credentials/{cid}.html'
  qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=8,border=4); qr.add_data(url); qr.make(fit=True)
  qr.make_image(fill_color='black',back_color='white').save(qrdir/f'{cid}-qr-v31.png')
  html=template
  vals={'{{CREDENTIAL_TITLE}}':TITLES[typ],'{{CREDENTIAL_ID}}':cid,'{{PUBLIC_NAME}}':row['public_name'],'{{ISSUE_DATE}}':row['issue_date'],'{{STATUS}}':row['status'],'{{CRITERIA_URL}}':f'../criteria/{SLUGS[typ]}.html','{{BADGE_URL}}':f'../assets/badges/{BADGES[typ]}','{{QR_URL}}':f'../assets/qr/{cid}-qr-v31.png'}
  for k,v in vals.items(): html=html.replace(k,v)
  (root/'credentials'/f'{cid}.html').write_text(html,encoding='utf-8')
