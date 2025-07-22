import streamlit as st
import math
from calculations import *
from constants import *

def display_fixed_costs_section():
    """Exibe a seção de custos fixos"""
    with st.expander("🏢 Custos Fixos", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Custos Operacionais**")
            tecnoponto = st.number_input("Tecnoponto", value=147.90, step=0.01)
            alarme = st.number_input("Alarme", value=180.00, step=0.01)
            aluguel = st.number_input("Aluguel", value=3019.67, step=0.01)
            energia = st.number_input("Energia (média)", value=1076.49, step=0.01)
            agua = st.number_input("Água (média)", value=181.76, step=0.01)
            vale_refeicao = st.number_input("Vale-refeição", value=1320.00, step=0.01)
            vale_transporte = st.number_input("Vale-transporte (média)", value=969.65, step=0.01)
            combustivel = st.number_input("Combustível", value=250.00, step=0.01)

        with col2:
            st.markdown("**Custos Administrativos**")
            inss = st.number_input("INSS (média)", value=792.68, step=0.01)
            fgts = st.number_input("FGTS (média)", value=826.02, step=0.01)
            das = st.number_input("DAS (média)", value=1373.00, step=0.01)
            cim_tlf_tvs = st.number_input("CIM/TLF/TVS", value=400.00, step=0.01)
            fronteira = st.number_input("Fronteira (média)", value=885.80, step=0.01)
            contabilidade = st.number_input("Contabilidade", value=600.00, step=0.01)
            marketing = st.number_input("Marketing", value=2200.00, step=0.01)
            juridico = st.number_input("Jurídico", value=1000.00, step=0.01)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Custos de Tecnologia**")
            adobe = st.number_input("Adobe", value=208.00, step=0.01)
            meli_plus = st.number_input("Meli+", value=8.90, step=0.01)
            kommo = st.number_input("Kommo", value=85.19, step=0.01)
            internet = st.number_input("Internet", value=105.00, step=0.01)

        with col4:
            st.markdown("**Custos de Pessoal**")
            financeiro = st.number_input("Financeiro", value=800.00, step=0.01)
            folha = st.number_input("Folha (média)", value=10489.60, step=0.01)

        # Calcular total dos custos fixos
        total_custos_fixos = (
            tecnoponto + alarme + aluguel + energia + agua + vale_refeicao + vale_transporte + combustivel +
            inss + fgts + das + cim_tlf_tvs + fronteira + contabilidade + marketing + juridico +
            adobe + meli_plus + kommo + internet + financeiro + folha
        )

        st.markdown(f"**💰 Total dos Custos Fixos Mensais: R$ {total_custos_fixos:.2f}**")
        
        return {
            'tecnoponto': tecnoponto,
            'alarme': alarme,
            'aluguel': aluguel,
            'energia': energia,
            'agua': agua,
            'vale_refeicao': vale_refeicao,
            'vale_transporte': vale_transporte,
            'combustivel': combustivel,
            'inss': inss,
            'fgts': fgts,
            'das': das,
            'cim_tlf_tvs': cim_tlf_tvs,
            'fronteira': fronteira,
            'contabilidade': contabilidade,
            'marketing': marketing,
            'juridico': juridico,
            'adobe': adobe,
            'meli_plus': meli_plus,
            'kommo': kommo,
            'internet': internet,
            'financeiro': financeiro,
            'folha': folha,
            'total_custos_fixos': total_custos_fixos
        }

def display_planification_section(estrutura, tipo_tampa, largura, altura, profundidade, quantidade_caixas):
    """Exibe a seção de planificação de chapas"""
    if estrutura == "Papelão":
        if tipo_tampa == "Tampa Solta":
            planificacao = calcular_planificacao_tampa_solta(largura, altura, profundidade)
            
            # Verificar se caixas_por_chapa é maior que zero para evitar divisão por zero
            if planificacao['caixas_por_chapa'] > 0:
                chapas_necessarias = math.ceil(quantidade_caixas / planificacao['caixas_por_chapa'])
            else:
                chapas_necessarias = quantidade_caixas  # Uma chapa por caixa se não couber nenhuma
            
            st.markdown("### 📐 Planificação de Chapas de Papelão (Tampa Solta)")
            st.markdown(f"**Dimensões da chapa:** 1040mm × 860mm")
            st.markdown(f"**Base planificada:** {planificacao['dimensoes_base'][0]:.0f}mm × {planificacao['dimensoes_base'][1]:.0f}mm")
            st.markdown(f"**Tampa planificada:** {planificacao['dimensoes_tampa'][0]:.0f}mm × {planificacao['dimensoes_tampa'][1]:.0f}mm")
            st.markdown(f"**Área da base:** {planificacao['area_base_mm2']/100:.1f} cm²")
            st.markdown(f"**Área da tampa:** {planificacao['area_tampa_mm2']/100:.1f} cm²")
            st.markdown(f"**Caixas por chapa:** {planificacao['caixas_por_chapa']}")
            st.markdown(f"**Chapas necessárias:** {chapas_necessarias}")
        
        elif tipo_tampa == "Tampa Livro":
            planificacao_livro = calcular_planificacao_tampa_livro(largura, altura, profundidade)
            
            # Verificar se caixas_por_chapa é maior que zero para evitar divisão por zero
            if planificacao_livro['caixas_por_chapa'] > 0:
                chapas_necessarias_livro = math.ceil(quantidade_caixas / planificacao_livro['caixas_por_chapa'])
            else:
                chapas_necessarias_livro = quantidade_caixas  # Uma chapa por caixa se não couber nenhuma
            
            st.markdown("### 📐 Planificação de Chapas de Papelão (Tampa-Livro)")
            st.markdown(f"**Dimensões da chapa:** 1040mm × 860mm")
            st.markdown(f"**Largura planificada:** {planificacao_livro['dimensoes_planificacao'][0]:.0f}mm")
            st.markdown(f"**Altura planificada:** {planificacao_livro['dimensoes_planificacao'][1]:.0f}mm")
            st.markdown(f"**Área planificada:** {planificacao_livro['area_planificada_mm2']/100:.1f} cm²")
            st.markdown(f"**Colunas por chapa:** {planificacao_livro['colunas_por_chapa']}")
            st.markdown(f"**Linhas por chapa:** {planificacao_livro['linhas_por_chapa']}")
            st.markdown(f"**Caixas por chapa:** {planificacao_livro['caixas_por_chapa']}")
            st.markdown(f"**Chapas necessárias:** {chapas_necessarias_livro}")
        
        elif tipo_tampa == "Tampa Imã":
            planificacao_ima = calcular_planificacao_tampa_ima(largura, altura, profundidade)
            
            # Verificar se caixas_por_chapa é maior que zero para evitar divisão por zero
            if planificacao_ima['caixas_por_chapa'] > 0:
                chapas_necessarias_ima = math.ceil(quantidade_caixas / planificacao_ima['caixas_por_chapa'])
            else:
                chapas_necessarias_ima = quantidade_caixas  # Uma chapa por caixa se não couber nenhuma
            
            st.markdown("### 📐 Planificação de Chapas de Papelão (Tampa-Imã)")
            st.markdown(f"**Dimensões da chapa:** 1040mm × 860mm")
            st.markdown(f"**Base planificada:** {planificacao_ima['dimensoes_base'][0]:.0f}mm × {planificacao_ima['dimensoes_base'][1]:.0f}mm")
            st.markdown(f"**Tampa planificada:** {planificacao_ima['dimensoes_tampa'][0]:.0f}mm × {planificacao_ima['dimensoes_tampa'][1]:.0f}mm")
            st.markdown(f"**Área para imã:** {planificacao_ima['dimensoes_ima'][0]:.0f}mm × {planificacao_ima['dimensoes_ima'][1]:.0f}mm")
            st.markdown(f"**Área da base:** {planificacao_ima['area_base_mm2']/100:.1f} cm²")
            st.markdown(f"**Área da tampa:** {planificacao_ima['area_tampa_mm2']/100:.1f} cm²")
            st.markdown(f"**Área do imã:** {planificacao_ima['area_ima_mm2']/100:.1f} cm²")
            st.markdown(f"**Caixas por chapa:** {planificacao_ima['caixas_por_chapa']}")
            st.markdown(f"**Chapas necessárias:** {chapas_necessarias_ima}")
        
        elif tipo_tampa == "Tampa Luva":
            planificacao_luva = calcular_planificacao_tampa_luva(largura, altura, profundidade)
            
            # Verificar se caixas_por_chapa é maior que zero para evitar divisão por zero
            if planificacao_luva['caixas_por_chapa'] > 0:
                chapas_necessarias_luva = math.ceil(quantidade_caixas / planificacao_luva['caixas_por_chapa'])
            else:
                chapas_necessarias_luva = quantidade_caixas  # Uma chapa por caixa se não couber nenhuma
            
            st.markdown("### 📐 Planificação de Chapas de Papelão (Tampa-Luva)")
            st.markdown(f"**Dimensões da chapa:** 1040mm × 860mm")
            st.markdown(f"**Base planificada:** {planificacao_luva['dimensoes_base'][0]:.0f}mm × {planificacao_luva['dimensoes_base'][1]:.0f}mm")
            st.markdown(f"**Tampa planificada:** {planificacao_luva['dimensoes_tampa'][0]:.0f}mm × {planificacao_luva['dimensoes_tampa'][1]:.0f}mm")
            st.markdown(f"**Aba lateral:** {planificacao_luva['dimensoes_aba'][0]:.0f}mm × {planificacao_luva['dimensoes_aba'][1]:.0f}mm")
            st.markdown(f"**Área da base:** {planificacao_luva['area_base_mm2']/100:.1f} cm²")
            st.markdown(f"**Área da tampa:** {planificacao_luva['area_tampa_mm2']/100:.1f} cm²")
            st.markdown(f"**Área da aba:** {planificacao_luva['area_aba_mm2']/100:.1f} cm²")
            st.markdown(f"**Caixas por chapa:** {planificacao_luva['caixas_por_chapa']}")
            st.markdown(f"**Chapas necessárias:** {chapas_necessarias_luva}")

def display_cost_breakdown(estrutura, tipo_tampa, largura, altura, profundidade, quantidade_caixas,
                         usar_serigrafia, num_cores_serigrafia, num_impressoes_serigrafia,
                         usar_impressao_digital, tipo_impressao, tipo_revestimento,
                         tem_berco, tem_nicho, metros_fita, num_rebites,
                         usar_cola_quente, usar_cola_isopor, custos_fixos):
    """Exibe o detalhamento completo dos custos como uma conta de restaurante"""
    
    # Calcular todos os custos
    custo_fixo_unitario = custos_fixos['total_custos_fixos'] / CAIXAS_POR_MES
    
    # Custos de estrutura
    if estrutura == "Papelão":
        # Calcular área de papelão baseada no tipo de tampa
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
        
        # Converter mm² para m²
        area_papelao_m2 = area_papelao / 1000000  # Converter mm² para m²
        custo_papelao = area_papelao_m2 * PRECO_PAPELAO_POR_M2
        custo_acrilico = 0
    else:
        area_acrilico = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
        area_acrilico_m2 = area_acrilico / 10000
        custo_acrilico = area_acrilico_m2 * PRECO_ACRILICO_POR_M2
        custo_papelao = 0
    
    # Custos gráficos
    custo_serigrafia = CUSTO_SERIGRAFIA_POR_COR * num_cores_serigrafia * num_impressoes_serigrafia if usar_serigrafia else 0
    custo_impressao = CUSTO_IMPRESSAO_A4 if (usar_impressao_digital and tipo_impressao == "A4") else (CUSTO_IMPRESSAO_A3 if (usar_impressao_digital and tipo_impressao == "A3") else 0)
    
    # Custos de revestimento
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
        
        # Multiplicar por 2 (interno e externo) e converter mm² para m²
        area_revestimento_m2 = (area_revestimento * 2) / 1000000  # Converter mm² para m²
        
        if tipo_revestimento == "Vinil UV":
            custo_revestimento = area_revestimento_m2 * CUSTO_VINIL_UV_POR_M2
        elif tipo_revestimento == "Papel":
            custo_revestimento = area_revestimento_m2 * CUSTO_PAPEL_POR_M2
        else:
            custo_revestimento = 0
    else:
        custo_revestimento = 0
    
    # Custos de cola
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
    else:
        area_acrilico_cola = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
        ml_cola_total = area_acrilico_cola * 0.01
        custo_cola_pva = 0
        custo_cola_adesiva = 0
        custo_cola_quente = 0
        custo_cola_isopor = 0
        custo_cola_acrilico = CUSTO_COLA_ACRILICO * ml_cola_total
    
    # Custos adicionais
    custo_fita = metros_fita * PRECO_FITA_POR_M
    custo_rebites = num_rebites * PRECO_REBITE_UNITARIO
    custo_ima_chapa = calcular_custo_ima_chapa_automatico(tipo_tampa, largura)
    
    # Custo das caixas de papelão
    num_caixas_por_embalagem = calcular_max_caixas_por_embalagem(largura, altura, profundidade)
    
    if num_caixas_por_embalagem > 0:
        num_caixas_papelao_necessarias = math.ceil(quantidade_caixas / num_caixas_por_embalagem)
        custo_caixa_papelao = (num_caixas_papelao_necessarias * PRECO_CAIXA_PAPELAO) / quantidade_caixas
    else:
        # Caixa não cabe na embalagem - não usar embalagem
        custo_caixa_papelao = 0
    
    # Custos adicionais de serigrafia
    custo_retardador = CUSTO_RETARDADOR_VINILICO if usar_serigrafia else 0
    custo_emulsao = CUSTO_EMULSAO_SENSIBILIZANTE if usar_serigrafia else 0
    custo_cola_permanente = CUSTO_COLA_PERMANENTE if usar_serigrafia else 0
    
    # Calcular total de custos variáveis
    total_custos_variaveis = (
        custo_papelao + custo_acrilico + custo_serigrafia + custo_impressao + 
        custo_revestimento + custo_cola_pva + custo_cola_adesiva + custo_cola_quente + custo_cola_isopor + 
        custo_cola_acrilico + custo_fita + custo_rebites + custo_ima_chapa + custo_caixa_papelao + 
        custo_retardador + custo_emulsao + custo_cola_permanente
    )
    
    # Aplicar multiplicador de complexidade
    total_custos_variaveis_complexidade = aplicar_multiplicador_complexidade(
        total_custos_variaveis, tem_berco, tem_nicho
    )
    
    # Custo final
    custo_final = custo_fixo_unitario + total_custos_variaveis_complexidade
    
    # Exibir como conta de restaurante
    st.markdown("### 🧾 CONTA DETALHADA")
    st.markdown("---")
    
    # Cabeçalho
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("**ITEM**")
    with col2:
        st.markdown("**QTD**")
    with col3:
        st.markdown("**VALOR**")
    
    st.markdown("---")
    
    # Custos fixos
    st.markdown("**💰 CUSTOS FIXOS**")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("Custo fixo unitário")
    with col2:
        st.markdown("1 un")
    with col3:
        st.markdown(f"R$ {custo_fixo_unitario:.2f}")
    
    # Custos de estrutura
    st.markdown("**💛 MATERIA-PRIMA**")
    if estrutura == "Papelão":
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Papelão ({area_papelao_m2:.3f} m²)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_papelao:.2f}")
    else:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Acrílico ({area_acrilico_m2:.3f} m²)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_acrilico:.2f}")
    
    # Custos gráficos
    st.markdown("**🎨 CUSTOS GRÁFICOS**")
    if usar_serigrafia:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Serigrafia ({num_cores_serigrafia} cores × {num_impressoes_serigrafia} impressões)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_serigrafia:.2f}")
    
    if usar_impressao_digital:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Impressão digital {tipo_impressao}")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_impressao:.2f}")
    
    # Custos de revestimento
    if custo_revestimento > 0:
        st.markdown("**🎨 CUSTOS DE REVESTIMENTO**")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"{tipo_revestimento} ({area_revestimento_m2:.3f} m²)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_revestimento:.2f}")
    
    # Custos de cola
    st.markdown("**🔧 CUSTOS DE COLA**")
    if custo_cola_pva > 0:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Cola PVA ({ml_cola_total:.1f} ml)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_cola_pva:.2f}")
    
    if custo_cola_adesiva > 0:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Cola adesiva ({ml_cola_adesiva_total:.1f} ml)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_cola_adesiva:.2f}")
    
    if custo_cola_quente > 0:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Cola quente ({ml_cola_total:.1f} ml)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_cola_quente:.2f}")
    
    if custo_cola_isopor > 0:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Cola de isopor ({ml_cola_total:.1f} ml)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_cola_isopor:.2f}")
    
    if custo_cola_acrilico > 0:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Cola de acrílico ({ml_cola_total:.1f} ml)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_cola_acrilico:.2f}")
    
    # Custos de embalagem
    st.markdown("**📦 CUSTOS DE EMBALAGEM**")
    
    if num_caixas_por_embalagem > 0:
        # Calcular número de embalagens necessárias
        num_embalagens_necessarias = math.ceil(quantidade_caixas / num_caixas_por_embalagem)
        custo_total_embalagem = num_embalagens_necessarias * PRECO_CAIXA_PAPELAO
        
        # Explicação do custo de embalagem
        st.info(f"💡 **Como funciona:** Cada caixa de embalagem (R$ 31,00) acomoda até {num_caixas_por_embalagem} caixas. Para {quantidade_caixas} caixas, precisamos de {num_embalagens_necessarias} embalagem(s).")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Caixa papelão ondulado ({num_caixas_por_embalagem} caixas/embalagem)")
        with col2:
            st.markdown(f"{num_embalagens_necessarias} un")
        with col3:
            st.markdown(f"R$ {custo_total_embalagem:.2f}")
        
        # Mostrar custo por caixa
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("Custo de embalagem por caixa")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_caixa_papelao:.2f}")
    else:
        # Caixa não cabe na embalagem - não usar embalagem
        st.info(f"💡 **Caixa não cabe na embalagem:** Dimensões da caixa ({largura}×{altura}×{profundidade} cm) são maiores que as dimensões da embalagem (50×35×35 cm). Não será usada embalagem.")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("Caixa papelão ondulado (não aplicável)")
        with col2:
            st.markdown("0 un")
        with col3:
            st.markdown("R$ 0,00")
        
        # Mostrar custo por caixa
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("Custo de embalagem por caixa")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown("R$ 0,00")
    
    # Custos adicionais
    st.markdown("**🔧 CUSTOS ADICIONAIS**")
    if custo_fita > 0:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Fita ({metros_fita:.1f} m)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_fita:.2f}")
    
    if custo_rebites > 0:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Rebites ({num_rebites} un)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_rebites:.2f}")
    
    if custo_ima_chapa > 0:
        num_pares_ima = int(custo_ima_chapa / PRECO_IMA_CHAPA_PAR)
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"Imã + chapa ({num_pares_ima} pares)")
        with col2:
            st.markdown("1 un")
        with col3:
            st.markdown(f"R$ {custo_ima_chapa:.2f}")
    
    # Custos adicionais de serigrafia
    if usar_serigrafia:
        st.markdown("**🎨 CUSTOS ADICIONAIS DE SERIGRAFIA**")
        if custo_retardador > 0:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown("Retardador vinílico")
            with col2:
                st.markdown("1 un")
            with col3:
                st.markdown(f"R$ {custo_retardador:.2f}")
        
        if custo_emulsao > 0:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown("Emulsão + sensibilizante")
            with col2:
                st.markdown("1 un")
            with col3:
                st.markdown(f"R$ {custo_emulsao:.2f}")
        
        if custo_cola_permanente > 0:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown("Cola permanente")
            with col2:
                st.markdown("1 un")
            with col3:
                st.markdown(f"R$ {custo_cola_permanente:.2f}")
    
    # Multiplicadores de complexidade
    if tem_berco or tem_nicho:
        st.markdown("**⚡ MULTIPLICADORES DE COMPLEXIDADE**")
        if tem_berco and tem_nicho:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown("Berço + Nicho (+80%)")
            with col2:
                st.markdown("1 un")
            with col3:
                st.markdown(f"R$ {total_custos_variaveis_complexidade - total_custos_variaveis:.2f}")
        elif tem_berco:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown("Berço (+30%)")
            with col2:
                st.markdown("1 un")
            with col3:
                st.markdown(f"R$ {total_custos_variaveis_complexidade - total_custos_variaveis:.2f}")
        elif tem_nicho:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown("Nicho (+50%)")
            with col2:
                st.markdown("1 un")
            with col3:
                st.markdown(f"R$ {total_custos_variaveis_complexidade - total_custos_variaveis:.2f}")
    
    # Total
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("**TOTAL UNITÁRIO**")
    with col2:
        st.markdown("")
    with col3:
        st.markdown(f"**R$ {custo_final:.2f}**")
    
    # Total do projeto
    custo_total_projeto = custo_final * quantidade_caixas
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("**TOTAL DO PROJETO**")
    with col2:
        st.markdown(f"({quantidade_caixas} un)")
    with col3:
        st.markdown(f"**R$ {custo_total_projeto:.2f}**")
    
    return custo_final, custo_total_projeto 