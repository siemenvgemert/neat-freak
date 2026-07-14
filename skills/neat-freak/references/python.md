# Python Architecture Blueprint (FastAPI + Poetry)

Choose between the Standard structured layout or the Ponytail-Lite single-file layout based on simplicity requirements.

---

## 1. Low / Clean Tiers (Recommended for simple apps)

### Folder Structure
```text
{{project_name}}/
├── .gitignore
├── app.py
├── pyproject.toml
├── README.md
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `pyproject.toml`
```toml
[tool.poetry]
name = "{{project_name}}"
version = "0.1.0"
description = "Minimal FastAPI service"
authors = ["Author <author@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.28.0"}

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### `app.py`
```python
# ponytail: single-file app utilizing fastAPI directly to avoid multi-module overhead
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="{{project_name}}")

@app.get("/health")
def health_check():
    # ponytail: environment settings read directly via os.environ instead of custom settings config class
    env = os.getenv("ENV", "development")
    return {"status": "ok", "environment": env}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
```

#### `test_app.py`
```python
# ponytail: test file alongside application to keep testing path flat and straightforward
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

---

## 2. Full OCD Tier (For modular applications)

### Folder Structure
```text
{{project_name}}/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── health.py
│   ├── core/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── schemas/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_health.py
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── README.md
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `pyproject.toml`
```toml
[tool.poetry]
name = "{{project_name}}"
version = "0.1.0"
description = "FastAPI backend service"
authors = ["Author <author@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.28.0"}
pydantic = "^2.6.0"
pydantic-settings = "^2.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
black = "^24.2.0"
isort = "^5.13.0"
mypy = "^1.8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### `app/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Application"
    env: str = "development"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
```

#### `app/main.py`
```python
import uvicorn
from fastapi import FastAPI
from app.api.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

#### `app/api/router.py`
```python
from fastapi import APIRouter
from app.api.v1 import health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
```

#### `app/api/v1/health.py`
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    environment: str

@router.get("", response_model=HealthResponse)
def get_health():
    from app.config import settings
    return HealthResponse(status="ok", environment=settings.env)
```

#### `tests/conftest.py`
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
```

#### `tests/test_health.py`
```python
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "development"}
```

---

## 3. General Configurations

### `.gitignore`
```text
__pycache__/
*.py[cod]
*$py.class
.env
.venv
env/
venv/
.pytest_cache/
.coverage
htmlcov/
/scratch/
```
