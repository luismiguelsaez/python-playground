
```bash
docker build -t ecr-http-proxy .
```

```bash
docker run -it --name ecr-http-proxy -p 8000:8000 \
    -e AWS_ACCESS_KEY_ID=**** \
    -e AWS_SECRET_ACCESS_KEY=**** \
    -e AWS_ACCOUNT_ID=053490547689 \
    -e AWS_REGION=eu-central-1 \
    ecr-http-proxy:latest
```

```python
import boto3

session = boto3.Session(profile_name='lokalise-admin-prod')
client = session.client("ecr")
```
