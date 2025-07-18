# app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Carregar artefatos do modelo
model = joblib.load("modelo_final/random_forest_model.pkl")
scaler = joblib.load("modelo_final/standard_scaler.pkl")
label_encoders = joblib.load("modelo_final/label_encoders.pkl")

# Config do app
st.set_page_config(page_title="Preditor de Obesidade", layout="centered")
st.title("🩺 Sistema Preditivo de Obesidade")
st.markdown("Preencha os dados abaixo para obter uma análise preditiva do nível de obesidade:")

# ------------------------------
# Formulário para entrada de dados
# ------------------------------
with st.form("formulario_paciente"):
    genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    idade = st.number_input("Idade", min_value=1, max_value=100, value=25)
    altura = st.number_input("Altura (em metros)", min_value=1.0, max_value=2.5, value=1.70)
    peso = st.number_input("Peso (em kg)", min_value=30.0, max_value=200.0, value=70.0)
    historico_familiar = st.selectbox("Algum familiar tem histórico de sobrepeso?", ["Sim", "Não"])
    favc = st.selectbox("Costuma consumir alimentos calóricos com frequência?", ["Sim", "Não"])
    fcvc = st.slider("Frequência de consumo de vegetais, onde 0 = nunca e 3 = sempre", 0.0, 3.0, 2.0)
    ncp = st.slider("Número de refeições principais por dia", 1, 4, 3, step=1)
    caec = st.selectbox("Costuma comer entre as refeições?", ["Às vezes", "Frequentemente", "Sempre", "Não"])
    fuma = st.selectbox("Fuma?", ["Sim", "Não"])
    ch2o = st.slider("Litros de água ingeridos por dia", 0.0, 3.0, 2.0)
    scc = st.selectbox("Controla as calorias consumidas?", ["Sim", "Não"])
    faf = st.slider("Frequência de atividade física, onde 0 = sendentário e 3 = diariamente", 0.0, 3.0, 1.0)
    tue = st.slider("Tempo diário com dispositivos eletrônicos, sendo 0 = quase nada e 2 = uso intenso", 0.0, 2.0, 1.0)
    calc = st.selectbox("Frequência de consumo de álcool", ["Não", "Às vezes", "Frequentemente", "Sempre"])
    transporte = st.selectbox("Meio de transporte mais utilizado", ["Transporte Público", "A pé", "Carro", "Moto", "Bicicleta"])

    enviar = st.form_submit_button("🔍 Prever")

# Dicionário de mapeamento reverso, pois o codigo original esta em ingles, e para melhorar a experiencia do usuário, resolvi tratar a questao do idioma no front.
mapas = {
    "Gender": {"Masculino": "Male", "Feminino": "Female"},
    "family_history": {"Sim": "yes", "Não": "no"},
    "FAVC": {"Sim": "yes", "Não": "no"},
    "CAEC": {"Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always", "Não": "no"},
    "SMOKE": {"Sim": "yes", "Não": "no"},
    "SCC": {"Sim": "yes", "Não": "no"},
    "CALC": {"Não": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"},
    "MTRANS": {
        "Transporte Público": "Public_Transportation",
        "A pé": "Walking",
        "Carro": "Automobile",
        "Moto": "Motorbike",
        "Bicicleta": "Bike"
    }
}

# Processamento e predição
if enviar:
    # Substituir valores para o formato original do modelo
    genero = mapas["Gender"][genero]
    historico_familiar = mapas["family_history"][historico_familiar]
    favc = mapas["FAVC"][favc]
    caec = mapas["CAEC"][caec]
    fuma = mapas["SMOKE"][fuma]
    scc = mapas["SCC"][scc]
    calc = mapas["CALC"][calc]
    transporte = mapas["MTRANS"][transporte]

    dados = pd.DataFrame([[
        genero, idade, altura, peso, historico_familiar, favc, fcvc, ncp, caec,
        fuma, ch2o, scc, faf, tue, calc, transporte
    ]], columns=[
        "Gender", "Age", "Height", "Weight", "family_history", "FAVC", "FCVC", "NCP", "CAEC",
        "SMOKE", "CH2O", "SCC", "FAF", "TUE", "CALC", "MTRANS"
    ])

    # Codificação
    for col in label_encoders:
        if col in dados.columns:
            dados[col] = label_encoders[col].transform(dados[col])

    dados["BMI"] = dados["Weight"] / (dados["Height"] ** 2)
    col_numericas = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE', 'BMI']
    dados[col_numericas] = scaler.transform(dados[col_numericas])

    # Predição
    pred = model.predict(dados)[0]
    resultado = label_encoders['Obesity'].inverse_transform([pred])[0]

    # Traduções dos níveis de obesidade
    rotulos_pt = {
        "Insufficient_Weight": "Peso insuficiente",
        "Normal_Weight": "Peso normal",
        "Overweight_Level_I": "Sobrepeso nível I",
        "Overweight_Level_II": "Sobrepeso nível II",
        "Obesity_Type_I": "Obesidade tipo I",
        "Obesity_Type_II": "Obesidade tipo II",
        "Obesity_Type_III": "Obesidade tipo III"
    }    
    resultado_pt = rotulos_pt.get(resultado, resultado)

    # Apresentação
    st.subheader("🎯 Resultado da Análise:")
    st.success(f"O modelo estimou que o paciente está classificado como: **{resultado_pt}**")

    st.subheader("📌 Recomendação:")
    if "Obesity" in resultado:
        st.warning("Recomenda-se procurar um nutricionista e médico especialista para avaliação clínica detalhada.")
    elif "Overweight" in resultado:
        st.info("Sinais de sobrepeso. Pode ser indicado ajustar hábitos alimentares e aumentar a prática de atividades físicas.")
    else:
        st.success("Nível dentro da normalidade. Continue mantendo um estilo de vida saudável!")
