import streamlit as st
from supabase import create_client
from datetime import datetime

# =========================
# CONFIG
# =========================
SUPABASE_URL = "https://rkrvmdqkmmlqzjrkwch.supabase.co"
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
    for f in fila:
        supabase.table(tabela).update({"ordem": f["ordem"] - 1}).eq("id", f["id"]).execute()
    supabase.table(tabela).update({"ordem": len(fila)}).eq("id", atual["id"]).execute()

def registrar_hist(tabela, nome, acao):
    supabase.table(tabela).insert({
        "nome": nome,
        "acao": acao,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }).execute()

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

    for i, f in enumerate(fila):
        if i == 0:
            st.markdown(f"👉👷 **{f['nome']}**")
            col1, col2 = st.columns(2)

            if col1.button("✅ Aceitar", key="dobra_aceitar"):
                mover_fila("fila_dobra", f)
                registrar_hist("hist_dobra", f["nome"], "aceitou")
                supabase.table("dobra_hoje").insert({"nome": f["nome"]}).execute()
                st.rerun()

            if col2.button("❌ Recusar", key="dobra_recusar"):
                mover_fila("fila_dobra", f)
                registrar_hist("hist_dobra", f["nome"], "recusou")
                st.rerun()
        else:
            st.write(f"{i+1}º → 👷 {f['nome']}")

    st.divider()
    st.subheader("📌 Ficaram na dobra de hoje")

    ficaram = supabase.table("dobra_hoje").select("*").execute().data
    if ficaram:
        for p in ficaram:
            st.write(f"👷 {p['nome']}")
    else:
        st.write("—")

    if st.button("🧹 Limpar lista da dobra de hoje"):
        supabase.table("dobra_hoje").delete().neq("id", 0).execute()
        st.rerun()

# =========================
# VIRADINHA OURO
# =========================
with tab_viradinha:
    fila = get_fila("fila_viradinha")

    st.subheader("Viradinha Ouro")

    for i, f in enumerate(fila):
        if i == 0:
            st.markdown(f"👉🥇 **{f['nome']}**")
            col1, col2 = st.columns(2)

            if col1.button("✅ Aceitar", key="vir_aceitar"):
                mover_fila("fila_viradinha", f)
                registrar_hist("hist_viradinha", f["nome"], "aceitou")
                st.rerun()

            if col2.button("❌ Recusar", key="vir_recusar"):
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

        if st.button("🚨 RESETAR HISTÓRICOS"):
            supabase.table("hist_dobra").delete().neq("id", 0).execute()
            supabase.table("hist_viradinha").delete().neq("id", 0).execute()
            supabase.table("dobra_hoje").delete().neq("id", 0).execute()
            st.success("Históricos limpos.")
            st.rerun()
    else:
        st.info("Área restrita 🔒")
