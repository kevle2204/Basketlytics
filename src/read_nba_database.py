"""Load real NBA teams into BigQuery using Application Default Credentials."""
import argparse
import csv
import io
from decimal import Decimal
import os
from pathlib import Path
import kagglehub
from google.cloud import bigquery

SOURCE = 'wyattowalsh/basketball/versions/238'
COLUMNS = ('id', 'full_name', 'abbreviation', 'nickname', 'city', 'state', 'year_founded')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default=os.environ.get('GOOGLE_CLOUD_PROJECT'))
    parser.add_argument('--location', default=os.environ.get('BQ_LOCATION', 'US'))
    parser.add_argument('--download-only', action='store_true')
    args = parser.parse_args()
    if not args.project and not args.download_only:
        parser.error('Set GOOGLE_CLOUD_PROJECT or pass --project')
    path = Path(kagglehub.dataset_download(SOURCE, path='csv/team.csv'))
    with path.open(newline='', encoding='utf-8-sig') as source:
        reader = csv.DictReader(source)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError(f'Unexpected source columns: {reader.fieldnames}')
        rows = list(reader)
    if not rows or len({row['id'] for row in rows}) != len(rows):
        raise ValueError('Expected nonempty source with unique team IDs')
    for row in rows:
        for column in ('id', 'year_founded'):
            value = Decimal(row[column])
            if not value.is_finite() or value != value.to_integral_value():
                raise ValueError(f'Expected integer {column}: {row[column]}')
            row[column] = str(int(value))
    print(f'Source: {SOURCE}/csv/team.csv')
    print(f'Source rows: {len(rows)}')
    if args.download_only:
        print('Download validated; no BigQuery tables created.')
        return
    client = bigquery.Client(project=args.project)
    dataset = bigquery.Dataset(f'{args.project}.cmpe138_project')
    dataset.location = args.location
    dataset = client.create_dataset(dataset, exists_ok=True)
    table_id = f'{args.project}.cmpe138_project.team'
    config = bigquery.LoadJobConfig(
        schema=[bigquery.SchemaField(c, 'INTEGER' if c in ('id', 'year_founded') else 'STRING') for c in COLUMNS],
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    normalized = io.StringIO(newline='')
    writer = csv.DictWriter(normalized, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)
    with io.BytesIO(normalized.getvalue().encode('utf-8')) as source:
        client.load_table_from_file(source, table_id, job_config=config, location=dataset.location).result()
    count = client.get_table(table_id).num_rows
    if count != len(rows):
        raise RuntimeError(f'Loaded {count} rows; expected {len(rows)}')
    print('BigQuery row counts:')
    print(f'{table_id}: {count} rows')


if __name__ == '__main__':
    main()
