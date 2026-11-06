# MedNova - New Age Healthcare Intelligence — Official Demonstration Guide

## 1. Start the application

### Windows
Double-click `run_demo.bat`.

### macOS/Linux
Run:

```bash
./run_demo.sh
```

The application opens at:

`http://localhost:8080`

The first Docker startup may take several minutes because the application creates the vector index and downloads the embedding model. Later starts are faster because the ChromaDB volume is persistent.

## 2. Demo accounts

| Role | Username | Password | Demonstrate |
|---|---|---|---|
| Provider | `provider` | `Provider@123` | Full clinical search and patient directory |
| Patient | `patient9` | `Patient@123` | Patient-only record boundary for P009 |
| Insurer | `insurer` | `Insurer@123` | Redacted identity/contact information |
| Administrator | `admin` | `Admin@123` | Audit logs and system administration |

These are synthetic academic-demo credentials. Change them before any non-demo deployment.

## 3. Recommended 5-minute presentation

### Step 1 — Login
Use the **Provider** demo account. Explain that authentication creates a signed JWT and the backend uses the token for authorization.

### Step 2 — Dashboard
Show the patient statistics and application status. Explain that the system is built around a role-aware clinical information retrieval workflow.

### Step 3 — Patient Directory
Search for a patient and open the record. Point out that records are retrieved through the backend API rather than being embedded in the frontend.

### Step 4 — Medical Inquiry
Try queries such as:

- `Show patients with diabetes`
- `Which patients have HbA1c above 7`
- `Summarize patient P009`
- `Show patients taking metformin`

Explain the RAG pipeline:

`Natural-language query → query processing → retrieval → context construction → response generation → provenance`

The default release works in **offline mode**, so the demonstration does not require an external AI API key.

### Step 5 — Patient privacy
Log out and sign in as `patient9`. Show that the patient can access only P009.

Then sign in as `insurer` and open a patient record. Show that phone, email and address fields are redacted.

### Step 6 — Audit trail
Sign in as `admin` and open **Audit Logs**. Demonstrate that logins, patient access and queries are recorded with user, role, timestamp, action and accessed patient IDs.

### Step 7 — System Health
Open **System Health** and show the dataset, vector database and LLM provider status.

## 4. Architecture to explain

```text
React/Vite UI
      │
      ▼
Nginx reverse proxy
      │
      ▼
Flask REST API
      │
      ├── JWT Authentication / RBAC
      ├── Patient Record API
      ├── Audit Logging
      │
      ▼
RAG Pipeline
      │
      ├── Query Processor
      ├── ChromaDB Vector Retrieval
      ├── Sentence-Transformer Embeddings
      ├── Context Builder
      └── Response Generator
              │
              ├── Offline fallback
              ├── LM Studio (optional)
              └── AWS Bedrock (optional)
```

## 5. What makes this a final-year project

- Full-stack web application
- Retrieval-Augmented Generation architecture
- Natural-language medical information retrieval
- Vector database and semantic search
- Role-Based Access Control
- Patient-level authorization
- Privacy-aware insurer redaction
- Audit trail and accountability
- Health monitoring
- Containerized deployment
- Automated data/index initialization
- Synthetic data for safe demonstration

## 6. Stop the demo

```bash
docker compose down
```

To remove persistent demo data as well:

```bash
docker compose down -v
```

## 7. Important academic disclaimer

MedNova is an academic clinical-information retrieval prototype. It is not a medical device, diagnostic system, or substitute for qualified clinical judgment. Demonstration data is synthetic.
