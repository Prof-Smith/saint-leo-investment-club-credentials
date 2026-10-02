# Saint Leo Investment Club Professional Credential Program

Production-ready starter repository for a controlled GitHub Pages credential-verification site.

## Repository contents
- Four individual badge master templates plus the master sheet
- Public pathway homepage and credential lookup
- Four public criteria pages
- Issuance, privacy, and revocation policies
- Public credential-page template
- CSV-to-credential-page generator
- Administrative checklist and private-register guidance
- Custom 404 page

## Publish with GitHub Pages
1. Create the final public repository.
2. Upload the contents of this package to the repository root.
3. In repository Settings, configure Pages to deploy from the `main` branch and root folder.
4. Replace placeholders in `scripts/generate_credential.py`, README, and site metadata with the final organization, repository, and contact information.
5. Test the sample workflow before issuing a real credential.

## Controlled issuance
Private evidence and the credential register stay outside GitHub. Only faculty-approved public records are committed. Students do not receive write access.

## Credential IDs
- `SLIC-EXP-YYYY-NNN` Finance Explorer
- `SLIC-NET-YYYY-NNN` Investment Networker
- `SLIC-CMS-YYYY-NNN` Capital Markets Scholar
- `SLIC-LIF-YYYY-NNN` Leo Investment Fellow

## Generate a page
```bash
BASE_URL="https://prof-smith.github.io/saint-leo-investment-club-credentials" python scripts/generate_credential.py sample-data/approved-credential.csv
```

## Unique issued badges
The generator writes `assets/issued/<CREDENTIAL_ID>.png`. Each PNG renders the CSV issue date and credential ID, and its QR code encodes the corresponding unique verification-page URL. Re-run the generator whenever an approved record changes.

## Before production
Confirm brand approval, official issuer wording, publication-consent language, repository ownership, the final Pages URL, and the authorized approvers.
