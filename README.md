# S3Verify: S3 Connection Checker

## Overview

Test connectivity with your s3 bucket. Verifies SSL configurations and provides detailed logs to simplify troubleshooting.

## Why Use S3Verify?
- **Test connectivity with your s3 bucket**: Test the workbench hability to connect to buckets, create list and remove files.
- **Instant Feedback:** See logs during connectivity tests.
- **Connection Modes:** Supports TLS with default or custom CA bundles and non-TLS connections.

## Usage
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/tavaresrodrigo/s3verify.git
   ```

2. **Run the Script:**
   Execute the Python script in your environment. Ensure the required environment variables are already set in the workbench.

## How It Works
- **Connection Types:**
  - **Default TLS:** Uses the default system certificate.
  - **Custom TLS:** If a custom CA bundle is specified via `AWS_CA_BUNDLE`, it will be used.
  - **Non-TLS:** Fallback to HTTP if specified.

- **Detailed Logs:** Logs every step for easier troubleshooting.

## Example Logs
```plaintext
Testing configuration: tls_default
Created S3 client using HTTPS with default SSL.
Created folder: test/tls_default/
Uploaded file: test/tls_default/file_test_tls_default.txt
Downloaded and verified file: test/tls_default/file_test_tls_default.txt

Testing configuration: tls_custom_bundle
Created S3 client using HTTPS with custom CA bundle.
Created folder: test/tls_custom_bundle/
Uploaded file: test/tls_custom_bundle/file_test_tls_custom_bundle.txt
Downloaded and verified file: test/tls_custom_bundle/file_test_tls_custom_bundle.txt

Testing configuration: http_connection
Created S3 client using HTTP with no SSL/TLS.
Created folder: test/http_connection/
Uploaded file: test/http_connection/file_test_http_connection.txt
Downloaded and verified file: test/http_connection/file_test_http_connection.txt

All files in bucket:
Created S3 client using HTTPS with default SSL.
 - memory_file.txt
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/README.md
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/config.json
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/generation_config.json
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/model.safetensors.index.json
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/params.json
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/special_tokens_map.json
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/tokenizer.json
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/tokenizer.model
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/tokenizer.model.v3
 - models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3/tokenizer_config.json
 - models/Mistral-7B-Instruct-v0.3/README.md
 - models/Mistral-7B-Instruct-v0.3/config.json
 - models/Mistral-7B-Instruct-v0.3/generation_config.json
 - models/Mistral-7B-Instruct-v0.3/model-00001-of-00003.safetensors
 - models/Mistral-7B-Instruct-v0.3/model-00002-of-00003.safetensors
 - models/Mistral-7B-Instruct-v0.3/model-00003-of-00003.safetensors
```

## Additional Resources
- [AWS CLI CA Bundle Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-settings)
- [Kubernetes TLS Guide](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)

## Contributing
Submit issues or pull requests to improve the tool.

## License
This project is licensed under the MIT License.
