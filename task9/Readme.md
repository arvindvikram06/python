# Task 9: Plugin-based Static Site Generator

A modular static site generator built in **Python** that supports a robust plugin architecture with dependency resolution and lifecycle management.

---

## Features

- **Dynamic Plugin Loading**
  - Scans a dedicated directory for `.py` files.
  - Uses `importlib` to dynamically load modules at runtime.
  - Automatically discovers classes inheriting from `PluginBase`.

- **Dependency Resolution**
  - Implements a **Directed Acyclic Graph (DAG)** approach to resolve plugin dependencies.
  - Detects circular dependencies and throws descriptive errors.
  - Ensures plugins are activated in the correct topological order.

- **Lifecycle Management**
  - Manages `activate` and `deactivate` hooks for all plugins.
  - Tracks plugin state (Active/Inactive) and handles activation failures gracefully.

- **Theme Support**
  - Supports command-line arguments to select different build themes.

---

## Tech Stack

- **Python 3**
- **Importlib** (Standard Library)
- **Argparse** (Standard Library)

---

## Project Workflow

1. **Scan**: `PluginManager` scans the `plugins/` directory for available scripts.
2. **Load**: Modules are loaded, and plugin instances are created.
3. **Resolve**: A dependency graph is built to determine the activation order (Topological Sort).
4. **Activate**: Plugins are activated sequentially based on their requirements.
5. **Execute**: The core "build" command is executed (e.g., generating site pages).
6. **Deactivate**: Plugins are deactivated in reverse order before application exit.

---

## Plugin Logic

- **PluginBase**: All plugins must inherit from this base class and define their `name` and `dependencies`.
- **Topological Order**: If Plugin B depends on Plugin A, Plugin A is guaranteed to be activated first and deactivated last.

---

## Installation

```bash
# Basic build command
python main.py build

# Specify a theme
python main.py build --theme modern
```
