# End-to-End MLOps Pipeline — Olivetti Face Recognizer

> **MLOps Major Assignment** 
> Dataset: Olivetti Faces (sklearn) | Model: DecisionTreeClassifier

---

## Repository Links

| Resource | URL |
|----------|-----|
| **GitHub Repository** | `https://github.com/priyanships31/mlops-major-g25ai1035` |
| **Docker Hub Image**  | `https://hub.docker.com/r/g25ai1035/olivetti-face-recognizer` |

---

## Project Structure

```
mlops-major/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── k8s/
│   ├── deployment.yaml         # Kubernetes Deployment (3 replicas)
│   └── service.yaml            # Kubernetes NodePort Service
├── templates/
│   └── index.html              # Flask UI template
├── train.py                    # Train & save DecisionTreeClassifier
├── test.py                     # Evaluate saved model accuracy
├── app.py                      # Flask web application
├── Dockerfile                  # Multi-stage Docker build
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Initial repo setup only |
| `dev` | Model development + CI job (`check_working_repo`) |
| `docker_cicd` | Docker build, push & Kubernetes deployment |

> Neither `dev` nor `docker_cicd` is merged back into `main` (per assignment spec).

---

## Step-by-Step Setup

### Step 1 — Clone & Branch Setup

```bash
# Clone the repository
git clone  https://github.com/priyanships31/mlops-major-g25ai1035
cd mlops-major-g25ai1035

# Verify branches
git branch -a
```

### Step 2 — Dev Branch: Model Training & Testing

```bash
git checkout dev

# Install dependencies
pip install -r requirements.txt

# Train the model → produces savedmodel.pth
python train.py

# Evaluate the model → prints test accuracy
python test.py
```

Expected output from `test.py`:
```
=============================================
  Test Accuracy : 56.67%
=============================================
```

### Step 3 — Docker Branch
```bash
git checkout docker_cicd
docker build -t g25ai1035/olivetti-face-recognizer:latest .
docker run -d -p 5000:5000 --name face-app g25ai1035/olivetti-face-recognizer:latest
curl http://localhost:5000/health
```

### Step 4 — Push to Docker Hub
```bash
docker login
docker push g25ai1035/olivetti-face-recognizer:latest
```

### Step 5 — Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
kubectl get services
minikube service olivetti-face-recognizer-service --url
```

### Step 6 — Self Healing Demo
```bash
kubectl get pods
kubectl delete pod <POD_NAME>
kubectl get pods -w
```

---

## CI/CD Workflow

### Secrets Required
| Secret Name | Value |
|-------------|-------|
| `DOCKERHUB_USERNAME` | g25ai1035 |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

### Jobs
| Job | Trigger | What it Does |
|-----|---------|--------------|
| `check_working_repo` | All branches | Train + Test model |
| `build_and_push_docker` | `docker_cicd` only | Build + Push Docker image |

---

## Model Details
| Parameter | Value |
|-----------|-------|
| Dataset | Olivetti Faces (400 samples, 40 subjects) |
| Features | 4096 (64×64 flattened pixels) |
| Train / Test Split | 70% / 30% (stratified) |
| Algorithm | DecisionTreeClassifier |
| Serialisation | joblib (savedmodel.pth) |

---

## Flask API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI for image upload |
| `/predict` | POST | Accepts image, returns predicted subject |
| `/health` | GET | Returns `{"status": "healthy"}` |

---

## Kubernetes Architecture
```
Internet
    │
    ▼
NodePort :30007
    │
    ▼
Service (ClusterIP :80)
    │
    ├─── Pod 1 (Flask :5000)
    ├─── Pod 2 (Flask :5000)
    └─── Pod 3 (Flask :5000)
          └── savedmodel.pth (baked into image)
```

---

## Troubleshooting
| Issue | Fix |
|-------|-----|
| `savedmodel.pth not found` | Run `python3 train.py` first |
| Docker build fails | Check requirements.txt |
| `ImagePullBackOff` | Check image name in deployment.yaml |
| NodePort not reachable | Run `minikube service ... --url` |