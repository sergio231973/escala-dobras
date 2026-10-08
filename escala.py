import streamlit as st
from supabase import create_client
from datetime import datetime

# =========================
# CONFIG
# =========================
SUPABASE_URL = "https://rkrvvmdqkmmlqzjrkwch.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJrcnZ2bWRxa21tbHF6anJrd2NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1MDYxMjUsImV4cCI6MjA5ODA4MjEyNX0.7CjM3FYaW-bPfXnjeF8raJdNymBSNEZYfQwYCvYSklY"
SENHA_ADMIN = "1234"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
st.set_page_config(page_title="🎮 Escalas da Equipe", page_icon="🎮")

# =========================
# FUNÇÕES
# =========================
def get_fila(tabela):
    return supabase.table(tabela).select("*").order("ordem").execute().data

def mover_fila(tabela, atual):
    fila = get_fila(tabela)

    # Remove o atual da lista
    fila_sem_atual = [
        f for f in fila
        if f["id"] != atual["id"]
    ]

    # Reorganiza a fila
    for i, f in enumerate(fila_sem_atual, start=1):
        supabase.table(tabela).update({
            "ordem": i
        }).eq("id", f["id"]).execute()

    # Coloca o atual no final
    supabase.table(tabela).update({
        "ordem": len(fila)
    }).eq("id", atual["id"]).execute()

def registrar_hist(tabela, nome, acao):
    supabase.table(tabela).insert({
        "nome": nome,
        "acao": acao,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }).execute()


def adicionar_colaborador(tabela, nome):
    fila = get_fila(tabela)

    ultima_ordem = len(fila) + 1

    supabase.table(tabela).insert({
        "nome": nome,
        "ordem": ultima_ordem
    }).execute()


def remover_colaborador(tabela, nome):

    supabase.table(tabela).delete().eq("nome", nome).execute()

    fila = get_fila(tabela)

    for i, f in enumerate(fila, start=1):
        supabase.table(tabela).update({
            "ordem": i
        }).eq("id", f["id"]).execute()

    return True

def obter_ultima_movimentacao():

    ultima_dobra = supabase.table(
        "hist_dobra"
    ).select("*").order("id", desc=True).limit(1).execute().data

    ultima_vir = supabase.table(
        "hist_viradinha"
    ).select("*").order("id", desc=True).limit(1).execute().data

    registros = []

    if ultima_dobra:
        ultimo = ultima_dobra[0]
        ultimo["tipo"] = "📋 Dobra"
        registros.append(ultimo)

    if ultima_vir:
        ultimo = ultima_vir[0]
        ultimo["tipo"] = "🏆 Viradinha Ouro"
        registros.append(ultimo)

    if not registros:
        return None

    registros.sort(
        key=lambda x: x["data"],
        reverse=True
    )

    return registros[0]
        
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
    fila = get_fila("fila_dobra")

    st.subheader("Fila da Dobra")

    st.success(f"🎯 Operador da Vez: {fila[0]['nome']}")

    for i, f in enumerate(fila):
        if i == 0:
            st.markdown(f"👉👷 **{f['nome']}**")

            col1, col2 = st.columns(2)

            if col1.button("✅ Aceitar", key="dobra_aceitar"):
                mover_fila("fila_dobra", f)
                registrar_hist("hist_dobra", f["nome"], "aceitou")
                supabase.table("dobra_hoje").insert(
                    {"nome": f["nome"]}
                ).execute()
                st.rerun()

            if col2.button("❌ Recusar", key="dobra_recusar"):
                mover_fila("fila_dobra", f)
                registrar_hist("hist_dobra", f["nome"], "recusou")
                st.rerun()

        else:
            st.write(f"{i+1}º → 👷 {f['nome']}")

    st.divider()

    ultima = obter_ultima_movimentacao()

    st.subheader("📋 Última Dobra Registrada")

    if ultima:
        st.write(f"👷 Operador: {ultima['nome']}")
        st.write(f"📋 Evento: {ultima['tipo']}")
        st.write(f"🕒 Data/Hora: {ultima['data']}")
    
    else:
        st.write("Nenhuma movimentação registrada.")

# =========================
# VIRADINHA OURO
# =========================
with tab_viradinha:
    fila = get_fila("fila_viradinha")

    st.subheader("Viradinha Ouro")

    st.success(
        f"🏆 Operador da Viradinha: {fila[0]['nome']}"
    )
    for i, f in enumerate(fila):
        if i == 0:
            st.markdown(f"👉🥇 **{f['nome']}**")
            col1, col2 = st.columns(2)

            if col1.button("✅ Aceitar", key="vir_aceitar"):
                import time

                with st.spinner(f"👷 {f['nome']} caminhando para a dobra..."):
                    time.sleep(2)

                mover_fila("fila_viradinha", f)
                registrar_hist("hist_viradinha", f["nome"], "aceitou")
                st.rerun()

            if col2.button("❌ Recusar", key="vir_recusar"):
                import time

                with st.spinner(f"👷 {f['nome']} indo para o final da fila..."):
                    time.sleep(2)

                mover_fila("fila_viradinha", f)
                registrar_hist("hist_viradinha", f["nome"], "recusou")
                st.rerun()

        else:
            st.write(f"{i+1}º → 🥇 {f['nome']}")
            
# =========================
# HISTÓRICO
# =========================
with tab_hist:
    st.subheader("📋 Dobras")
    for h in supabase.table("hist_dobra").select("*").order("id", desc=True).execute().data:
        st.write(f"{h['nome']} — {h['acao']} — {h['data']}")

    st.subheader("🥇 Viradinha Ouro")
    for h in supabase.table("hist_viradinha").select("*").order("id", desc=True).execute().data:
        st.write(f"{h['nome']} — {h['acao']} — {h['data']}")

# =========================
# ADMIN
# =========================
with tab_admin:
    senha = st.text_input("Senha do administrador", type="password")

    if senha == SENHA_ADMIN:
        st.success("Modo administrador ativado ✅")

        st.subheader("👥 Gerenciar Colaboradores")

        tabela_escolhida = st.selectbox(
            "Escala",
            ["fila_dobra", "fila_viradinha"]
        )

        novo_nome = st.text_input("Nome do colaborador")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("➕ Adicionar Colaborador"):
                if novo_nome:
                    adicionar_colaborador(
                        tabela_escolhida,
                        novo_nome
                    )
                    st.success(f"{novo_nome} adicionado ao fim da fila.")
                    st.rerun()

        with col2:
            if st.button("➖ Remover Colaborador"):
                if novo_nome:
                    remover_colaborador(
                        tabela_escolhida,
                        novo_nome
                    )
                    st.success(f"{novo_nome} removido.")
                    st.rerun()

        st.divider()

        if st.button("🚨 RESETAR HISTÓRICOS"):
            supabase.table("hist_dobra").delete().neq("id", 0).execute()
            supabase.table("hist_viradinha").delete().neq("id", 0).execute()
            supabase.table("dobra_hoje").delete().neq("id", 0).execute()
            st.success("Históricos limpos.")
            st.rerun()

    else:
        st.info("Área restrita 🔒")
