# David Musumali — Personal REST API

A clean, modular **FastAPI + SQLite** backend serving profile, skills, projects,
education, services and contact messages for my personal website, portfolio and
future mobile applications.

- **Interactive docs:** http://127.0.0.1:8000/docs (Swagger UI) · http://127.0.0.1:8000/redoc
- **Python:** 3.10+ (tested on 3.14) · **Framework:** FastAPI · **ORM:** SQLAlchemy 2 · **DB:** SQLite

---

## 1. Architecture

```
personal_api/
├── main.py            # App entry point: FastAPI app, CORS, routers, error handlers
├── database.py        # SQLAlchemy engine, session factory, get_db dependency
├── config.py          # All settings read from environment variables (.env)
├── security.py        # bcrypt password hashing + JWT creation/verification
├── deps.py            # require_admin dependency that guards private endpoints
├── init_db.py         # Creates tables + seeds admin, profile, skills, projects…
├── pytest.ini         # Test configuration
├── run.bat            # Windows double-click launcher
├── requirements.txt
├── .env               # Your local secrets (never committed)
├── .env.example       # Template to copy from
│
├── models/            # SQLAlchemy ORM models (database tables)
│   ├── admin.py       #   admins          — admin accounts (hashed passwords)
│   ├── profile.py     #   profile         — single-row personal information
│   ├── project.py     #   projects        — portfolio projects
│   ├── skill.py       #   skills          — skills (unique names)
│   ├── education.py   #   education       — institutions / programmes
│   ├── service.py     #   services        — service offerings
│   └── contact.py     #   contact_messages— private form submissions
│
├── schemas/           # Pydantic schemas (request validation + response shape)
│   ├── auth.py        #   login + token models
│   ├── profile.py / project.py / skill.py / education.py / contact.py / service.py
│
├── routes/            # API endpoints (one file per resource)
│   ├── auth.py        #   POST /api/auth/login
│   ├── profile.py     #   GET  /api/profile
│   ├── projects.py    #   GET/POST/PUT/DELETE /api/projects[/{id}]
│   ├── skills.py      #   GET/POST/PUT/DELETE /api/skills[/{id}]
│   ├── education.py   #   GET/POST/PUT/DELETE /api/education[/{id}]
│   ├── services.py    #   GET  /api/services
│   └── contact.py     #   POST /api/contact · GET /api/contact/messages (admin)
│                      #   contact accepts: name, email, phone?, subject?, message
│
├── tests/             # Pytest suite (profile, skills, projects, education,
│                      # services, contact, auth, invalid requests)
└── data/
    └── personal_api.db  # SQLite database (created automatically)
```

**Request flow:** `HTTP request → route (validates with Pydantic schema) →
service logic in the route → SQLAlchemy model → SQLite → Pydantic response model → JSON`.

Routes never open DB sessions themselves — they receive one via `Depends(get_db)`.
Private routes additionally depend on `require_admin`, which decodes the JWT and
loads the admin user.

---

## 2. Database

- SQLite file at `data/personal_api.db`, created **automatically** on first start.
- Tables are created with SQLAlchemy (`Base.metadata.create_all`) from the models —
  primary keys, unique constraints and timestamps are declared in the models.
- Seeding (`init_db.py`) is **idempotent**: rows are inserted only when a table is
  empty, so restarting never duplicates content.
- To move to PostgreSQL later: `pip install psycopg[binary]` and change
  `DATABASE_URL` — no code changes needed.

### Example SQL schema (what SQLAlchemy generates in SQLite)

```sql
CREATE TABLE admins (
    id              INTEGER PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    email           VARCHAR(160) NOT NULL,
    hashed_password VARCHAR(128) NOT NULL,       -- bcrypt hash only
    created_at      TIMESTAMP NOT NULL
);

CREATE TABLE profile (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(120) NOT NULL,
    profession VARCHAR(160) NOT NULL,
    university VARCHAR(160) NOT NULL,
    email      VARCHAR(160) NOT NULL,
    phone      VARCHAR(40)  NOT NULL,
    alt_phone  VARCHAR(40),
    location   VARCHAR(120),
    bio        TEXT
);

CREATE TABLE projects (
    id           INTEGER PRIMARY KEY,
    name         VARCHAR(160) NOT NULL,
    description  TEXT NOT NULL,
    tagline      VARCHAR(200),
    technologies VARCHAR(400) NOT NULL DEFAULT '',  -- comma-separated
    project_url  VARCHAR(300),
    created_at   VARCHAR(30) NOT NULL
);

CREATE TABLE skills (
    id       INTEGER PRIMARY KEY,
    name     VARCHAR(100) NOT NULL UNIQUE,  -- uq_skill_name
    category VARCHAR(80)  NOT NULL DEFAULT 'General'
);

CREATE TABLE education (
    id          INTEGER PRIMARY KEY,
    institution VARCHAR(200) NOT NULL,
    programme   VARCHAR(200) NOT NULL,
    level       VARCHAR(80)  NOT NULL,
    status      VARCHAR(80)  NOT NULL DEFAULT 'Currently Studying'
);

CREATE TABLE services (
    id          INTEGER PRIMARY KEY,
    title       VARCHAR(160) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE contact_messages (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(120) NOT NULL,
    email      VARCHAR(160) NOT NULL,
    phone      VARCHAR(40),
    subject    VARCHAR(200),
    message    TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,   -- indexed
    is_read    BOOLEAN NOT NULL DEFAULT 0
);
```

---

## 3. Install & run

```bash
cd personal_api

# 1) Create a virtual environment (first time only)
python -m venv .venv
.venv\Scripts\activate            # Windows  (Git Bash: source .venv/Scripts/activate)
pip install -r requirements.txt

# 2) Create your .env
copy .env.example .env            # then edit values, especially SECRET_KEY

# 3) Start the API
uvicorn main:app --reload
```

**Windows shortcut:** double-click `run.bat` — it creates the venv on first run
and starts the API afterwards.

Then open:

| URL | Purpose |
|---|---|
| http://127.0.0.1:8000/docs | Swagger UI — try every endpoint interactively |
| http://127.0.0.1:8000/redoc | ReDoc reference documentation |
| http://127.0.0.1:8000/api/profile | Quick sanity check |

Run the tests:

```bash
python -m pytest          # from personal_api/ (uses an isolated test DB)
```

---

## 4. Environment variables (.env)

| Variable | Purpose | Default / example |
|---|---|---|
| `APP_NAME` | Shown in docs and health endpoint | `David Musumali Personal API` |
| `ENVIRONMENT` | `development` or `production` | `development` |
| `SECRET_KEY` | JWT signing secret — **change it, never commit it** | long random string |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Admin token lifetime | `60` |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` / `ADMIN_EMAIL` | First admin, created on startup | `admin` / `ChangeMe-Admin-2026` |
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./data/personal_api.db` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5500,...` |

Generate a strong secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 5. Endpoints

### PUBLIC — no authentication

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check / API index |
| GET | `/api/profile` | Personal information |
| GET | `/api/skills` | All skills |
| GET | `/api/skills/{id}` | One skill |
| GET | `/api/projects` | All projects |
| GET | `/api/projects/{id}` | One project |
| GET | `/api/education` | Education records |
| GET | `/api/services` | Service offerings |
| POST | `/api/contact` | Submit a contact message |
| POST | `/api/auth/login` | Admin login (issues JWT) |

### PRIVATE — require `Authorization: Bearer <token>` from `/api/auth/login`

| Method | Path | Description |
|---|---|---|
| GET | `/api/contact/messages` | Read contact submissions (private data) |
| POST | `/api/projects` | Create a project |
| PUT | `/api/projects/{id}` | Update a project |
| DELETE | `/api/projects/{id}` | Delete a project |
| POST | `/api/skills` | Add a skill |
| PUT | `/api/skills/{id}` | Update a skill |
| DELETE | `/api/skills/{id}` | Delete a skill |
| POST | `/api/education` | Add an education record |
| PUT | `/api/education/{id}` | Update an education record |
| DELETE | `/api/education/{id}` | Delete an education record |

In Swagger (`/docs`), click **Authorize**, log in with your admin credentials, and
the private endpoints become callable from the UI.

### Example: profile response

```json
{
  "name": "David Musumali",
  "profession": "Third-Year Mining Engineering Student",
  "university": "The Copperbelt University",
  "email": "DMUSUMALI01@GMAIL.COM",
  "phone": "+260773108622",
  "alt_phone": "+260761031385",
  "location": "Zambia",
  "bio": "Mining Engineering student combining engineering knowledge with software development…"
}
```

### Example: project response

```json
{
  "id": 3,
  "name": "KITE",
  "description": "A technology and engineering concept focused on software development, AI…",
  "tagline": "Engineering Ideas. Building the Future.",
  "technologies": ["Software Development", "AI", "Automation", "Databases"],
  "project_url": null,
  "created_at": "2026-09-23T10:00:00+00:00"
}
```

### Example: admin flow from the command line

```bash
# 1) Login (note: form data, not JSON)
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -d "username=admin" -d "password=ChangeMe-Admin-2026"

# 2) Use the returned token
TOKEN="eyJhbGciOi..."
curl http://127.0.0.1:8000/api/contact/messages -H "Authorization: Bearer $TOKEN"

# 3) Add a project
curl -X POST http://127.0.0.1:8000/api/projects \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "New Project", "description": "What it does for users.", "technologies": ["Python"]}'
```

---

## 6. Security

- **Secrets** live only in `.env` (git-ignored); `config.py` reads them via
  pydantic-settings — nothing is hard-coded.
- **Passwords** are hashed with bcrypt; only hashes are stored and never returned
  by any endpoint.
- **Authentication:** admin endpoints require a signed JWT (OAuth2 bearer scheme);
  invalid/expired tokens get `401`.
- **Validation:** every request body passes through strict Pydantic schemas
  (types, lengths, email format) — bad input gets `422` with field details.
- **CORS:** only origins listed in `CORS_ORIGINS` may call the API from a browser.
- **Error handling:** unhandled errors are logged server-side and return a generic
  `500` — no stack traces or internals leak to clients.
- **Private data:** contact submissions are never exposed publicly; only token
  holders can read them.

---

## 6b. Going online (deployment)

The stack is deployed **free** across two platforms:

| Piece | Platform | URL |
|---|---|---|
| Portfolio website (static) | **Netlify** | `https://<site>.netlify.app` |
| Personal API (FastAPI) | **Render** | `https://personal-api-xxxx.onrender.com` |

### Render (API) — via `render.yaml` Blueprint

1. Push this repository to GitHub.
2. On https://dashboard.render.com → **New → Blueprint**, select the repo.
   Render reads `render.yaml` and creates the `personal-api` web service
   (root dir `personal_api`, free plan, env vars auto-generated).
3. After the first deploy, open **Environment** and note the generated
   `ADMIN_PASSWORD` (or set your own) — you need it to log in at `/docs`.
4. Once you know your Netlify URL, set `CORS_ORIGINS` to
   `https://<site>.netlify.app` (comma-separated if you keep local ones).

Note: the free plan spins the API down after 15 minutes idle (~1 min cold
start on the next request) and the disk is ephemeral — content re-seeds from
`init_db.py`, but contact messages are lost on restart. For persistent
messages, upgrade to a paid plan with a persistent disk or move to PostgreSQL.

### Netlify (website)

1. On https://app.netlify.com → **Add new site → Import an existing project**,
   pick the GitHub repo.
2. Publish directory: `.` (repo root — `index.html` lives there).
   No build command needed.
3. Edit `js/apiConfig.js` and set
   `window.PORTFOLIO_API_BASE = "https://personal-api-xxxx.onrender.com"`
   (your Render URL), then push — Netlify redeploys automatically.

---

## 7. Connecting the website (fetch)

The website never touches the database — it only calls the API. Put this in your
frontend (adjust `API_BASE`, and add your origin to `CORS_ORIGINS` in `.env`):

```js
const API_BASE = "http://127.0.0.1:8000"; // e.g. https://api.yoursite.com in production

async function getJSON(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

// Load projects into the portfolio grid
getJSON("/api/projects").then((projects) => {
  projects.forEach((p) => console.log(p.name, p.technologies));
});

// Submit the contact form
async function sendContact(form) {
  const res = await fetch(`${API_BASE}/api/contact`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },      body: JSON.stringify({
        name: form.name.value,
        email: form.email.value,
        subject: form.subject.value || null,  // optional
        phone: form.phone.value || null,      // optional
        message: form.message.value,
      }),
  });
  if (res.status === 201) alert("Message sent!");
  else alert("Please check your inputs and try again.");
}
```

### Adding content as admin

1. `POST /api/auth/login` → copy `access_token`.
2. `POST /api/projects` (or `/api/skills`) with the bearer token → the website
   picks it up automatically on the next `GET`.
3. Or do it visually from `/docs` after clicking **Authorize**.

### Moving to a React frontend later

- The API is already CORS-enabled and returns plain JSON — a React app (or mobile
  app) consumes the same endpoints unchanged.
- Store the admin token in memory (or httpOnly cookie via a future refresh-token
  flow) and attach it as `Authorization: Bearer`.
- The foundation is ready for future additions: blog articles, certifications,
  work experience, file uploads, email notifications, analytics and PostgreSQL —
  each becomes a new model + schema + route file following the same pattern.
