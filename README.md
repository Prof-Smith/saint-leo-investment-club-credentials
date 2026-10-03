# Saint Leo Investment Club Professional Credential Program
Production-ready repository for a controlled GitHub Pages credential-verification site.

## Generate credential pages
```bash
BASE_URL="https://prof-smith.github.io/saint-leo-investment-club-credentials" python scripts/generate_credential.py sample-data/approved-credential.csv
```
Generated pages are written to `credentials/`; QR codes are written to `assets/qr/`.
