
# CI/CD Pipeline — Flask + Docker + GitHub Actions + AWS EC2

![CI/CD Pipeline](https://github.com/Vigneshwari-08/My-CICD-app/actions/workflows/deploy.yml/badge.svg)

A production-style CI/CD pipeline that automatically tests, builds, and deploys a Flask application to AWS EC2 on every `git push` to `main`. Built as part of a DevOps learning portfolio.

---

## What this project does

Every time code is pushed to the `main` branch, GitHub Actions automatically:

1. **Tests** the application using `pytest` — if any test fails, deployment is blocked
2. **Builds** a Docker image and pushes it to Docker Hub
3. **Deploys** the new image to an AWS EC2 instance via SSH

Zero manual steps. One `git push` = live deployment.

---

## Architecture

```
Developer → git push → GitHub Actions
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
                  test    build &     deploy
                 (pytest)   push     (SSH into
                          (Docker    EC2, pull
                           Hub)    & run image)
                              │
                              ▼
                        AWS EC2 (t2.micro)
                        Flask app on :5000
                        served by Gunicorn
```

---

## Tech stack

| Tool | Purpose |
|---|---|
| Python + Flask | Web application |
| Gunicorn | Production WSGI server |
| Docker | Containerisation |
| Docker Hub | Container registry |
| GitHub Actions | CI/CD pipeline |
| AWS EC2 (t2.micro) | Cloud hosting (free tier) |
| pytest | Automated testing |

---

## Project structure

```
my-cicd-app/
├── .github/
│   └── workflows/
│       └── deploy.yml       # Pipeline definition
├── app/
│   ├── __init__.py
│   └── main.py              # Flask application
├── tests/
│   ├── __init__.py
│   └── test_app.py          # pytest test suite
├── Dockerfile               # Container definition
├── requirements.txt         # Pinned dependencies
└── README.md
```

---

## API endpoints

| Endpoint | Method | Response |
|---|---|---|
| `/` | GET | `{"message": "Hello from my CI/CD pipeline!", "status": "running", "version": "1.0.0"}` |
| `/health` | GET | `{"status": "healthy"}` |

---

## Pipeline stages

### Stage 1 — Test
Runs `pytest tests/ -v` on every push. If any test fails, the pipeline stops here and nothing is deployed. This is the safety gate.

### Stage 2 — Build and push
Builds a Docker image from the `Dockerfile` and pushes it to Docker Hub with the `latest` tag. Only runs if Stage 1 passes.

### Stage 3 — Deploy
SSHs into the EC2 instance, pulls the new image, stops the old container, and starts the new one. Only runs if Stage 2 passes.

---

## Running locally

**Clone the repo:**
```bash
git clone https://github.com/Vigneshwari-08/My-CICD-app.git
cd My-CICD-app
```

**Run with Docker:**
```bash
docker build -t my-cicd-app .
docker run -p 5000:5000 my-cicd-app
```

**Visit:** `http://localhost:5000`

**Run tests:**
```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## GitHub Actions secrets required

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password |
| `EC2_HOST` | EC2 public IP address |
| `EC2_SSH_KEY` | Contents of the `.pem` private key file |

---

## Key learnings

- **Reproducible builds** — pinning dependency versions in `requirements.txt` ensures the pipeline produces the same artifact every time regardless of when it runs
- **Secrets management** — all credentials are stored as encrypted GitHub Actions Secrets and are never hardcoded or visible in logs
- **Test-gated deployment** — the `needs` keyword in the workflow creates a hard dependency chain that makes it physically impossible to deploy broken code
- **Port conflicts** — learned to use `lsof -i :5000` to debug port binding issues, a skill directly transferable to production Linux servers
- **SSH key permissions** — `chmod 400` on `.pem` files is required by SSH as a security enforcement, not just a best practice

---

## What I would add next

- Nginx reverse proxy on port 80 (so users don't need `:5000` in the URL)
- Docker layer caching in the pipeline to speed up builds
- Slack or email notification on pipeline failure

---

*Part of a DevOps portfolio project series. Built from scratch without using any pre-built pipeline templates.*
