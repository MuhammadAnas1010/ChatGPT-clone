# 🚀 ChatGPT Clone — Full Stack AI Chat Application

A fully-functional ChatGPT-like clone built with:
- 🛡️ **Authentication Backend** — FastAPI
- 🤖 **Chat Backend with LLM API Integration** — FastAPI
- 🎨 **Frontend Interface** — Streamlit
- 📬 **Notifications via RabbitMQ**
- 🗄️ **Redis & PostgreSQL** for session and persistent storage

---

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Backend Services](#backend-services)
  - [Authentication Backend](#authentication-backend)
  - [Chat Backend](#chat-backend)
- [Frontend](#frontend)
- [Database](#database)
- [Message Queue (RabbitMQ)](#message-queue-rabbitmq)
- [Environment Variables](#environment-variables)
- [Features](#features)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)

---

## 📌 Project Overview
This project is a **ChatGPT-inspired full-stack application** featuring:
- Secure user **authentication and authorization**
- A **chat interface** that interacts with an LLM API like OpenAI or DeepSeek
- **Session management** with Redis
- Persistent **chat history stored in PostgreSQL**
- **Background notifications** triggered via RabbitMQ (like sending a "Congratulations" message on successful registration)

---

## 📌 Tech Stack

| Layer          | Technology               |
| -------------- | ------------------------ |
| Frontend       | Streamlit                |
| Chat Backend   | FastAPI, LLM API (e.g., OpenAI, DeepSeek) |
| Auth Backend   | FastAPI, JWT for authentication |
| Databases      | PostgreSQL, Redis        |
| Message Queue  | RabbitMQ + Pika          |
| Background Jobs| Celery (optional future addition) |

---

## 📌 Architecture

User (Frontend - Streamlit)
|
v
Authentication Backend <--- PostgreSQL (User DB)
|
v
Message Queue (RabbitMQ) -- Notification on Registration
|
v
Chat Backend (LLM API Integration) <--- PostgreSQL (Chat History)
|
v
Redis (Session Cache)

yaml
Copy
Edit

---

## 📌 Project Structure

ChatGPT-Clone/
│
├── backend_auth/ # Auth service with FastAPI & JWT
├── chat_backend/ # Chat service with FastAPI & LLM API
├── frontend/ # Streamlit frontend
├── .gitignore
└── README.md

yaml
Copy
Edit

---

## 📌 Setup & Installation

### 1. Clone Repository
bash
git clone https://github.com/MuhammadAnas1010/ChatGPT-Clone.git
cd ChatGPT-Clone
2. Install Dependencies
Each folder (backend_auth, chat_backend, frontend) has its own requirements.txt file. Activate virtual environments accordingly.

For example:

bash
Copy
Edit
cd backend_auth
pip install -r requirements.txt
📌 Backend Services
🔐 Authentication Backend
Built with FastAPI

Provides:

User registration

Login & JWT Token generation

Protected endpoints with JWT verification

On successful registration, pushes a congratulation notification via RabbitMQ to the message queue.

Start the auth backend:

bash
Copy
Edit
uvicorn main:app --reload
🧠 Chat Backend
Also built on FastAPI

Communicates with OpenAI/DeepSeek API for generating chat responses.

Uses:

Redis to cache active sessions

PostgreSQL to store chat history permanently

Provides endpoints to:

Send chat messages

Resume previous chats

Start the chat backend:

bash
Copy
Edit
uvicorn main:app --reload
📌 Frontend
Built with Streamlit

User authentication, chatting interface, and viewing chat history.

Communicates with both auth backend and chat backend.

Start the frontend:

bash
Copy
Edit
cd frontend
streamlit run app.py
📌 Database
PostgreSQL

Stores users, hashed passwords, and chat history.

Redis

Caches active chat sessions for quick access.

📌 Message Queue (RabbitMQ)
Used to push a background notification ("Congratulations on Registering!") when a new user signs up.

Integrated via Pika library in Python.

RabbitMQ must be running locally:

bash
Copy
Edit
# Linux
sudo systemctl start rabbitmq-server

# Docker
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq:3
📌 Environment Variables
Each service uses .env files for sensitive configs:

ini
Copy
Edit
# Example
POSTGRES_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379
JWT_SECRET=your_secret
OPENAI_API_KEY=your_openai_api_key
RABBITMQ_URL=amqp://localhost
📌 Features
✅ User Registration & Login (JWT)
✅ Chat with LLM API
✅ Persistent chat history
✅ Resume previous sessions
✅ Background notification via RabbitMQ
✅ Redis session caching
✅ Streamlit-based UI

📌 Future Improvements
Add WebSockets for real-time chat.

Integrate Celery with RabbitMQ for more background task handling.

User-specific analytics on chat usage.

Deployable via Docker Compose.

📌 Contributors
Muhammad Anas — Developer & Architect
