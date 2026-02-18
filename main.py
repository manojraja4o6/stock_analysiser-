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

FILE_PATH = r"C:\Users\pds217\Documents\project\stock_analysis_data.csv"

def save_user_history(row: dict):
    try:
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

        new_df = pd.DataFrame([row])

        if os.path.exists(FILE_PATH):
            new_df.to_csv(FILE_PATH, mode="a", header=False, index=False)
        else:
            new_df.to_csv(FILE_PATH, index=False)

    except PermissionError:
        # If Excel is open, skip saving
        print("CSV file is open. Close Excel and try again.")



# ---------------- SERVICES ----------------
class StockService:
    @staticmethod
    def fetch(symbol: str):
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="6mo", interval="1d", auto_adjust=True)

            # ---------- HARD SAFETY CHECK ----------
            if hist is None or hist.empty:
                raise ValueError("No market data returned from Yahoo Finance")

            if "Close" not in hist.columns:
                raise ValueError("Close price column missing in market data")

            hist = hist.dropna(subset=["Close"])

            if len(hist) < 10:
                raise ValueError("Not enough historical data available")

            returns = hist["Close"].pct_change().dropna()

            if returns.empty:
                volatility = 0.0
            else:
                volatility = returns.std() * np.sqrt(252)

            current_price = float(hist["Close"].iloc[-1])

            return hist, current_price, volatility

        except Exception as e:
            raise ValueError(f"Data fetch failed: {str(e)}")


class Predictor:
    @staticmethod
    def predict(hist):
        try:
            if hist is None or hist.empty or len(hist) < 10:
                return 0.0, 0.0

            df = hist.copy()
            df = df.dropna(subset=["Close"])
            df["x"] = range(len(df))

            model = LinearRegression()
            model.fit(df[["x"]], df["Close"])

            next_price = model.predict(
                pd.DataFrame([[len(df)]], columns=["x"])
            )[0]

            confidence = model.score(df[["x"]], df["Close"]) * 100

            if np.isnan(next_price) or np.isnan(confidence):
                return 0.0, 0.0

            return float(next_price), float(confidence)

        except:
            return 0.0, 0.0



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
        # 1️⃣ Fetch stock data
        hist, current_price, volatility = StockService.fetch(q.stock)

        # 2️⃣ Predict next price
        predicted_price, confidence_score = Predictor.predict(hist)

        # 3️⃣ Detect risk level
        risk_level = auto_detect_risk(volatility)

        # 4️⃣ Detect user intent
        intent_detected = detect_intent(q.question)

        # 5️⃣ Create reply message
        bot_reply = (
            f"Current Price: ₹{current_price:.2f}\n"
            f"Predicted Price: ₹{predicted_price:.2f}\n"
            f"Risk Level: {risk_level.upper()}\n"
            f"Intent: {intent_detected.upper()}\n\n"
            "⚠️ Not financial advice."
        )

        # 6️⃣ Save user history
        save_user_history({
            "timestamp": datetime.now().isoformat(),
            "stock": q.stock,
            "question": q.question,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "risk": risk_level,
            "intent": intent_detected,
            "confidence": confidence_score
        })

        # 7️⃣ Return structured response
        return {
            "stock": q.stock,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "risk_preference": risk_level,
            "bot_reply": bot_reply,
            "intent_detected": intent_detected,
            "confidence_score": confidence_score
        }

    except Exception as e:
        # 8️⃣ Error fallback (never crash backend)
        return {
            "stock": q.stock,
            "current_price": 0.0,
            "predicted_price": 0.0,
            "risk_preference": "unknown",
            "bot_reply": f"Error occurred: {str(e)}",
            "intent_detected": "error",
            "confidence_score": 0.0
        }


