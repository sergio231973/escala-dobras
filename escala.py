import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Escala de Dobras", page_icon="📋")

ARQUIVO = "escala.json"
SENHA_ADMIN = "1234"

# =========================
# CARREGAR / SALVAR
# =========================
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Garantir estrutura da Viradinha Ouro
        dados.setdefault("viradinha_fila", [
            "Sergio", "Cardoso", "Daniel", "Caio"
            "Washington", "Digones", "Anderson", "Wilian",
        ])
        dados.setdefault("viradinha_historico", [])
        # Garantir chaves novas
        dados.setdefault("viradinha_fila", [
            "Washington", "Digones", "Anderson", "Wilian",
            "Sergio", "Cardoso", "Daniel", "Caio"
        ])
        dados.setdefault("viradinha_historico", [])
        return dados

    return {
        "fila": [
            "Wilian", "Sergio", "Daniel", "Caio",
            "Washington", "Cardoso", "Digones", "Anderson"
        ],
        "historico": [],
        "viradinha_fila": [
            "Washington", "Digones", "Anderson", "Wilian",
            "Sergio", "Cardoso", "Daniel", "Caio"
        ],
        "viradinha_historico": []
    }

def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados

# =========================
# INTERFACE
# =========================
st.title("🎮 Escalas da Equipe")

tab_escala, tab_viradinha, tab_historico, tab_admin = st.tabs(
    ["📋 Dobra", "🥇 Viradinha Ouro", "📜 Histórico", "🔐 Admin"]
)

# =========================
# ABA DOBRA (IGUAL À ETAPA 1)
# =========================
with tab_escala:
    st.subheader("👷 Escala de Dobras")

    fila = dados["fila"]

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

    if "conf_dobra" not in st.session_state:
        st.session_state.conf_dobra = None

    col1, col2 = st.columns(2)

    if col1.button("✅ Aceitou dobra"):
        st.session_state.conf_dobra = "aceitou"

    if col2.button("❌ Recusou dobra"):
        st.session_state.conf_dobra = "recusou"

    st.divider()

    if st.button("🔄 Resetar escala de dobra"):
        # Procurar último que aceitou
        ultimo_aceitou = None
        for h in dados["historico"]:
            if h["acao"] == "aceitou":
                ultimo_aceitou = h["nome"]
                break

        if not ultimo_aceitou:
            st.warning("Nenhuma dobra aceita ainda. Reset não aplicado.")
        else:
            if ultimo_aceitou in fila:
                idx = fila.index(ultimo_aceitou)
                dados["fila"] = fila[idx+1:] + fila[:idx+1]
                salvar(dados)
                st.success(
                    f"Escala resetada a partir do último que aceitou: {ultimo_aceitou}"
                )
                st.rerun()
    if st.session_state.conf_dobra:
        acao = st.session_state.conf_dobra
        proximo = fila[0]

        st.warning(f"Confirmar que **{proximo}** {acao} a dobra?")

        ok, cancel = st.columns(2)

        if ok.button("✔️ Confirmar"):
            quem = fila.pop(0)
            fila.append(quem)

            dados["historico"].insert(0, {
                "nome": quem,
                "acao": acao,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            salvar(dados)
            st.session_state.conf_dobra = None
            st.rerun()

        if cancel.button("❌ Cancelar"):
            st.session_state.conf_dobra = None
            st.rerun()

# =========================
# ABA VIRADINHA OURO
# =========================
with tab_viradinha:
    st.subheader("🥇 Viradinha Ouro")

    fila_v = dados["viradinha_fila"]

    for i, nome in enumerate(fila_v, 1):
        if i == 1:
            st.markdown(
                f"""
                <div style="font-size:18px">
                    <span style="font-size:40px">👉🥇</span>
                    <b>{nome}</b>
                    <span style="color:gold">(PRÓXIMO)</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="font-size:18px">
                    {i}º →
                    <span style="font-size:30px">🥇</span>
                    {nome}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    if "conf_viradinha" not in st.session_state:
        st.session_state.conf_viradinha = None

    colv1, colv2 = st.columns(2)

    if colv1.button("✅ Aceitou viradinha"):
        st.session_state.conf_viradinha = "aceitou"

    if colv2.button("❌ Recusou viradinha"):
        st.session_state.conf_viradinha = "recusou"

    if st.session_state.conf_viradinha:
        acao = st.session_state.conf_viradinha
        proximo = fila_v[0]

        st.warning(f"Confirmar que **{proximo}** {acao} a viradinha?")

        ok, cancel = st.columns(2)

        if ok.button("✔️ Confirmar"):
            quem = fila_v.pop(0)
            fila_v.append(quem)

            dados["viradinha_historico"].insert(0, {
                "nome": quem,
                "acao": acao,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            salvar(dados)
            st.session_state.conf_viradinha = None
            st.rerun()

        if cancel.button("❌ Cancelar"):
            st.session_state.conf_viradinha = None
            st.rerun()

# =========================
# ABA HISTÓRICO (AMBOS)
# =========================
with tab_historico:
    st.subheader("📜 Histórico Dobras")

    for h in dados["historico"]:
        emoji = "✅" if h["acao"] == "aceitou" else "❌"
        st.markdown(
            f"<span style='font-size:26px'>{emoji}</span> "
            f"<b>{h['nome']}</b> — {h['data']}",
            unsafe_allow_html=True
        )

    st.divider()
    st.subheader("📜 Histórico Viradinha Ouro")

    for h in dados["viradinha_historico"]:
        emoji = "✅" if h["acao"] == "aceitou" else "❌"
        st.markdown(
            f"<span style='font-size:26px'>{emoji}</span> "
            f"<b>{h['nome']}</b> — {h['data']}",
            unsafe_allow_html=True
        )

# =========================
# ABA ADMIN (MANTIDA)
# =========================
st.divider()
st.subheader("🥇 Editar datas da Viradinha Ouro")

if dados["viradinha_historico"]:
    opcoes_v = [
        f"{i+1} - {h['nome']} ({h['data']})"
        for i, h in enumerate(dados["viradinha_historico"])
    ]

    escolha_v = st.selectbox(
        "Escolha o registro da viradinha",
        opcoes_v,
        key="select_viradinha"
    )

    indice_v = opcoes_v.index(escolha_v)

    nova_data_v = st.text_input(
        "Nova data da viradinha",
        value=dados["viradinha_historico"][indice_v]["data"],
        key="input_data_viradinha"
    )

    if st.button("💾 Salvar data da viradinha", key="btn_salvar_viradinha"):
        dados["viradinha_historico"][indice_v]["data"] = nova_data_v
        salvar(dados)
        st.success("✅ Data da viradinha atualizada!")
        st.rerun()
else:
    st.info("Nenhum histórico de viradinha ainda.")
