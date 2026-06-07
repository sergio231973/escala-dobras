import streamlit as st

import json

import os

 

st.set_page_config(page_title="Escala de Dobras", page_icon="📋")

 

ARQUIVO = "escala.json"

 

def carregar_escala():

    if os.path.exists(ARQUIVO):

        with open(ARQUIVO, "r") as f:

            return json.load(f)

    return [

        "CAIO", "WASHINGTON", "CARDOSO", "DIGONES",

        "ANDERSON", "WILIAN", "SERGIO", "DANIEL", 

    ]

 

def salvar_escala(lista):

    with open(ARQUIVO, "w") as f:

        json.dump(lista, f)

 

if "colaboradores" not in st.session_state:

    st.session_state.colaboradores = carregar_escala()

 

colaboradores = st.session_state.colaboradores

 

st.title("📋 Escala de Dobras")

 

for i, nome in enumerate(colaboradores, 1):

    if i == 1:

        st.success(f"👉 PRÓXIMO: {nome}")

    else:

        st.write(f"{i}º lugar: {nome}")

 

col1, col2 = st.columns(2)

 

if col1.button("✅ Aceitou"):

    quem = colaboradores.pop(0)

    colaboradores.append(quem)

    salvar_escala(colaboradores)

    st.rerun()

 

if col2.button("❌ Recusou"):

    quem = colaboradores.pop(0)

    colaboradores.append(quem)

    salvar_escala(colaboradores)

    st.rerun()