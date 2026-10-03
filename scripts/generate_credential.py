#!/usr/bin/env python3
import csv,os,sys
from pathlib import Path
import qrcode
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('BASE_URL','https://prof-smith.github.io/saint-leo-investment-club-credentials').rstrip('/')
MAP={
'finance-explorer':('Finance Explorer','../assets/badges/finance-explorer-landing-v38.png','../criteria/finance-explorer.html'),
'investment-networker':('Investment Networker','../assets/badges/investment-networker-landing-v38.png','../criteria/investment-networker.html'),
'capital-markets-scholar':('Capital Markets Scholar','../assets/badges/capital-markets-scholar-landing-v38.png','../criteria/capital-markets-scholar.html'),
'leo-investment-fellow':('Leo Investment Fellow','../assets/badges/leo-investment-fellow-landing-v38.png','../criteria/leo-investment-fellow.html')}
tpl=(ROOT/'templates/credential-template.html').read_text()
with open(sys.argv[1],newline='',encoding='utf-8-sig') as f:
 for row in csv.DictReader(f):
  typ=row['credential_type'].strip(); cid=row['credential_id'].strip().upper(); title,badge,criteria=MAP[typ]
  url=f'{BASE}/credentials/{cid}.html'; qrname=f'{cid}-qr-v31.png'; qrcode.make(url).save(ROOT/'assets/qr'/qrname)
  vals={'TITLE':title,'CREDENTIAL_ID':cid,'PUBLIC_NAME':row['public_name'].strip(),'ISSUE_DATE':row['issue_date'].strip(),'STATUS':row['status'].strip().upper(),'BADGE_URL':badge,'QR_URL':f'../assets/qr/{qrname}','CRITERIA_URL':criteria}
  html=tpl
  for k,v in vals.items(): html=html.replace('{{'+k+'}}',v)
  (ROOT/'credentials'/f'{cid}.html').write_text(html)
