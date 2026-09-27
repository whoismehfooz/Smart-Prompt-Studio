# ⚡ Smart Prompt Studio

> A production-minded backend for managing, rendering, validating, and executing reusable AI prompts.

<p align="center">
  🧠 Prompt Management • 🛡️ Guardrails • 🤖 AI Execution • 📋 Evaluation • 📦 Docker • 🔄 CI
</p>

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-Responses%20API-412991?logo=openai&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-19%20passing-success?logo=pytest&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)

---

## 🚀 What is Smart Prompt Studio?

Smart Prompt Studio is a FastAPI-based backend built around one simple idea:

**Treat prompts like backend-managed application assets, not random strings buried inside code.**

Instead of scattering prompts throughout an application, this service provides a central layer for:

- 📝 Creating prompts
- 🔢 Managing prompt versions
- 🧩 Rendering variables
- 🛡️ Validating prompts before execution
- 🤖 Sending prompts to an AI provider
- 📊 Tracking execution behavior
- 🧪 Testing failure paths
- 📋 Evaluating prompt behavior
- 🪵 Logging requests and services
- 🐳 Running inside Docker
- 🔄 Validating changes through GitHub Actions

The project is intentionally small.

The engineering lessons are not.

---

## ✨ Core Features
📝 Prompt Management

Create reusable prompts through the API.
```text
POST /prompts
```
Prompts contain structured messages instead of one giant string.

This keeps prompt construction explicit and maintainable.

---
## 🎯 Project Goal

The goal is to build a clean foundation for AI-powered backend systems.

Smart Prompt Studio focuses on the engineering layer surrounding an LLM:

```text
Client
  │
  ▼
FastAPI API
  │
  ▼
Prompt Service
  │
  ├── Versioning
  ├── Variable Rendering
  └── Validation
  │
  ▼
Guardrail Service
  │
  ▼
AI Service
  │
  ▼
AI Provider
  │
  ▼
Response

```
---
## 🏗️ Architecture

```text
The project follows a service-oriented FastAPI structure.

Smart-Prompt-Studio/
│
├── app/
│   ├── config.py
│   ├── logging_config.py
│   ├── main.py
│   ├── schemas.py
│   │
│   ├── exceptions/
│   │   ├── custom_exceptions.py
│   │   └── handlers.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── request_logging.py
│   │
│   └── services/
│       ├── ai_service.py
│       ├── guardrail_service.py
│       └── prompt_service.py
│
├── tests/
│   ├── test_ai_service_errors.py
│   ├── test_ai_service_logging.py
│   └── test_prompt_evalutation.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
└── requirements.txt
```
---
## 🧰 Tech Stack

```text
Technology                                  Purpose
-🐍 Python                               Application language
-⚡ FastAPI                              API framework
-📦 Pydantic                             Data validation
-🤖 OpenAI-compatible SDK                AI communication
-🧪 Pytest                               Automated testing
-🐳 Docker                               Containerization
-🔄 GitHub Actions                       CI
-🪵 Python Logging                       Observability
-🌿 Git                                  Version control
```
---
## 📌 Current Status

```text
┌──────────────────────────────┐
│ Smart Prompt Studio          │
├──────────────────────────────┤
│ Prompt Management       ✅   │
│ Versioning              ✅   │
│ Variable Rendering      ✅   │
│ Guardrails              ✅   │
│ AI Integration          ✅   │
│ Error Handling          ✅   │
│ Logging                 ✅   │
│ Automated Tests         ✅   │
│ Docker                  ✅   │
│ GitHub Actions CI       ✅   │
└──────────────────────────────┘
```
Local test suite:

```text
10 passed
```
CI:
```text
✅ Passed
```
Docker:
```text
✅ Verified
```
---
---
## ⚡ Final Snapshot

Smart Prompt Studio is a compact AI backend focused on one principle:

Build the engineering around the model, not just the model call.

It combines:
```text
⚡ FastAPI
🧠 Prompt Management
🛡️ Guardrails
🤖 AI Execution
🪵 Logging
🧪 Testing
🐳 Docker
🔄 CI
🌿 Git
```
Small enough to understand.

Structured enough to extend.

Practical enough to build upon.

---
## 🗿 Built With Python

Made as part of a hands-on journey toward production-grade AI Backend Engineering.
```text
Code → Test → Containerize → Automate → Ship
```
Smart Prompt Studio

The prompt is only the beginning.