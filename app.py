import streamlit as st
import pandas as pd

st.set_page_config(page_title="BSJP AI Screener", layout="wide")

st.markdown("""
<style>
.stApp {
    background: #020617;
    color: white;
}

.title {
    font-size: 34px;
    font-weight: 900;
    color: white;
}

.subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}

thead th {
    background: #111827;
    color: #f8fafc;
    padding: 10px;
    border: 1px solid #334155;
    text-align: center;
}

tbody td {
    padding: 9px;
    border: 1px solid #1e293b;
    text-align: center;
    font-weight: 700;
}

.kode { background: #1e40af; color: white; font-weight: 900; }
.green { background: #064e3b; color: #22c55e; }
.red { background: #7f1d1d; color: #fecaca; }
.yellow { background: #713f12; color: #fde68a; }
.purple { background: #581c87; color: #f0abfc; }
.blue { background: #1e3a8a; color: #93c5fd; }
.orange { background: #7c2d12; color: #fdba74; }
.dark { background: #0f172a; color: #e5e7eb; }
</style>
""", unsafe_allow_html=True)


def bsjp_logic(now, entry_low=138, entry_high=141, s1=136, r1=145, sl=134, rsi=46):
    if now > r1 and rsi >= 50:
        return {
            "FASE": "AKUM",
            "SETUP": "BREAKOUT",
            "AKSI": "ON TRACK",
            "DAY": "Breakout, volume wajib besar",
            "SINYAL": "📈 ON TRACK - BREAKOUT 145",
            "AI SCORE": 72,
            "STATUS BANDAR": "AKUMULASI",
            "RISK LEVEL": "MEDIUM",
            "MOMENTUM": "KUAT"
        }

    elif now < s1:
        return {
            "FASE": "LEMAH",
            "SETUP": "BREAKDOWN",
            "AKSI": "EXIT",
            "DAY": "Turun, gagal tahan support",
            "SINYAL": "💀 BREAKDOWN - JAGA SL",
            "AI SCORE": 35,
            "STATUS BANDAR": "DISTRIBUSI",
            "RISK LEVEL": "HIGH",
            "MOMENTUM": "LEMAH"
        }

    elif entry_low <= now <= entry_high:
        return {
            "FASE": "PART",
            "SETUP": "REBOUND20",
            "AKSI": "WAIT",
            "DAY": "Konsolidasi area entry",
            "SINYAL": "⚠️ WAIT - PANTAU VOLUME",
            "AI SCORE": 58,
            "STATUS BANDAR": "NETRAL",
            "RISK LEVEL": "MEDIUM",
            "MOMENTUM": "LEMAH"
        }

    elif now > entry_high and now < r1:
        return {
            "FASE": "PART",
            "SETUP": "REBOUND20",
            "AKSI": "HOLD TRAIL",
            "DAY": "Naik tipis menuju resistance",
            "SINYAL": "✔️ HOLD - BELUM BREAKOUT",
            "AI SCORE": 64,
            "STATUS BANDAR": "NETRAL",
            "RISK LEVEL": "MEDIUM",
            "MOMENTUM": "SEDANG"
        }

    else:
        return {
            "FASE": "PART",
            "SETUP": "WAIT",
            "AKSI": "WAIT",
            "DAY": "Belum ada sinyal kuat",
            "SINYAL": "⚠️ WAIT",
            "AI SCORE": 50,
            "STATUS BANDAR": "NETRAL",
            "RISK LEVEL": "MEDIUM",
            "MOMENTUM": "LEMAH"
        }


now_bsjp = 141
entry_bsjp = 138
s1_bsjp = 136
r1_bsjp = 145
sl_bsjp = 134
rsi_bsjp = 46
value_bsjp = "Pantau > rata-rata"

logic = bsjp_logic(
    now=now_bsjp,
    entry_low=138,
    entry_high=141,
    s1=s1_bsjp,
    r1=r1_bsjp,
    sl=sl_bsjp,
    rsi=rsi_bsjp
)

gain_bsjp = ((now_bsjp - entry_bsjp) / entry_bsjp) * 100

data = [[
    "BSJP",
    logic["FASE"],
    logic["SETUP"],
    logic["AKSI"],
    f"{gain_bsjp:.2f}%",
    logic["DAY"],
    entry_bsjp,
    now_bsjp,
    "145/150/158",
    sl_bsjp,
    f"{gain_bsjp:.2f}%",
    rsi_bsjp,
    logic["SINYAL"],
    s1_bsjp,
    r1_bsjp,
    value_bsjp,
    logic["AI SCORE"],
    logic["STATUS BANDAR"],
    logic["RISK LEVEL"],
    logic["MOMENTUM"]
]]

columns = [
    "EMITEN", "FASE", "SETUP", "AKSI", "GAIN", "DAY", "ENTRY", "NOW",
    "TP1/TP2/TP3", "TRAIL SL", "PROFIT%", "RSI", "SINYAL",
    "S1", "R1", "VALUE", "AI SCORE", "STATUS BANDAR", "RISK LEVEL", "MOMENTUM"
]

df = pd.DataFrame(data, columns=columns)


def cell_class(col, value):
    if col == "EMITEN":
        return "kode"

    if col in ["GAIN", "PROFIT%"]:
        return "green" if "-" not in str(value) else "red"

    if col == "RSI":
        if value > 70:
            return "yellow"
        elif value < 40:
            return "blue"
        return "green"

    if col in ["AKSI", "SINYAL"]:
        text = str(value)
        if "BREAKDOWN" in text or "DEAD" in text or "EXIT" in text:
            return "red"
        if "GOLDEN" in text:
            return "purple"
        if "ON TRACK" in text:
            return "blue"
        if "WAIT" in text:
            return "yellow"
        return "green"

    if col == "DAY":
        text = str(value).lower()
        if "turun" in text:
            return "red"
        if "naik" in text or "breakout" in text:
            return "green"
        if "konsolidasi" in text:
            return "yellow"
        return "dark"

    if col == "STATUS BANDAR":
        if value == "AKUMULASI":
            return "green"
        if value == "DISTRIBUSI":
            return "orange"
        return "yellow"

    if col == "RISK LEVEL":
        if value == "HIGH":
            return "red"
        if value == "MEDIUM":
            return "yellow"
        return "green"

    if col == "MOMENTUM":
        if value == "KUAT":
            return "green"
        if value == "SEDANG":
            return "yellow"
        return "red"

    if col == "AI SCORE":
        if value >= 70:
            return "green"
        elif value >= 50:
            return "yellow"
        return "red"

    if col == "SETUP":
        if "BREAKOUT" in str(value):
            return "green"
        if "BREAKDOWN" in str(value):
            return "red"
        if "GC" in str(value):
            return "purple"
        if "WAIT" in str(value):
            return "yellow"
        return "dark"

    return "dark"


html = "<table><thead><tr>"
for col in df.columns:
    html += f"<th>{col}</th>"
html += "</tr></thead><tbody>"

for _, row in df.iterrows():
    html += "<tr>"
    for col in df.columns:
        cls = cell_class(col, row[col])
        html += f"<td class='{cls}'>{row[col]}</td>"
    html += "</tr>"

html += "</tbody></table>"

st.markdown('<div class="title">📊 BSJP AI Stock Screener</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dashboard dark mode untuk scalping & swing trading cepat</div>', unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)
