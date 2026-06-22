import streamlit as st
from datetime import datetime

st.set_page_config(page_title="🎮 Escalas da Equipe", page_icon="🎮")

# =========================
# CONFIGURAÇÕES
# =========================
SENHA_ADMIN = "1234"  # altere se quiser

# =========================
# INICIALIZAÇÃO (SESSION STATE)
# =========================
if "fila_dobra" not in st.session_state:
    st.session_state.fila_dobra = [
        "Wilian", "Sergio", "Daniel", "Caio",
        "Washington", "Cardoso", "Digones", "Anderson"
    ]
    st.session_state.hist_dobra = []

if "fila_viradinha" not in st.session_state:
    st.session_state.fila_viradinha = [
        "Washington", "Digones", "Anderson", "Wilian",
        "Sergio", "Cardoso", "Daniel", "Caio"
    ]
    st.session_state.hist_viradinha = []

# =========================
# INTERFACE
# =========================
st.title("🎮 Escalas da Equipe")

tab_dobra, tab_viradinha, tab_hist, tab_admin = st.tabs(
    ["📋 Dobra", "🥇 Viradinha Ouro", "📜 Histórico", "🔐 Admin"]
)

# =====================================================
# 📋 DOBRA
# =====================================================
with tab_dobra:
    st.subheader("👷 Escala de Dobras")

    fila = st.session_state.fila_dobra

    for i, nome in enumerate(fila, 1):
        if i == 1:
            st.markdown(f"👉👷 **{nome}** (PRÓXIMO)")
        else:
            st.markdown(f"{i}º → 👷 {nome}")

    st.divider()

    col1, col2 = st.columns(2)

    if col1.button("✅ Aceitou dobra"):
        quem = fila.pop(0)
        fila.append(quem)
        st.session_state.hist_dobra.insert(0, {
            "nome": quem,
            "acao": "aceitou",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        st.rerun()

    if col2.button("❌ Recusou dobra"):
        quem = fila.pop(0)
        fila.append(quem)
        st.session_state.hist_dobra.insert(0, {
            "nome": quem,
            "acao": "recusou",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        st.rerun()

    st.divider()

    if st.button("🔄 Resetar escala de dobra"):
        ultimo_aceitou = None
        for h in st.session_state.hist_dobra:
            if h["acao"] == "aceitou":
                ultimo_aceitou = h["nome"]
                break

        if ultimo_aceitou and ultimo_aceitou in fila:
            idx = fila.index(ultimo_aceitou)
            st.session_state.fila_dobra = fila[idx+1:] + fila[:idx+1]
            st.success(f"Escala resetada a partir de {ultimo_aceitou}")
            st.rerun()
        else:
            st.warning("Nenhuma dobra aceita ainda.")

# =====================================================
# 🥇 VIRADINHA OURO
# =====================================================
with tab_viradinha:
    st.subheader("🥇 Viradinha Ouro")

    fila = st.session_state.fila_viradinha

    for i, nome in enumerate(fila, 1):
        if i == 1:
            st.markdown(f"👉🥇 **{nome}** (PRÓXIMO)")
        else:
            st.markdown(f"{i}º → 🥇 {nome}")

    st.divider()

    col1, col2 = st.columns(2)

    if col1.button("✅ Aceitou viradinha"):
        quem = fila.pop(0)
        fila.append(quem)
        st.session_state.hist_viradinha.insert(0, {
            "nome": quem,
            "acao": "aceitou",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        st.rerun()

    if col2.button("❌ Recusou viradinha"):
        quem = fila.pop(0)
        fila.append(quem)
        st.session_state.hist_viradinha.insert(0, {
            "nome": quem,
            "acao": "recusou",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        st.rerun()

# =====================================================
# 📜 HISTÓRICO
# =====================================================
with tab_hist:
    st.subheader("📋 Dobras")
    for h in st.session_state.hist_dobra:
        st.write(f"{h['nome']} — {h['acao']} — {h['data']}")

    st.subheader("🥇 Viradinha Ouro")
    for h in st.session_state.hist_viradinha:
        st.write(f"{h['nome']} — {h['acao']} — {h['data']}")

# =====================================================
# 🔐 ADMIN (SÓ VOCÊ)
# =====================================================
with tab_admin:
    senha = st.text_input("Senha do administrador", type="password")

    if senha == SENHA_ADMIN:
        st.success("Modo administrador ativado ✅")

        # ===== Editar datas da Viradinha =====
        st.subheader("📅 Editar datas da Viradinha")

        if st.session_state.hist_viradinha:
            idx = st.selectbox(
                "Escolha o registro",
                range(len(st.session_state.hist_viradinha)),
                format_func=lambda i: f"{st.session_state.hist_viradinha[i]['nome']} - {st.session_state.hist_viradinha[i]['data']}"
            )

            nova_data = st.text_input(
                "Nova data",
                st.session_state.hist_viradinha[idx]["data"]
            )

            if st.button("💾 Salvar data"):
                st.session_state.hist_viradinha[idx]["data"] = nova_data
                st.success("Data atualizada!")
                st.rerun()

        st.divider()

        # ===== Editar nomes =====
        st.subheader("✏️ Editar nomes")

        pessoa = st.selectbox(
            "Editar nome (Dobra)",
            st.session_state.fila_dobra
        )

        novo_nome = st.text_input("Novo nome", pessoa)

        if st.button("Salvar nome da dobra"):
            i = st.session_state.fila_dobra.index(pessoa)
            st.session_state.fila_dobra[i] = novo_nome
            st.success("Nome atualizado!")
            st.rerun()

        pessoa_v = st.selectbox(
            "Editar nome (Viradinha)",
            st.session_state.fila_viradinha
        )

        novo_nome_v = st.text_input("Novo nome viradinha", pessoa_v)

        if st.button("Salvar nome da viradinha"):
            i = st.session_state.fila_viradinha.index(pessoa_v)
            st.session_state.fila_viradinha[i] = novo_nome_v
            st.success("Nome atualizado!")
            st.rerun()

        st.divider()

        # ===== Reset total =====
        if st.button("🚨 RESET TOTAL (ADMIN)"):
            st.session_state.clear()
            st.success("Sistema resetado completamente.")
            st.rerun()

    else:
        st.info("Área restrita 🔒")
