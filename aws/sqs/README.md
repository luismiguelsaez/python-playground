
## Start Localstack Docker container

```bash
docker run -d -p 4566:4566 -p 4571:4571 --name localstack localstack/localstack
```

## Create Python virtual environment and load dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```