import streamlit as st
import math
from calculations import *
from constants import *

def display_fixed_costs_section():
    """Exibe a seção de custos fixos"""
    with st.expander("🏢 Custos operacionais mensais", expanded=False):
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
        elif tipo_tampa == "Tampa Redonda":
            area_corte = calcular_planificacao_tampa_redonda(largura, altura, profundidade)
            area_papelao = area_corte['area_planificada_mm2']

        
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
        elif tipo_tampa == "Tampa Redonda":
            area_corte = calcular_planificacao_tampa_redonda(largura, altura, profundidade)
            area_revestimento = area_corte['area_planificada_mm2']

        
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
    # Retardador, emulsão e cola permanente serão aplicados ao total do projeto, não por unidade
    custo_retardador = 0
    custo_emulsao = 0
    custo_cola_permanente = 0
    
    # Calcular total de custos variáveis (sem embalagem e sem custos de serigrafia adicionais)
    total_custos_variaveis = (
        custo_papelao + custo_acrilico + custo_serigrafia + custo_impressao + 
        custo_revestimento + custo_cola_pva + custo_cola_adesiva + custo_cola_quente + custo_cola_isopor + 
        custo_cola_acrilico + custo_fita + custo_rebites + custo_ima_chapa
    )
    
    # Aplicar multiplicador de complexidade
    total_custos_variaveis_complexidade = aplicar_multiplicador_complexidade(
        total_custos_variaveis, tem_berco, tem_nicho
    )
    
    # Custo final
    custo_final = custo_fixo_unitario + total_custos_variaveis_complexidade

    st.info(f"💡 Custos operacionais mensais divididos por {CAIXAS_POR_MES} caixas/mês para obter o custo fixo unitário.")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Custo fixo unitário")
    with col2:
        st.markdown(f"R$ {custo_fixo_unitario:.2f}")

    if estrutura == "Papelão":
        st.info(f"💡 Área do papelão = área planificada da caixa (incluindo desperdício) em m² x R$ {PRECO_PAPELAO_POR_M2}/m².")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Papelão ({area_papelao_m2:.3f} m²)")
        with col2:
            st.markdown(f"R$ {custo_papelao:.2f}")
            
    else:
        st.info(f"💡 Área do acrílico = área planificada da caixa (incluindo desperdício) em m² x R$ {PRECO_ACRILICO_POR_M2}/m².")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Acrílico ({area_acrilico_m2:.3f} m²)")
        with col2:
            st.markdown(f"R$ {custo_acrilico:.2f}")

    if usar_serigrafia:
        st.info(f"💡 Custo de serigrafia = numero de cores ({num_cores_serigrafia}) x número de impressões ({num_impressoes_serigrafia}) x R$ {CUSTO_SERIGRAFIA_POR_COR}.")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Serigrafia ({num_cores_serigrafia} cores × {num_impressoes_serigrafia} impressões)")
        with col2:
            st.markdown(f"R$ {custo_serigrafia:.2f}")    
    
    if usar_impressao_digital:
        st.info(f"💡 Custo de impressão digital = A4 R\$ {CUSTO_IMPRESSAO_A4} ou A3 R$ {CUSTO_IMPRESSAO_A3}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Impressão digital {tipo_impressao}")
        with col2:
            st.markdown(f"R$ {custo_impressao:.2f}")    
    
    # Custos de revestimento
    if custo_revestimento > 0:
        if tipo_revestimento == "Vinil UV":
            st.info(f"💡 O custo de vinil UV é calculado pela área do revestimento, que é 2x a área do papelão útil (pois o revestimento é interno e externo) x R$ {CUSTO_VINIL_UV_POR_M2}/m²")
        else:
            st.info(f"💡 O custo de papel é calculado pela área do revestimento, que é 2x a área do papelão útil (pois o revestimento é interno e externo) x R$ {CUSTO_PAPEL_POR_M2}/m²")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"{tipo_revestimento} ({area_revestimento_m2:.3f} m²)")
        with col2:
            st.markdown(f"R$ {custo_revestimento:.2f}")

    # Custos de cola
    if estrutura == "Papelão":
        st.info(f"💡 O custo de cola PVA é igual a área de colagem, que é área interna + externa do papelão, em m² dividido por 120ml/m². Depois multiplicado por R$ {CUSTO_COLA_PVA}/ml")
    else:
        st.info(f"💡 O custo de cola de acrílico é igual a área de colagem, que é área interna + externa do acrílico, em m² dividido por 120ml/m². Depois multiplicado por R$ {CUSTO_COLA_ACRILICO}/ml")
    if custo_cola_pva > 0:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Cola PVA ({ml_cola_total:.1f} ml)")
        with col2:
            st.markdown(f"R$ {custo_cola_pva:.2f}")    
    
    if custo_cola_adesiva > 0:
        st.info(f"💡 Custo de cola adesiva = perímetro x 10ml/m x R$ {CUSTO_COLA_ADESIVA}/ml")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Cola adesiva ({ml_cola_adesiva_total:.1f} ml)")
        with col2:
            st.markdown(f"R$ {custo_cola_adesiva:.2f}")    
    
    if custo_cola_quente > 0:
        st.info(f"💡 Custo de cola quente = custo de cola PVA (R\$ {custo_cola_pva:.2f}) x R$ {CUSTO_COLA_QUENTE}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Cola quente")
        with col2:
            st.markdown(f"R$ {custo_cola_quente:.2f}")    
    
    if custo_cola_isopor > 0:
        st.info(f"💡 Custo de cola de isopor = custo de cola PVA (R\$ {custo_cola_pva:.2f}) x R$ {CUSTO_COLA_ISOPOR}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Cola de isopor")
        with col2:
            st.markdown(f"R$ {custo_cola_isopor:.2f}")    
    
    if custo_cola_acrilico > 0:
        st.info(f"💡 Custo de cola de acrílico = ml de cola acrílico x R$ {CUSTO_COLA_ACRILICO}/ml")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Cola de acrílico ({ml_cola_total:.1f} ml)")
        with col2:
            st.markdown(f"R$ {custo_cola_acrilico:.2f}")    

    # Custos adicionais
    if custo_fita > 0:
        st.info(f"💡 Custo de fita = numero de metros utilizados x R$ {PRECO_FITA_POR_M}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Fita ({metros_fita:.1f} m)")
        with col2:
            st.markdown(f"R$ {custo_fita:.2f}")
    
    if custo_rebites > 0:
        st.info(f"💡 Custo de rebites = numero de unidades x R$ {PRECO_REBITE_UNITARIO}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Rebites ({num_rebites} un)")
        with col2:
            st.markdown(f"R$ {custo_rebites:.2f}")
    
    if custo_ima_chapa > 0:
        st.info(f"💡 Custo do par imã + chapa = numero de pares x R$ {PRECO_IMA_CHAPA_PAR}")
        num_pares_ima = int(custo_ima_chapa / PRECO_IMA_CHAPA_PAR)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Imã + chapa ({num_pares_ima} pares)")
        with col2:
            st.markdown(f"R$ {custo_ima_chapa:.2f}")
            
    

    # Multiplicadores de complexidade
    if tem_berco or tem_nicho:
        if tem_berco and tem_nicho:
            st.info(f"💡 Berço + Nicho adicionamos 50% ao custo total devido ao grau de dificuldade + material")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("Berço + Nicho (+50%)")
            with col2:
                st.markdown(f"R$ {total_custos_variaveis_complexidade - total_custos_variaveis:.2f}")
        elif tem_berco:
            st.info(f"💡 Berço adicionamos 30% ao custo total devido ao grau de dificuldade + material")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("Berço (+30%)")
            with col2:
                st.markdown(f"R$ {total_custos_variaveis_complexidade - total_custos_variaveis:.2f}")

    # Calcular custo total do projeto incluindo embalagem
    custo_total_projeto = custo_final * quantidade_caixas
    
    # Adicionar custo de embalagem ao total do projeto
    if num_caixas_por_embalagem > 0:
        num_embalagens_necessarias = math.ceil(quantidade_caixas / num_caixas_por_embalagem)
        custo_total_embalagem = num_embalagens_necessarias * PRECO_CAIXA_PAPELAO
        custo_total_projeto += custo_total_embalagem

        # Mostrar seção de embalagem no total do projeto
        st.markdown("---")
        st.markdown("**📦 CUSTOS DE DESPACHE (INCLUÍDOS NO TOTAL DO PROJETO)**")
        st.info(f"💡 Cada caixa de papelão ondulado embala até {num_caixas_por_embalagem} caixas desta dimensão. Para {quantidade_caixas} caixa(s), precisamos de {num_embalagens_necessarias} caixa(s) de papelão ondulado") 
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"Caixa de papelão ondulado ({num_embalagens_necessarias} und)")
        with col2:
            st.markdown(f"R$ {custo_total_embalagem:.2f}")
    
    # Adicionar custos de serigrafia ao total do projeto (se há serigrafia)
    if usar_serigrafia:
        custo_total_projeto += CUSTO_COLA_PERMANENTE + CUSTO_RETARDADOR_VINILICO + CUSTO_EMULSAO_SENSIBILIZANTE
        
        # Mostrar seção de custos de serigrafia no total do projeto
        st.markdown("---")
        st.markdown("**🎨 CUSTOS ADICIONAIS DE SERIGRAFIA (INCLUÍDOS NO TOTAL DO PROJETO)**")
        st.info(f"❌ Cola permanente R\$ {CUSTO_COLA_PERMANENTE}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("Cola permanente")
        with col2:
            st.markdown(f"R$ {CUSTO_COLA_PERMANENTE:.2f}")
        
        st.info(f"❌ Retardador vinílico R\$ {CUSTO_RETARDADOR_VINILICO}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("Retardador vinílico")
        with col2:
            st.markdown(f"R$ {CUSTO_RETARDADOR_VINILICO:.2f}")
        
        st.info(f"❌ Emulsão + sensibilizante R$ {CUSTO_EMULSAO_SENSIBILIZANTE}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("Emulsão + sensibilizante")
        with col2:
            st.markdown(f"R$ {CUSTO_EMULSAO_SENSIBILIZANTE:.2f}")
    
    return custo_final, custo_total_projeto 