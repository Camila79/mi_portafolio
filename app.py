import streamlit as st
import yfinance as yf
import json
import os

PASSWORD = "miporta"
DATA_FILE = "portfolio.json"

st.set_page_config(page_title="Mi Portafolio", layout="wide")

password = st.text_input("Introduce la palabra clave:", type="password")

if password != PASSWORD:
    st.stop()

st.title("📊 Mi Portafolio en Tiempo Real")

# Cargar datos
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        portfolio = json.load(f)
else:
    portfolio = {}

st.subheader("➕ Añadir o Modificar Activo")

ticker = st.text_input("Ticker (ej: AAPL, MSFT, BTC-USD)").upper()
quantity = st.number_input("Cantidad", min_value=0.0, step=1.0)
buy_price = st.number_input("Precio de compra", min_value=0.0, step=0.01)

if st.button("Guardar"):
    portfolio[ticker] = {
        "quantity": quantity,
        "buy_price": buy_price
    }
    with open(DATA_FILE, "w") as f:
        json.dump(portfolio, f)
    st.success("Guardado correctamente")

st.subheader("➖ Eliminar Activo")

ticker_delete = st.text_input("Ticker a eliminar").upper()

if st.button("Eliminar"):
    if ticker_delete in portfolio:
        del portfolio[ticker_delete]
        with open(DATA_FILE, "w") as f:
            json.dump(portfolio, f)
        st.success("Eliminado correctamente")

st.subheader("📈 Portafolio Actual")

total_value = 0
total_gain = 0

for ticker, data in portfolio.items():
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]

        quantity = data["quantity"]
        buy_price = data["buy_price"]

        current_value = price * quantity
        invested = buy_price * quantity
        gain = current_value - invested
        percent = ((price / buy_price) - 1) * 100 if buy_price > 0 else 0

        total_value += current_value
        total_gain += gain

        st.write(f"""
        {ticker}
        | Cantidad: {quantity}
        | Precio actual: ${price:.2f}
        | Precio compra: ${buy_price:.2f}
        | Valor actual: ${current_value:.2f}
        | Ganancia/Pérdida: ${gain:.2f} ({percent:.2f}%)
        """)

    except:
        st.write(f"{ticker} | Error obteniendo precio")

st.markdown("---")
st.subheader(f"💰 Valor Total: ${total_value:.2f}")
st.subheader(f"📊 Ganancia/Pérdida Total: ${total_gain:.2f}")


