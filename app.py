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

st.title("🩺 Preditor de Obesidade")
st.markdown("Preencha os dados abaixo para obter uma previsão:")

# ------------------------------
# Formulário para entrada de dados
# ------------------------------
with st.form("input_form"):
    gender = st.selectbox("Gênero", ["Male", "Female"])
    age = st.slider("Idade", 10, 100, 25)
    height = st.number_input("Altura (em metros)", min_value=1.0, max_value=2.5, value=1.70)
    weight = st.number_input("Peso (em kg)", min_value=30.0, max_value=200.0, value=70.0)
    family_history = st.selectbox("Histórico familiar de sobrepeso?", ["yes", "no"])
    favc = st.selectbox("Consome alimentos calóricos frequentemente?", ["yes", "no"])
    fcvc = st.slider("Frequência de vegetais na alimentação (0-3)", 0.0, 3.0, 2.0)
    ncp = st.slider("Nº de refeições principais por dia", 1.0, 4.0, 3.0)
    caec = st.selectbox("Come entre as refeições?", ["Sometimes", "Frequently", "Always", "no"])
    smoke = st.selectbox("Fuma?", ["yes", "no"])
    ch2o = st.slider("Quantidade de água por dia (litros)", 0.0, 3.0, 2.0)
    scc = st.selectbox("Monitora calorias consumidas?", ["yes", "no"])
    faf = st.slider("Frequência de atividade física (0-3)", 0.0, 3.0, 1.0)
    tue = st.slider("Tempo com dispositivos eletrônicos (0-2)", 0.0, 2.0, 1.0)
    calc = st.selectbox("Frequência de bebida alcoólica", ["no", "Sometimes", "Frequently", "Always"])
    mtrans = st.selectbox("Meio de transporte mais utilizado", ["Public_Transportation", "Walking", "Automobile", "Motorbike", "Bike"])
    
    submitted = st.form_submit_button("🔍 Prever Nível de Obesidade")

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
