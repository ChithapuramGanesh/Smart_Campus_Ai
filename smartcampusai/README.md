# SmartCampusAIA

SmartCampusAIA is a premium, modern, AI-powered campus management dashboard built using Python and Streamlit. It provides administrators and educators with tools to monitor student enrollments, faculty directories, attendance trends, and resource analytics while integrating an OpenAI-compatible conversational assistant.

## Features

- **Secure Session Authentication**: Dual username/email matching, client-side session persistence, and password validation with high-entropy checks and `bcrypt` password hashing.
- **Atomic JSON Database Layer**: High-safety atomic write operations with error detection and automatic corrupted file backup/recovery.
- **Glassmorphism UI/UX**: Premium custom stylesheet overrides including responsive multi-columns, neon glow hover cards, system-wide light/dark themes, and custom typography.
- **Plotly Visualizations**: Daily attendance timelines, department breakdown histograms, GPA distribution curves, and course syllabus pass rate radar figures.
- **Context-Aware AI Chat Assistant**: Supports streaming chat with custom base configurations (base URL, key verification, model override), and features a local mock database search engine fallback if no API key is specified.

---

## Folder Structure

```
SmartCampusAIA/
│── app.py                   # Main routing entry point
│── requirements.txt         # Project dependencies
│── .env                     # Custom environmental properties
│── .env.example             # Environment configuration template
│── README.md                # System documentation
│
├── .streamlit/
│      config.toml           # Hides default Streamlit menu & applies dark base theme
│
├── database/
│      users.json            # Stores user credentials securely
│      activity.json         # Stores user logs and campus logs
│      settings.json         # Campus records: students, faculty, attendance
│
├── assets/
│      logo.png              # Campus branding asset
│      background.png        # Glassmorphic background asset
│
├── pages/
│      login.py              # Account sign-in view
│      register.py           # Account creation view
│      dashboard.py          # Dashboard sub-page views container
│      profile.py            # User account settings view
│      settings.py           # System preferences & API configurations
│
├── components/
│      navbar.py             # Top brand header component
│      sidebar.py            # Custom option-menu sidebar component
│      cards.py              # Grid metrics, notifications, and data tables
│      footer.py             # Standard footer branding
│
├── utils/
│      auth.py               # Cryptographic validation & login verification
│      database.py           # Safe file operations & JSON reading/writing
│      helpers.py            # Data filters & Plotly graph configurations
│      ai.py                 # OpenAI wrappers & offline mock responses
│      session.py            # Streamlit session state initialization & clear
│
└── styles/
       style.css             # Main UI theme overriding Streamlit styles
```

---

## Installation & Local Run

Follow these instructions to run the application on your local machine.

### Prerequisites
- Python 3.12 or higher installed.

### 1. Clone the project and navigate into it
```bash
cd SmartCampusAIA
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

### 4. Create and configure environment variables
Copy the `.env.example` template to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your OpenAI API Key:
```
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini
```
*Note: If you leave the key blank, the application will run in offline demo mode using local campus statistics.*

### 5. Launch the application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## Deployment

The application is deployment-ready for cloud platforms:

### Streamlit Community Cloud
1. Push your repository to GitHub.
2. Log in to [Streamlit Share](https://share.streamlit.io/).
3. Connect your repository, select `app.py` as the entrypoint, and specify your environment variables (like `OPENAI_API_KEY`) under **Advanced Settings > Secrets**.
4. Click **Deploy**.

### Railway, Render, or Hugging Face Spaces
- Ensure the `requirements.txt` is in the root directory.
- Set the start command to `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.
- Inject your `.env` variables under the deployment config environment settings.

---

## Screenshots Placeholder

- **Login Screen**: Glassmorphic modal with input sanitization.
- **Home Dashboard**: Custom metrics layout, attendance timelines, and notifications log.
- **AI Assistant**: Fluid user-agent dialog box with status indicators.
- **Interactive Analytics**: Interactive Plotly distribution dashboards.
