<div align="center">

# 🚢 Titanic Survival Predictor
### AIML Minor Project — 5th Semester

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-orange?style=for-the-badge&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Would you have survived the night of April 14–15, 1912?**  
> Enter your passenger details and let our ML model predict your fate aboard the RMS Titanic.

</div>

---

## 📸 Preview

> Ocean-themed dark UI with animated ship, twinkling stars, and an interactive probability gauge.

```
┌─────────────────────────────────────────────────┐
│  🚢  Titanic Survival Predictor                  │
│  ─────────────────────────────────────────────  │
│  Passenger Class  │  Gender                      │
│  [ 1st ] [2nd] [3rd]   [ Male ] [ Female ]       │
│  Age ________   Fare ________                   │
│  Siblings/Spouse ___   Parents/Children ___      │
│  Port: [Southampton] [Cherbourg] [Queenstown]    │
│                                                  │
│          [ 🔍 Predict My Fate ]                  │
└─────────────────────────────────────────────────┘
         ▼  Result Card  ▼
┌─────────────────────────────────────────────────┐
│   🛟  YOU SURVIVED!                              │
│   Survival Probability ████████░░  87.2%        │
│   "As a 29-year-old woman in 1st Class…"        │
└─────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🤖 **ML Model** | Random Forest Classifier (200 estimators, depth 6) |
| 📊 **Accuracy** | ~73% on held-out test set |
| 🌐 **Web Interface** | Flask backend + vanilla JS frontend |
| 🎨 **Ocean Theme** | Animated ship, stars, wave effects, gold accents |
| 📡 **Public URL** | Built-in ngrok tunnel (optional, free) |
| 📈 **Probability Gauge** | Animated bar showing survival % |
| 📋 **Historical Stats** | Real Titanic statistics panel |
| ✅ **Validation** | Client-side + server-side input checking |

---

## 🧠 Machine Learning Details

### Model
- **Algorithm:** `RandomForestClassifier` (scikit-learn)
- **Estimators:** 200 trees
- **Max depth:** 6
- **Class weight:** Balanced (handles class imbalance)

### Features Used

| Feature | Description |
|---------|-------------|
| `Pclass` | Passenger class (1 / 2 / 3) |
| `Sex` | Gender (encoded: female=1, male=0) |
| `Age` | Age in years |
| `SibSp` | # of siblings/spouses aboard |
| `Parch` | # of parents/children aboard |
| `Fare` | Ticket fare in £ |
| `Embarked` | Port (S=0, C=1, Q=2) |
| `FamilySize` | SibSp + Parch + 1 *(engineered)* |
| `IsAlone` | 1 if travelling alone *(engineered)* |
| `FarePerPerson` | Fare ÷ FamilySize *(engineered)* |

### Key Survival Insights

- 👩 **Women & Children First** — strongest predictor (~92% influence)
- 🎩 **1st Class Advantage** — upper-deck proximity to lifeboats
- 💰 **Higher Fare** — correlated with better cabin location
- 👨‍👩‍👧 **Family Size** — very large families had lower survival rates

---

## 🗂️ Project Structure

```
titanic_web/
│
├── app.py               # Flask backend + ngrok tunnel
├── train_model.py       # Model training script
├── start.bat            # Double-click launcher (Windows)
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html       # Full HTML UI
│
└── static/
    ├── css/
    │   └── style.css    # Ocean-themed stylesheet
    └── js/
        └── main.js      # Fetch API + animations + validation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- pip

### 2. Clone the Repository

```bash
git clone https://github.com/TriptiGayakwad/Titanic-Survival-Prediction---AIML-Minor-1-Project-.git
cd Titanic-Survival-Prediction---AIML-Minor-1-Project-
```

### 3. Install Dependencies

```bash
pip install flask scikit-learn pandas numpy pyngrok
```

### 4. Train the Model

```bash
python train_model.py
```

> This generates `model.pkl` locally (not committed to git).  
> Output: `Model trained! Test Accuracy: 73.3%`

### 5. Run the App

**Option A — Double-click launcher (recommended for Windows):**
```
Double-click  start.bat
```

**Option B — Command line (local only):**
```bash
python app.py
```

**Option C — With public internet URL via ngrok:**
```bash
python app.py --token YOUR_NGROK_TOKEN
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 🌐 Public URL (Share with Anyone)

Get a free public internet URL using [ngrok](https://ngrok.com):

1. Sign up free at **https://ngrok.com**
2. Copy your authtoken from **https://dashboard.ngrok.com/get-started/your-authtoken**
3. Run:
   ```bash
   python app.py --token YOUR_TOKEN_HERE
   ```
4. Terminal prints:
   ```
   ============================================================
   PUBLIC URL  : https://xxxx.ngrok-free.app   ← share this!
   Local URL   : http://127.0.0.1:5000
   ============================================================
   ```

---

## 📡 API Reference

### `POST /predict`

**Request body (JSON):**
```json
{
  "pclass":   "1",
  "sex":      "female",
  "age":      "29",
  "sibsp":    "0",
  "parch":    "0",
  "fare":     "100",
  "embarked": "C"
}
```

**Response:**
```json
{
  "survived":    1,
  "probability": 87.2
}
```

---

## 📊 Historical Titanic Statistics

| Group | Survival Rate |
|-------|--------------|
| 1st Class Women | ~97% |
| 2nd Class Women | ~86% |
| 3rd Class Women | ~49% |
| 1st Class Men | ~37% |
| 2nd Class Men | ~15% |
| 3rd Class Men | ~13% |
| **Overall** | **~31.9%** |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask 3.1 |
| ML | scikit-learn 1.9, pandas, numpy |
| Frontend | HTML5, CSS3, Vanilla JS |
| Tunneling | pyngrok (ngrok) |
| Fonts | Google Fonts — Cinzel, Lato |

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ by **Tripti Gayakwad**  
5th Semester AIML Minor Project

</div>
