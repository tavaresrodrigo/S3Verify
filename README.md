# S3Verify: S3 Connection Checker

## Overview
S3Verify is a lightweight tool for testing S3-compatible storage connectivity. It verifies SSL configurations, generates custom CA bundles, and provides detailed logs to simplify troubleshooting.

## Why Use S3Verify?
- **Instant Feedback:** Receive real-time logs during connectivity tests.
- **Automatic Fallbacks:** If SSL verification fails, the tool creates a custom CA bundle or retries without SSL.
- **Platform Compatibility:** Designed to work seamlessly in containerized environments like OpenShiftAI.

## Usage
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/s3verify.git
   ```

2. **Open the Notebook:**
   Load `s3verify_notebook.ipynb` in Jupyter.

3. **Run the Notebook:**
   Execute all cells. Environment variables must be inherited from the container’s data connection.

## How It Works
- **SSL Verification:** Attempts an SSL connection.
- **Fallback to Custom CA Bundle:** If SSL fails, a custom CA bundle (`storage.crt`) is generated using OpenSSL.
- **Non-SSL Mode:** If all else fails, attempts connection without SSL.
- **Detailed Logs:** Displays logs for each step.

## Example Logs
```plaintext
[Step 1] [INFO] Connecting to the S3 bucket with SSL...
[Step 1] [ERROR] SSL connection failed.
[Step 1] [INFO] Generating storage.crt...
[Step 1] [SUCCESS] Connected using custom CA bundle.
[Step 2] [INFO] Uploading file...
[Step 2] [SUCCESS] File uploaded successfully.

1. Provide a Custom CA Bundle:
   [AWS CA Bundle Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-settings)

2. Correct the Certificate Chain:
   - [Kubernetes TLS Guide](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)
   - [OpenShift Certificate Management](https://docs.openshift.com/container-platform/latest/security/certificates/index.html)
```

## Contributing
Submit issues or pull requests to improve the tool.

## License
This project is licensed under the MIT License.

