# Project 1 – Serverless Data Pipeline (AWS S3 + Lambda + Athena)

**Cloud concepts:** serverless, event-driven architecture, object storage, IAM, Infrastructure as Code (SAM).

## Architecture
CSV upload -> S3 raw bucket -> (event) -> Lambda cleans data -> Parquet in curated bucket -> query with Athena.

## Run locally
```
pip install -r requirements.txt
cd src && python local_test.py
```
## Deploy (AWS free tier)
```
pip install aws-sam-cli
sam build && sam deploy --guided
aws s3 cp sample_data/sales.csv s3://<RawBucket-name>/
```
Then create an Athena table / Glue crawler on the curated bucket and run SQL.

## Extensions
Add SNS email alerts, a Glue crawler, data-quality checks, a QuickSight dashboard.
