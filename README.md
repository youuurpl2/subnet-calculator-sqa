## Docker

Build image:

```bash
docker build -t subnet-calculator .
```

Jalankan container:

```bash
docker run -d --name subnet-app -p 8000:8000 subnet-calculator
```

Jalankan smoke test:

```bash
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```