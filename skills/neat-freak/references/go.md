# Go Architecture Blueprint

Choose between a single-file standard library web server or a modular microservice layout based on simplicity requirements.

---

## 1. Low / Clean Tiers (Recommended for simple microservices)

### Folder Structure
```text
{{project_name}}/
├── .gitignore
├── go.mod
├── main.go
├── README.md
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `go.mod`
```go
module {{project_name}}

go 1.21
```

#### `main.go`
```go
// ponytail: single-file web server using only standard net/http package to avoid external dependency overhead
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
)

type HealthResponse struct {
	Status      string `json:"status"`
	Environment string `json:"environment"`
}

func main() {
	// ponytail: configuration read directly from environment variables inside main to avoid setting up configuration modules
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	env := os.Getenv("ENV")
	if env == "" {
		env = "development"
	}

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(HealthResponse{
			Status:      "ok",
			Environment: env,
		})
	})

	log.Printf("Starting ponytail-lite server on port %s...", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
```

---

## 2. Full OCD Tier (For modular Go projects)

### Folder Structure
```text
{{project_name}}/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── app/
│   │   └── app.go
│   ├── config/
│   │   └── config.go
│   └── handler/
│       └── health.go
├── .gitignore
├── Dockerfile
├── go.mod
├── README.md
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `go.mod`
```go
module {{project_name}}

go 1.21
```

#### `cmd/server/main.go`
```go
package main

import (
	"log"
	"net/http"
	"{{project_name}}/internal/app"
	"{{project_name}}/internal/config"
)

func main() {
	cfg := config.Load()
	
	log.Printf("Starting server on port %s...", cfg.Port)
	server := app.New(cfg)
	if err := server.Start(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Could not listen on %s: %v\n", cfg.Port, err)
	}
}
```

#### `internal/config/config.go`
```go
package config

import (
	"os"
)

type Config struct {
	Port string
	Env  string
}

func Load() *Config {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	env := os.Getenv("ENV")
	if env == "" {
		env = "development"
	}

	return &Config{
		Port: port,
		Env:  env,
	}
}
```

#### `internal/app/app.go`
```go
package app

import (
	"fmt"
	"net/http"
	"{{project_name}}/internal/config"
	"{{project_name}}/internal/handler"
)

type App struct {
	config *config.Config
	router *http.ServeMux
}

func New(cfg *config.Config) *App {
	mux := http.NewServeMux()
	
	// Register Routes
	mux.HandleFunc("/health", handler.HealthHandler(cfg))

	return &App{
		config: cfg,
		router: mux,
	}
}

func (a *App) Start() error {
	return http.ListenAndServe(fmt.Sprintf(":%s", a.config.Port), a.router)
}
```

#### `internal/handler/health.go`
```go
package handler

import (
	"encoding/json"
	"net/http"
	"{{project_name}}/internal/config"
)

type HealthResponse struct {
	Status      string `json:"status"`
	Environment string `json:"environment"`
}

func HealthHandler(cfg *config.Config) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		
		response := HealthResponse{
			Status:      "ok",
			Environment: cfg.Env,
		}
		
		json.NewEncoder(w).Encode(response)
	}
}
```

#### `internal/handler/health_test.go`
```go
package handler

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"{{project_name}}/internal/config"
)

func TestHealthHandler(t *testing.T) {
	cfg := &config.Config{Port: "8080", Env: "testing"}
	req, err := http.NewRequest("GET", "/health", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := HealthHandler(cfg)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response HealthResponse
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatal(err)
	}

	if response.Status != "ok" {
		t.Errorf("expected status 'ok', got %s", response.Status)
	}
	if response.Environment != "testing" {
		t.Errorf("expected environment 'testing', got %s", response.Environment)
	}
}
```

---

## 3. General Configurations

### `.gitignore`
```text
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
.DS_Store
/scratch/
```
