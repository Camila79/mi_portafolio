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

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        portfolio = json.load(f)
else:
    portfolio = {}

st.subheader("➕ Añadir o Modificar Activo")

ticker = st.text_input("Ticker (ej: AAPL, MSFT, BTC-USD)").upper()
quantity = st.number_input("Cantidad", min_value=0.0, step=1.0)

if st.button("Guardar"):
    portfolio[ticker] = quantity
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

for ticker, quantity in portfolio.items():
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        value = price * quantity
        total_value += value
        st.write(f"{ticker} | Cantidad: {quantity} | Precio: ${price:.2f} | Valor: ${value:.2f}")
    except:
        st.write(f"{ticker} | Error obteniendo precio")

st.markdown("---")
st.subheader(f"💰 Valor Total: ${total_value:.2f}")


