
mport streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Escala de Dobras", page_icon="📋")

ARQUIVO = "escala.json"
SENHA_ADMIN = "1234"  # 🔐 altere se quiser

# =========================
# CARREGAR / SALVAR
# =========================
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)

    return {
        "fila": [
            "Wilian", "Sergio", "Daniel", "Caio",
            "Washington", "Cardoso", "Digones", "Anderson"
        ],
        "historico": []
    }

def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados
fila = dados["fila"]

# =========================
# INTERFACE
# =========================
st.title("🎮 Escala de Dobras")

tab_escala, tab_historico, tab_admin = st.tabs(
    ["📋 Escala", "📜 Histórico", "🔐 Admin"]
)

# =========================
# ABA ESCALA
# =========================
with tab_escala:
    st.subheader("👷 Fila atual")

    for i, nome in enumerate(fila, 1):
        if i == 1:
            st.markdown(
                f"""
                <div style="font-size:18px">
                    <span style="font-size:40px">👉👷‍♂️</span>
                    <b>{nome}</b>
                    <span style="color:green">(PRÓXIMO)</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="font-size:18px">
                    {i}º →
                    <span style="font-size:30px">👷‍♂️</span>
                    {nome}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

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
            f"⚠️ Tem certeza que **{proximo}** vai **{acao.upper()}** a dobra?"
        )

        col_ok, col_cancel = st.columns(2)

        if col_ok.button("✔️ Confirmar"):
            quem = fila.pop(0)
            fila.append(quem)

            dados["historico"].insert(0, {
                "nome": quem,
                "acao": acao,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            salvar(dados)
            st.session_state.confirmacao = None
            st.rerun()

        if col_cancel.button("❌ Cancelar"):
            st.session_state.confirmacao = None
            st.rerun()

# =========================
# ABA HISTÓRICO
# =========================
with tab_historico:
    st.subheader("📜 Histórico completo")

    if not dados["historico"]:
        st.info("Nenhum registro ainda.")
    else:
        for h in dados["historico"]:
            emoji = "✅" if h["acao"] == "aceitou" else "❌"
            st.markdown(
                f"""
                <div style="font-size:16px">
                    <span style="font-size:28px">{emoji}</span>
                    <b>{h['nome']}</b> —
                    {h['data']}
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# ABA ADMIN
# =========================
with tab_admin:
    senha = st.text_input("Senha do administrador", type="password")

    if senha == SENHA_ADMIN:
        st.success("Modo administrador ativado ✅")

        if dados["historico"]:
            opcoes = [
                f"{i+1} - {h['nome']} ({h['data']})"
                for i, h in enumerate(dados["historico"])
            ]

            escolha = st.selectbox(
                "Escolha o registro para editar",
                opcoes
            )

            indice = opcoes.index(escolha)

            nova_data = st.text_input(
                "Nova data",
                value=dados["historico"][indice]["data"]
            )

            if st.button("💾 Salvar nova data"):
                dados["historico"][indice]["data"] = nova_data
                salvar(dados)
                st.success("Data atualizada com sucesso!")
                st.rerun()
    else:
        st.info("Área restrita 🔒")
