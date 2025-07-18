# app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Carregar artefatos do modelo
model = joblib.load("modelo_final/random_forest_model.pkl")
scaler = joblib.load("modelo_final/standard_scaler.pkl")
label_encoders = joblib.load("modelo_final/label_encoders.pkl")

st.set_page_config(page_title="Preditor de Obesidade", layout="centered")

st.title("🩺 Sistema Preditivo de Obesidade")
st.markdown("Preencha os dados abaixo para obter uma análise preditiva do nível de obesidade:")

# ------------------------------
# Formulário para entrada de dados
# ------------------------------
with st.form("formulario_paciente"):
    genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    idade = st.number_input("Idade", min_value=1, max_value=100, value="")
    altura = st.number_input("Altura (em metros)", min_value=1.0, max_value=2.5, value=1.70)
    peso = st.number_input("Peso (em kg)", min_value=30.0, max_value=200.0, value=70.0)
    historico_familiar = st.selectbox("Algum familiar tem histórico de sobrepeso?", ["Sim", "Não"])
    favc = st.selectbox("Costuma consumir alimentos calóricos com frequência?", ["Sim", "Não"])
    fcvc = st.slider("Frequência de consumo de vegetais (0-3)", 0.0, 3.0, 2.0)
    ncp = st.slider("Número de refeições principais por dia", 1.0, 4.0, 3.0)
    caec = st.selectbox("Costuma comer entre as refeições?", ["Às vezes", "Frequentemente", "Sempre", "Não"])
    fuma = st.selectbox("Fuma?", ["Sim", "Não"])
    ch2o = st.slider("Litros de água ingeridos por dia", 0.0, 3.0, 2.0)
    scc = st.selectbox("Controla as calorias consumidas?", ["Sim", "Não"])
    faf = st.slider("Frequência de atividade física na semana (0 a 3 vezes na semana)", 0.0, 3.0, 1.0)
    tue = st.slider("Tempo diário com dispositivos eletrônicos (0 a 2hs)", 0.0, 2.0, 1.0)
    calc = st.selectbox("Frequência de consumo de álcool", ["Não", "Às vezes", "Frequentemente", "Sempre"])
    transporte = st.selectbox("Meio de transporte mais utilizado", ["Transporte Público", "A pé", "Carro", "Moto", "Bicicleta"])
    
    enviar = st.form_submit_button("🔍 Prever")

# ------------------------------
# Processamento e Previsão
# ------------------------------
if submitted:
    # Criar dataframe com a entrada
    input_data = pd.DataFrame([[
        gender, age, height, weight, family_history, favc, fcvc, ncp, caec,
        smoke, ch2o, scc, faf, tue, calc, mtrans
    ]], columns=[
        "Gender", "Age", "Height", "Weight", "family_history", "FAVC", "FCVC", "NCP", "CAEC",
        "SMOKE", "CH2O", "SCC", "FAF", "TUE", "CALC", "MTRANS"
    ])

    # Codificar variáveis categóricas
    for col in label_encoders:
        if col in input_data.columns:
            input_data[col] = label_encoders[col].transform(input_data[col])

    # Criar variável IMC (BMI)
    input_data["BMI"] = input_data["Weight"] / (input_data["Height"] ** 2)

    # Padronizar dados numéricos
    num_cols = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE', 'BMI']
    input_data[num_cols] = scaler.transform(input_data[num_cols])

    # Fazer a previsão
    pred = model.predict(input_data)[0]
    pred_label = label_encoders['Obesity'].inverse_transform([pred])[0]

    # Exibir resultado
    st.subheader("🎯 Resultado da Previsão:")
    st.success(f"Nível estimado de obesidade: **{pred_label.replace('_', ' ')}**")

    # Feedback básico
    st.subheader("📌 Recomendação:")
    if "Obesity" in pred_label:
        st.warning("Recomenda-se procurar um nutricionista e um profissional de saúde para acompanhamento personalizado.")
    elif "Overweight" in pred_label:
        st.info("Considere revisar seus hábitos alimentares e sua rotina de exercícios físicos.")
    else:
        st.success("Seu nível está dentro da normalidade, continue mantendo hábitos saudáveis!")
