import os
from io import BytesIO
from typing import Dict, Any, List

import boto3
from botocore.exceptions import BotoCoreError, ClientError, SSLError

def get_aws_config() -> Dict[str, str]:
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_DEFAULT_REGION',
        'AWS_S3_ENDPOINT',
        'AWS_S3_BUCKET'
    ]
    config = {}
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        exit(1)
    for var in required_vars:
        config[var.lower()] = os.environ[var]
    return config

def create_s3_client(config: Dict[str, str], desc: str) -> Any:
    endpoint = config['aws_s3_endpoint']
    cert_bundle = os.environ.get('AWS_CA_BUNDLE')
    
    # Decide based on the desired connection type:
    if desc == "tls_default":
        # Always HTTPS with default cert, ignore custom bundle
        use_http = False
        verify = True
        connection_desc = "HTTPS with default SSL"
    elif desc == "tls_custom_bundle":
        # HTTPS, use custom CA if available
        use_http = False
        verify = cert_bundle if cert_bundle else True
        connection_desc = (
            "HTTPS with custom CA bundle"
            if cert_bundle else
            "HTTPS with default SSL (no custom bundle found)"
        )
    elif desc == "http_connection":
        # HTTP, no certificate
        use_http = True
        verify = False
        connection_desc = "HTTP with no SSL/TLS"
    else:
        # Fallback: treat as default
        use_http = False
        verify = True
        connection_desc = "HTTPS with default SSL"

    # Switch endpoint to http if needed
    if use_http and endpoint.startswith("https://"):
        endpoint = endpoint.replace("https://", "http://", 1)

    try:
        client = boto3.client(
            's3',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['aws_default_region'],
            endpoint_url=endpoint,
            verify=verify
        )
        print(f"Created S3 client using {connection_desc}.")
        return client
    except (BotoCoreError, ClientError, SSLError) as e:
        print(f"Failed to create S3 client: {e}")
        exit(1)

def perform_s3_tasks(client: Any, bucket: str, folder: str, content: bytes) -> str:
    file_name = f"file_{folder.strip('/').replace('/', '_')}.txt"
    file_key = f"{folder}{file_name}"
    try:
        client.put_object(Bucket=bucket, Key=folder)
        print(f"Created folder: {folder}")

        client.upload_fileobj(BytesIO(content), bucket, file_key)
        print(f"Uploaded file: {file_key}")

        download_buffer = BytesIO()
        client.download_fileobj(bucket, file_key, download_buffer)
        downloaded_content = download_buffer.getvalue()
        if downloaded_content != content:
            raise ValueError("Downloaded content does not match uploaded content.")
        print(f"Downloaded and verified file: {file_key}")

        return file_key
    except Exception as e:
        print(f"Error during S3 tasks for {folder}: {e}")
        raise

def list_all_files(client: Any, bucket: str) -> List[str]:
    try:
        paginator = client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket)
        return [obj['Key'] for page in pages for obj in page.get('Contents', [])]
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to list all files: {e}")
        return []

def cleanup(client: Any, bucket: str, keys: List[str]) -> None:
    for key in keys:
        try:
            client.delete_object(Bucket=bucket, Key=key)
            print(f"Deleted: {key}")
        except (BotoCoreError, ClientError) as e:
            print(f"Failed to delete {key}: {e}")

def main():
    config = get_aws_config()
    bucket = config['aws_s3_bucket']
    scenarios = [
        {
            "desc": "tls_default",
            "content": b"Content for TLS default connection."
        },
        {
            "desc": "tls_custom_bundle",
            "content": b"Content for TLS with custom certificate bundle."
        },
        {
            "desc": "http_connection",
            "content": b"Content for HTTP connection."
        }
    ]

    created_keys = []
    for scenario in scenarios:
        print(f"\nTesting configuration: {scenario['desc']}")
        try:
            client = create_s3_client(config, scenario['desc'])
            folder = f"test/{scenario['desc']}/"
            file_key = perform_s3_tasks(client, bucket, folder, scenario['content'])
            created_keys.extend([folder, file_key])
        except Exception:
            print(f"Skipping cleanup for {scenario['desc']} due to errors.")

    print("\nAll files in bucket:")
    try:
        client = create_s3_client(config, "tls_default")  # Just to list, default TLS is fine
        all_files = list_all_files(client, bucket)
        for file in all_files:
            print(f" - {file}")
    except Exception as e:
        print(f"Failed to list all files: {e}")

    print("\nStarting cleanup...")
    try:
        client = create_s3_client(config, "tls_default")
        cleanup(client, bucket, created_keys)
    except Exception as e:
        print(f"Cleanup failed: {e}")

    print("\nScript execution completed.")

if __name__ == "__main__":
    main()
