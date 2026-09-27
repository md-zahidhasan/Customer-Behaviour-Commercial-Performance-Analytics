# Customer Behaviour & Commercial Performance Intelligence Dashboard

Streamlit dashboard for customer behaviour, transactions, offers, rewards and customer journey analysis.

## Deploy on Streamlit Community Cloud
1. Upload this folder to a public GitHub repository.
2. Keep `app.py`, `requirements.txt`, `customer_master_full1.csv`, `events_clean.csv.gz`, and `offers.csv`.
3. Do **not** upload the original 55 MB SQLite database; the dashboard uses the exported deployment data files instead.
4. In Streamlit Community Cloud choose the repository, `main` branch, and `app.py`.

The compressed event file is about 6.3 MB, so the deployment data stays well below the original database size.
