import datetime
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Gestão de Porcelanato e Cerâmica",
    layout="wide",
    page_icon="🏗️"
)

ARQUIVO_EXCEL = "dados_obra.xlsx"
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

# ---------------------------------------------------------
# PERSISTÊNCIA DOS DADOS E EQUIPES
# ---------------------------------------------------------
@st.cache_data(ttl=5)
def carregar_dados():
    if os.path.exists(ARQUIVO_EXCEL):
        df = pd.read_excel(ARQUIVO_EXCEL)
        # Formata a coluna Data estritamente como string YYYY-MM-DD
        df["Data"] = pd.to_datetime(df["Data"]).dt.strftime('%Y-%m-%d')
        return df
    else:
        return pd.DataFrame(columns=[
            "Data", "Equipe", "Pavimento", "Unidade", "Ambiente", 
            "% Concluído", "Área Executada (m²)", "Peças 70x70", 
            "Peças 45x45", "Sacos Argamassa", "Kg Argamassa"
        ])

def salvar_dados(df):
    df.to_excel(ARQUIVO_EXCEL, index=False)
    st.cache_data.clear()

def calcular_pct_acumulado(df, pavimento, unidade, ambiente):
    if df.empty:
        return 0.0
    filtro = (df["Pavimento"] == pavimento) & (df["Unidade"] == unidade) & (df["Ambiente"] == ambiente)
    return float(df[filtro]["% Concluído"].sum())

# Salvar nomes das equipes no Session State
if "eq1" not in st.session_state: st.session_state["eq1"] = "Equipe 1 - Pedro"
if "eq2" not in st.session_state: st.session_state["eq2"] = "Equipe 2 - João"
if "eq3" not in st.session_state: st.session_state["eq3"] = "Equipe 3 - Carlos"
if "eq4" not in st.session_state: st.session_state["eq4"] = "Equipe 4 - Lucas"

st.sidebar.header("⚙️ Nomes das Equipes")
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
# ATALHO PARA PAVIMENTOS JÁ CONCLUÍDOS NA BARRA LATERAL
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🏆 Concluir Pavimento Inteiro")

pav_pronto = st.sidebar.selectbox("Pavimento Concluído", range(1, 22), format_func=lambda x: f"Pavimento {x:02d}", key="pav_pronto_sel")
eq_pronto = st.sidebar.selectbox("Equipe Responsável", LISTA_EQUIPES, key="eq_pronto_sel")
dt_pronto = st.sidebar.date_input("Data de Conclusão", datetime.date.today(), key="dt_pronto_sel")

if st.sidebar.button("Marcar Pavimento 100% Concluído"):
    str_pav = f"Pavimento {pav_pronto:02d}"
    novos = []
    
    unidades_list = [
        ("Apt A", "A", ELEVATION_MAP[pav_pronto][0]),
        ("Apt B", "B", ELEVATION_MAP[pav_pronto][1]),
        ("Apt B1", "B1", ELEVATION_MAP[pav_pronto][2]),
        ("Apt A1", "A1", ELEVATION_MAP[pav_pronto][3]),
        ("Circulação / WC Serviço", "CIRCULACAO", "Padrão")
    ]
    
    for un_nome, un_key, custom in unidades_list:
        ambs = AREAS_DETALHADAS[un_key][custom]
        for amb_nome, (area_m2, mat_tipo) in ambs.items():
            pct_ja = calcular_pct_acumulado(df_atual, str_pav, un_nome, amb_nome)
            pct_rest = max(0.0, 100.0 - pct_ja)
            
            if pct_rest > 0:
                area_ef = (area_m2 * pct_rest) / 100.0
                novos.append({
                    "Data": dt_pronto.strftime('%Y-%m-%d'),
                    "Equipe": eq_pronto,
                    "Pavimento": str_pav,
                    "Unidade": un_nome,
                    "Ambiente": amb_nome,
                    "% Concluído": pct_rest,
                    "Área Executada (m²)": area_ef,
                    "Peças 70x70": 0,
                    "Peças 45x45": 0,
                    "Sacos Argamassa": 0,
                    "Kg Argamassa": 0
                })
                
    if novos:
        df_novo = pd.concat([df_atual, pd.DataFrame(novos)], ignore_index=True)
        salvar_dados(df_novo)
        st.sidebar.success(f"{str_pav} marcado como 100% concluído!")
        st.rerun()
    else:
        st.sidebar.warning(f"{str_pav} já possui 100% dos lançamentos salvos.")

if not df_atual.empty:
    st.sidebar.markdown("---")
    st.sidebar.header("📥 Relatório")
    csv = df_atual.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Exportar para CSV",
        data=csv,
        file_name=f"relatorio_obra_{datetime.date.today()}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------------------------------------------------
# INTERFACE DE LANÇAMENTO DIÁRIO
# ---------------------------------------------------------
st.title("🏗️ Gestão de Porcelanato e Cerâmica")
st.subheader("📝 Lançamento Diário de Produção")

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

tab1, tab2 = st.tabs(["✅ Ambientes Concluídos", "📐 Lançamento Parcial (%)"])

with tab1:
    st.markdown("##### Selecione os ambientes que foram finalizados totalmente (ou o restante):")
    ambientes_100 = st.multiselect("Ambientes Concluídos", options=list(ambientes_dict.keys()))
    
    if ambientes_100:
        area_somada_100 = sum([ambientes_dict[a][0] for a in ambientes_100])
        st.success(f"**Área Total Selecionada:** `{area_somada_100:.2f} m²`")
        
        st.markdown("**Insumos Utilizados no Lançamento:**")
        c1, c2, c3 = st.columns(3)
        p70_100 = c1.number_input("Peças Porcelanato 70x70", min_value=0, value=0, key="p70_100")
        p45_100 = c2.number_input("Peças Cerâmica 45x45", min_value=0, value=0, key="p45_100")
        sacos_100 = c3.number_input("Sacos Argamassa (30kg)", min_value=0, value=0, key="sacos_100")
        
        if st.button("🚀 Salvar Lançamento Total", use_container_width=True):
            novos_registros = []
            
            ambs_porcelanato = [a for a in ambientes_100 if ambientes_dict[a][1] == "Porcelanato 70x70"]
            ambs_ceramica = [a for a in ambientes_100 if ambientes_dict[a][1] == "Cerâmica 45x45"]
            
            qtd_porc = len(ambs_porcelanato)
            qtd_ceram = len(ambs_ceramica)
            qtd_tot = len(ambientes_100)
            
            for amb in ambientes_100:
                area_m2, mat_tipo = ambientes_dict[amb]
                pct_ja_feita = calcular_pct_acumulado(df_atual, str_pavimento, unidade_sel, amb)
                pct_restante = max(0.0, 100.0 - pct_ja_feita)
                area_efetiva = (area_m2 * pct_restante) / 100.0

                p70_item = (p70_100 / qtd_porc) if (mat_tipo == "Porcelanato 70x70" and qtd_porc > 0) else 0
                p45_item = (p45_100 / qtd_ceram) if (mat_tipo == "Cerâmica 45x45" and qtd_ceram > 0) else 0
                sacos_item = sacos_100 / qtd_tot if qtd_tot > 0 else 0

                novos_registros.append({
                    "Data": data_reg.strftime('%Y-%m-%d'),
                    "Equipe": equipe_sel,
                    "Pavimento": str_pavimento,
                    "Unidade": unidade_sel,
                    "Ambiente": amb,
                    "% Concluído": pct_restante,
                    "Área Executada (m²)": area_efetiva,
                    "Peças 70x70": p70_item,
                    "Peças 45x45": p45_item,
                    "Sacos Argamassa": sacos_item,
                    "Kg Argamassa": sacos_item * 30
                })
            
            df_novo = pd.concat([df_atual, pd.DataFrame(novos_registros)], ignore_index=True)
            salvar_dados(df_novo)
            st.success("Lançamento concluído com sucesso!")
            st.rerun()

with tab2:
    st.markdown("##### Selecione um ambiente para informar o progresso diário:")
    amb_parcial = st.selectbox("Ambiente Parcial", options=list(ambientes_dict.keys()))
    
    area_tot_p, tipo_mat_p = ambientes_dict[amb_parcial]
    pct_ja_feita = calcular_pct_acumulado(df_atual, str_pavimento, unidade_sel, amb_parcial)
    pct_max_permitida = max(0.0, 100.0 - pct_ja_feita)

    st.write(f"**Área Total:** `{area_tot_p:.2f} m²` | **Material:** `{tipo_mat_p}` | **Já Executado:** `{pct_ja_feita:.1f}%`")
    
    if pct_max_permitida <= 0:
        st.warning("⚠️ Este ambiente já atingiu 100% de conclusão!")
    else:
        valor_padrao = min(50.0, float(pct_max_permitida))
        pct_parcial = st.number_input(
            f"Porcentagem Concluída Hoje (Resta no máximo {pct_max_permitida:.1f}%)", 
            min_value=1.0, 
            max_value=float(pct_max_permitida), 
            value=valor_padrao, 
            step=5.0
        )
        area_efetiva_p = (area_tot_p * pct_parcial) / 100.0
        st.info(f"**Área Parcial Calculada:** `{area_efetiva_p:.2f} m²`")
        
        st.markdown("**Insumos Utilizados Hoje:**")
        cp1, cp2, cp3 = st.columns(3)
        
        p70_p = cp1.number_input("Peças Porcelanato 70x70", min_value=0, value=0, disabled=(tipo_mat_p != "Porcelanato 70x70"))
        p45_p = cp2.number_input("Peças Cerâmica 45x45", min_value=0, value=0, disabled=(tipo_mat_p != "Cerâmica 45x45"))
        sacos_p = cp3.number_input("Sacos Argamassa (30kg)", min_value=0, value=0)
        
        if st.button("🚀 Salvar Lançamento Parcial", use_container_width=True):
            novo_reg = pd.DataFrame([{
                "Data": data_reg.strftime('%Y-%m-%d'),
                "Equipe": equipe_sel,
                "Pavimento": str_pavimento,
                "Unidade": unidade_sel,
                "Ambiente": amb_parcial,
                "% Concluído": pct_parcial,
                "Área Executada (m²)": area_efetiva_p,
                "Peças 70x70": p70_p,
                "Peças 45x45": p45_p,
                "Sacos Argamassa": sacos_p,
                "Kg Argamassa": sacos_p * 30
            }])
            
            df_novo = pd.concat([df_atual, novo_reg], ignore_index=True)
            salvar_dados(df_novo)
            st.success("Lançamento parcial salvo com sucesso!")
            st.rerun()

# ---------------------------------------------------------
# PAINEL DE MÉTRICAS E GRÁFICOS
# ---------------------------------------------------------
st.markdown("---")
st.header("📊 Dashboard de Produção e Consumos")

df = carregar_dados()

if not df.empty:
    df_dt_parsed = pd.to_datetime(df["Data"])
    
    tot_exec = df["Área Executada (m²)"].sum()
    pct_predio = (tot_exec / TOTAL_AREA_PREDIO) * 100
    tot_kg = df["Kg Argamassa"].sum()
    
    media_tradicional = (tot_exec / tot_kg) if tot_kg > 0 else 0
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avanço Geral do Prédio", f"{pct_predio:.2f}%")
    m2.metric("Área Executada Total", f"{tot_exec:.2f} m²")
    m3.metric("Média Argamassa (Tradicional)", f"{media_tradicional:.3f} m²/kg")
    m4.metric("Argamassa Total Utilizada", f"{tot_kg:.0f} kg")
    
    # ---------------------------------------------------------
    # GRÁFICO COMPARATIVO
    # ---------------------------------------------------------
    st.subheader("⚔️ Comparativo de Produção das Equipes (Hoje vs. Média do Mês)")
    
    data_sel_comp = st.date_input("Selecione o Dia para Comparação", datetime.date.today())
    dt_str = data_sel_comp.strftime('%Y-%m-%d')
    dt_comp = pd.to_datetime(data_sel_comp)
    
    df_mes = df[(df_dt_parsed.dt.year == dt_comp.year) & (df_dt_parsed.dt.month == dt_comp.month)]
    
    df_dia_eq = df[df["Data"] == dt_str].groupby("Equipe")["Área Executada (m²)"].sum()
    
    dias_trabalhados = df_mes.groupby(["Equipe", "Data"])["Área Executada (m²)"].sum().reset_index()
    df_media_eq = dias_trabalhados.groupby("Equipe")["Área Executada (m²)"].mean()
    
    prod_hoje_list = []
    media_mes_list = []
    
    for eq in LISTA_EQUIPES:
        prod_hoje_list.append(df_dia_eq.get(eq, 0.0))
        media_mes_list.append(df_media_eq.get(eq, 0.0))
        
    fig_comp = go.Figure()
    
    fig_comp.add_trace(go.Bar(
        x=LISTA_EQUIPES,
        y=prod_hoje_list,
        name="Produção Hoje (m²)",
        marker_color="#1f77b4",
        text=[f"{v:.1f} m²" for v in prod_hoje_list],
        textposition="outside"
    ))
    
    fig_comp.add_trace(go.Bar(
        x=LISTA_EQUIPES,
        y=media_mes_list,
        name="Média Diária no Mês (m²)",
        marker_color="#7f7f7f",
        text=[f"{v:.1f} m²" for v in media_mes_list],
        textposition="outside"
    ))
    
    fig_comp.add_shape(
        type="line", x0=-0.5, x1=len(LISTA_EQUIPES)-0.5, y0=20, y1=20,
        line=dict(color="orange", width=2, dash="dash")
    )
    
    fig_comp.update_layout(
        barmode='group',
        title=f"Comparativo por Equipe em {dt_comp.strftime('%d/%m/%Y')}",
        xaxis_title="Equipe",
        yaxis_title="Área Executada (m²)",
        template="plotly_white",
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)

    # ---------------------------------------------------------
    # AVANÇO POR PAVIMENTO
    # ---------------------------------------------------------
    st.subheader("🏢 Percentual de Avanço por Pavimento")
    pav_sel = st.selectbox("Selecione o Pavimento para Análise", range(1, 22), format_func=lambda x: f"Pavimento {x:02d}")
    
    area_pav_teorica = 52.90
    for idx, u in enumerate(["Apt A", "Apt B", "Apt B1", "Apt A1"]):
        cust = ELEVATION_MAP[pav_sel][idx]
        key = u.replace("Apt ", "")
        area_pav_teorica += sum([v[0] for v in AREAS_DETALHADAS[key][cust].values()])
        
    exec_pav = df[df["Pavimento"] == f"Pavimento {pav_sel:02d}"]["Área Executada (m²)"].sum()
    pct_pav = (exec_pav / area_pav_teorica) * 100
    
    st.progress(min(pct_pav / 100.0, 1.0))
    st.caption(f"Concluído: **{pct_pav:.2f}%** ({exec_pav:.2f} m² de {area_pav_teorica:.2f} m²)")
    
    # ---------------------------------------------------------
    # HISTÓRICO DIÁRIO
    # ---------------------------------------------------------
    st.subheader("📈 Produção Diária (Meta de 20 m²/dia)")
    
    eq_filtro = st.radio("Filtrar Análise Por Equipe", ["Todas"] + LISTA_EQUIPES, horizontal=True)
    df_graph = df if eq_filtro == "Todas" else df[df["Equipe"] == eq_filtro]
    
    df_diario = df_graph.groupby("Data").agg(
        Area_Dia=("Área Executada (m²)", "sum")
    ).reset_index()
    
    if not df_diario.empty:
        df_diario["Cor"] = df_diario["Area_Dia"].apply(lambda x: "#2ca02c" if x >= 20 else "#d62728")
        media_dia = df_diario["Area_Dia"].mean()
        
        st.info(f"Média diária de produção da seleção: **{media_dia:.2f} m²/dia**")
        
        max_y = max(df_diario["Area_Dia"].max() + 4, 26)
        
        fig = go.Figure()
        
        datas_formatadas = pd.to_datetime(df_diario["Data"]).dt.strftime('%d/%m/%Y')
        
        fig.add_trace(go.Bar(
            x=datas_formatadas,
            y=df_diario["Area_Dia"],
            marker_color=df_diario["Cor"],
            text=df_diario["Area_Dia"].apply(lambda x: f"{x:.1f} m²"),
            textposition="outside"
        ))
        
        fig.add_shape(
            type="line", x0=-0.5, x1=len(df_diario)-0.5, y0=20, y1=20,
            line=dict(color="orange", width=3, dash="dash")
        )
        
        fig.update_layout(
            title=f"Desempenho Diário ({eq_filtro})",
            xaxis_title="Data de Trabalho",
            yaxis_title="Área Executada (m²)",
            yaxis=dict(tick0=0, dtick=2, range=[0, max_y]),
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Tabela de Lançamentos e Exclusão")
    
    # Formata a data para exibir na tabela sem o horário (DD/MM/YYYY)
    df_exibicao = df.copy()
    df_exibicao["Data"] = pd.to_datetime(df_exibicao["Data"]).dt.strftime('%d/%m/%Y')
    
    st.dataframe(df_exibicao.sort_values(by="Data", ascending=False), use_container_width=True)

    with st.expander("🗑️ Excluir Último Lançamento (Correção)"):
        if st.button("Remover Última Linha Registrada"):
            df_restr = df.drop(df.index[-1])
            salvar_dados(df_restr)
            st.warning("Último lançamento removido com sucesso!")
            st.rerun()