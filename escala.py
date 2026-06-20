
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Escala de Dobras", page_icon="📋")

ARQUIVO = "escala.json"

# -------------------------
# CARREGAR / SALVAR DADOS
# -------------------------
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)

    return {
        "fila": [
            "Wilian", "Sergio", "Daniel", "Caio",
            "Washington", "Cardoso", "Digones", "Anderson"
        ],
        "historico": [],
        "ultimo_evento": None
    }

def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

# -------------------------
# INICIALIZAÇÃO
# -------------------------
if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados
fila = dados["fila"]

# -------------------------
# INTERFACE
# -------------------------
st.title("🎮 Escala de Dobras")

tabs = st.tabs(["📋 Escala", "📜 Histórico"])

# ======================================================
# ABA 1 - ESCALA
# ======================================================
with tabs[0]:
    st.subheader("👷 Fila atual")

    for i, nome in enumerate(fila, 1):
        if i == 1:
            st.success(f"👉 PRÓXIMO DA DOBRA: 👷 {nome}")
        else:
            st.write(f"{i}º → 👷 {nome}")

    st.divider()

    # CONFIRMAÇÃO
    if "confirmacao" not in st.session_state:
        st.session_state.confirmacao = None

    col1, col2 = st.columns(2)

    if col1.button("✅ Aceitar dobra"):
        st.session_state.confirmacao = "aceitou"

    if col2.button("❌ Recusar dobra"):
        st.session_state.confirmacao = "recusou"

    if st.session_state.confirmacao:
        acao = st.session_state.confirmacao
        proximo = fila[0]

        st.warning(
            f"⚠️ Tem certeza que **{proximo}** "
            f"vai **{acao.upper()}** a dobra?"
        )

        col_ok, col_cancel = st.columns(2)

        if col_ok.button("✔️ Confirmar"):
            quem = fila.pop(0)
            fila.append(quem)

            evento = {
                "nome": quem,
                "acao": acao,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }

            dados["historico"].insert(0, evento)
            dados["ultimo_evento"] = evento

            salvar(dados)

            st.session_state.confirmacao = None
            st.rerun()

        if col_cancel.button("❌ Cancelar"):
            st.session_state.confirmacao = None
            st.rerun()

# ======================================================
# ABA 2 - HISTÓRICO
# ======================================================
with tabs[1]:
    st.subheader("📜 Histórico completo")

    if not dados["historico"]:
        st.info("Ainda não há registros.")
    else:
        for h in dados["historico"]:
            emoji = "✅" if h["acao"] == "aceitou" else "❌"
            st.write(
                f"{emoji} **{h['nome']}** "
                f"{h['acao']} — 📅 {h['data']}"
            )
