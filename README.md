# 🩺 Obesity Predictor - Sistema Preditivo de Nível de Obesidade

Este projeto foi desenvolvido como parte do **Tech Challenge - Fase 4 da Pós-Tech**. Ele aplica técnicas de **Machine Learning** para prever o nível de obesidade de uma pessoa com base em dados comportamentais, físicos e hábitos de vida.

---

## 🎯 Objetivo

Ajudar **profissionais da saúde** a identificar de forma automatizada e preventiva possíveis níveis de obesidade, com:
- Interface simples via Streamlit
- Predição imediata
- Recomendação básica para o usuário

---

## 💡 Funcionalidades

- Previsão de nível de obesidade com base em 16 variáveis.
- Feedback e recomendações personalizadas para o paciente.
- Dashboard com:
  - Comparativos por faixa etária e gênero.
  - Perfis de risco baseados em hábitos e histórico familiar.
  - Análises de correlação e padrões comportamentais.

---

## 🧠 Modelo de Machine Learning

- Algoritmo Random Forest Classifier
- Acurácia de 99,19% com validação cruzada (Stratified K-Fold)
- Feature Engineering:
  - Criação da variável IMC (BMI)
  - Pré-processamento: `LabelEncoder` + `StandardScaler`

---

## 📂 Estrutura do Projeto
```bash
obesity-predictor/
├── modelo_final/
│   ├── random_forest_model.pkl
│   ├── standard_scaler.pkl
│   └── label_encoders.pkl
├── notebook/
    └── modelagem_obesidade.ipynb
├── Obesity.csv
├── app.py                  # Sistema preditivo
├── dashboard.py            # Análise interativa de dados
├── requirements.txt
└── README.md
```
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

4. Ou visualize a análise exploratória:
```bash
streamlit run dashboard.py
```
---

## 🌐 Acesse o App Online
🔍 Aplicativo Preditivo: [Streamlit App](https://jess-furlan-obesity-predictor.streamlit.app)

---

## 📌 Resultados da Previsão
O modelo retorna:
- O nível de obesidade estimado (ex: Normal, Overweight, Obesity Type I)
- Um feedback textual personalizado com sugestão de ação (ex: “Procure um nutricionista”)

---

## 🌐 Acesse o Dashboard Online
📈 Dashboard Analítico: [Dashboard Interativo](https://jess-furlan-obesity-dashboard.streamlit.app)

---

## 📌 Destaques do Dashboard
- Faixa de 30 a 45 anos tem maior média de IMC (31,48).
- Homens predominam na obesidade tipo II, mulheres na tipo III.
- Alta correlação entre uso de dispositivos e menor atividade física.
- Comportamentos como beliscar entre refeições e não controlar calorias estão fortemente presentes entre indivíduos com obesidade tipo III.

---

## 📊 Tecnologias Utilizadas
- Python (pandas, numpy, scikit-learn, joblib)
- Streamlit (interfaces interativas)
- Plotly, Matplotlib, Seaborn (visualização de dados)
- Jupyter Notebook (modelagem exploratória)
- XGBoost e LightGBM (testes comparativos de modelos)

---
## ⚙️ Justificativa Técnica: Por que o projeto não utiliza Docker?
Embora o Docker seja uma ferramenta amplamente adotada para empacotar aplicações e garantir portabilidade entre ambientes, a decisão de não utilizá-lo neste projeto foi tomada com base em critérios técnicos e estratégicos:

✅ Deploy simplificado via Streamlit Cloud: a aplicação foi publicada diretamente na nuvem por meio do Streamlit Cloud, que já oferece um ambiente virtual isolado e compatível com o requirements.txt. Isso garante reprodutibilidade e isolamento sem a complexidade adicional do Docker.

✅ Público-alvo não técnico: como o foco da solução é auxiliar profissionais da saúde, foi priorizada uma abordagem acessível, com uso via navegador, sem necessidade de instalação local ou familiaridade com containers.

✅ Escopo monolítico e simples: o projeto consiste em uma única aplicação Streamlit, com pipeline de Machine Learning embarcada. Não há múltiplos serviços (ex: APIs, bancos de dados) que justifiquem uma arquitetura containerizada.

✅ Reprodutibilidade garantida: todo o ambiente é controlado por meio do arquivo requirements.txt, o que assegura consistência de dependências tanto localmente quanto na nuvem.

Caso o projeto venha a evoluir para um cenário mais complexo (ex: múltiplas aplicações, uso de APIs, banco de dados, CI/CD), a adoção de Docker será reavaliada conforme as boas práticas de MLOps.

---

## ✍️ Autoria
Desenvolvido por Jess Furlan
github.com/jess-furlan


