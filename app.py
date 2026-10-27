"""
Flask backend for Titanic Survival Prediction
– with automatic ngrok public URL (direct web access) –

HOW IT WORKS
------------
1. Run:  python app.py
2. The terminal will print something like:

      ╔══════════════════════════════════════════╗
      ║  🌐 PUBLIC URL: https://xxxx.ngrok-free.app ║
      ╚══════════════════════════════════════════╝

3. Share that URL with anyone — it works over the internet.

NGROK AUTH TOKEN (optional but recommended)
-------------------------------------------
Free ngrok accounts get a stable tunnel and no browser warning page.
Sign up at https://ngrok.com → Dashboard → Your Authtoken
Then set it once:

    python app.py --token YOUR_AUTHTOKEN_HERE

Or set the environment variable:
    set NGROK_AUTHTOKEN=YOUR_AUTHTOKEN_HERE

Without a token the tunnel still works but ngrok may show an
interstitial page for new visitors.
"""

import os
import sys
import pickle
import threading
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ── Load model ────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "model.pkl not found. Run  python train_model.py  first."
        )
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

model = load_model()

# ── Feature engineering (must match train_model.py) ───────────────────────────
def prepare_features(data):
    pclass       = int(data['pclass'])
    sex          = 1 if data['sex'] == 'female' else 0
    age          = float(data['age'])
    sibsp        = int(data['sibsp'])
    parch        = int(data['parch'])
    fare         = float(data['fare'])
    embarked     = {'S': 0, 'C': 1, 'Q': 2}.get(data['embarked'], 0)

    family_size     = sibsp + parch + 1
    is_alone        = 1 if family_size == 1 else 0
    fare_per_person = fare / family_size

    return np.array([[pclass, sex, age, sibsp, parch, fare,
                      embarked, family_size, is_alone, fare_per_person]])

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features   = prepare_features(data)
        prediction  = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
        return jsonify({
            'survived':    prediction,
            'probability': round(probability * 100, 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ── ngrok tunnel ──────────────────────────────────────────────────────────────
def start_ngrok(port: int, auth_token: str | None = None):
    """Open a public ngrok tunnel and print the URL."""
    try:
        from pyngrok import ngrok, conf

        # Resolve token: CLI arg > env var
        token = auth_token or os.environ.get('NGROK_AUTHTOKEN')

        if not token:
            print("\n" + "=" * 60)
            print("  NGROK AUTH TOKEN REQUIRED FOR PUBLIC URL")
            print("=" * 60)
            print("  1. Sign up FREE at: https://ngrok.com")
            print("  2. Copy your token from: https://dashboard.ngrok.com/get-started/your-authtoken")
            print("  3. Start with token:")
            print("       python app.py --token YOUR_TOKEN_HERE")
            print("     OR set environment variable:")
            print("       set NGROK_AUTHTOKEN=YOUR_TOKEN_HERE")
            print("=" * 60)
            print("  App is still running locally at:")
            print(f"  http://127.0.0.1:{port}  (this machine only)")
            print("=" * 60 + "\n")
            return

        conf.get_default().auth_token = token
        print("  ngrok auth token applied.")

        tunnel = ngrok.connect(port, bind_tls=True)
        public_url = tunnel.public_url

        border = "=" * 60
        print(f"\n  {border}")
        print(f"  PUBLIC URL  : {public_url}")
        print(f"  Local URL   : http://127.0.0.1:{port}")
        print(f"  {border}")
        print("  Share the PUBLIC URL with anyone on the internet!")
        print("  Press CTRL+C to stop the server.\n")

    except ImportError:
        print("\n  pyngrok not installed. Run:  pip install pyngrok")
        print(f"  Running locally only at http://127.0.0.1:{port}\n")
    except Exception as exc:
        print(f"\n  ngrok tunnel error: {exc}")
        print(f"  Running locally at http://127.0.0.1:{port}\n")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    PORT = 5000

    # Optional: pass --token YOUR_TOKEN as a CLI argument
    auth_token = None
    if '--token' in sys.argv:
        idx = sys.argv.index('--token')
        if idx + 1 < len(sys.argv):
            auth_token = sys.argv[idx + 1]

    # Start ngrok tunnel in a background thread so Flask starts immediately
    threading.Thread(
        target=start_ngrok,
        args=(PORT, auth_token),
        daemon=True
    ).start()

    print(f"\n  Titanic Survival Predictor")
    print(f"  Starting server on port {PORT}...\n")

    app.run(host='0.0.0.0', port=PORT, debug=False)
