#!/usr/bin/env python3
"""Generate a public credential page from an approved CSV row.
Usage: python scripts/generate_credential.py sample-data/approved-credential.csv
Set BASE_URL before production use. This script intentionally does not publish private evidence.
"""
import csv, os, sys
from pathlib import Path
BASE_URL=os.getenv('BASE_URL','https://USERNAME.github.io/REPOSITORY')
TITLES={'EXP':'Finance Explorer','NET':'Investment Networker','CMS':'Capital Markets Scholar','LIF':'Leo Investment Fellow'}
SLUGS={'EXP':'finance-explorer','NET':'investment-networker','CMS':'capital-markets-scholar','LIF':'leo-investment-fellow'}
BADGES={'EXP':'finance-explorer-master.png','NET':'investment-networker-master.png','CMS':'capital-markets-scholar-master.png','LIF':'leo-investment-fellow-master.png'}
root=Path(__file__).resolve().parents[1]
template=(root/'templates/credential-template.html').read_text(encoding='utf-8')
with open(sys.argv[1],newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        typ=row['credential_type'].upper(); cid=row['credential_id'].upper()
        html=template
        values={'{{CREDENTIAL_TITLE}}':TITLES[typ],'{{CREDENTIAL_ID}}':cid,'{{PUBLIC_NAME}}':row['public_name'],'{{ISSUE_DATE}}':row['issue_date'],'{{STATUS}}':row['status'],'{{CRITERIA_URL}}':f'../criteria/{SLUGS[typ]}.html','{{BADGE_URL}}':f'../assets/badges/{BADGES[typ]}'}
        for k,v in values.items(): html=html.replace(k,v)
        (root/'credentials'/f'{cid}.html').write_text(html,encoding='utf-8')
        print(f'Created {BASE_URL}/credentials/{cid}.html')
