<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT" />
  <img src="https://img.shields.io/badge/GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white" alt="GPT-4o-mini" />
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render" />
</p>

<h1 align="center">🚀 Lunex Bot — Backend API</h1>

<p align="center">
  <em>The intelligent backbone powering the <a href="https://github.com/prithvihn/lunex-bot-frontend">Lunex Bot</a> AI chatbot experience.</em>
</p>

<p align="center">
  <a href="https://fastapi-with-db-backend.onrender.com/docs">
    <img src="https://img.shields.io/badge/🔗_Live_API-Swagger_Docs-00C853?style=for-the-badge" alt="Live API" />
  </a>
  &nbsp;
  <a href="https://github.com/prithvihn/lunex-bot-frontend">
    <img src="https://img.shields.io/badge/🖥️_Frontend-Lunex_Bot_UI-7C4DFF?style=for-the-badge" alt="Frontend Repo" />
  </a>
</p>

---

## 📌 1. About This Repository

This is the **backend REST API** for [Lunex Bot](https://github.com/prithvihn/lunex-bot-frontend) — a modern, full-stack AI chatbot application. Built with **FastAPI**, this server handles everything the frontend needs: user authentication, real-time AI responses powered by **GPT-4o-mini**, persistent chat history, email notifications, and more.

> **Frontend ↔ Backend:** The Lunex Bot frontend (React + Vite, deployed on Vercel) communicates with this backend (deployed on Render) over HTTPS. Every chat message, login attempt, and conversation action flows through the API endpoints defined here.

| Layer                        | Repository                                                                      | Deployment                                             |
| ---------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Frontend**                 | [lunex-bot-frontend](https://github.com/prithvihn/lunex-bot-frontend)           | Vercel                                                 |
| **Backend** _(you are here)_ | [fastapi_with_db_backend](https://github.com/prithvihn/fastapi_with_db_backend) | [Render](https://fastapi-with-db-backend.onrender.com) |

---

## 🏗️ 2. System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                             │
│                   Lunex Bot React Frontend                           │
│                    lunexbot.vercel.app                                │
└──────────────────────┬───────────────────────────────────────────────┘
                       │  HTTPS (REST API Calls)
                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND SERVER                          │
│              fastapi-with-db-backend.onrender.com                    │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ User Routes  │  │ AI Routes   │  │ Email    │  │ Conversation │  │
│  │  /signup     │  │  /ask       │  │ Routes   │  │   Routes     │  │
│  │  /login      │  │             │  │ /send-   │  │  /api/...    │  │
│  │  /refresh    │  │             │  │  email   │  │              │  │
│  └──────┬───────┘  └──────┬──────┘  └────┬─────┘  └──────┬───────┘  │
│         │                 │              │               │           │
│  ┌──────▼─────────────────▼──────────────▼───────────────▼────────┐  │
│  │                     UTILITY LAYER                              │  │
│  │  jwt_handler.py │ auth.py │ ai_response.py │ email_sender.py  │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │                                      │
│  ┌────────────────────────────▼──────────────────────────────────┐  │
│  │                  REPOSITORY LAYER (ORM)                       │  │
│  │          User_repo.py  │  conversation_repo.py                │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │                                      │
│  ┌────────────────────────────▼──────────────────────────────────┐  │
│  │                  SQLAlchemy + Database                         │  │
│  │                   (SQLite / PostgreSQL)                        │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────┐   ┌───────────────────────────────────┐  │
│  │ Azure AI Inference    │   │        Gmail SMTP Server          │  │
│  │ (GPT-4o-mini via      │   │     (Email Notifications)         │  │
│  │  GitHub Models)       │   │                                   │  │
│  └───────────────────────┘   └───────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ 3. Tech Stack

| Category           | Technology                                                |
| ------------------ | --------------------------------------------------------- |
| **Framework**      | FastAPI (Python)                                          |
| **ORM**            | SQLAlchemy                                                |
| **Database**       | SQLite (dev) / PostgreSQL (prod)                          |
| **AI Model**       | GPT-4o-mini via Azure AI Inference (GitHub Models)        |
| **Authentication** | JWT (Access + Refresh tokens) using `python-jose`         |
| **Email**          | SMTP via Gmail (with App Password)                        |
| **Validation**     | Pydantic v2 Schemas                                       |
| **Server**         | Uvicorn (ASGI)                                            |
| **Deployment**     | Render (Web Service)                                      |
| **CORS**           | Configured for `localhost:5173` and `lunexbot.vercel.app` |

---

## ✨ 4. Features

### 🔐 Authentication & Security

- **User Signup & Login** — Email/password-based registration and authentication
- **JWT Token System** — Short-lived access tokens (30 min) + long-lived refresh tokens (7 days)
- **Token Refresh** — Seamless session extension without re-login
- **Protected Routes** — Bearer token middleware guards all conversation endpoints

### 🤖 AI Chat Engine

- **GPT-4o-mini Integration** — Powered by Azure AI Inference through GitHub Models
- **Custom System Prompts** — Each request supports configurable system instructions
- **Instant Responses** — Direct completion API for low-latency replies

### 💬 Conversation Management

- **Full CRUD** — Create, list, rename, and delete conversations
- **Message Persistence** — Save both user and assistant messages with timestamps
- **Ownership Verification** — Every action validates that the conversation belongs to the logged-in user
- **Auto-Title Generation** — Conversations are automatically titled from the first user message
- **Last Message Preview** — Conversation lists include a truncated preview of the latest message
- **Chronological Ordering** — Messages sorted by creation time, conversations sorted by last update

### 📧 Email Service

- **Transactional Emails** — Send emails directly from the app via Gmail SMTP
- **Validated Input** — Pydantic `EmailStr` validation ensures proper email formatting

---

## 🗄️ 5. Database Schema

```
┌──────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│      USERS       │       │    CONVERSATIONS      │       │      MESSAGES        │
├──────────────────┤       ├──────────────────────┤       ├──────────────────────┤
│ id       (PK)    │──┐    │ id          (PK)     │──┐    │ id              (PK) │
│ email    (UNIQUE)│  │    │ user_id     (FK)     │  │    │ conversation_id (FK) │
│ password         │  └───>│ title                │  └───>│ role                 │
└──────────────────┘       │ created_at           │       │ content              │
                           │ updated_at           │       │ created_at           │
                           └──────────────────────┘       └──────────────────────┘

  One User ──── has many ──── Conversations ──── has many ──── Messages
                               (cascade delete)                (cascade delete)
```

<p align="center">
  <img src="assets/schema-design.png" alt="Database Schema Visual" width="700" />
</p>

---

## 📸 6. Screenshots

<p align="center">
  <img src="assets/Fastapi-swagger-ui.png" alt="Swagger UI — Interactive API Docs" width="750" />
  <br />
  <em>FastAPI Swagger UI — Interactive API Documentation</em>
</p>

<br />

<p align="center">
  <img src="assets/workflow-frontend-backend.png" alt="Frontend ↔ Backend Workflow" width="750" />
  <br />
  <em>Frontend ↔ Backend Communication Workflow</em>
</p>

---

## 📂 7. Project Structure

```
fastapi_with_db_backend/
│
├── main.py                      # 🚀 Application entry point & CORS config
├── db.py                        # 🗄️ Database engine & session management
├── models.py                    # 📦 SQLAlchemy ORM models (User, Conversation, Message)
│
├── routes/
│   ├── user_routes.py           # 🔐 Signup, Login, Token Refresh
│   ├── ai_response_routes.py    # 🤖 AI completion endpoint
│   ├── conversation_routes.py   # 💬 Conversation & Message CRUD
│   └── email_routes.py          # 📧 Email sending endpoint
│
├── schemas/
│   ├── User_schemas.py          # 👤 User request/response models
│   ├── Token_schemas.py         # 🎫 JWT token models
│   ├── ai_response_schemas.py   # 🧠 AI request/response models
│   ├── conversation_schemas.py  # 💬 Conversation & Message models
│   └── email_schema.py          # 📧 Email request/response models
│
├── repositories/
│   ├── User_repo.py             # 👤 User database operations
│   └── conversation_repo.py     # 💬 Conversation & Message DB operations
│
├── utils/
│   ├── jwt_handler.py           # 🔑 JWT creation & verification
│   ├── auth.py                  # 🛡️ Bearer token auth middleware
│   ├── ai_response.py           # 🤖 Azure AI Inference client
│   └── email_sender.py          # 📧 Gmail SMTP email utility
│
├── assets/                      # 🖼️ Screenshots & diagrams
├── requirements.txt             # 📦 Python dependencies
├── .gitignore                   # 🚫 Ignored files
└── .env                         # 🔒 Environment variables (not committed)
```

---

## 🛠️ 8. Installation & Setup

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **Git**

### Step-by-step

```bash
# 1. Clone the repository
git clone https://github.com/prithvihn/fastapi_with_db_backend.git
cd fastapi_with_db_backend

# 2. Create a virtual environment
python -m venv env

# 3. Activate the virtual environment
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables (see section below)
# Create a .env file in the root directory

# 6. Start the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at **`http://localhost:8000`** and the interactive docs at **`http://localhost:8000/docs`**.

---

## 🔑 9. Environment Variables

Create a `.env` file in the project root with the following:

```env
# ─── Database ───────────────────────────────────
DATABASE_URL=sqlite:///./test.db
# For production (PostgreSQL):
# DATABASE_URL=postgresql://user:password@host:port/dbname

# ─── JWT Authentication ────────────────────────
JWT_SECRET_KEY=your-super-secret-key-change-in-production

# ─── AI Model (GitHub Models / Azure AI) ───────
GITHUB_TOKEN=your-github-personal-access-token

# ─── Email Service (Gmail SMTP) ────────────────
sender_email=your-email@gmail.com
app_password=your-gmail-app-password
```

| Variable         | Description                                                                   |
| ---------------- | ----------------------------------------------------------------------------- |
| `DATABASE_URL`   | SQLAlchemy connection string (SQLite for dev, PostgreSQL for prod)            |
| `JWT_SECRET_KEY` | Secret key for signing JWT tokens                                             |
| `GITHUB_TOKEN`   | GitHub PAT with access to GitHub Models for AI inference                      |
| `sender_email`   | Gmail address used for sending transactional emails                           |
| `app_password`   | Gmail App Password (generated from Google Account → Security → App passwords) |

---

## 📡 10. API Endpoints

### 🔐 Authentication

| Method | Endpoint   | Description                   | Auth |
| ------ | ---------- | ----------------------------- | ---- |
| `POST` | `/signup`  | Register a new user           | ❌   |
| `POST` | `/login`   | Authenticate & get JWT tokens | ❌   |
| `POST` | `/refresh` | Refresh expired access token  | ❌   |

### 🤖 AI

| Method | Endpoint | Description                        | Auth |
| ------ | -------- | ---------------------------------- | ---- |
| `POST` | `/ask`   | Send a message and get AI response | ❌   |

### 💬 Conversations & Messages

| Method   | Endpoint                           | Description                    | Auth |
| -------- | ---------------------------------- | ------------------------------ | ---- |
| `POST`   | `/api/conversations/create`        | Create a new conversation      | ✅   |
| `GET`    | `/api/conversations/list`          | List all user conversations    | ✅   |
| `GET`    | `/api/conversations/{id}/messages` | Get messages in a conversation | ✅   |
| `PATCH`  | `/api/conversations/{id}/rename`   | Rename a conversation          | ✅   |
| `DELETE` | `/api/conversations/{id}`          | Delete a conversation          | ✅   |
| `POST`   | `/api/messages/create`             | Save a user message            | ✅   |
| `POST`   | `/api/messages/save-assistant`     | Save an assistant message      | ✅   |

### 📧 Email

| Method | Endpoint      | Description                | Auth |
| ------ | ------------- | -------------------------- | ---- |
| `POST` | `/send-email` | Send an email notification | ❌   |

> **✅ Auth** = Requires `Authorization: Bearer <access_token>` header

---

## 🔄 11. Request & Response Examples

### Login

```bash
curl -X POST https://fastapi-with-db-backend.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword"}'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Ask AI

```bash
curl -X POST https://fastapi-with-db-backend.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Linux?", "system_prompt": "You are a helpful Linux assistant."}'
```

**Response:**

```json
{
  "response": "Linux is an open-source operating system kernel..."
}
```

### Create Conversation (Protected)

```bash
curl -X POST https://fastapi-with-db-backend.onrender.com/api/conversations/create \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Chat"}'
```

**Response:**

```json
{
  "id": 1,
  "user_id": 1,
  "title": "My First Chat",
  "created_at": "2025-02-14T10:00:00",
  "updated_at": "2025-02-14T10:00:00"
}
```

---

## 🔒 12. Authentication Flow

```
┌──────────┐                              ┌──────────────┐
│  Client  │                              │   Backend    │
└─────┬────┘                              └──────┬───────┘
      │                                          │
      │  POST /signup {email, password}          │
      │─────────────────────────────────────────>│
      │                  201 Created              │
      │<─────────────────────────────────────────│
      │                                          │
      │  POST /login {email, password}           │
      │─────────────────────────────────────────>│
      │     {access_token, refresh_token}        │
      │<─────────────────────────────────────────│
      │                                          │
      │  GET /api/conversations/list             │
      │  Authorization: Bearer <access_token>    │
      │─────────────────────────────────────────>│
      │           [conversations]                │
      │<─────────────────────────────────────────│
      │                                          │
      │  ── access_token expires (30 min) ──     │
      │                                          │
      │  POST /refresh {refresh_token}           │
      │─────────────────────────────────────────>│
      │     {new access_token, refresh_token}    │
      │<─────────────────────────────────────────│
      │                                          │
```

---

## 🗺️ 13. Future Roadmap

| Feature                        | Status     |
| ------------------------------ | ---------- |
| 📎 File Attachments (RAG)      | 🔜 Planned |
| 📌 Pin Conversations (up to 3) | 🔜 Planned |
| 🔗 Share a Chat                | 🔜 Planned |
| 👥 Group Chat                  | 🔜 Planned |
| 🎤 Voice Input                 | 🔜 Planned |
| 🌍 Multi-language Support      | 🔜 Planned |
| 📝 Quiz Canvas                 | 🔜 Planned |
| 🔍 Web Search Integration      | 🔜 Planned |
| 🔎 Search Chat History         | 🔜 Planned |

---

## 🤝 14. Contributing

Contributions are welcome! Here's how:

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

<p align="center">
  <strong>Built with ❤️ by <a href="https://github.com/prithvihn">prithvihn</a></strong>
</p>

<p align="center">
  <a href="https://github.com/prithvihn/fastapi_with_db_backend">
    <img src="https://img.shields.io/badge/⭐_Star_this_repo-GitHub-181717?style=for-the-badge&logo=github" alt="Star on GitHub" />
  </a>
</p>
