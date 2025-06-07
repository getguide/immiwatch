# Express Entry Draw Checker Lambda Function

import json
import urllib.request
import boto3
import datetime
import os

# Constants
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = "last_draw.json"
JSON_DATA_URL = "https://www.canada.ca/content/dam/ircc/documents/json/ee_rounds_123_en.json"

# Initialize S3 client
s3 = boto3.client("s3")

def fetch_latest_draw():
    print(f"Fetching JSON data from: {JSON_DATA_URL}")
    try:
        with urllib.request.urlopen(JSON_DATA_URL) as response:
            json_data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Failed to fetch JSON data: {e}")
        raise Exception(f"Failed to fetch JSON data: {e}")

    # Log the JSON data for debugging
    print(f"JSON data: {json.dumps(json_data, indent=2)[:1000]}...")

    # Validate JSON structure
    if not isinstance(json_data, dict) or "rounds" not in json_data or not json_data["rounds"]:
        print("Invalid JSON structure or no rounds found")
        raise Exception("Invalid JSON structure or no rounds found")

    # Get the latest draw
    latest_draw = json_data["rounds"][0]

    # Extract fields
    draw_date_full = latest_draw.get("drawDateFull", "Unknown Date")
    score = latest_draw.get("drawCRS", "Unknown Score")
    invitations = str(latest_draw.get("drawSize", "0")).replace(",", "")
    draw_name = latest_draw.get("drawName", "Express Entry")

    # Convert date to YYYY-MM-DD
    try:
        draw_date = datetime.datetime.strptime(draw_date_full, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"Failed to parse date: {draw_date_full}, using fallback format")
        draw_date = draw_date_full

    # Map program and category based on drawName
    draw_name_lower = draw_name.lower()
    if "provincial nominee program" in draw_name_lower:
        program = "EE-PNP"
        category = "General"
    elif "canadian experience class" in draw_name_lower:
        program = "EE-CEC"
        category = "General"
    elif "french language proficiency" in draw_name_lower:
        program = "EE-French"
        category = "French"
    elif "education occupations" in draw_name_lower:
        program = "EE-Education"
        category = "Education"
    elif "healthcare" in draw_name_lower:
        program = "EE-Health"
        category = "Health"
    elif "trade occupations" in draw_name_lower:
        program = "EE-Trade"
        category = "Trade"
    elif "general" in draw_name_lower:
        program = "EE-General"
        category = "General"
    elif "agriculture" in draw_name_lower:
        program = "EE-Agriculture"
        category = "Agriculture"
    elif "stem" in draw_name_lower:
        program = "EE-STEM"
        category = "STEM"
    else:
        program = "EE-General"
        category = "General"

    draw_data = {
        "Program": program,
        "Category": category,
        "Region": "All",
        "draw.date.most.recent": draw_date,
        "Score": score,
        "Scoring System": "CRS",
        "Filter by program": "Express Entry",
        "Invitation": invitations,
        "Last Checked": datetime.datetime.utcnow().isoformat(),
        "Draw Number": latest_draw.get("drawNumber", "Unknown")
    }

    print(f"Parsed draw data: {draw_data}")
    return draw_data

def get_last_draw():
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        content = obj["Body"].read()
        return json.loads(content)
    except s3.exceptions.NoSuchKey:
        print("No previous draw found in S3")
        return None
    except Exception as e:
        print(f"Error reading from S3: {e}")
        raise

def save_last_draw(draw_data):
    try:
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=S3_KEY,
            Body=json.dumps(draw_data).encode("utf-8"),
            ContentType="application/json"
        )
        print("Saved draw data to S3")
    except Exception as e:
        print(f"Error saving to S3: {e}")
        raise

def send_webhook(url, data):
    try:
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode()
    except Exception as e:
        print(f"Error sending webhook: {e}")
        raise

def lambda_handler(event, context):
    print("Starting Lambda function to check latest Express Entry draw...")

    # Fetch the latest draw
    try:
        latest_draw = fetch_latest_draw()
    except Exception as e:
        print(f"Error in fetch_latest_draw: {e}")
        return {"statusCode": 500, "body": f"Failed to fetch latest draw: {str(e)}"}

    # Get the last saved draw from S3
    last_draw = get_last_draw()

    # Compare draw numbers
    latest_draw_number = latest_draw.get("Draw Number", "0")
    last_draw_number = last_draw.get("Draw Number", "0") if last_draw else "0"

    try:
        latest_draw_number_int = int(latest_draw_number)
        last_draw_number_int = int(last_draw_number)
    except ValueError:
        print(f"Invalid draw numbers: latest={latest_draw_number}, last={last_draw_number}")
        return {"statusCode": 500, "body": "Invalid draw numbers"}

    if last_draw and latest_draw_number_int <= last_draw_number_int:
        print(f"No new draw found. Latest draw number: {latest_draw_number_int}, Last draw number: {last_draw_number_int}")
        return {"statusCode": 200, "body": "No new draw."}

    print(f"New draw detected. Latest draw number: {latest_draw_number_int}, Last draw number: {last_draw_number_int}")

    # New draw found, send to Airtable
    try:
        response_text = send_webhook(WEBHOOK_URL, latest_draw)
        print(f"Webhook sent: {response_text}")
    except Exception as e:
        print(f"Failed to send webhook: {e}")
        return {"statusCode": 500, "body": f"Failed to send webhook: {str(e)}"}

    # Save the latest draw to S3
    try:
        save_last_draw(latest_draw)
    except Exception as e:
        print(f"Warning: Failed to save to S3, but webhook was sent: {e}")

    return {
        "statusCode": 200,
        "body": "New draw processed and webhook sent."
    }