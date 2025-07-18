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
            chapas_necessarias = math.ceil(quantidade_caixas / planificacao['caixas_por_chapa'])
            
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
            chapas_necessarias_livro = math.ceil(quantidade_caixas / planificacao_livro['caixas_por_chapa'])
            
            st.markdown("### 📐 Planificação de Chapas de Papelão (Tampa-Livro)")
            st.markdown(f"**Dimensões da chapa:** 1040mm × 860mm")
            st.markdown(f"**Largura planificada:** {planificacao_livro['dimensoes_planificacao'][0]:.0f}mm")
            st.markdown(f"**Altura planificada:** {planificacao_livro['dimensoes_planificacao'][1]:.0f}mm")
            st.markdown(f"**Área planificada:** {planificacao_livro['area_planificada_mm2']/100:.1f} cm²")
            st.markdown(f"**Colunas por chapa:** {planificacao_livro['colunas_por_chapa']}")
            st.markdown(f"**Linhas por chapa:** {planificacao_livro['linhas_por_chapa']}")
            st.markdown(f"**Caixas por chapa:** {planificacao_livro['caixas_por_chapa']}")
            st.markdown(f"**Chapas necessárias:** {chapas_necessarias_livro}")

def display_cost_breakdown(estrutura, tipo_tampa, largura, altura, profundidade, quantidade_caixas,
                         usar_serigrafia, num_cores_serigrafia, num_impressoes_serigrafia,
                         usar_impressao_digital, tipo_impressao, tipo_revestimento,
                         tem_berco, tem_nicho, metros_fita, num_rebites,
                         usar_cola_quente, usar_cola_isopor, custos_fixos):
    """Exibe o detalhamento completo dos custos"""
    st.markdown("### 📋 Descrição Completa dos Custos")
    
    st.markdown("**💰 CUSTOS FIXOS:**")
    st.markdown("- **Custo fixo unitário:** Calculado dividindo o total dos custos fixos mensais pela produção média mensal (1000 caixas/mês)")
    st.markdown("- **Inclui:** Aluguel, energia, água, vale-refeição, vale-transporte, combustível, INSS, FGTS, DAS, contabilidade, marketing, jurídico, Adobe, Meli+, Kommo, internet, financeiro, folha de pagamento")
    
    st.markdown("**🏗️ CUSTOS DE ESTRUTURA:**")
    if estrutura == "Papelão":
        st.markdown("- **Papelão:** Calculado pela área total da caixa (base + laterais + tampa) × R$ 8,31/m²")
        st.markdown("- **Área calculada:** Baseada nas dimensões e tipo de tampa (solta, livro, luva, imã)")
    elif estrutura == "Acrílico":
        st.markdown("- **Acrílico:** Calculado pela área principal × R$ 95,50/m²")
        st.markdown("- **Sem revestimentos:** Acrílico não permite revestimentos")
    
    st.markdown("**🎨 CUSTOS GRÁFICOS:**")
    if usar_serigrafia:
        st.markdown("- **Serigrafia:** R$ 1,01 por cor por impressão")
        st.markdown(f"- **Aplicado:** {num_cores_serigrafia} cores × {num_impressoes_serigrafia} impressões")
    else:
        st.markdown("- **Serigrafia:** R$ 1,01 por cor por impressão ❌ **Não aplicado**")
    
    if usar_impressao_digital:
        st.markdown(f"- **Impressão digital {tipo_impressao}:** R$ {CUSTO_IMPRESSAO_A4 if tipo_impressao == 'A4' else CUSTO_IMPRESSAO_A3:.2f} por unidade")
    else:
        st.markdown("- **Impressão digital A4:** R$ 3,50 por unidade ❌ **Não aplicado**")
        st.markdown("- **Impressão digital A3:** R$ 5,00 por unidade ❌ **Não aplicado**")
    
    st.markdown("**🎨 CUSTOS DE REVESTIMENTO:**")
    if estrutura == "Papelão":
        if tipo_revestimento == "Vinil UV":
            st.markdown("- **Vinil UV:** R$ 140,00/m² aplicado na área total da caixa")
            st.markdown("- **Papel:** R$ 15,00/m² ❌ **Não aplicado**")
        elif tipo_revestimento == "Papel":
            st.markdown("- **Vinil UV:** R$ 140,00/m² ❌ **Não aplicado**")
            st.markdown("- **Papel:** R$ 15,00/m² aplicado na área total da caixa")
        else:
            st.markdown("- **Vinil UV:** R$ 140,00/m² ❌ **Não aplicado**")
            st.markdown("- **Papel:** R$ 15,00/m² ❌ **Não aplicado**")
    else:
        st.markdown("- **Vinil UV:** R$ 140,00/m² ❌ **Não aplicado (apenas para papelão)**")
        st.markdown("- **Papel:** R$ 15,00/m² ❌ **Não aplicado (apenas para papelão)**")
    
    st.markdown("**🔧 CUSTOS DE COLA:**")
    if estrutura == "Papelão":
        area_papelao = calcular_area_papelao(largura, altura, profundidade, tipo_tampa)
        ml_cola_total = area_papelao * 0.01  # 1ml por 100cm²
        st.markdown(f"- **Cola PVA:** R$ 0,469/ml × {ml_cola_total:.1f} ml (automática)")
        st.markdown(f"- **Cola adesiva:** R$ 0,058/ml × {ml_cola_total:.1f} ml (automática)")
        if usar_cola_quente:
            st.markdown(f"- **Cola quente:** R$ 0,0125/ml × {ml_cola_total:.1f} ml (opcional)")
        else:
            st.markdown("- **Cola quente:** R$ 0,0125/ml ❌ **Não aplicado**")
        if usar_cola_isopor:
            st.markdown(f"- **Cola de isopor:** R$ 0,015/ml × {ml_cola_total:.1f} ml (opcional)")
        else:
            st.markdown("- **Cola de isopor:** R$ 0,015/ml ❌ **Não aplicado**")
        st.markdown("- **Cola de acrílico:** R$ 0,085/ml ❌ **Não aplicado (apenas para acrílico)**")
        st.markdown(f"- **Quantidade calculada:** {ml_cola_total:.1f} ml (proporcional à área)")
    elif estrutura == "Acrílico":
        area_acrilico = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
        ml_cola_total = area_acrilico * 0.01
        st.markdown("- **Cola PVA:** R$ 0,469/ml ❌ **Não aplicado (apenas para papelão)**")
        st.markdown("- **Cola adesiva:** R$ 0,058/ml ❌ **Não aplicado (apenas para papelão)**")
        st.markdown("- **Cola quente:** R$ 0,0125/ml ❌ **Não aplicado (apenas para papelão)**")
        st.markdown("- **Cola de isopor:** R$ 0,015/ml ❌ **Não aplicado (apenas para papelão)**")
        st.markdown(f"- **Cola de acrílico:** R$ 0,085/ml × {ml_cola_total:.1f} ml (automática)")
        st.markdown(f"- **Quantidade calculada:** {ml_cola_total:.1f} ml (proporcional à área)")
    
    st.markdown("**📦 CUSTOS DE EMBALAGEM:**")
    num_caixas_por_embalagem = calcular_max_caixas_por_embalagem(largura, altura, profundidade)
    if num_caixas_por_embalagem > 0:
        num_caixas_papelao_necessarias = math.ceil(quantidade_caixas / num_caixas_por_embalagem)
        st.markdown(f"- **Caixas de papelão ondulado:** {num_caixas_papelao_necessarias} caixas de 50×50×60 cm")
        st.markdown(f"- **Custo por caixa de papelão:** R$ {PRECO_CAIXA_PAPELAO:.2f}")
        st.markdown(f"- **Caixas por embalagem:** {num_caixas_por_embalagem} (calculado com rotação)")
    else:
        st.markdown("- **Caixas de papelão ondulado:** 1 caixa por unidade (caixa muito grande)")
    
    st.markdown("**🔧 CUSTOS ADICIONAIS:**")
    if metros_fita > 0:
        st.markdown(f"- **Fita:** R$ 0,627/m × {metros_fita:.1f} m")
    else:
        st.markdown("- **Fita:** R$ 0,627/m ❌ **Não aplicado**")
    
    if num_rebites > 0:
        st.markdown(f"- **Rebites:** R$ 0,10/un × {num_rebites} unidades")
    else:
        st.markdown("- **Rebites:** R$ 0,10/un ❌ **Não aplicado**")
    
    custo_ima_chapa = calcular_custo_ima_chapa_automatico(tipo_tampa, largura)
    if custo_ima_chapa > 0:
        num_pares_ima = int(custo_ima_chapa / PRECO_IMA_CHAPA_PAR)
        st.markdown(f"- **Imã + chapa:** R$ 1,58/par × {num_pares_ima} pares (automático baseado no tipo de tampa)")
    else:
        st.markdown("- **Imã + chapa:** R$ 1,58/par ❌ **Não aplicado (apenas para tampa imã)**")
    
    st.markdown("**🎨 CUSTOS ADICIONAIS DE SERIGRAFIA:**")
    if usar_serigrafia:
        st.markdown("- **Retardador vinílico:** R$ 0,041 (por unidade)")
        st.markdown("- **Emulsão + sensibilizante:** R$ 0,058 (por unidade)")
        st.markdown("- **Cola permanente:** R$ 0,028 (por unidade)")
    else:
        st.markdown("- **Retardador vinílico:** R$ 0,041 ❌ **Não aplicado (apenas com serigrafia)**")
        st.markdown("- **Emulsão + sensibilizante:** R$ 0,058 ❌ **Não aplicado (apenas com serigrafia)**")
        st.markdown("- **Cola permanente:** R$ 0,028 ❌ **Não aplicado (apenas com serigrafia)**")
    
    st.markdown("**⚡ MULTIPLICADORES DE COMPLEXIDADE:**")
    if tem_berco and tem_nicho:
        st.markdown("- **Berço + Nicho:** +80% no total de custos variáveis")
    elif tem_berco:
        st.markdown("- **Berço:** +30% no total de custos variáveis")
        st.markdown("- **Nicho:** +50% ❌ **Não aplicado**")
    elif tem_nicho:
        st.markdown("- **Berço:** +30% ❌ **Não aplicado**")
        st.markdown("- **Nicho:** +50% no total de custos variáveis")
    else:
        st.markdown("- **Berço:** +30% ❌ **Não aplicado**")
        st.markdown("- **Nicho:** +50% ❌ **Não aplicado**")
    
    st.markdown("**📊 CÁLCULO FINAL:**")
    custo_fixo_unitario = custos_fixos['total_custos_fixos'] / CAIXAS_POR_MES
    st.markdown(f"- **Custo fixo unitário:** R$ {custo_fixo_unitario:.2f}")
    # Aqui você pode adicionar mais cálculos conforme necessário 