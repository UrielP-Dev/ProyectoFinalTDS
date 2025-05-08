# 🥗 Weekly Meal Planning System

This project allows students to plan their weekly meals by registering recipes and assigning them to specific days and times (breakfast, lunch, dinner).

---

## 📦 Requirements

- Python 3.10 or higher  
- MongoDB Atlas or local MongoDB instance  
- `pip` (Python package manager)

---

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/UrielP-Dev/ProyectoFinalTDS.git
cd proyecto_plan_comidas
````

2. **Create and activate a virtual environment (optional but recommended):**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🔐 `.env` Configuration

In the root of the project, create a file named `.env` with the following content:

```env
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
```

🔒 Make sure the `.env` file is included in your `.gitignore` to avoid pushing credentials to GitHub.

---

## 🚀 Running the Application

Run the application from the main file:

```bash
python app/main.py
```

---

## 📁 Project Structure

```
proyecto_plan_comidas/
├── app/                        # Application entry point
├── gui/                        # Graphical interfaces using Tkinter
├── controllers/                # Interface control logic
├── services/                   # Business logic
├── models/                     # Entity definitions
├── repositories/               # MongoDB connection and data access
├── utils/                      # Utility functions (e.g., validators)
├── requirements.txt
└── .env                        # Configuration with Mongo URI
```
