import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="🎮 Escalas da Equipe", page_icon="🎮")

DB = "escala.db"
SENHA_ADMIN = "1234"

# =====================================================
# BANCO DE DADOS
# =====================================================
def conectar():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS fila_dobra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS hist_dobra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        acao TEXT,
        data TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS fila_viradinha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS hist_viradinha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        acao TEXT,
        data TEXT
    )""")

    conn.commit()

    # Popular com nomes iniciais (se vazio)
    if c.execute("SELECT COUNT(*) FROM fila_dobra").fetchone()[0] == 0:
        nomes = [
            "Wilian", "Sergio", "Daniel", "Caio",
            "Washington", "Cardoso", "Digones", "Anderson"
        ]
        c.executemany("INSERT INTO fila_dobra (nome) VALUES (?)", [(n,) for n in nomes])

    if c.execute("SELECT COUNT(*) FROM fila_viradinha").fetchone()[0] == 0:
        nomes = [
            "Washington", "Digones", "Anderson", "Wilian",
            "Sergio", "Cardoso", "Daniel", "Caio"
        ]
        c.executemany("INSERT INTO fila_viradinha (nome) VALUES (?)", [(n,) for n in nomes])

    conn.commit()
    conn.close()

def listar(tabela):
    conn = conectar()
    c = conn.cursor()
    dados = c.execute(f"SELECT nome FROM {tabela}").fetchall()
    conn.close()
    return [d[0] for d in dados]

def mover_fila(tabela, nome):
    conn = conectar()
    c = conn.cursor()
    c.execute(f"DELETE FROM {tabela} WHERE nome=?", (nome,))
    c.execute(f"INSERT INTO {tabela} (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def inserir_hist(tabela, nome, acao):
    conn = conectar()
    c = conn.cursor()
    c.execute(
        f"INSERT INTO {tabela} (nome, acao, data) VALUES (?,?,?)",
        (nome, acao, datetime.now().strftime("%d/%m/%Y %H:%M"))
    )
    conn.commit()
    conn.close()

def listar_hist(tabela):
    conn = conectar()
    c = conn.cursor()
    dados = c.execute(
        f"SELECT id, nome, acao, data FROM {tabela} ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return dados

def atualizar_data(tabela, id_reg, nova_data):
    conn = conectar()
    c = conn.cursor()
    c.execute(f"UPDATE {tabela} SET data=? WHERE id=?", (nova_data, id_reg))
    conn.commit()
    conn.close()

def resetar_tudo():
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM fila_dobra")
    c.execute("DELETE FROM hist_dobra")
    c.execute("DELETE FROM fila_viradinha")
    c.execute("DELETE FROM hist_viradinha")
    conn.commit()
    conn.close()
    init_db()

# =====================================================
# INICIALIZAÇÃO
# =====================================================
init_db()

# =====================================================
# INTERFACE
# =====================================================
st.title("🎮 Escalas da Equipe")

tab_dobra, tab_viradinha, tab_hist, tab_admin = st.tabs(
    ["📋 Dobra", "🥇 Viradinha Ouro", "📜 Histórico", "🔐 Admin"]
)

# =====================================================
# DOBRA
# =====================================================
with tab_dobra:
    fila = listar("fila_dobra")

    for i, nome in enumerate(fila, 1):
        st.write(f"{'👉👷' if i==1 else f'{i}º → 👷'} {nome}")

    col1, col2 = st.columns(2)

    if col1.button("✅ Aceitou dobra"):
        nome = fila[0]
        mover_fila("fila_dobra", nome)
        inserir_hist("hist_dobra", nome, "aceitou")
        st.rerun()

    if col2.button("❌ Recusou dobra"):
        nome = fila[0]
        mover_fila("fila_dobra", nome)
        inserir_hist("hist_dobra", nome, "recusou")
        st.rerun()

# =====================================================
# VIRADINHA
# =====================================================
with tab_viradinha:
    fila = listar("fila_viradinha")

    for i, nome in enumerate(fila, 1):
        st.write(f"{'👉🥇' if i==1 else f'{i}º → 🥇'} {nome}")

    col1, col2 = st.columns(2)

    if col1.button("✅ Aceitou viradinha"):
        nome = fila[0]
        mover_fila("fila_viradinha", nome)
        inserir_hist("hist_viradinha", nome, "aceitou")
        st.rerun()

    if col2.button("❌ Recusou viradinha"):
        nome = fila[0]
        mover_fila("fila_viradinha", nome)
        inserir_hist("hist_viradinha", nome, "recusou")
        st.rerun()

# =====================================================
# HISTÓRICO
# =====================================================
with tab_hist:
    st.subheader("📋 Dobras")
    for _, nome, acao, data in listar_hist("hist_dobra"):
        st.write(f"{nome} — {acao} — {data}")

    st.subheader("🥇 Viradinha Ouro")
    for _, nome, acao, data in listar_hist("hist_viradinha"):
        st.write(f"{nome} — {acao} — {data}")

# =====================================================
# ADMIN
# =====================================================
with tab_admin:
    senha = st.text_input("Senha do administrador", type="password")

    if senha == SENHA_ADMIN:
        st.success("Modo administrador ativado ✅")

        st.subheader("📅 Editar datas das Dobras")
        hist = listar_hist("hist_dobra")

        if hist:
            op = st.selectbox(
                "Registro da dobra",
                hist,
                format_func=lambda x: f"{x[1]} - {x[3]} ({x[2]})"
            )
            nova_data = st.text_input("Nova data", op[3])
            if st.button("Salvar data da dobra"):
                atualizar_data("hist_dobra", op[0], nova_data)
                st.success("Data atualizada!")
                st.rerun()

        st.subheader("📅 Editar datas da Viradinha")
        histv = listar_hist("hist_viradinha")

        if histv:
            opv = st.selectbox(
                "Registro da viradinha",
                histv,
                format_func=lambda x: f"{x[1]} - {x[3]} ({x[2]})"
            )
            nova_data_v = st.text_input("Nova data", opv[3])
            if st.button("Salvar data da viradinha"):
                atualizar_data("hist_viradinha", opv[0], nova_data_v)
                st.success("Data atualizada!")
                st.rerun()

        st.divider()
        if st.button("🚨 RESET TOTAL (ADMIN)"):
            resetar_tudo()
            st.success("Sistema resetado!")
            st.rerun()
    else:
        st.info("Área restrita 🔒")

