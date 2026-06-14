import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Escala de Dobras", page_icon="📋")

ARQUIVO = "escala.json"

# CARREGAR DADOS
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {
        "fila": [
            "Wilian", "Sergio", "Daniel", "Caio",
            "Washington", "Cardoso", "Digones", "Anderson"
        ],
        "ultimo_aceitou": "",
        "data_aceitou": "",
        "ultimo_recusou": "",
        "data_recusou": ""
    }

# SALVAR
def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

# INICIALIZAR
if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados
fila = dados["fila"]

# TÍTULO
st.title("🎮 Escala de Dobras")

st.write("")

# MOSTRAR FILA
st.markdown("### 👷 Fila de colaboradores")

for i, nome in enumerate(fila, 1):
    if i == 1:
        st.success(f"👉 👷 {nome} (PRÓXIMO)")
    else:
        st.write(f"{i}º → 👷 {nome}")

st.write("")

# BOTÕES
col1, col2 = st.columns(2)

# ACEITOU
if col1.button("✅ Aceitou 👍"):
    quem = fila.pop(0)
    fila.append(quem)

    dados["ultimo_aceitou"] = quem
    dados["data_aceitou"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    salvar(dados)
    st.success(f"👷 {quem} aceitou 👍 e foi pro final!")
    st.balloons()
    st.rerun()

# RECUSOU
if col2.button("❌ Recusou 🏍️"):
    quem = fila.pop(0)
    fila.append(quem)

    dados["ultimo_recusou"] = quem
    dados["data_recusou"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    salvar(dados)
    st.warning(f"👷 {quem} recusou 🏍️ e foi embora!")
    st.rerun()

st.write("")
st.markdown("---")

# HISTÓRICO
st.markdown("### 📊 Histórico recente")

col3, col4 = st.columns(2)

with col3:
    st.info(f"✅ Último que aceitou:\n\n👷 {dados['ultimo_aceitou']}\n📅 {dados['data_aceitou']}")

with col4:
    st.error(f"❌ Último que recusou:\n\n👷 {dados['ultimo_recusou']}\n📅 {dados['data_recusou']}")

# RESET
st.write("")
if st.button("🔄 Resetar escala"):
    dados["fila"] = [
        "Wilian", "Sergio", "Daniel", "Caio",
        "Washington", "Cardoso", "Digones", "Anderson"
    ]
    salvar(dados)
    st.rerun()
