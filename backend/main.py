# backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import os

app = FastAPI(title="AI Stock Market Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ----------------
class StockQuery(BaseModel):
    stock: str
    question: str

class StockResponse(BaseModel):
    stock: str
    current_price: float
    predicted_price: float
    risk_preference: str
    bot_reply: str
    intent_detected: str
    confidence_score: float

# ---------------- HELPERS ----------------
def auto_detect_risk(volatility: float) -> str:
    if volatility > 0.4:
        return "high"
    elif volatility > 0.2:
        return "medium"
    return "low"

def save_user_history(row: dict):
    os.makedirs("user_history", exist_ok=True)
    file = os.path.join("user_history", "user_history.csv")

    new_df = pd.DataFrame([row])

    try:
        if os.path.exists(file):
            old_df = pd.read_csv(file)
            final_df = pd.concat([old_df, new_df], ignore_index=True)
        else:
            final_df = new_df

        final_df.to_csv(file, index=False)

    except PermissionError:
        # Windows Excel lock – skip saving silently
        return


# ---------------- SERVICES ----------------
class StockService:
    @staticmethod
    def fetch(symbol: str):
        t = yf.Ticker(symbol)
        hist = t.history(period="1mo")

        returns = hist["Close"].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)

        return hist, float(hist["Close"].iloc[-1]), volatility

class Predictor:
    @staticmethod
    def predict(hist):
        df = hist.copy()
        df["x"] = range(len(df))
        model = LinearRegression()
        model.fit(df[["x"]], df["Close"])
        next_price = model.predict(pd.DataFrame([[len(df)]], columns=["x"]))[0]

        confidence = model.score(df[["x"]], df["Close"]) * 100
        return float(next_price), float(confidence)

def detect_intent(q):
    q = q.lower()
    if "trend" in q:
        return "trend"
    if "buy" in q:
        return "buy"
    if "sell" in q:
        return "sell"
    return "general"

# ---------------- API ----------------
@app.post("/chat", response_model=StockResponse)
async def chat(q: StockQuery):
    try:
        hist, current, vol = StockService.fetch(q.stock)
        predicted, confidence = Predictor.predict(hist)
        risk = auto_detect_risk(vol)
        intent = detect_intent(q.question)

        reply = f"""
Current Price: ₹{current:.2f}
Predicted Price: ₹{predicted:.2f}
Risk Level: {risk.upper()}
Intent: {intent.upper()}

⚠️ Not financial advice.
"""

        save_user_history({
            "timestamp": datetime.now().isoformat(),
            "stock": q.stock,
            "question": q.question,
            "current_price": current,
            "predicted_price": predicted,
            "risk": risk,
            "intent": intent,
            "confidence": confidence
        })

        return {
            "stock": q.stock,
            "current_price": current,
            "predicted_price": predicted,
            "risk_preference": risk,
            "bot_reply": reply,
            "intent_detected": intent,
            "confidence_score": confidence
        }

    except Exception as e:
        return {
            "stock": q.stock,
            "current_price": 0.0,
            "predicted_price": 0.0,
            "risk_preference": "unknown",
            "bot_reply": f"Error occurred: {str(e)}",
            "intent_detected": "error",
            "confidence_score": 0.0
        }

