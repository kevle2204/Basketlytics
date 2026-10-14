# Basketlytics

## 1. What the application is

Basketlytics is an analytics dashboard for analysts and casual NBA fans. It will let users explore and compare player and team statistics across games, quarters, and seasons, including offensive and defensive performance, home-versus-away results, player efficiency and more.

## 2. System diagram

To come.

## 3. What to install

Install Python 3.10+ and the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install). From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`.

## 4. How to sign in

Use Application Default Credentials (ADC):

```bash
gcloud auth login
gcloud auth application-default login
```

The second command is required for Python; CLI login alone is not ADC. Credentials remain in your Cloud CLI user configuration outside the repository. Never commit keys, tokens, passwords, or Kaggle credentials. The public Kaggle download works anonymously.

## 5. How to set the project ID

The current course project is `cmpe138-project-1`. Teammates can substitute their own project, with billing/credits and the Phase 1 budget alert configured:

```bash
export GOOGLE_CLOUD_PROJECT="cmpe138-project-1"
export BQ_LOCATION="US"
gcloud config set project "$GOOGLE_CLOUD_PROJECT"
gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"
gcloud services enable bigquery.googleapis.com --project="$GOOGLE_CLOUD_PROJECT"
```

PowerShell: `$env:GOOGLE_CLOUD_PROJECT = "YOUR_PROJECT_ID"`. Each teammate can choose a project without editing code. The account needs permission to create BigQuery jobs, datasets and tables, and write access to an existing dataset. API enablement and quota-project setup may require a project administrator.

## 6. How to seed

With the virtual environment active, ADC configured, and project ID set:

```bash
python src/read_nba_database.py
```

Alternatively pass `--project YOUR_PROJECT_ID`. The seed downloads only `csv/team.csv` from version 238 of the team's selected [Kaggle NBA dataset](https://www.kaggle.com/datasets/wyattowalsh/basketball/versions/238). These are real NBA team records. Pinning the version gives each teammate the same source. It validates columns and unique IDs, creates the BigQuery dataset `cmpe138_project`, loads `cmpe138_project.team`, and prints the completed table's row count. Existing datasets retain their location.

Rerunning replaces the `team` table with `WRITE_TRUNCATE`; it does not double rows. Manual changes to that table are replaced. Other tables are unaffected. The full proposal slice is to come.

This seed uses a file load and table metadata, with no billed SQL scan. A query estimate and `maximum_bytes_billed` do not apply to file load jobs. Storage charges can apply; retain the budget alert. Future public-table SQL copies must use a dry run, inspect estimated bytes, and set `maximum_bytes_billed` before execution.

To validate the real source without accessing BigQuery:

```bash
python src/read_nba_database.py --download-only
```

### Output of one BigQuery seed run

Command run from the repository root:

```bash
.venv/bin/python src/read_nba_database.py --project cmpe138-project-1
```

Actual output from a successful BigQuery load:

```text
Source: wyattowalsh/basketball/versions/238/csv/team.csv
Source rows: 30
BigQuery row counts:
cmpe138-project-1.cmpe138_project.team: 30 rows
```

The same command was run a second time successfully and printed the same 30-row count, verifying that rerunning the seed does not double the rows.

## 7. How to run the workload

To come.

## 8. How to start the application

To come.

## 9. How to reset

To come. Rerunning the current seed replaces only the `team` table.

## Checkpoint submission

A public repository is allowed per the team's clarified course instructions. Verify the instructor has the required access/invitation, and submit the repository URL in Canvas (once per team). Every member should begin making their own contributions and commits.
