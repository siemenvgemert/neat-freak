# Rust Architecture Blueprint

Choose between a simple single-package binary crate or a modular Cargo workspace layout based on simplicity requirements.

---

## 1. Low / Clean Tiers (Recommended for basic scripts and utilities)

### Folder Structure
```text
{{project_name}}/
├── Cargo.toml
├── .gitignore
├── src/
│   └── main.rs
├── README.md
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `Cargo.toml`
```toml
[package]
name = "{{project_name}}"
version = "0.1.0"
edition = "2021"

[dependencies]
# ponytail: keep dependencies minimal. Use standard library unless parsing or async is strictly needed.
```

#### `src/main.rs`
```rust
// ponytail: single binary package to avoid cargo workspace complexity
fn main() {
    let env = std::env::var("ENV").unwrap_or_else(|_| "development".to_string());
    println!("Application starting in env: {}", env);
    println!("Hello, Developer! Welcome to {{project_name}}.");
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_simple() {
        assert!(true);
    }
}
```

---

## 2. Full OCD Tier (For modular systems using workspaces)

### Folder Structure
```text
{{project_name}}/
├── Cargo.toml
├── README.md
├── .gitignore
├── crates/
│   ├── {{project_name}}-cli/
│   │   ├── Cargo.toml
│   │   └── src/
│   │       └── main.rs
│   └── {{project_name}}-core/
│       ├── Cargo.toml
│       └── src/
│           ├── lib.rs
│           └── config.rs
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `Cargo.toml` (Root)
```toml
[workspace]
members = [
    "crates/{{project_name}}-cli",
    "crates/{{project_name}}-core"
]
resolver = "2"
```

#### `crates/{{project_name}}-core/Cargo.toml`
```toml
[package]
name = "{{project_name}}-core"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
```

#### `crates/{{project_name}}-core/src/config.rs`
```rust
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct AppConfig {
    pub env: String,
    pub debug: bool,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            env: std::env::var("ENV").unwrap_or_else(|_| "development".to_string()),
            debug: true,
        }
    }
}
```

#### `crates/{{project_name}}-core/src/lib.rs`
```rust
pub mod config;

pub fn get_greeting(name: &str) -> String {
    format!("Hello, {}! Welcome to {{project_name}} core.", name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greeting() {
        assert_eq!(
            get_greeting("World"),
            "Hello, World! Welcome to {{project_name}} core."
        );
    }
}
```

#### `crates/{{project_name}}-cli/Cargo.toml`
```toml
[package]
name = "{{project_name}}-cli"
version = "0.1.0"
edition = "2021"

[dependencies]
{{project_name}}-core = { path = "../{{project_name}}-core" }
```

#### `crates/{{project_name}}-cli/src/main.rs`
```rust
use {{project_name}}_core::config::AppConfig;
use {{project_name}}_core::get_greeting;

fn main() {
    let config = AppConfig::default();
    println!("Application starting in env: {}", config.env);

    let greeting = get_greeting("Developer");
    println!("{}", greeting);
}
```

---

## 3. General Configurations

### `.gitignore`
```text
/target
.DS_Store
/scratch/
```
