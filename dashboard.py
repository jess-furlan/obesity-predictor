import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Estilo visual
st.set_page_config(page_title="Dashboard Obesidade", layout="wide")
st.markdown(\"\"\"
    <style>
    .main { background-color: #f5f9ff; }
    h1, h2, h3 {
        color: #20639B;
    }
    .stDataFrame th {
        background-color: #B3D4FC;
        color: black;
    }
    .css-1aumxhk, .css-1v0mbdj {
        background-color: #ffffff;
    }
    </style>
\"\"\", unsafe_allow_html=True)

# Carregar dados
df = pd.read_csv("Obesity.csv")
df["BMI"] = df["Weight"] / (df["Height"] ** 2)
df["Age_Group"] = pd.cut(df["Age"], bins=[0, 18, 30, 45, 60, 100],
                         labels=["<18", "18-30", "30-45", "45-60", "60+"])

# Traduções
df.replace({
    "Gender": {"Male": "Homem", "Female": "Mulher"},
    "family_history": {"yes": "Sim", "no": "Não"},
    "FAVC": {"yes": "Sim", "no": "Não"},
    "SMOKE": {"yes": "Sim", "no": "Não"},
    "SCC": {"yes": "Sim", "no": "Não"},
    "CAEC": {"Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre", "no": "Não"},
    "CALC": {"Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre", "no": "Não"},
    "MTRANS": {
        "Public_Transportation": "Transporte Público",
        "Walking": "A pé",
        "Automobile": "Carro",
        "Motorbike": "Moto",
        "Bike": "Bicicleta"
    },
    "Obesity": {
        "Insufficient_Weight": "Peso Insuficiente",
        "Normal_Weight": "Peso Normal",
        "Overweight_Level_I": "Sobrepeso I",
        "Overweight_Level_II": "Sobrepeso II",
        "Obesity_Type_I": "Obesidade I",
        "Obesity_Type_II": "Obesidade II",
        "Obesity_Type_III": "Obesidade III"
    }
}, inplace=True)

st.title("🩺 Dashboard Interativo - Obesidade e Hábitos de Saúde")

# Navegação e Filtros
aba = st.sidebar.radio("Navegar por:", ["📈 Visão Geral", "💡 Hábitos e Riscos", "🩺 Recomendações e Perfis de Risco"])
st.sidebar.header("🎛️ Filtros")
genero = st.sidebar.multiselect("Gênero", options=df["Gender"].unique(), default=df["Gender"].unique())
faixa_etaria = st.sidebar.multiselect("Faixa Etária", options=df["Age_Group"].unique(), default=df["Age_Group"].unique())
df_filt = df[df["Gender"].isin(genero) & df["Age_Group"].isin(faixa_etaria)]

# 📈 Visão Geral
if aba == "📈 Visão Geral":
    st.header("📊 Distribuição dos níveis de obesidade")
    fig1 = px.histogram(df_filt, x="Obesity", color="Gender", facet_col="Age_Group", barmode="group",
                        category_orders={"Age_Group": ["<18", "18-30", "30-45", "45-60", "60+"]})
    st.plotly_chart(fig1, use_container_width=True)
    st.info("🔍 A faixa de 30-45 anos apresenta uma maior concentração de casos graves de obesidade, especialmente entre indivíduos com histórico familiar positivo.")
    
    st.subheader("📈 Média de IMC por Faixa Etária")
    st.bar_chart(df_filt.groupby("Age_Group")["BMI"].mean())
    st.info("🔎 A faixa de 30 a 45 anos apresenta o maior IMC médio entre todas as faixas, com 31,48, indicando maior risco de obesidade severa justamente na idade produtiva. Essa faixa merece atenção prioritária para ações de prevenção e acompanhamento contínuo.")

    st.subheader("📊 Proporção de Gênero por Nível de Obesidade")
    st.plotly_chart(px.histogram(df_filt, x="Gender", color="Obesity", barmode="group"), use_container_width=True)
    st.info("🔎 Homens predominam nos níveis de obesidade tipo II (99,3%) e sobrepeso II (64,5%), enquanto mulheres estão altamente representadas nos casos de obesidade tipo III (99,7%) e peso insuficiente (63,6%). Isso evidencia padrões distintos de risco por gênero, que devem ser considerados em estratégias clínicas diferenciadas.")

# 💡 Hábitos e Riscos
elif aba == "💡 Hábitos e Riscos":
    st.header("💡 Hábitos e Comportamentos Relacionados")

    st.subheader("⚖️ Atividade física vs Uso de dispositivos")
    fig2 = px.scatter(df_filt, x="FAF", y="TUE", color="Obesity", symbol="Gender", size="BMI",
                      labels={"FAF": "Atividade Física", "TUE": "Tempo com Dispositivos"})
    st.plotly_chart(fig2, use_container_width=True)
    st.warning("📉 Indivíduos com baixo nível de atividade física (FAF) e alto tempo de tela (TUE) concentram os níveis mais altos de obesidade.")

    st.subheader("📊 Frequência de Consumo de Água por Obesidade")
    fig4 = px.box(df_filt, x="Obesity", y="CH2O", points="all")
    st.plotly_chart(fig4, use_container_width=True)
    st.info("🔎 Embora a ingestão média de água seja mais alta entre os indivíduos com obesidade tipo III, os níveis mais leves de obesidade (tipo II e sobrepeso) e peso normal estão associados a menor consumo hídrico, o que pode indicar que a hidratação adequada não está sendo consistentemente usada como prática preventiva nos estágios iniciais da obesidade.")

    st.subheader("🧪 Correlação entre variáveis numéricas")
    corr = df_filt[["Age", "Height", "Weight", "BMI", "FAF", "TUE", "CH2O"]].corr()
    fig3, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig3)
    st.success("✅ Correlações mostram que peso e altura são os principais fatores que impactam diretamente o IMC, enquanto maior tempo com dispositivos eletrônicos está inversamente relacionado com atividade física.")
    
# 🩺 Recomendações e Perfis de Risco
elif aba == "🩺 Recomendações e Perfis de Risco":
    st.header("🩺 Perfis de Risco com Base em Histórico Familiar")

    risco_hist = pd.crosstab(
        df_filt["family_history"], df_filt["Obesity"], normalize="index"
    ) * 100
    st.bar_chart(risco_hist.T)

    st.subheader("📊 Hábitos Frequentes entre Obesos Graves")
    obesos = df_filt[df_filt["Obesity"].isin([
        "Obesidade I", "Obesidade II", "Obesidade III"
    ])]
    col1, col2 = st.columns(2)

    with col1:
        favc = obesos["FAVC"].value_counts(normalize=True) * 100
        caec = obesos["CAEC"].value_counts(normalize=True) * 100
        st.write("🔸 Consumo de alimentos calóricos")
        st.dataframe(favc.rename("Percentual (%)"))
        st.write("🔸 Lanches entre refeições")
        st.dataframe(caec.rename("Percentual (%)"))

    with col2:
        transp = obesos["MTRANS"].value_counts(normalize=True) * 100
        smoke = obesos["SMOKE"].value_counts(normalize=True) * 100
        st.write("🔸 Transporte mais utilizado")
        st.dataframe(transp.rename("Percentual (%)"))
        st.write("🔸 Fuma?")
        st.dataframe(smoke.rename("Percentual (%)"))

    st.markdown("---")
    st.subheader("📌 Recomendações Clínicas")
    st.markdown(\"\"\"
    - 🧬 Histórico familiar positivo + maus hábitos = **alto risco**.
    - 🍟 Reduzir consumo calórico e beliscos fora de hora.
    - 🚶 Incentivar transporte ativo e atividade física leve.
    - 💧 Monitorar ingestão hídrica e promover orientação nutricional.
    \"\"\")

# Rodapé
st.markdown("---")
st.markdown("<center><small>Desenvolvido para o Tech Challenge • Pós-Tech FIAP • por Jess Furlan</small></center>", unsafe_allow_html=True)



