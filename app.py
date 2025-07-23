import streamlit as st
import math
from calculations import *
from constants import *
from ui_components import *

# Configuração da página
st.set_page_config(
    page_title="Touché | CDP",
    page_icon="📦"
)

# Interface principal
st.title("📦 Custo de produção | Touché")
st.markdown("---")

# Seção 1: Dados técnicos da caixa
# Número de caixas, tipo de caixa e estrutura em uma coluna
col1, col2, col3 = st.columns(3)
with col1:
    quantidade_caixas = st.number_input("Número de caixas", min_value=1, value=1, step=1)
with col2:
    tipo_tampa = st.selectbox(
        "Tipo da Caixa",
        ["Tampa Solta", "Tampa Livro", "Tampa Luva", "Tampa Imã", "Tampa Redonda"]
    )
with col3:
    estrutura = st.selectbox(
        "Tipo de Estrutura",
        ["Papelão", "Acrílico"],
        help="Papelão permite revestimentos, Acrílico não"
    )

# Dimensões baseadas no tipo de caixa
if tipo_tampa == "Tampa Redonda":
    col1, col2 = st.columns(2)
    with col1:
        raio = st.number_input("Raio (cm)", min_value=1.0, value=10.0, step=0.1)
        largura = raio * 2  # Diâmetro = 2 * raio
        altura = raio * 2   # Para caixas redondas, altura = diâmetro
    with col2:
        profundidade = st.number_input("Profundidade (cm)", min_value=1.0, value=10.0, step=0.1)
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        largura = st.number_input("Largura (cm)", min_value=1.0, value=20.0, step=0.1)
    with col2:
        altura = st.number_input("Altura (cm)", min_value=1.0, value=15.0, step=0.1)
    with col3:
        profundidade = st.number_input("Profundidade (cm)", min_value=1.0, value=10.0, step=0.1)

# Determinar colas automaticamente baseado na estrutura
colas_automaticas = determinar_colas_automaticas(estrutura, False)

# Revestimentos disponíveis baseados na estrutura
if estrutura == "Papelão":
    tipo_revestimento = st.selectbox(
        "Tipo de revestimento",
        ["Vinil UV", "Papel"],
        index=1,  # Papel pré-selecionado (índice 1)
        help="Vinil UV: +R\$140,00/m² | Papel: +R$15,00/m²"
    )
elif estrutura == "Acrílico":
    st.write("❌ **Nenhum revestimento** disponível para acrílico")
    tipo_revestimento = "Nenhum"

# Complexidade
tem_berco = st.checkbox(
    "Tem berço", 
    help="+30% do total"
)
tem_nicho = st.checkbox(
    "Nicho também", 
    help="+20% do total",
    disabled=not tem_berco
)

# Insumos gráficos
usar_serigrafia = st.checkbox(
    "Serigrafia",
    help="+R$ 1,01/cor/impressão",
)
num_cores_serigrafia = st.number_input("Nº de cores", min_value=1, value=1, disabled=not usar_serigrafia)
num_impressoes_serigrafia = st.number_input("Nº de impressões", min_value=1, value=1, disabled=not usar_serigrafia)

usar_impressao_digital = st.checkbox("Impressão digital")
tipo_impressao = st.selectbox(
    "Tipo de impressão",
    ["A4", "A3"],
    disabled=not usar_impressao_digital,
    help="A4: R$ 3,50 | A3: R$ 5,00"
)

# Fita e Rebites
metros_fita = st.number_input(
    "Fita (m)", 
    min_value=0.0, 
    value=0.0, 
    step=0.1,
    help="+R$ 0,627/m"
)
num_rebites = st.number_input(
    "Rebites (un)", 
    min_value=0, 
    value=0, 
    step=1,
    help="+R$ 0,10/un"
)

# Colas opcionais (apenas para papelão)
if estrutura == "Papelão":
    usar_cola_quente = st.checkbox(
        "Cola quente",
        help="+R$ 0,0125/caixa"
    )
    usar_cola_isopor = st.checkbox(
        "Cola de isopor",
        help="+R$ 0,015/caixa"
    )
else:
    usar_cola_quente = False
    usar_cola_isopor = False

# Seção de Custos Fixos
custos_fixos = display_fixed_costs_section()

# Cálculos
with st.expander("💰 Detalhamento de custos por unidade", expanded=True):
    # Cálculo da área baseado na estrutura
    if estrutura == "Papelão":
        # Calcular área de corte com desperdício baseada no tipo de tampa
        if tipo_tampa == "Tampa Solta":
            area_corte = calcular_planificacao_tampa_solta(largura, altura, profundidade)
            area_papelao = area_corte['area_base_mm2'] + area_corte['area_tampa_mm2']
        elif tipo_tampa == "Tampa Livro":
            area_corte = calcular_planificacao_tampa_livro(largura, altura, profundidade)
            area_papelao = area_corte['area_planificada_mm2']
        elif tipo_tampa == "Tampa Imã":
            area_corte = calcular_planificacao_tampa_ima(largura, altura, profundidade)
            area_papelao = area_corte['area_base_mm2'] + area_corte['area_tampa_mm2'] + area_corte['area_ima_mm2']
        elif tipo_tampa == "Tampa Luva":
            area_corte = calcular_planificacao_tampa_luva(largura, altura, profundidade)
            area_papelao = area_corte['area_base_mm2'] + area_corte['area_tampa_mm2'] + area_corte['area_aba_mm2']
        elif tipo_tampa == "Tampa Redonda":
            area_corte = calcular_planificacao_tampa_redonda(largura, altura, profundidade)
            area_papelao = area_corte['area_planificada_mm2']

        
        # Converter mm² para m² e calcular custo
        area_papelao_m2 = area_papelao / 1000000  # Converter mm² para m²
        custo_papelao = area_papelao_m2 * PRECO_PAPELAO_POR_M2
        custo_acrilico = 0
    elif estrutura == "Acrílico":
        area_papelao = 0
        custo_papelao = 0
        # Para acrílico, calculamos a área total da caixa
        area_total_acrilico = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
        custo_acrilico = calcular_custo_acrilico(largura, altura)  # Usando as dimensões principais

    # Custos variáveis
    custo_serigrafia = CUSTO_SERIGRAFIA_POR_COR * num_cores_serigrafia * num_impressoes_serigrafia if usar_serigrafia else 0
    custo_impressao = CUSTO_IMPRESSAO_A4 if (usar_impressao_digital and tipo_impressao == "A4") else (CUSTO_IMPRESSAO_A3 if (usar_impressao_digital and tipo_impressao == "A3") else 0)

    # Cálculo do custo de revestimento
    if estrutura == "Papelão":
        # Calcular área de revestimento baseada no tipo de tampa (multiplicar por 2: interno e externo)
        if tipo_tampa == "Tampa Solta":
            area_corte = calcular_planificacao_tampa_solta(largura, altura, profundidade)
            area_revestimento = area_corte['area_base_mm2'] + area_corte['area_tampa_mm2']
        elif tipo_tampa == "Tampa Livro":
            area_corte = calcular_planificacao_tampa_livro(largura, altura, profundidade)
            area_revestimento = area_corte['area_planificada_mm2']
        elif tipo_tampa == "Tampa Imã":
            area_corte = calcular_planificacao_tampa_ima(largura, altura, profundidade)
            area_revestimento = area_corte['area_base_mm2'] + area_corte['area_tampa_mm2'] + area_corte['area_ima_mm2']
        elif tipo_tampa == "Tampa Luva":
            area_corte = calcular_planificacao_tampa_luva(largura, altura, profundidade)
            area_revestimento = area_corte['area_base_mm2'] + area_corte['area_tampa_mm2'] + area_corte['area_aba_mm2']
        elif tipo_tampa == "Tampa Redonda":
            area_corte = calcular_planificacao_tampa_redonda(largura, altura, profundidade)
            area_revestimento = area_corte['area_planificada_mm2']

        
        # Multiplicar por 2 (interno e externo) e converter mm² para m²
        area_revestimento_m2 = (area_revestimento * 2) / 1000000  # Converter mm² para m²
        
        # Custos por m² para cada tipo de revestimento
        if tipo_revestimento == "Vinil UV":
            custo_revestimento = area_revestimento_m2 * CUSTO_VINIL_UV_POR_M2
        elif tipo_revestimento == "Papel":
            custo_revestimento = area_revestimento_m2 * CUSTO_PAPEL_POR_M2
        else:
            custo_revestimento = 0
    else:
        custo_revestimento = 0

    # Custos de cola baseados na estrutura
    if estrutura == "Papelão":
        # Calcular área de colagem PVA baseada no tipo de tampa (multiplicar por 2: ambos os lados)
        if tipo_tampa == "Tampa Solta":
            area_colagem = calcular_area_colagem_pva_tampa_solta(largura, altura, profundidade)
            area_colagem_total = area_colagem['area_colagem_total_mm2']
        elif tipo_tampa == "Tampa Livro":
            area_colagem = calcular_area_colagem_pva_tampa_livro(largura, altura, profundidade)
            area_colagem_total = area_colagem['area_colagem_total_mm2']
        elif tipo_tampa == "Tampa Imã":
            area_colagem = calcular_area_colagem_pva_tampa_ima(largura, altura, profundidade)
            area_colagem_total = area_colagem['area_colagem_total_mm2']
        elif tipo_tampa == "Tampa Luva":
            area_colagem = calcular_area_colagem_pva_tampa_luva(largura, altura, profundidade)
            area_colagem_total = area_colagem['area_colagem_total_mm2']
        elif tipo_tampa == "Tampa Redonda":
            area_colagem = calcular_area_colagem_pva_tampa_redonda(largura, altura, profundidade)
            area_colagem_total = area_colagem['area_colagem_total_mm2']

        
        # Multiplicar por 2 (ambos os lados do papelão) e converter mm² para m²
        area_colagem_m2 = (area_colagem_total * 2) / 1000000  # Converter mm² para m²
        ml_cola_total = area_colagem_m2 * ML_COLA_PVA_POR_M2
        
        custo_cola_pva = CUSTO_COLA_PVA * ml_cola_total
        
        # Calcular cola adesiva baseada no perímetro do papelão
        perimetro_papelao = calcular_perimetro_papelao(largura, altura, profundidade, tipo_tampa)
        ml_cola_adesiva_total = perimetro_papelao['perimetro_total_m'] * ML_COLA_ADESIVA_POR_M
        custo_cola_adesiva = CUSTO_COLA_ADESIVA * ml_cola_adesiva_total
        
        custo_cola_quente = CUSTO_COLA_QUENTE * ml_cola_total if usar_cola_quente else 0
        custo_cola_isopor = CUSTO_COLA_ISOPOR * ml_cola_total if usar_cola_isopor else 0
        custo_cola_acrilico = 0
    elif estrutura == "Acrílico":
        # Para acrílico, usar área da superfície
        area_acrilico = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
        ml_cola_por_cm2 = 0.01
        ml_cola_total = area_acrilico * ml_cola_por_cm2
        
        custo_cola_pva = 0
        custo_cola_adesiva = 0
        custo_cola_quente = 0
        custo_cola_isopor = 0
        custo_cola_acrilico = CUSTO_COLA_ACRILICO * ml_cola_total
    else:
        custo_cola_pva = 0
        custo_cola_adesiva = 0
        custo_cola_quente = 0
        custo_cola_isopor = 0
        custo_cola_acrilico = 0

    custo_fita = metros_fita * PRECO_FITA_POR_M
    custo_rebites = num_rebites * PRECO_REBITE_UNITARIO
    custo_ima_chapa = calcular_custo_ima_chapa_automatico(tipo_tampa, largura)
    
    # Calcular custo das caixas de papelão para embalar todas as caixas (apenas para o total do projeto)
    num_caixas_por_embalagem = calcular_max_caixas_por_embalagem(largura, altura, profundidade)
    if num_caixas_por_embalagem > 0:
        num_caixas_papelao_necessarias = math.ceil(quantidade_caixas / num_caixas_por_embalagem)
        custo_caixa_papelao_total = num_caixas_papelao_necessarias * PRECO_CAIXA_PAPELAO
    else:
        # Se a caixa é muito grande, cada caixa precisa de uma embalagem própria
        custo_caixa_papelao_total = quantidade_caixas * PRECO_CAIXA_PAPELAO
    
    # Para o custo unitário, não incluir embalagem
    custo_caixa_papelao = 0

    # Custos adicionais (só aplicados se há serigrafia)
    # Retardador, emulsão e cola permanente serão aplicados ao total do projeto, não por unidade
    custo_retardador = 0
    custo_emulsao = 0
    custo_cola_permanente = 0

    # Total de custos variáveis (sem embalagem e sem custos de serigrafia adicionais)
    total_custos_variaveis = (
        custo_papelao + custo_acrilico + custo_serigrafia + custo_impressao + 
        custo_revestimento + custo_cola_pva + custo_cola_adesiva + custo_cola_quente + custo_cola_isopor + 
        custo_cola_acrilico + custo_fita + custo_rebites + custo_ima_chapa
    )

    # Aplicar multiplicador de complexidade
    total_custos_variaveis_complexidade = aplicar_multiplicador_complexidade(
        total_custos_variaveis, tem_berco, tem_nicho
    )

    # Calcular custo fixo unitário baseado nos custos fixos mensais
    custo_fixo_unitario = custos_fixos['total_custos_fixos'] / CAIXAS_POR_MES

    # Custo final
    custo_final = custo_fixo_unitario + total_custos_variaveis_complexidade

    # Custo total do projeto (incluindo embalagem)
    custo_total_projeto = (custo_final * quantidade_caixas) + custo_caixa_papelao_total
    
    # Adicionar custos de serigrafia ao total do projeto (se há serigrafia)
    if usar_serigrafia:
        custo_total_projeto += CUSTO_COLA_PERMANENTE + CUSTO_RETARDADOR_VINILICO + CUSTO_EMULSAO_SENSIBILIZANTE

    # Exibir seções de custos
    custo_final_detalhado, custo_total_projeto_detalhado = display_cost_breakdown(estrutura, tipo_tampa, largura, altura, profundidade, quantidade_caixas,
                          usar_serigrafia, num_cores_serigrafia, num_impressoes_serigrafia,
                          usar_impressao_digital, tipo_impressao, tipo_revestimento,
                          tem_berco, tem_nicho, metros_fita, num_rebites,
                          usar_cola_quente, usar_cola_isopor, custos_fixos)

# Custo Total de Produção
st.markdown("### 🎯 Custo Total de Produção")
st.markdown(f"**Custo unitário:** R$ {custo_final_detalhado:.2f}")
st.markdown(f"**Custo total do projeto:** R$ {custo_total_projeto_detalhado:.2f}")