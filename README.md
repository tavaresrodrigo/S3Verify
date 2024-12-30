## Overview

This repository contains scripts and notebooks for verifying S3 connectivity, downloading models, and making REST requests for inference.

## Files

- \`0_verify_s3.py\`: Script to verify S3 connectivity. Creates S3 clients with different configurations, performs upload/download tasks, lists all files in the bucket, and cleans up.
- \`1_download_save.ipynb\`: Jupyter notebook to download models from Hugging Face and upload them to an S3 bucket.
- \`2_vllm_rest_requests.ipynb\`: Jupyter notebook to make REST requests to a deployed model's inference endpoint.

## Usage

1. **Verify S3 Connectivity:**
   \`\`\`
   python 0_verify_s3.py
   \`\`\`

2. **Download and Upload Model:**
   Open and run [\`1_download_save.ipynb\`](1_download_save.ipynb) in Jupyter Notebook.

3. **Make REST Requests:**
   Open and run [\`2_vllm_rest_requests.ipynb\`](2_vllm_rest_requests.ipynb) in Jupyter Notebook.

## Additional Resources
- [AWS CLI CA Bundle Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-settings)
- [Kubernetes TLS Guide](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)

## Contributing
Submit issues or pull requests to improve the tool.

## License
This project is licensed under the MIT License." > README.md