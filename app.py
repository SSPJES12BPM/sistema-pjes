import streamlit as st
from supabase import create_client, Client
import pandas as pd

st.set_page_config(page_title="PJES - 12º BPM", page_icon="🛡️", layout="wide")

st.sidebar.title("🛡️ PJES - 12º BPM")

# Leitura segura dos Secrets removendo possíveis espaços em branco
try:
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Erro ao carregar as credenciais: {e}")
    st.stop()

# Menu Lateral
opcao = st.sidebar.radio(
    "Selecione o Módulo:",
    ["📋 Efetivo", "⚙️ Cadastrar Postos", "📝 Preferências", "⚡ Escala Gerada"]
)

# MÓDULO 1: EFETIVO
if opcao == "📋 Efetivo":
    st.header("📋 Efetivo Cadastrado")
    try:
        res = supabase.table("efetivo").select("matricula, nome_guerra, posto_grad, telefone, habilitado_mot, ativo").execute()
        if res.data:
            df = pd.DataFrame(res.data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum policial encontrado.")
    except Exception as err:
        st.error("Não foi possível conectar ao banco de dados do Supabase.")
        st.warning(f"Verifique as chaves em Settings > Secrets. Detalhe: {err}")

# MÓDULO 2: CADASTRO DE POSTOS
elif opcao == "⚙️ Cadastrar Postos":
    st.header("⚙️ Cadastro de Vagas/Postos do Mês")
    st.info("Módulo de cadastro de postos em desenvolvimento.")

# MÓDULO 3: PREFERÊNCIAS
elif opcao == "📝 Preferências":
    st.header("📝 Coleta de Preferências do Policial")
    st.info("Módulo de preferências do policial em desenvolvimento.")

# MÓDULO 4: ESCALA
elif opcao == "⚡ Escala Gerada":
    st.header("⚡ Algoritmo de Geração da Escala")
    st.info("Módulo de geração automática em desenvolvimento.")
