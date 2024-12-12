import boto3
import os
import subprocess
from io import BytesIO
from botocore.exceptions import SSLError


def check_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        log_message("ENV CHECK", "ERROR", f"Environment variable '{var_name}' is not set.")
    return value.strip().replace("https://", "").replace("http://", "").split(":")[0] + ":443"


def log_message(step, status, message):
    print(f"[{step}] [{status}] {message}")


def connect_to_s3(verify_ssl=True):
    cert_bundle_path = os.environ.get('AWS_CA_BUNDLE')
    if cert_bundle_path:
        log_message("CONFIG", "INFO", f"Using custom CA bundle: {cert_bundle_path}")
    return boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['AWS_DEFAULT_REGION'],
        endpoint_url=f"https://{os.environ['AWS_S3_ENDPOINT']}",
        verify=cert_bundle_path if cert_bundle_path else verify_ssl
    )


def perform_ssl_check():
    log_message("SSL CHECK", "INFO", "Attempting custom CA bundle creation using OpenSSL...")
    subprocess.run(
        f"openssl s_client -connect {os.environ['AWS_S3_ENDPOINT']} -showcerts </dev/null 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > storage.crt",
        shell=True,
        check=True
    )
    os.environ['AWS_CA_BUNDLE'] = "storage.crt"


# Initialize Environment Variables
AWS_S3_ENDPOINT = check_env_var('AWS_S3_ENDPOINT')
os.environ['AWS_S3_ENDPOINT'] = AWS_S3_ENDPOINT

# Check S3 Connection
ssl_failed = False
cert_bundle_used = False
log_message("Step 1", "INFO", "Connecting to the S3 bucket with SSL...")

try:
    s3 = connect_to_s3()
    s3.list_buckets()
    log_message("Step 1", "SUCCESS", "Successfully verified SSL connection.")
except SSLError:
    log_message("Step 1", "ERROR", "SSL connection using default CA failed.")
    log_message("Step 1", "INFO", "Generating storage.crt using OpenSSL...")
    try:
        perform_ssl_check()
        cert_bundle_used = True
        s3 = connect_to_s3()
        s3.list_buckets()
        log_message("Step 1", "SUCCESS", "Connected using custom CA bundle (storage.crt).")
    except SSLError:
        ssl_failed = True
        log_message("Step 1", "INFO", "Retrying connection without SSL verification...")
        try:
            s3 = connect_to_s3(verify_ssl=False)
            log_message("Step 1", "SUCCESS", "Connected to the S3 bucket without SSL.")
        except Exception as e:
            log_message("Step 1", "ERROR", f"Connection failed: {e.__class__.__name__}: {e}")
            raise e

# Perform S3 Tasks
content = b"Sample in-memory file content for testing."
file_stream = BytesIO(content)

for step, action, task in [
    ("Step 2", "Uploading file...", lambda: s3.upload_fileobj(file_stream, os.environ['AWS_S3_BUCKET'], 'memory_file.txt')),
    ("Step 3", "Downloading file...", lambda: s3.download_fileobj(os.environ['AWS_S3_BUCKET'], 'memory_file.txt', BytesIO())),
    ("Step 4", "Creating folder...", lambda: s3.put_object(Bucket=os.environ['AWS_S3_BUCKET'], Key='new_folder/')),
    ("Step 5", "Listing files...", lambda: s3.list_objects_v2(Bucket=os.environ['AWS_S3_BUCKET'], Prefix='new_folder/'))
]:
    log_message(step, "INFO", action)
    try:
        result = task()
        if step == "Step 5":
            for obj in result.get('Contents', []):
                log_message(step, "FILE", obj['Key'])
        log_message(step, "SUCCESS", f"{action} completed successfully.")
    except Exception as e:
        log_message(step, "ERROR", f"{action} failed: {e.__class__.__name__}: {e}")

# Summary Message
final_messages = []
if ssl_failed:
    final_messages.append("SSL connection failed. Connected using HTTP instead.")

if cert_bundle_used:
    final_messages.append(
        "SSL connection succeeded using a custom CA bundle (storage.crt).\n"
        "Refer to AWS documentation for configuring CA bundles:\n"
        "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-settings"
    )

final_messages.append(
    "Consider the following actions:\n"
    "1. Provide a Custom CA Bundle. Learn more: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-settings\n"
    "2. Correct the Certificate Chain. Refer to Kubernetes/OpenShift documentation:\n"
    "https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/\n"
    "https://docs.openshift.com/container-platform/4.17/security/certificates/updating-ca-bundle.html"
)

# Print Final Messages
for message in final_messages:
    log_message("FINAL MESSAGE", "INFO", message)
