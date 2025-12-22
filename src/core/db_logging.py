import os
import boto3
from decimal import Decimal

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

table = dynamodb.Table(os.environ["LOG_TABLE"])


def _d(x):
    return Decimal(str(x)) if x is not None else None

def log_event(interest_rate, current_payment, mortgage_balance, timestamp, primary_key):
   
    item = {
        "interest_rate": _d(interest_rate),
        "current_payment": _d(current_payment),
        "mortgage_balance": _d(mortgage_balance),
        "timestamp": timestamp,
        "primary_key": primary_key
    }

    table.put_item(Item=item)
    print("Successfully logged to DB!")