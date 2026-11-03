"""AWS Lambda: triggered when a CSV lands in the raw S3 bucket.
Cleans the data (drop duplicates, fix types, fill nulls) and writes Parquet to the curated bucket."""
import io, os, urllib.parse
import boto3
import pandas as pd

s3 = boto3.client("s3")
CURATED_BUCKET = os.environ.get("CURATED_BUCKET", "my-curated-bucket")

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for col in df.select_dtypes(include="number"):
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].fillna("unknown").str.strip()
    return df

def lambda_handler(event, context):
    rec = event["Records"][0]["s3"]
    bucket = rec["bucket"]["name"]
    key = urllib.parse.unquote_plus(rec["object"]["key"])
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    df = clean(pd.read_csv(io.BytesIO(body)))
    out = io.BytesIO()
    df.to_parquet(out, index=False)           # needs pyarrow (use AWS SDK Pandas layer)
    out_key = key.rsplit(".", 1)[0] + ".parquet"
    s3.put_object(Bucket=CURATED_BUCKET, Key=out_key, Body=out.getvalue())
    return {"rows": len(df), "output": f"s3://{CURATED_BUCKET}/{out_key}"}
