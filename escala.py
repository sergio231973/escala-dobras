import streamlit as st
from datetime import datetime

st.set_page_config(page_title="🎮 Escalas da Equipe", page_icon="🎮")

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

# =========================
# DOBRA
# =========================
with tab_dobra:
    fila = st.session_state.fila_dobra

    for i, nome in enumerate(fila, 1):
        if i == 1:
            st.markdown(f"👉👷 **{nome}** (PRÓXIMO)")
        else:
            st.markdown(f"{i}º → 👷 {nome}")

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

# =========================
# VIRADINHA
# =========================
with tab_viradinha:
    fila = st.session_state.fila_viradinha

    for i, nome in enumerate(fila, 1):
        if i == 1:
            st.markdown(f"👉🥇 **{nome}** (PRÓXIMO)")
        else:
            st.markdown(f"{i}º → 🥇 {nome}")

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

# =========================
# HISTÓRICO
# =========================
with tab_hist:
    st.subheader("📋 Dobras")
    for h in st.session_state.hist_dobra:
        st.write(f"{h['nome']} — {h['acao']} — {h['data']}")

    st.subheader("🥇 Viradinha Ouro")
    for h in st.session_state.hist_viradinha:
        st.write(f"{h['nome']} — {h['acao']} — {h['data']}")

# =========================
# ADMIN (SÓ VOCÊ)
# =========================
with tab_admin:
    senha = st.text_input("Senha do administrador", type="password")

    if senha == SENHA_ADMIN:
        st.success("Modo administrador ativado ✅")

        st.subheader("✏️ Editar datas da Viradinha")
st.divider()
st.subheader("✏️ Editar nomes da Dobra")

fila = st.session_state.fila_dobra

if fila:
    pessoa = st.selectbox(
        "Escolha o nome da dobra",
        fila,
        key="select_nome_dobra"
    )

    novo_nome = st.text_input(
        "Novo nome",
        value=pessoa,
        key="input_nome_dobra"
    )

    col_edit, col_del = st.columns(2)

    if col_edit.button("💾 Salvar nome", key="btn_salvar_nome_dobra"):
        idx = fila.index(pessoa)
        fila[idx] = novo_nome
        st.success("✅ Nome atualizado na dobra!")
        st.rerun()

    if col_del.button("❌ Remover da dobra", key="btn_remover_nome_dobra"):
        fila.remove(pessoa)
        st.success("✅ Nome removido da dobra!")
        st.rerun()
else:
    st.info("Nenhum nome na escala de dobra.")
    st.divider()
st.subheader("🥇 Editar nomes da Viradinha Ouro")

fila_v = st.session_state.fila_viradinha

if fila_v:
    pessoa_v = st.selectbox(
        "Escolha o nome da viradinha",
        fila_v,
        key="select_nome_viradinha"
    )

    novo_nome_v = st.text_input(
        "Novo nome",
        value=pessoa_v,
        key="input_nome_viradinha"
    )

    col_edit_v, col_del_v = st.columns(2)

    if col_edit_v.button("💾 Salvar nome", key="btn_salvar_nome_viradinha"):
        idx = fila_v.index(pessoa_v)
        fila_v[idx] = novo_nome_v
        st.success("✅ Nome atualizado na viradinha!")
        st.rerun()

    if col_del_v.button("❌ Remover da viradinha", key="btn_remover_nome_viradinha"):
        fila_v.remove(pessoa_v)
        st.success("✅ Nome removido da viradinha!")
        st.rerun()
else:
    st.info("Nenhum nome na viradinha ouro.")
        if st.session_state.hist_viradinha:
            op = st.selectbox(
                "Escolha o registro",
                range(len(st.session_state.hist_viradinha)),
                format_func=lambda i: f"{st.session_state.hist_viradinha[i]['nome']} - {st.session_state.hist_viradinha[i]['data']}"
            )

            nova_data = st.text_input(
                "Nova data",
                st.session_state.hist_viradinha[op]["data"]
            )

            if st.button("💾 Salvar nova data"):
                st.session_state.hist_viradinha[op]["data"] = nova_data
                st.success("Data alterada com sucesso!")
                st.rerun()
    else:
        st.info("Área restrita 🔒")
