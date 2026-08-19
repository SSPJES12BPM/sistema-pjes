import streamlit as st
from supabase import create_client, Client
import pandas as pd

st.set_page_config(page_title="PJES - 12º BPM", page_icon="🛡️", layout="wide")

# Inicialização da conexão com Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error("Erro na conexão com o banco. Configure as chaves em Settings > Secrets.")
    st.stop()

# Menu Lateral
st.sidebar.title("🛡️ PJES - 12º BPM")
opcao = st.sidebar.radio(
    "Selecione o Módulo:",
    ["📋 Efetivo", "⚙️ Cadastrar Postos", "📝 Preferências", "⚡ Escala Gerada"]
)

# MÓDULO 1: EFETIVO
if opcao == "📋 Efetivo":
    st.header("📋 Efetivo Cadastrado")
    res = supabase.table("efetivo").select("matricula, nome_guerra, posto_grad, telefone, habilitado_mot, ativo").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum policial encontrado.")

# MÓDULO 2: CADASTRO DE POSTOS
elif opcao == "⚙️ Cadastrar Postos":
    st.header("⚙️ Cadastro de Vagas/Postos do Mês")
    
    with st.form("form_posto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            mes_ref = st.date_input("Mês de Referência")
            tipo = st.selectbox("Tipo de Serviço", ["TI", "viatura", "operacao"])
            codigo = st.text_input("Código do Posto (Ex: VTR-01)")
            local = st.text_input("Local de Atuação")
        with col2:
            data_especifica = st.date_input("Data do Serviço")
            hora_inicio = st.time_input("Hora Início")
            hora_fim = st.time_input("Hora Fim")
            funcao = st.selectbox("Função", ["CMT", "PAT", "MOT", "FISCAL"])
            vagas = st.number_input("Vagas", min_value=1, value=1)
        
        btn_salvar = st.form_submit_button("Cadastrar Posto")
        if btn_salvar:
            dados = {
                "mes_referencia": str(mes_ref),
                "tipo": tipo,
                "codigo": codigo,
                "local": local,
                "data_especifica": str(data_especifica),
                "hora_inicio": str(hora_inicio),
                "hora_fim": str(hora_fim),
                "funcao": funcao,
                "vagas": int(vagas)
            }
            supabase.table("postos_config").insert(dados).execute()
            st.success("Posto cadastrado com sucesso!")

    st.subheader("Postos Cadastrados")
    postos = supabase.table("postos_config").select("*").execute()
    if postos.data:
        st.dataframe(pd.DataFrame(postos.data), use_container_width=True)

# MÓDULO 3: PREFERÊNCIAS
elif opcao == "📝 Preferências":
    st.header("📝 Coleta de Preferências do Policial")
    st.info("Em breve: Formulário para o policial indicar disponibilidade.")

# MÓDULO 4: ESCALA
elif opcao == "⚡ Escala Gerada":
    st.header("⚡ Algoritmo de Geração da Escala")
    st.info("Em breve: Processamento automático com base na ordem hierárquica e restrições.")
