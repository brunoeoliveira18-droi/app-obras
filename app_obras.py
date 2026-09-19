import datetime
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Gestão de Porcelanato e Cerâmica", layout="wide")

ARQUIVO_EXCEL = "dados_obra.xlsx"

# 1. FACHADÁRIO E MAPEAMENTO EXATO DA PLANILHA
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

TOTAL_AREA_PREDIO = 5135.44

def carregar_dados():
    if os.path.exists(ARQUIVO_EXCEL):
        return pd.read_excel(ARQUIVO_EXCEL)
    else:
        return pd.DataFrame(columns=[
            "Data", "Equipe", "Pavimento", "Unidade", "Ambiente", 
            "% Concluído", "Área Executada (m²)", "Peças 70x70", 
            "Peças 45x45", "Sacos Argamassa", "Kg Argamassa"
        ])

def salvar_dados(df):
    df.to_excel(ARQUIVO_EXCEL, index=False)

# 2. CONFIGURAÇÃO DE EQUIPES
st.sidebar.header("⚙️ Nomes das Equipes")
eq1 = st.sidebar.text_input("Equipe 1", "Equipe 1 - Pedro")
eq2 = st.sidebar.text_input("Equipe 2", "Equipe 2 - João")
eq3 = st.sidebar.text_input("Equipe 3", "Equipe 3 - Carlos")
eq4 = st.sidebar.text_input("Equipe 4", "Equipe 4 - Lucas")

LISTA_EQUIPES = [eq1, eq2, eq3, eq4]

# 3. INTERFACE DE LANÇAMENTO
st.title("📱 Acompanhamento de Assentamento")
st.subheader("📝 Lançamento Diário de Produção")

col1, col2 = st.columns(2)
with col1:
    data_reg = st.date_input("Data do Serviço", datetime.date.today())
    equipe_sel = st.selectbox("Equipe Responsável", LISTA_EQUIPES)

with col2:
    num_pav = st.selectbox("Pavimento", range(1, 22), format_func=lambda x: f"Pavimento {x:02d}")
    unidade_sel = st.selectbox("Unidade / Área", ["Apt A", "Apt B", "Apt B1", "Apt A1", "Circulação / WC Serviço"])

if unidade_sel != "Circulação / WC Serviço":
    idx_map = {"Apt A": 0, "Apt B": 1, "Apt B1": 2, "Apt A1": 3}
    tipo_key = unidade_sel.replace("Apt ", "")
    customizacao = ELEVATION_MAP[num_pav][idx_map[unidade_sel]]
    st.info(f"💡 Tipologia Identificada: **{customizacao}**")
else:
    tipo_key = "CIRCULACAO"
    customizacao = "Padrão"

ambientes_dict = AREAS_DETALHADAS[tipo_key][customizacao]

tab1, tab2 = st.tabs(["✅ Ambientes 100% Concluídos", "📐 Lançamento Parcial (%)"])

with tab1:
    st.markdown("##### Selecione um ou mais ambientes concluídos totalmente:")
    ambientes_100 = st.multiselect("Ambientes 100%", options=list(ambientes_dict.keys()))
    
    if ambientes_100:
        area_somada_100 = sum([ambientes_dict[a][0] for a in ambientes_100])
        st.success(f"**Área Total Selecionada (100%):** `{area_somada_100:.2f} m²`")
        
        st.markdown("**Insumos Utilizados (Total da Seleção):**")
        c1, c2, c3 = st.columns(3)
        p70_100 = c1.number_input("Peças Porcelanato 70x70", min_value=0, value=0, key="p70_100")
        p45_100 = c2.number_input("Peças Cerâmica 45x45", min_value=0, value=0, key="p45_100")
        sacos_100 = c3.number_input("Sacos Argamassa (30kg)", min_value=0, value=0, key="sacos_100")
        
        if st.button("🚀 Salvar Lançamento (100%)", use_container_width=True):
            df_ant = carregar_dados()
            novos_registros = []
            
            for amb in ambientes_100:
                area_m2, _ = ambientes_dict[amb]
                novos_registros.append({
                    "Data": data_reg,
                    "Equipe": equipe_sel,
                    "Pavimento": f"Pavimento {num_pav:02d}",
                    "Unidade": unidade_sel,
                    "Ambiente": amb,
                    "% Concluído": 100.0,
                    "Área Executada (m²)": area_m2,
                    "Peças 70x70": p70_100 / len(ambientes_100),
                    "Peças 45x45": p45_100 / len(ambientes_100),
                    "Sacos Argamassa": sacos_100 / len(ambientes_100),
                    "Kg Argamassa": (sacos_100 * 30) / len(ambientes_100)
                })
            
            df_novo = pd.concat([df_ant, pd.DataFrame(novos_registros)], ignore_index=True)
            salvar_dados(df_novo)
            st.success("Lançamento de 100% concluído com sucesso!")
            st.rerun()

with tab2:
    st.markdown("##### Selecione apenas um ambiente para informar a % feita:")
    amb_parcial = st.selectbox("Ambiente Parcial", options=list(ambientes_dict.keys()))
    
    area_tot_p, tipo_mat_p = ambientes_dict[amb_parcial]
    st.write(f"**Área Total do Ambiente:** `{area_tot_p:.2f} m²` | **Material:** `{tipo_mat_p}`")
    
    pct_parcial = st.number_input("Digite a Porcentagem Concluída Hoje (%)", min_value=1.0, max_value=99.0, value=50.0, step=5.0)
    area_efetiva_p = (area_tot_p * pct_parcial) / 100.0
    st.info(f"**Área Parcial Calculada:** `{area_efetiva_p:.2f} m²`")
    
    st.markdown("**Insumos Utilizados Hoje:**")
    cp1, cp2, cp3 = st.columns(3)
    p70_p = cp1.number_input("Peças Porcelanato 70x70", min_value=0, value=0, key="p70_p")
    p45_p = cp2.number_input("Peças Cerâmica 45x45", min_value=0, value=0, key="p45_p")
    sacos_p = cp3.number_input("Sacos Argamassa (30kg)", min_value=0, value=0, key="sacos_p")
    
    if st.button("🚀 Salvar Lançamento Parcial", use_container_width=True):
        df_ant = carregar_dados()
        novo_reg = pd.DataFrame([{
            "Data": data_reg,
            "Equipe": equipe_sel,
            "Pavimento": f"Pavimento {num_pav:02d}",
            "Unidade": unidade_sel,
            "Ambiente": amb_parcial,
            "% Concluído": pct_parcial,
            "Área Executada (m²)": area_efetiva_p,
            "Peças 70x70": p70_p,
            "Peças 45x45": p45_p,
            "Sacos Argamassa": sacos_p,
            "Kg Argamassa": sacos_p * 30
        }])
        
        df_novo = pd.concat([df_ant, novo_reg], ignore_index=True)
        salvar_dados(df_novo)
        st.success("Lançamento parcial concluído com sucesso!")
        st.rerun()

# 4. PAINEL DE MÉTRICAS E GRÁFICOS
st.markdown("---")
st.header("📊 Painel de Controle de Produção e Consumos")

df = carregar_dados()

if not df.empty:
    df["Data"] = pd.to_datetime(df["Data"])
    
    tot_exec = df["Área Executada (m²)"].sum()
    pct_predio = (tot_exec / TOTAL_AREA_PREDIO) * 100
    tot_kg = df["Kg Argamassa"].sum()
    cons_arg = (tot_kg / tot_exec) if tot_exec > 0 else 0
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avanço Geral do Prédio", f"{pct_predio:.2f}%")
    m2.metric("Área Executada Total", f"{tot_exec:.2f} m²")
    m3.metric("Consumo Médio Argamassa", f"{cons_arg:.2f} kg/m²")
    m4.metric("Argamassa Total Gastos", f"{tot_kg:.0f} kg")
    
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
    
    st.subheader("📈 Produção Diária (Graduação de 2 em 2 m²)")
    
    eq_filtro = st.radio("Filtrar Análise Por Equipe", ["Todas"] + LISTA_EQUIPES, horizontal=True)
    df_graph = df if eq_filtro == "Todas" else df[df["Equipe"] == eq_filtro]
    
    df_diario = df_graph.groupby("Data").agg(
        Area_Dia=("Área Executada (m²)", "sum"),
        Pec_70=("Peças 70x70", "sum"),
        Pec_45=("Peças 45x45", "sum")
    ).reset_index()
    
    if not df_diario.empty:
        df_diario["Cor"] = df_diario["Area_Dia"].apply(lambda x: "#1f77b4" if x >= 20 else "#d62728")
        media_dia = df_diario["Area_Dia"].mean()
        
        st.info(f"Média diária de produção da seleção: **{media_dia:.2f} m²/dia**")
        
        max_y = max(df_diario["Area_Dia"].max() + 4, 26)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_diario["Data"].dt.strftime('%d/%m/%Y'),
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
            title=f"Desempenho Diário ({eq_filtro}) - Graduação de 2 em 2 m²",
            xaxis_title="Data de Trabalho",
            yaxis_title="Área Executada (m²)",
            yaxis=dict(tick0=0, dtick=2, range=[0, max_y]),
            template="plotly_white",
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Tabela de Lançamentos")
    st.dataframe(df.sort_values(by="Data", ascending=False), use_container_width=True)