# Packfora ATS — Streamlit

Internal recruiting tool built with Streamlit + Supabase.

## Structure

```
packfora-ats/
├── app.py              # main Streamlit app (entry point + nav)
├── db.py               # database connection & shared queries
├── pages/              # one file per page
│   ├── dashboard.py
│   ├── candidates.py
│   ├── requisitions.py
│   └── offers.py
├── utils/
│   └── excel_loader.py # Excel import logic
├── data/
│   └── sample.xlsx     # seed data (optional)
├── .env                # secrets (copy from .env.example)
├── requirements.txt
├── Dockerfile          # for containerised deploy
└── README.md
```

## Local development

```bash
cd packfora-ats
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # fill in SUPABASE_URL + key
streamlit run app.py
```

Open http://localhost:8501.

## Docker

```bash
docker build -t packfora-ats .
docker run --rm -p 8501:8501 --env-file .env packfora-ats
```

## Environment variables

| Variable | Required | Notes |
|---|---|---|
| `SUPABASE_URL` | yes | Project URL |
| `SUPABASE_PUBLISHABLE_KEY` | yes* | Public/anon key (respects RLS) |
| `SUPABASE_SERVICE_ROLE_KEY` | no | Admin key — bypasses RLS; server-side only |

\* either the publishable or service-role key works.

## Data model

Reads/writes these Supabase tables: `candidates`, `requisitions`, `interviews`, `offers`.

## Excel import

Every entity page has an **Import from Excel** tab. Column headers in the
spreadsheet must match the target table's columns exactly. A preview of the
first 20 rows is shown before insert.
