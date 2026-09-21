import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA E CSS PERSONALIZADO (TONS DE VERDE)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Produção de Porcelanato",
    layout="wide",
    page_icon="🧱"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #f2f7f2;
        color: #1c3b1e;
    }
    section[data-testid="stSidebar"] {
        background-color: #e2efe2 !important;
        border-right: 2px solid #70B450;
    }
    h1, h2, h3, h4 {
        color: #004716 !important;
        font-weight: 800 !important;
    }
    .stButton > button {
        background-color: #55A453 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover {
        background-color: #008000 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #004716 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

TOTAL_AREA_PREDIO = 5135.44

# ---------------------------------------------------------
# CONSTANTES E MAPEAMENTOS
# ---------------------------------------------------------
ELEVATION_MAP = {
    21: ["Padrão", "Padrão", "Padrão", "Sala, Cozinha e Varanda"],
    20: ["Padrão", "Padrão", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda"],
    19: ["Sala, Cozinha e Varanda", "Padrão", "Padrão", "Padrão"],
    18: ["Sala, Cozinha e Varanda", "Padrão", "Padrão", "Sala, Cozinha e Varanda"],
    17: ["Sala, Cozinha e Varanda", "Padrão", "Padrão", "Sala, Cozinha e Varanda"],
    16: ["Padrão", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Padrão"],
    15: ["Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda"],
    14: ["Padrão", "Padrão", "Padrão", "Sala, Cozinha e Varanda"],
    13: ["Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda"],
    12: ["Padrão", "Padrão", "Padrão", "Padrão"],
    11: ["Padrão", "Padrão", "Padrão", "Sala, Cozinha e Varanda"],
    10: ["Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Padrão", "Padrão"],
    9:  ["Padrão", "Padrão", "Padrão", "Padrão"],
    8:  ["Sala, Cozinha e Varanda", "Padrão", "Padrão", "Padrão"],
    7:  ["Padrão", "Padrão", "Padrão", "Padrão"],
    6:  ["Padrão", "Padrão", "Sala, Cozinha e Varanda", "Padrão"],
    5:  ["Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda"],
    4:  ["Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda"],
    3:  ["Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda"],
    2:  ["Padrão", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda", "Sala, Cozinha e Varanda"],
    1:  ["Padrão", "Padrão", "Padrão", "Padrão"]
}

AREAS_DETALHADAS = {
    "A": {
        "Padrão": {
            "WC Reversível Piso": (3.11, "Porcelanato 70x70"),
            "WC Reversível Parede": (8.46, "Porcelanato 70x70"),
            "WC Suíte Piso": (3.51, "Porcelanato 70x70"),
            "WC Suíte Parede": (6.90, "Porcelanato 70x70"),
            "Área de Serviço Piso": (1.88, "Cerâmica 45x45"),
            "Área de Serviço Parede": (6.33, "Cerâmica 45x45"),
            "Varanda Cozinha": (6.53, "Porcelanato 70x70"),
            "Varanda Suíte": (4.36, "Porcelanato 70x70"),
            "Parede Cozinha Padrão": (7.45, "Porcelanato 70x70")
        },
        "Sala, Cozinha e Varanda": {
            "WC Reversível Piso": (3.11, "Porcelanato 70x70"),
            "WC Reversível Parede": (8.46, "Porcelanato 70x70"),
            "WC Suíte Piso": (3.51, "Porcelanato 70x70"),
            "WC Suíte Parede": (6.90, "Porcelanato 70x70"),
            "Área de Serviço Piso": (1.88, "Cerâmica 45x45"),
            "Área de Serviço Parede": (6.33, "Cerâmica 45x45"),
            "Varanda Cozinha": (6.53, "Porcelanato 70x70"),
            "Varanda Suíte": (4.36, "Porcelanato 70x70"),
            "Parede Cozinha Conjugado": (11.275, "Porcelanato 70x70")
        }
    },
    "B": {
        "Padrão": {
            "WC Reversível Piso": (3.15, "Porcelanato 70x70"),
            "WC Reversível Parede": (6.51, "Porcelanato 70x70"),
            "WC Suíte Piso": (3.01, "Porcelanato 70x70"),
            "WC Suíte Parede": (6.56, "Porcelanato 70x70"),
            "Área de Serviço Piso": (1.81, "Cerâmica 45x45"),
            "Área de Serviço Parede": (6.23, "Cerâmica 45x45"),
            "Varanda Cozinha": (6.91, "Porcelanato 70x70"),
            "Varanda c/ Área Tec": (2.79, "Porcelanato 70x70"),
            "Parede Cozinha Padrão": (7.33, "Porcelanato 70x70")
        },
        "Sala, Cozinha e Varanda": {
            "WC Reversível Piso": (3.15, "Porcelanato 70x70"),
            "WC Reversível Parede": (6.51, "Porcelanato 70x70"),
            "WC Suíte Piso": (3.01, "Porcelanato 70x70"),
            "WC Suíte Parede": (6.56, "Porcelanato 70x70"),
            "Área de Serviço Piso": (1.81, "Cerâmica 45x45"),
            "Área de Serviço Parede": (6.23, "Cerâmica 45x45"),
            "Varanda Cozinha": (6.91, "Porcelanato 70x70"),
            "Varanda c/ Área Tec": (2.79, "Porcelanato 70x70"),
            "Parede Cozinha Conjugado": (12.83, "Porcelanato 70x70")
        }
    },
    "A1": {
        "Padrão": {
            "WC Reversível Piso": (3.11, "Porcelanato 70x70"),
            "WC Reversível Parede": (8.46, "Porcelanato 70x70"),
            "WC Suíte Piso": (3.51, "Porcelanato 70x70"),
            "WC Suíte Parede": (6.90, "Porcelanato 70x70"),
            "Área de Serviço Piso": (1.88, "Cerâmica 45x45"),
            "Área de Serviço Parede": (6.33, "Cerâmica 45x45"),
            "Varanda Cozinha": (6.53, "Porcelanato 70x70"),
            "Varanda Suíte": (1.88, "Porcelanato 70x70"),
            "Parede Cozinha Padrão": (7.45, "Porcelanato 70x70")
        },
        "Sala, Cozinha e Varanda": {
            "WC Reversível Piso": (3.11, "Porcelanato 70x70"),
            "WC Reversível Parede": (8.46, "Porcelanato 70x70"),
            "WC Suíte Piso": (3.51, "Porcelanato 70x70"),
            "WC Suíte Parede": (6.90, "Porcelanato 70x70"),
            "Área de Serviço Piso": (1.88, "Cerâmica 45x45"),
            "Área de Serviço Parede": (6.33, "Cerâmica 45x45"),
            "Varanda Cozinha": (6.53, "Porcelanato 70x70"),
            "Varanda Suíte": (1.88, "Porcelanato 70x70"),
            "Parede Cozinha Conjugado": (11.275, "Porcelanato 70x70")
        }
    },
    "CIRCULACAO": {
        "Padrão": {
            "WC Serviço Piso": (3.84, "Cerâmica 45x45"),
            "WC Serviço Parede": (4.78, "Cerâmica 45x45"),
            "Corredor": (44.28, "Porcelanato 70x70")
        }
    }
}
AREAS_DETALHADAS["B1"] = AREAS_DETALHADAS["B"]

CORES_PAVIMENTOS = [
    "#E8F5E9", "#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A",
    "#4CAF50", "#43A047", "#388E3C", "#2E7D32", "#1B5E20",
    "#DCECC9", "#B9E3A5", "#97D780", "#73C75B", "#52B436",
    "#C5E1A5", "#AED581", "#9CCC65", "#8BC34A", "#7CB342", "#689F38"
]

COLUNAS = [
    "ID", "Data", "Equipe", "Pavimento", "Unidade", "Ambiente", 
    "% Concluído", "Área Executada (m²)", "Peças Porcelanato", 
    "Peças Cerâmica", "Sacos Argamassa (30kg)"
]

if "dados_obra" not in st.session_state:
    st.session_state["dados_obra"] = pd.DataFrame(columns=COLUNAS)

def carregar_dados():
    return st.session_state["dados_obra"]

def salvar_dados(df):
    st.session_state["dados_obra"] = df

def calcular_pct_acumulado(df, pavimento, unidade, ambiente):
    if df.empty:
        return 0.0
    filtro = (df["Pavimento"] == pavimento) & (df["Unidade"] == unidade) & (df["Ambiente"] == ambiente)
    return float(df[filtro]["% Concluído"].sum())

def calcular_area_pavimento_teorica(pav_num):
    area_pav = 52.90
    for idx, u in enumerate(["Apt A", "Apt B", "Apt B1", "Apt A1"]):
        cust = ELEVATION_MAP[pav_num][idx]
        key = u.replace("Apt ", "")
        area_pav += sum([v[0] for v in AREAS_DETALHADAS[key][cust].values()])
    return area_pav

# Nomes das equipes
if "eq1" not in st.session_state: st.session_state["eq1"] = "Equipe 1 - Pedro"
if "eq2" not in st.session_state: st.session_state["eq2"] = "Equipe 2 - João"
if "eq3" not in st.session_state: st.session_state["eq3"] = "Equipe 3 - Carlos"
if "eq4" not in st.session_state: st.session_state["eq4"] = "Equipe 4 - Lucas"

st.sidebar.header("⚙️ Equipes de Trabalho")
st.session_state["eq1"] = st.sidebar.text_input("Equipe 1", st.session_state["eq1"])
st.session_state["eq2"] = st.sidebar.text_input("Equipe 2", st.session_state["eq2"])
st.session_state["eq3"] = st.sidebar.text_input("Equipe 3", st.session_state["eq3"])
st.session_state["eq4"] = st.sidebar.text_input("Equipe 4", st.session_state["eq4"])

LISTA_EQUIPES = [
    st.session_state["eq1"],
    st.session_state["eq2"],
    st.session_state["eq3"],
    st.session_state["eq4"]
]

df_atual = carregar_dados()

# ---------------------------------------------------------
# ATALHO PARA PAVIMENTOS JÁ CONCLUÍDOS (SEM AFETAR EQUIPES)
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🏆 Concluir Pavimento Antigo")
st.sidebar.caption("Utilize para marcar pavimentos já prontos sem associar à produção atual de nenhuma equipe.")

pav_pronto = st.sidebar.selectbox("Pavimento Concluído", range(1, 22), format_func=lambda x: f"Pavimento {x:02d}", key="pav_pronto_sel")

if st.sidebar.button("Marcar como 100% Concluído"):
    str_pav = f"Pavimento {pav_pronto:02d}"
    novos = []
    
    unidades_list = [
        ("Apt A", "A", ELEVATION_MAP[pav_pronto][0]),
        ("Apt B", "B", ELEVATION_MAP[pav_pronto][1]),
        ("Apt B1", "B1", ELEVATION_MAP[pav_pronto][2]),
        ("Apt A1", "A1", ELEVATION_MAP[pav_pronto][3]),
        ("Circulação / WC Serviço", "CIRCULACAO", "Padrão")
    ]
    
    start_id = len(df_atual) + 1
    for un_nome, un_key, custom in unidades_list:
        ambs = AREAS_DETALHADAS[un_key][custom]
        for amb_nome, (area_m2, mat_tipo) in ambs.items():
            pct_ja = calcular_pct_acumulado(df_atual, str_pav, un_nome, amb_nome)
            pct_rest = max(0.0, 100.0 - pct_ja)
            
            if pct_rest > 0:
                area_ef = (area_m2 * pct_rest) / 100.0
                novos.append({
                    "ID": start_id,
                    "Data": "2000-01-01",  # Data retroativa para não interferir nas análises do mês
                    "Equipe": "Nenhuma / Legado",
                    "Pavimento": str_pav,
                    "Unidade": un_nome,
                    "Ambiente": amb_nome,
                    "% Concluído": pct_rest,
                    "Área Executada (m²)": round(area_ef, 2),
                    "Peças Porcelanato": 0,
                    "Peças Cerâmica": 0,
                    "Sacos Argamassa (30kg)": 0
                })
                start_id += 1
                
    if novos:
        df_novo = pd.concat([df_atual, pd.DataFrame(novos)], ignore_index=True)
        salvar_dados(df_novo)
        st.sidebar.success(f"{str_pav} finalizado com sucesso!")
        st.rerun()
    else:
        st.sidebar.warning(f"{str_pav} já está 100% concluído.")

if not df_atual.empty:
    st.sidebar.markdown("---")
    csv = df_atual.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Exportar Dados (CSV)",
        data=csv,
        file_name=f"relatorio_porcelanato_{datetime.date.today()}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------------------------------------------------
# INTERFACE PRINCIPAL DE LANÇAMENTO
# ---------------------------------------------------------
st.title("🧱 Produção de Porcelanato")
st.subheader("📝 Registros Diários de Produção")

col1, col2 = st.columns(2)
with col1:
    data_reg = st.date_input("Data do Serviço", datetime.date.today())
    equipe_sel = st.selectbox("Equipe Responsável", LISTA_EQUIPES)

with col2:
    num_pav = st.selectbox("Pavimento", range(1, 22), format_func=lambda x: f"Pavimento {x:02d}")
    unidade_sel = st.selectbox("Unidade / Área", ["Apt A", "Apt B", "Apt B1", "Apt A1", "Circulação / WC Serviço"])

str_pavimento = f"Pavimento {num_pav:02d}"

if unidade_sel != "Circulação / WC Serviço":
    idx_map = {"Apt A": 0, "Apt B": 1, "Apt B1": 2, "Apt A1": 3}
    tipo_key = unidade_sel.replace("Apt ", "")
    customizacao = ELEVATION_MAP[num_pav][idx_map[unidade_sel]]
    st.info(f"💡 Tipologia Identificada: **{customizacao}**")
else:
    tipo_key = "CIRCULACAO"
    customizacao = "Padrão"

ambientes_dict = AREAS_DETALHADAS[tipo_key][customizacao]

tab1, tab2, tab3 = st.tabs(["✅ Ambientes Concluídos", "📐 Lançamento Parcial (%)", "🏢 Status dos Pavimentos"])

with tab1:
    st.markdown("##### Selecione os ambientes concluídos:")
    ambientes_100 = st.multiselect("Ambientes Finalizados", options=list(ambientes_dict.keys()))
    
    if ambientes_100:
        area_somada_100 = sum([ambientes_dict[a][0] for a in ambientes_100])
        st.success(f"**Área Total Selecionada:** `{area_somada_100:.2f} m²`")
        
        st.markdown("##### Quantidade de Peças por Ambiente:")
        pecas_dict = {}
        for amb in ambientes_100:
            mat_tipo = ambientes_dict[amb][1]
            pecas_dict[amb] = st.number_input(f"Peças para {amb} ({mat_tipo})", min_value=0, value=0, key=f"pecas_{amb}")
            
        st.markdown("##### Argamassa Utilizada no Dia:")
        sacos_dia_100 = st.number_input("Total de Sacos de Argamassa (30kg) no dia pela equipe", min_value=0, value=0, key="sacos_100_dia")
        
        if st.button("🚀 Salvar Lançamentos Totais", use_container_width=True):
            novos_registros = []
            start_id = len(df_atual) + 1
            
            for idx, amb in enumerate(ambientes_100):
                area_m2, mat_tipo = ambientes_dict[amb]
                pct_ja_feita = calcular_pct_acumulado(df_atual, str_pavimento, unidade_sel, amb)
                pct_restante = max(0.0, 100.0 - pct_ja_feita)
                area_efetiva = (area_m2 * pct_restante) / 100.0

                p_porc = pecas_dict[amb] if mat_tipo == "Porcelanato 70x70" else 0
                p_ceram = pecas_dict[amb] if mat_tipo == "Cerâmica 45x45" else 0
                
                arg_item = sacos_dia_100 if idx == 0 else 0

                novos_registros.append({
                    "ID": start_id,
                    "Data": data_reg.strftime('%Y-%m-%d'),
                    "Equipe": equipe_sel,
                    "Pavimento": str_pavimento,
                    "Unidade": unidade_sel,
                    "Ambiente": amb,
                    "% Concluído": round(pct_restante, 2),
                    "Área Executada (m²)": round(area_efetiva, 2),
                    "Peças Porcelanato": p_porc,
                    "Peças Cerâmica": p_ceram,
                    "Sacos Argamassa (30kg)": arg_item
                })
                start_id += 1
            
            df_novo = pd.concat([df_atual, pd.DataFrame(novos_registros)], ignore_index=True)
            salvar_dados(df_novo)
            st.success("Produção registrada com sucesso!")
            st.rerun()

with tab2:
    st.markdown("##### Lançamento Parcial do Ambiente:")
    amb_parcial = st.selectbox("Ambiente Parcial", options=list(ambientes_dict.keys()))
    
    area_tot_p, tipo_mat_p = ambientes_dict[amb_parcial]
    pct_ja_feita = calcular_pct_acumulado(df_atual, str_pavimento, unidade_sel, amb_parcial)
    pct_max_permitida = max(0.0, 100.0 - pct_ja_feita)

    st.write(f"**Área Total:** `{area_tot_p:.2f} m²` | **Material:** `{tipo_mat_p}` | **Já Executado:** `{pct_ja_feita:.2f}%`")
    
    if pct_max_permitida <= 0:
        st.warning("⚠️ Este ambiente já atingiu 100.00% de conclusão!")
    else:
        valor_padrao = min(50.0, float(pct_max_permitida))
        pct_parcial = st.number_input(
            f"Porcentagem Concluída Hoje (Máximo: {pct_max_permitida:.2f}%)", 
            min_value=1.0, 
            max_value=float(pct_max_permitida), 
            value=valor_padrao, 
            step=5.0
        )
        area_efetiva_p = (area_tot_p * pct_parcial) / 100.0
        st.info(f"**Área Parcial Calculada:** `{area_efetiva_p:.2f} m²`")
        
        c_p1, c_p2 = st.columns(2)
        pecas_p = c_p1.number_input(f"Quantidade de Peças ({tipo_mat_p})", min_value=0, value=0)
        sacos_p = c_p2.number_input("Total de Sacos de Argamassa (30kg) no Dia", min_value=0, value=0)
        
        p_porc_p = pecas_p if tipo_mat_p == "Porcelanato 70x70" else 0
        p_ceram_p = pecas_p if tipo_mat_p == "Cerâmica 45x45" else 0
        
        if st.button("🚀 Salvar Lançamento Parcial", use_container_width=True):
            novo_id = len(df_atual) + 1
            novo_reg = pd.DataFrame([{
                "ID": novo_id,
                "Data": data_reg.strftime('%Y-%m-%d'),
                "Equipe": equipe_sel,
                "Pavimento": str_pavimento,
                "Unidade": unidade_sel,
                "Ambiente": amb_parcial,
                "% Concluído": round(pct_parcial, 2),
                "Área Executada (m²)": round(area_efetiva_p, 2),
                "Peças Porcelanato": p_porc_p,
                "Peças Cerâmica": p_ceram_p,
                "Sacos Argamassa (30kg)": sacos_p
            }])
            
            df_novo = pd.concat([df_atual, novo_reg], ignore_index=True)
            salvar_dados(df_novo)
            st.success("Lançamento parcial salvo com sucesso!")
            st.rerun()

with tab3:
    st.markdown("### 🏢 Status dos Pavimentos")
    
    pav_summary = []
    for p in range(1, 22):
        str_p = f"Pavimento {p:02d}"
        area_teorica = calcular_area_pavimento_teorica(p)
        
        if not df_atual.empty:
            df_p = df_atual[df_atual["Pavimento"] == str_p]
            area_exec = df_p["Área Executada (m²)"].sum()
            eqs_validas = [eq for eq in df_p["Equipe"].unique() if eq != "Nenhuma / Legado"]
            equipes = ", ".join(eqs_validas) if eqs_validas else ("Concluído (Legado)" if "Nenhuma / Legado" in df_p["Equipe"].values else "Pendente")
        else:
            area_exec = 0.0
            equipes = "Pendente"
            
        pct_exec = min((area_exec / area_teorica) * 100, 100.0)
        
        pav_summary.append({
            "Pavimento": str_p,
            "Equipes Atuantes": equipes,
            "% Concluído": f"{pct_exec:.2f}%",
            "Área Executada": f"{area_exec:.2f} m² / {area_teorica:.2f} m²"
        })
        
    st.dataframe(pd.DataFrame(pav_summary), use_container_width=True)

# ---------------------------------------------------------
# PRODUÇÃO E INSUMOS
# ---------------------------------------------------------
st.markdown("---")
df = carregar_dados()

if not df.empty:
    st.header("📊 Produção e Insumos")
    
    tot_exec = df["Área Executada (m²)"].sum()
    pct_predio = (tot_exec / TOTAL_AREA_PREDIO) * 100
    tot_sacos = df["Sacos Argamassa (30kg)"].sum()
    tot_porc = df["Peças Porcelanato"].sum()
    tot_ceram = df["Peças Cerâmica"].sum()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avanço Geral do Prédio", f"{pct_predio:.2f}%")
    m2.metric("Produção Total", f"{tot_exec:.2f} m²")
    m3.metric("Peças Utilizadas", f"{tot_porc + tot_ceram:.0f} un")
    m4.metric("Argamassa Total", f"{tot_sacos:.0f} sacos")
    
    # ---------------------------------------------------------
    # RESUMO DE PEÇAS POR EQUIPE
    # ---------------------------------------------------------
    st.markdown("### 🧩 Consumo de Peças por Equipe")
    df_equipes_pecas = df[df["Equipe"] != "Nenhuma / Legado"].groupby("Equipe").agg(
        Porcelanato=("Peças Porcelanato", "sum"),
        Cerâmica=("Peças Cerâmica", "sum"),
        Area_Total=("Área Executada (m²)", "sum")
    ).reset_index()
    
    df_equipes_pecas["Area_Total"] = df_equipes_pecas["Area_Total"].map(lambda x: f"{x:.2f} m²")
    st.dataframe(df_equipes_pecas, use_container_width=True)

    # ---------------------------------------------------------
    # GRÁFICO DIÁRIO COM COR AZUL (>=20) E VERMELHO (<20)
    # ---------------------------------------------------------
    st.markdown("### 📈 Produção Diária (Meta: 20,00 m²/dia)")
    
    eq_filtro = st.radio("Filtrar Equipe no Gráfico", ["Todas"] + LISTA_EQUIPES, horizontal=True)
    df_graph = df[(df["Equipe"] == eq_filtro)] if eq_filtro != "Todas" else df[df["Equipe"] != "Nenhuma / Legado"]
    
    df_diario = df_graph.groupby("Data").agg(Area_Dia=("Área Executada (m²)", "sum")).reset_index()
    
    if not df_diario.empty:
        # Lógica de cor: Azul se >= 20, Vermelho se < 20
        df_diario["Cor"] = df_diario["Area_Dia"].apply(lambda x: "#1f77b4" if x >= 20.0 else "#d62728")
        max_y = max(df_diario["Area_Dia"].max() + 5, 25)
        
        fig = go.Figure()
        datas_formatadas = pd.to_datetime(df_diario["Data"]).dt.strftime('%d/%m/%Y')
        
        fig.add_trace(go.Bar(
            x=datas_formatadas,
            y=df_diario["Area_Dia"],
            marker_color=df_diario["Cor"],
            text=df_diario["Area_Dia"].apply(lambda x: f"<b>{x:.2f} m²</b>"),
            textposition="outside"
        ))
        
        fig.add_shape(
            type="line", x0=-0.5, x1=len(df_diario)-0.5, y0=20, y1=20,
            line=dict(color="black", width=2, dash="dash")
        )
        
        fig.update_layout(
            title=dict(text=f"<b>Desempenho Diário de Produção ({eq_filtro})</b>", font=dict(color="#004716", size=18)),
            xaxis_title="<b>Data</b>",
            yaxis_title="<b>Área Executada (m²)</b>",
            yaxis=dict(range=[0, max_y]),
            template="plotly_white",
            height=400,
            font=dict(color="#004716", size=13)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------
    # DIVISION DE TABELAS: DO DIA VS HISTÓRICO COMPLETO
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("📋 Tabelas de Lançamentos")
    
    dt_hoje_str = data_reg.strftime('%Y-%m-%d')
    
    def colorir_pavimentos(val):
        try:
            num = int(str(val).replace("Pavimento ", ""))
            cor = CORES_PAVIMENTOS[(num - 1) % len(CORES_PAVIMENTOS)]
            return f'background-color: {cor}; color: #000; font-weight: bold;'
        except:
            return ''

    # Tabela 1: Apensas Lançamentos do Dia Selecionado
    st.markdown(f"#### 📅 Lançamentos do Dia ({data_reg.strftime('%d/%m/%Y')})")
    df_hoje = df[df["Data"] == dt_hoje_str].copy()
    
    if not df_hoje.empty:
        df_hoje["Data"] = pd.to_datetime(df_hoje["Data"]).dt.strftime('%d/%m/%Y')
        df_hoje["% Concluído"] = df_hoje["% Concluído"].map(lambda x: f"{x:.2f}%")
        df_hoje["Área Executada (m²)"] = df_hoje["Área Executada (m²)"].map(lambda x: f"{x:.2f}")
        
        st.dataframe(df_hoje.sort_values(by="ID", ascending=False).style.map(colorir_pavimentos, subset=["Pavimento"]), use_container_width=True)
    else:
        st.info("Nenhum lançamento registrado nesta data.")

    # Tabela 2: Lançamentos Históricos Totais
    st.markdown("#### 📜 Histórico Geral de Lançamentos")
    df_exibicao = df.copy()
    df_exibicao["Data"] = pd.to_datetime(df_exibicao["Data"]).dt.strftime('%d/%m/%Y')
    df_exibicao["% Concluído"] = df_exibicao["% Concluído"].map(lambda x: f"{x:.2f}%")
    df_exibicao["Área Executada (m²)"] = df_exibicao["Área Executada (m²)"].map(lambda x: f"{x:.2f}")

    st.dataframe(df_exibicao.sort_values(by="ID", ascending=False).style.map(colorir_pavimentos, subset=["Pavimento"]), use_container_width=True)

    # ---------------------------------------------------------
    # PAINEL DE EXCLUSÃO DE LANÇAMENTOS
    # ---------------------------------------------------------
    st.markdown("##### 🗑️ Gerenciar e Apagar Lançamentos")
    c_del1, c_del2 = st.columns(2)
    
    with c_del1:
        st.markdown("**Apagar um Lançamento Específico:**")
        id_para_deletar = st.selectbox("Selecione o ID do Lançamento para Apagar", options=df_exibicao["ID"].tolist())
        if st.button("❌ Apagar Lançamento ID Selecionado"):
            df_novo = df[df["ID"] != id_para_deletar].reset_index(drop=True)
            salvar_dados(df_novo)
            st.success(f"Lançamento ID {id_para_deletar} removido com sucesso!")
            st.rerun()

    with c_del2:
        st.markdown("**Limpar Registros de Teste:**")
        if st.button("🔥 APAGAR TODOS OS DADOS"):
            salvar_dados(pd.DataFrame(columns=COLUNAS))
            st.warning("Todos os lançamentos foram apagados!")
            st.rerun()
