# frontend.py
import streamlit as st
import requests
from datetime import datetime

st.set_page_config("AI Stock Assistant", layout="wide")

API_URL = "https://stock-analysiser.onrender.com/chat"

# ---------- STYLE ----------
st.markdown("""
<style>
body {
    background-color: #b2b5b8;
}
.main {
    background-color: #b2b5b8;
}
h1, h2, h3, h4, label {
    color: black !important;
    font-weight: bold;
}
textarea {
    background-color: #e6e6e6 !important;
}
</style>
""", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

if "auto_send" not in st.session_state:
    st.session_state.auto_send = False

if "question" not in st.session_state:
    st.session_state.question = ""

# -------- SIDEBAR --------
with st.sidebar:
    st.title("⚙️ Configuration")

    stock = st.selectbox("Choose Stock", {
         "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "State Bank of India",
    "HDFC.NS": "Housing Development Finance Corp",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "AXISBANK.NS": "Axis Bank",
    "ITC.NS": "ITC Limited",
    "BHARTIARTL.NS": "Bharti Airtel",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "LT.NS": "Larsen & Toubro",
    "MARUTI.NS": "Maruti Suzuki",
    "SUNPHARMA.NS": "Sun Pharmaceutical",
    "TATAMOTORS.NS": "Tata Motors",
    "TITAN.NS": "Titan Company",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "WIPRO.NS": "Wipro",
    "ASIANPAINT.NS": "Asian Paints",
    "BAJFINANCE.NS": "Bajaj Finance",
    "BAJAJFINSV.NS": "Bajaj Finserv",
    "DMART.NS": "Avenue Supermarts",
    "NESTLEIND.NS": "Nestle India",
    "POWERGRID.NS": "Power Grid Corp",
    "NTPC.NS": "NTPC",
    "ONGC.NS": "Oil & Natural Gas Corp",
    "COALINDIA.NS": "Coal India",
    "M&M.NS": "Mahindra & Mahindra",
    "BRITANNIA.NS": "Britannia Industries",
    
    # ========== INDIAN STOCKS (BSE) ==========
    "RELIANCE.BO": "Reliance Industries (BSE)",
    "TCS.BO": "Tata Consultancy Services (BSE)",
    "INFY.BO": "Infosys (BSE)",
    "TATAMOTORS.BO": "Tata Motors (BSE)",
    
    # ========== US TECHNOLOGY ==========
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc. (Class A)",
    "GOOG": "Alphabet Inc. (Class C)",
    "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "NVDA": "NVIDIA Corporation",
    "AVGO": "Broadcom Inc.",
    "CSCO": "Cisco Systems",
    "ADBE": "Adobe Inc.",
    "CRM": "Salesforce Inc.",
    "INTC": "Intel Corporation",
    "AMD": "Advanced Micro Devices",
    "QCOM": "Qualcomm Inc.",
    "ORCL": "Oracle Corporation",
    "IBM": "International Business Machines",
    "TXN": "Texas Instruments",
    "MU": "Micron Technology",
    "NOW": "ServiceNow",
    "PYPL": "PayPal Holdings",
    "SQ": "Block Inc.",
    "SHOP": "Shopify Inc.",
    "NET": "Cloudflare Inc.",
    "CRWD": "CrowdStrike Holdings",
    "PANW": "Palo Alto Networks",
    "UBER": "Uber Technologies",
    "LYFT": "Lyft Inc.",
    "SNAP": "Snap Inc.",
    "TWTR": "Twitter (X Corp)",
    "SPOT": "Spotify Technology",
    
    # ========== US SEMICONDUCTORS ==========
    "TSM": "Taiwan Semiconductor",
    "ASML": "ASML Holding",
    "AMD": "Advanced Micro Devices",
    "NVDA": "NVIDIA Corporation",
    "INTC": "Intel Corporation",
    "QCOM": "Qualcomm Inc.",
    "TXN": "Texas Instruments",
    "MU": "Micron Technology",
    "AMAT": "Applied Materials",
    "LRCX": "Lam Research",
    "KLAC": "KLA Corporation",
    
    # ========== US FINANCIAL SERVICES ==========
    "JPM": "JPMorgan Chase & Co.",
    "BAC": "Bank of America",
    "WFC": "Wells Fargo & Company",
    "C": "Citigroup Inc.",
    "GS": "Goldman Sachs Group",
    "MS": "Morgan Stanley",
    "V": "Visa Inc.",
    "MA": "Mastercard Inc.",
    "AXP": "American Express",
    "BRK-B": "Berkshire Hathaway (Class B)",
    "SCHW": "Charles Schwab Corp",
    "BLK": "BlackRock Inc.",
    "PYPL": "PayPal Holdings",
    "SQ": "Block Inc.",
    "COIN": "Coinbase Global",
    
    # ========== US HEALTHCARE ==========
    "JNJ": "Johnson & Johnson",
    "UNH": "UnitedHealth Group",
    "PFE": "Pfizer Inc.",
    "ABBV": "AbbVie Inc.",
    "MRK": "Merck & Co.",
    "TMO": "Thermo Fisher Scientific",
    "ABT": "Abbott Laboratories",
    "DHR": "Danaher Corporation",
    "LLY": "Eli Lilly and Company",
    "BMY": "Bristol-Myers Squibb",
    "AMGN": "Amgen Inc.",
    "GILD": "Gilead Sciences",
    "CVS": "CVS Health",
    "MRNA": "Moderna Inc.",
    "BIIB": "Biogen Inc.",
    "REGN": "Regeneron Pharmaceuticals",
    "VRTX": "Vertex Pharmaceuticals",
    
    # ========== US CONSUMER ==========
    "WMT": "Walmart Inc.",
    "COST": "Costco Wholesale",
    "HD": "Home Depot",
    "LOW": "Lowe's Companies",
    "TGT": "Target Corporation",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "NKE": "Nike Inc.",
    "SBUX": "Starbucks Corporation",
    "MCD": "McDonald's Corporation",
    "KO": "Coca-Cola Company",
    "PEP": "PepsiCo Inc.",
    "PG": "Procter & Gamble",
    "CL": "Colgate-Palmolive",
    "UL": "Unilever PLC",
    "DIS": "Walt Disney Company",
    "NFLX": "Netflix Inc.",
    "CMCSA": "Comcast Corporation",
    "CHTR": "Charter Communications",
    "PM": "Philip Morris International",
    "MO": "Altria Group",
    
    # ========== US INDUSTRIALS ==========
    "BA": "Boeing Company",
    "CAT": "Caterpillar Inc.",
    "GE": "General Electric",
    "HON": "Honeywell International",
    "UPS": "United Parcel Service",
    "FDX": "FedEx Corporation",
    "RTX": "Raytheon Technologies",
    "LMT": "Lockheed Martin",
    "GD": "General Dynamics",
    "NOC": "Northrop Grumman",
    "DE": "Deere & Company",
    "MMM": "3M Company",
    
    # ========== US ENERGY ==========
    "XOM": "Exxon Mobil Corporation",
    "CVX": "Chevron Corporation",
    "COP": "ConocoPhillips",
    "SLB": "Schlumberger",
    "EOG": "EOG Resources",
    "PXD": "Pioneer Natural Resources",
    "MPC": "Marathon Petroleum",
    "PSX": "Phillips 66",
    "VLO": "Valero Energy",
    "OXY": "Occidental Petroleum",
    
    # ========== US UTILITIES ==========
    "NEE": "NextEra Energy",
    "DUK": "Duke Energy",
    "SO": "Southern Company",
    "D": "Dominion Energy",
    "EXC": "Exelon Corporation",
    "AEP": "American Electric Power",
    
    # ========== US REAL ESTATE ==========
    "AMT": "American Tower Corporation",
    "PLD": "Prologis Inc.",
    "CCI": "Crown Castle International",
    "EQIX": "Equinix Inc.",
    "PSA": "Public Storage",
    "SPG": "Simon Property Group",
    
    # ========== US TELECOM ==========
    "VZ": "Verizon Communications",
    "T": "AT&T Inc.",
    "TMUS": "T-Mobile US",
    "CHTR": "Charter Communications",
    "CMCSA": "Comcast Corporation",
    
    # ========== CHINESE STOCKS ==========
    "BABA": "Alibaba Group",
    "PDD": "Pinduoduo Inc.",
    "JD": "JD.com Inc.",
    "BIDU": "Baidu Inc.",
    "NTES": "NetEase Inc.",
    "TCEHY": "Tencent Holdings",
    "NIO": "NIO Inc.",
    "LI": "Li Auto Inc.",
    "XPEV": "XPeng Inc.",
    "BZUN": "Baozun Inc.",
    "TCOM": "Trip.com Group",
    
    # ========== EUROPEAN STOCKS ==========
    "ASML.AS": "ASML Holding (Netherlands)",
    "SHEL": "Shell PLC (UK)",
    "BP": "BP PLC (UK)",
    "HSBC": "HSBC Holdings (UK)",
    "ULVR.L": "Unilever PLC (UK)",
    "AZN": "AstraZeneca PLC (UK)",
    "GSK": "GSK PLC (UK)",
    "SAP": "SAP SE (Germany)",
    "SIEGY": "Siemens AG (Germany)",
    "MBG.DE": "Mercedes-Benz Group (Germany)",
    "BMW.DE": "BMW AG (Germany)",
    "VOW.DE": "Volkswagen AG (Germany)",
    "AIR.PA": "Airbus SE (France)",
    "TTE": "TotalEnergies SE (France)",
    "SAN": "Santander (Spain)",
    "BBVA": "BBVA (Spain)",
    "ENB": "Enbridge Inc. (Canada)",
    "RY": "Royal Bank of Canada",
    "TD": "Toronto-Dominion Bank",
    "SHOP": "Shopify Inc. (Canada)",
    
    # ========== JAPANESE STOCKS ==========
    "TM": "Toyota Motor Corp",
    "HMC": "Honda Motor Co",
    "SONY": "Sony Group Corp",
    "NTDOY": "Nintendo Co",
    "MUFG": "Mitsubishi UFJ Financial",
    
    # ========== AUSTRALIAN STOCKS ==========
    "BHP": "BHP Group Ltd",
    "RIO": "Rio Tinto Ltd",
    "CBA.AX": "Commonwealth Bank (Australia)",
    
    # ========== SOUTH KOREAN STOCKS ==========
    "005930.KS": "Samsung Electronics",
    "000660.KS": "SK Hynix",
    "035420.KS": "Naver Corp",
    "051910.KS": "LG Chem",
    
    # ========== TAIWANESE STOCKS ==========
    "2330.TW": "Taiwan Semiconductor",
    "2454.TW": "MediaTek Inc.",
    
    # ========== HONG KONG STOCKS ==========
    "0700.HK": "Tencent Holdings",
    "0941.HK": "China Mobile",
    "0388.HK": "Hong Kong Exchanges",
    
    # ========== BRAZILIAN STOCKS ==========
    "VALE": "Vale SA",
    "ITUB": "Itau Unibanco",
    "BBD": "Banco Bradesco",
    "PBR": "Petrobras",
    
    # ========== RUSSIAN STOCKS ==========
    "OGZPY": "Gazprom",
    "LKOHY": "Lukoil",
    "SBRCY": "Sberbank",
    
    # ========== CRYPTOCURRENCY-RELATED ==========
    "COIN": "Coinbase Global",
    "MSTR": "MicroStrategy",
    "RIOT": "Riot Platforms",
    "MARA": "Marathon Digital",
    
    # ========== EV & CLEAN ENERGY ==========
    "TSLA": "Tesla Inc.",
    "NIO": "NIO Inc.",
    "LI": "Li Auto Inc.",
    "XPEV": "XPeng Inc.",
    "RIVN": "Rivian Automotive",
    "LCID": "Lucid Group",
    "FSR": "Fisker Inc.",
    "PLUG": "Plug Power",
    "BLDP": "Ballard Power Systems",
    "RUN": "Sunrun Inc.",
    "ENPH": "Enphase Energy",
    "SEDG": "SolarEdge Technologies",
    
    # ========== BIOTECH ==========
    "MRNA": "Moderna Inc.",
    "BNTX": "BioNTech SE",
    "VRTX": "Vertex Pharmaceuticals",
    "REGN": "Regeneron Pharmaceuticals",
    "ILMN": "Illumina Inc.",
    "CRSP": "CRISPR Therapeutics",
    "EDIT": "Editas Medicine",
    "NTLA": "Intellia Therapeutics",
    
    # ========== FINTECH ==========
    "PYPL": "PayPal Holdings",
    "SQ": "Block Inc.",
    "SOFI": "SoFi Technologies",
    "AFRM": "Affirm Holdings",
    "UPST": "Upstart Holdings",
    "HOOD": "Robinhood Markets",
    
    # ========== RETAIL & E-COMMERCE ==========
    "AMZN": "Amazon.com Inc.",
    "WMT": "Walmart Inc.",
    "TGT": "Target Corporation",
    "COST": "Costco Wholesale",
    "HD": "Home Depot",
    "LOW": "Lowe's Companies",
    "BABA": "Alibaba Group",
    "JD": "JD.com Inc.",
    "PDD": "Pinduoduo Inc.",
    "MELI": "MercadoLibre",
    "SE": "Sea Limited",
    "SHOP": "Shopify Inc.",
    
    # ========== ENTERTAINMENT & GAMING ==========
    "DIS": "Walt Disney Company",
    "NFLX": "Netflix Inc.",
    "SPOT": "Spotify Technology",
    "ATVI": "Activision Blizzard",
    "EA": "Electronic Arts",
    "TTWO": "Take-Two Interactive",
    "NTDOY": "Nintendo Co",
    "SONY": "Sony Group Corp",
    "ROKU": "Roku Inc.",
    "CHTR": "Charter Communications",
    "CMCSA": "Comcast Corporation",
    
    # ========== AEROSPACE & DEFENSE ==========
    "BA": "Boeing Company",
    "LMT": "Lockheed Martin",
    "RTX": "Raytheon Technologies",
    "NOC": "Northrop Grumman",
    "GD": "General Dynamics",
    "HII": "Huntington Ingalls",
    
    # ========== AUTOMOTIVE ==========
    "TM": "Toyota Motor Corp",
    "F": "Ford Motor Company",
    "GM": "General Motors",
    "STLA": "Stellantis NV",
    "HMC": "Honda Motor Co",
    "VWAGY": "Volkswagen AG",
    "MBG.DE": "Mercedes-Benz Group",
    "BMW.DE": "BMW AG",
    "RACE": "Ferrari NV",
    
    # ========== PHARMACEUTICALS ==========
    "JNJ": "Johnson & Johnson",
    "PFE": "Pfizer Inc.",
    "MRK": "Merck & Co.",
    "ABBV": "AbbVie Inc.",
    "BMY": "Bristol-Myers Squibb",
    "AMGN": "Amgen Inc.",
    "GILD": "Gilead Sciences",
    "AZN": "AstraZeneca PLC",
    "GSK": "GSK PLC",
    "SNY": "Sanofi",
    "NVO": "Novo Nordisk",
    "LLY": "Eli Lilly and Company",
    
    # ========== MINING & MATERIALS ==========
    "BHP": "BHP Group Ltd",
    "RIO": "Rio Tinto Ltd",
    "VALE": "Vale SA",
    "FCX": "Freeport-McMoRan",
    "NEM": "Newmont Corporation",
    "GOLD": "Barrick Gold",
    "AA": "Alcoa Corporation",
    "STLD": "Steel Dynamics",
    "NUE": "Nucor Corporation",
    
    # ========== LOGISTICS & TRANSPORTATION ==========
    "UPS": "United Parcel Service",
    "FDX": "FedEx Corporation",
    "DHL.DE": "Deutsche Post DHL",
    "EXPD": "Expeditors International",
    "CHRW": "C.H. Robinson Worldwide",
    
    # ========== HOTELS & TRAVEL ==========
    "MAR": "Marriott International",
    "HLT": "Hilton Worldwide",
    "EXPE": "Expedia Group",
    "ABNB": "Airbnb Inc.",
    "BKNG": "Booking Holdings",
    "TCOM": "Trip.com Group",
    "LYV": "Live Nation Entertainment",
    
    # ========== FOOD & BEVERAGE ==========
    "KO": "Coca-Cola Company",
    "PEP": "PepsiCo Inc.",
    "MNST": "Monster Beverage",
    "KDP": "Keurig Dr Pepper",
    "STZ": "Constellation Brands",
    "BUD": "Anheuser-Busch InBev",
    "DEO": "Diageo PLC",
    "SAM": "Boston Beer Company",
    "TAP": "Molson Coors Beverage",
    
    # ========== FASHION & LUXURY ==========
    "NKE": "Nike Inc.",
    "LULU": "Lululemon Athletica",
    "ULTA": "Ulta Beauty",
    "RL": "Ralph Lauren",
    "PVH": "PVH Corp",
    "VFC": "VF Corporation",
    "TPR": "Tapestry Inc.",
    "CPRI": "Capri Holdings",
    
    # ========== INSURANCE ==========
    "BRK-B": "Berkshire Hathaway",
    "UNH": "UnitedHealth Group",
    "ANTM": "Anthem Inc.",
    "HUM": "Humana Inc.",
    "CI": "Cigna Corporation",
    "AET": "Aetna Inc. (CVS)",
    "AFL": "Aflac Inc.",
    "PRU": "Prudential Financial",
    "MET": "MetLife Inc.",
    "ALL": "Allstate Corporation",
    
    # ========== REAL ESTATE INVESTMENT TRUSTS (REITs) ==========
    "O": "Realty Income Corporation",
    "VNQ": "Vanguard Real Estate ETF",
    "AMT": "American Tower Corporation",
    "PLD": "Prologis Inc.",
    "EQIX": "Equinix Inc.",
    "CCI": "Crown Castle International",
    "PSA": "Public Storage",
    "SPG": "Simon Property Group",
    "WELL": "Welltower Inc.",
    "VTR": "Ventas Inc.",
    "DLR": "Digital Realty Trust",
    
    # ========== MAJOR INDICES (ETFs) ==========
    "SPY": "SPDR S&P 500 ETF",
    "QQQ": "Invesco QQQ Trust",
    "DIA": "SPDR Dow Jones Industrial Average ETF",
    "IWM": "iShares Russell 2000 ETF",
    "VTI": "Vanguard Total Stock Market ETF",
    "VOO": "Vanguard S&P 500 ETF",
    "IVV": "iShares Core S&P 500 ETF",
    "GLD": "SPDR Gold Shares",
    "SLV": "iShares Silver Trust",
    "USO": "United States Oil Fund",
    "TLT": "iShares 20+ Year Treasury Bond ETF",
    "HYG": "iShares iBoxx $ High Yield Corporate Bond ETF",
    "LQD": "iShares iBoxx $ Investment Grade Corporate Bond ETF",
    "BND": "Vanguard Total Bond Market ETF",
    })

    st.markdown("### 💡 **Quick Questions**")
    for q in [
        "What is the current trend?",
        "Should I buy this stock?",
        "Is this a good time to sell?"
    ]:
        if st.button(q, use_container_width=True):
            st.session_state.question = q
            st.session_state.auto_send = True
            st.rerun()

# -------- MAIN --------
st.markdown("## 🖤 **AI Stock Market Assistant – Trade Analyzer**")

question = st.text_area(
    "**Ask your detailed question**",
    value=st.session_state.question
)

send = st.button("🚀 Analyze")

if send or st.session_state.auto_send:
    st.session_state.auto_send = False

    payload = {
        "stock": stock,
        "question": question
    }

    with st.spinner("Analyzing..."):
        r = requests.post(API_URL, json=payload)
        data = r.json()

    st.session_state.chat.append({
        "q": question,
        "a": data["bot_reply"],
        "time": datetime.now().strftime("%H:%M:%S")
    })

    st.session_state.question = ""
    st.rerun()

# -------- CHAT --------
for c in reversed(st.session_state.chat):
    st.markdown(f"**You:** {c['q']}")
    st.markdown(f"**AI:** {c['a']}")
    st.caption(c["time"])
    st.markdown("---")
