# 🩺 Obesity Predictor - Sistema Preditivo de Nível de Obesidade

Este projeto foi desenvolvido como parte do **Tech Challenge - Fase 4 da Pós-Tech**. Ele aplica técnicas de **Machine Learning** para prever o nível de obesidade de uma pessoa com base em dados comportamentais, físicos e hábitos de vida.

---

## 🎯 Objetivo

Ajudar **profissionais da saúde** a identificar de forma automatizada e preventiva possíveis níveis de obesidade, com:
- Interface simples via Streamlit
- Predição imediata
- Recomendação básica para o usuário

---

## 💻 Como executar o projeto localmente

1. Clone este repositório:
```bash
git clone https://github.com/jess-furlan/obesity-predictor.git
cd obesity-predictor
```

2. Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run app.py
```

---

## 🧠 Modelo de Machine Learning

- Random Forest Classifier
- Acurácia de 99,19% com validação cruzada (Stratified K-Fold)
- Feature derivada: IMC (BMI = Peso / Altura²)
- Pré-processamento: LabelEncoder + StandardScaler

---

## 📂 Estrutura do Projeto
```bash
obesity-predictor/
├── modelo_final/
│   ├── random_forest_model.pkl
│   ├── standard_scaler.pkl
│   └── label_encoders.pkl
├── app.py
├── requirements.txt
└── README.md
```
---

## 🌐 Acesse o App Online
➡️ Acesse o app online:

https://jess-furlan-obesity-predictor.streamlit.app

---

## 📌 Resultados da Previsão
O modelo retorna:
- O nível de obesidade estimado (ex: Normal, Overweight, Obesity Type I)
- Um feedback textual personalizado com sugestão de ação (ex: “Procure um nutricionista”)

---

## 📊 Tecnologias Utilizadas
- Python
- Streamlit
- scikit-learn
- pandas
- joblib

---

## ✍️ Autoria
Desenvolvido por Jess Furlan
github.com/jess-furlan


