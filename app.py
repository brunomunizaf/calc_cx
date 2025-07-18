import streamlit as st
import math

# Configuração da página
st.set_page_config(
    page_title="Touché | Orçamentos",
    page_icon="📦"
)

# Constantes de custo
CUSTO_FIXO_UNITARIO = 26.92
PRECO_PAPELAO_POR_M2 = 8.31
PRECO_VINIL_UV_POR_M2 = 140.0
PRECO_ACRILICO_POR_M2 = 95.50
PRECO_FITA_POR_M = 0.627
PRECO_REBITE_UNITARIO = 0.10
PRECO_IMA_CHAPA_PAR = 1.58
PRECO_CAIXA_KRAFT = 8.0

# Custos de cola
CUSTO_COLA_PVA = 0.469
CUSTO_COLA_ADESIVA = 0.058
CUSTO_COLA_QUENTE = 0.0125
CUSTO_COLA_ISOPOR = 0.015  # Adicionado cola de isopor
CUSTO_COLA_ACRILICO = 0.085  # Adicionado cola de acrílico

# Custos de impressão
CUSTO_IMPRESSAO_A4 = 3.50
CUSTO_IMPRESSAO_A3 = 5.00
CUSTO_SERIGRAFIA_POR_COR = 1.01

# Custos adicionais
CUSTO_RETARDADOR_VINILICO = 0.041
CUSTO_EMULSAO_SENSIBILIZANTE = 0.058
CUSTO_COLA_PERMANENTE = 0.028

# Custos de frete por tipo
CUSTO_FRETE_RECIFE = 15.0
CUSTO_FRETE_RMR = 20.0
CUSTO_FRETE_INTERESTADUAL = 35.0

# Multiplicadores de complexidade
MULTIPLICADOR_BERCO = 1.3
MULTIPLICADOR_NICHO = 1.5
MULTIPLICADOR_AMBOS = 1.8

def calcular_area_papelao(largura, altura, profundidade, tipo_tampa):
    """Calcula a área de papelão necessária baseada no tipo de tampa"""
    # Área da base
    area_base = largura * altura
    
    # Área das laterais
    area_laterais = 2 * (largura * profundidade) + 2 * (altura * profundidade)
    
    # Área da tampa baseada no tipo
    if tipo_tampa == "Tampa Solta":
        folga = 1.0
        area_tampa = (largura + folga) * (altura + folga)
    elif tipo_tampa == "Tampa Livro":
        folga = 2.0
        area_tampa = 2 * (largura + folga) * (altura + folga) + profundidade * (altura + folga)
    elif tipo_tampa == "Tampa Luva":
        folga = 1.5
        area_tampa = (largura + folga) * (altura + folga) * 2
    elif tipo_tampa == "Tampa Imã":
        folga = 2.0
        area_livro = 2 * (largura + folga) * (altura + folga) + profundidade * (altura + folga)
        area_lingua = (profundidade - 0.5) * (altura + folga)
        area_tampa = area_livro + area_lingua
    else:
        area_tampa = largura * altura  # Fallback
    
    return area_base + area_laterais + area_tampa

def calcular_custo_papelao(largura, altura):
    """Calcula o custo do papelão baseado na área em mm²"""
    area_mm2 = largura * altura * 100  # Converte cm para mm
    area_m2 = area_mm2 / 1_000_000  # Converte mm² para m²
    return area_m2 * PRECO_PAPELAO_POR_M2

def calcular_custo_vinil_uv(largura_vinil, altura_vinil):
    """Calcula o custo do vinil UV"""
    area_cm2 = largura_vinil * altura_vinil
    area_m2 = area_cm2 / 10000
    return area_m2 * PRECO_VINIL_UV_POR_M2

def calcular_custo_acrilico(largura_acrilico, altura_acrilico):
    """Calcula o custo do acrílico"""
    area_cm2 = largura_acrilico * altura_acrilico
    area_m2 = area_cm2 / 10000
    return area_m2 * PRECO_ACRILICO_POR_M2

def calcular_custo_ima_chapa_automatico(tipo_tampa, largura):
    """Calcula automaticamente o custo de imã + chapa baseado nas regras"""
    if tipo_tampa == "Tampa Imã":
        if largura <= 10:
            return 1 * PRECO_IMA_CHAPA_PAR  # 1 par
        else:
            return 2 * PRECO_IMA_CHAPA_PAR  # 2 pares
    else:
        return 0

def calcular_custo_caixa_kraft(num_caixas_por_embalagem):
    """Calcula o custo da caixa kraft por unidade"""
    if num_caixas_por_embalagem > 0:
        return PRECO_CAIXA_KRAFT / num_caixas_por_embalagem
    return 0

def aplicar_multiplicador_complexidade(custo_variavel, tem_berco, tem_nicho):
    """Aplica multiplicador de complexidade"""
    if tem_berco and tem_nicho:
        return custo_variavel * MULTIPLICADOR_AMBOS
    elif tem_berco:
        return custo_variavel * MULTIPLICADOR_BERCO
    elif tem_nicho:
        return custo_variavel * MULTIPLICADOR_NICHO
    else:
        return custo_variavel

def determinar_colas_automaticas(estrutura, usar_acrilico):
    """Determina automaticamente quais colas usar baseado na estrutura"""
    if estrutura == "Papelão":
        return {
            "cola_pva": True,
            "cola_adesiva": True,
            "cola_quente": False,
            "cola_isopor": False,
            "cola_acrilico": False
        }
    elif estrutura == "Acrílico":
        return {
            "cola_pva": False,
            "cola_adesiva": False,
            "cola_quente": False,
            "cola_isopor": False,
            "cola_acrilico": True
        }
    else:
        return {
            "cola_pva": False,
            "cola_adesiva": False,
            "cola_quente": False,
            "cola_isopor": False,
            "cola_acrilico": False
        }

def determinar_revestimentos_disponiveis(estrutura):
    """Determina quais revestimentos estão disponíveis para cada estrutura"""
    if estrutura == "Papelão":
        return ["Vinil UV", "Papel"]
    elif estrutura == "Acrílico":
        return ["Nenhum"]
    else:
        return []

# Interface principal
st.title("📦 Gerador de orçamentos | Touché")
st.markdown("---")

# Seção 1: Dados técnicos da caixa

quantidade_caixas = st.number_input("Número de caixas", min_value=1, value=1, step=1)

col1, col2, col3 = st.columns(3)
with col1:
    largura = st.number_input("Largura (cm)", min_value=1.0, value=20.0, step=0.1)
with col2:
    altura = st.number_input("Altura (cm)", min_value=1.0, value=15.0, step=0.1)
with col3:
    profundidade = st.number_input("Profundidade (cm)", min_value=1.0, value=10.0, step=0.1)

tipo_tampa = st.selectbox(
    "Tipo da Caixa",
    ["Tampa Solta", "Tampa Livro", "Tampa Luva", "Tampa Imã"]
)

estrutura = st.selectbox(
    "Tipo de Estrutura",
    ["Papelão", "Acrílico"],
    help="Papelão permite revestimentos, Acrílico não"
)

# Determinar colas automaticamente baseado na estrutura
colas_automaticas = determinar_colas_automaticas(estrutura, False)

# Revestimentos disponíveis baseados na estrutura
if estrutura == "Papelão":
    tipo_revestimento = st.selectbox(
        "Tipo de revestimento",
        ["Vinil UV", "Papel"],
        index=1,  # Papel pré-selecionado (índice 1)
        help="Vinil UV: +R$ 140,00/m² | Papel: +R$ 15,00/m²"
    )
elif estrutura == "Acrílico":
    st.write("❌ **Nenhum revestimento** disponível para acrílico")
    tipo_revestimento = "Nenhum"

# Complexidade
tem_berco = st.checkbox("Berço (+30%)")
tem_nicho = st.checkbox("Nicho (+50%)")

# Insumos gráficos
usar_serigrafia = st.checkbox("Serigrafia (+R$ 1,01 por cor)")
num_cores_serigrafia = st.number_input("Nº de cores", min_value=1, value=1, disabled=not usar_serigrafia)

usar_impressao_digital = st.checkbox("Impressão digital")
tipo_impressao = st.selectbox(
    "Tipo de impressão",
    ["A4", "A3"],
    disabled=not usar_impressao_digital,
    help="A4: R$ 3,50 | A3: R$ 5,00"
)

# Fita e Rebites
metros_fita = st.number_input("Fita (+R$ 0,627/m)", min_value=0.0, value=0.0, step=0.1)
num_rebites = st.number_input("Rebites (+R$ 0,10/un)", min_value=0, value=0, step=1)

# Colas opcionais (apenas para papelão)
if estrutura == "Papelão":
    usar_cola_quente = st.checkbox("Cola quente (+R$ 0,0125)")
    usar_cola_isopor = st.checkbox("Cola de isopor (+R$ 0,015)")
else:
    usar_cola_quente = False
    usar_cola_isopor = False

# Frete
tem_frete = st.checkbox("Frete")
tipo_frete = st.selectbox(
    "Tipo de frete",
    ["Recife", "RMR", "Interestadual"],
    disabled=not tem_frete,
    help="Recife: R$ 15,00 | RMR: R$ 20,00 | Interestadual: R$ 35,00"
)

# Urgência
urgencia = st.selectbox(
    "Urgência",
    ["1 semana", "3 semanas", ">1 mês"],
    help="Prazo de entrega desejado"
)

# Seção 2: Insumos físicos
# st.markdown("---")
# st.subheader("🔧 Insumos Físicos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Colas (Automáticas baseadas na estrutura)**")
    
    # Mostrar colas determinadas automaticamente
    if estrutura == "Papelão":
        st.write("✅ **Cola PVA:** R$ 0,469 (automática)")
        st.write("✅ **Cola Adesiva:** R$ 0,058 (automática)")
        st.write("❌ **Cola Quente:** Opcional")
        st.write("❌ **Cola de Isopor:** Opcional")
        st.write("❌ **Cola de Acrílico:** Não aplicável")
    elif estrutura == "Acrílico":
        st.write("❌ **Cola PVA:** Não aplicável")
        st.write("❌ **Cola Adesiva:** Não aplicável")
        st.write("❌ **Cola Quente:** Não aplicável")
        st.write("❌ **Cola de Isopor:** Não aplicável")
        st.write("✅ **Cola de Acrílico:** R$ 0,085 (automática)")

with col2:
    st.markdown("**Imã + Chapa (Automático baseado no tipo)**")
    
    # Calcular automaticamente imãs baseado no tipo de tampa
    num_pares_ima_auto = calcular_custo_ima_chapa_automatico(tipo_tampa, largura) / PRECO_IMA_CHAPA_PAR
    if num_pares_ima_auto > 0:
        st.write(f"✅ **Pares de imã + chapa:** {int(num_pares_ima_auto)} (automático)")
        st.write(f"**Custo:** R$ {calcular_custo_ima_chapa_automatico(tipo_tampa, largura):.2f}")
    else:
        st.write("❌ **Imã + chapa:** Não aplicável para este tipo")
    
    st.markdown("**Caixa Kraft (Automático)**")
    # Calcular automaticamente baseado no volume da caixa
    volume_caixa = largura * altura * profundidade
    if volume_caixa <= 1000:  # Até 1L
        num_caixas_por_embalagem = 50
    elif volume_caixa <= 5000:  # Até 5L
        num_caixas_por_embalagem = 20
    elif volume_caixa <= 10000:  # Até 10L
        num_caixas_por_embalagem = 10
    else:  # Mais de 10L
        num_caixas_por_embalagem = 5
    
    #st.write(f"**Caixas por embalagem:** {num_caixas_por_embalagem} (automático)")
    #st.write(f"**Custo por caixa:** R$ {PRECO_CAIXA_KRAFT / num_caixas_por_embalagem:.2f}")

# Cálculos
#st.markdown("---")
#st.subheader("💰 Resumo de Custos")

# Cálculo da área baseado na estrutura
if estrutura == "Papelão":
    area_papelao = calcular_area_papelao(largura, altura, profundidade, tipo_tampa)
    custo_papelao = calcular_custo_papelao(largura, altura)
    custo_acrilico = 0
elif estrutura == "Acrílico":
    area_papelao = 0
    custo_papelao = 0
    # Para acrílico, calculamos a área total da caixa
    area_total_acrilico = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
    custo_acrilico = calcular_custo_acrilico(largura, altura)  # Usando as dimensões principais

# Custos variáveis
custo_serigrafia = CUSTO_SERIGRAFIA_POR_COR * num_cores_serigrafia if usar_serigrafia else 0
custo_impressao = CUSTO_IMPRESSAO_A4 if (usar_impressao_digital and tipo_impressao == "A4") else (CUSTO_IMPRESSAO_A3 if (usar_impressao_digital and tipo_impressao == "A3") else 0)

# Cálculo do custo de revestimento
if estrutura == "Papelão":
    # Calcular área de revestimento baseada nas dimensões da caixa
    area_revestimento = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
    area_revestimento_m2 = area_revestimento / 10000  # Converter cm² para m²
    
    # Custos por m² para cada tipo de revestimento
    if tipo_revestimento == "Vinil UV":
        custo_revestimento = area_revestimento_m2 * 140.0  # R$ 140,00/m²
    elif tipo_revestimento == "Papel":
        custo_revestimento = area_revestimento_m2 * 15.0  # R$ 15,00/m²
    else:
        custo_revestimento = 0
else:
    custo_revestimento = 0

# Custos de cola baseados na estrutura
if estrutura == "Papelão":
    custo_cola_pva = CUSTO_COLA_PVA
    custo_cola_adesiva = CUSTO_COLA_ADESIVA
    custo_cola_quente = CUSTO_COLA_QUENTE if usar_cola_quente else 0
    custo_cola_isopor = CUSTO_COLA_ISOPOR if usar_cola_isopor else 0
    custo_cola_acrilico = 0
elif estrutura == "Acrílico":
    custo_cola_pva = 0
    custo_cola_adesiva = 0
    custo_cola_quente = 0
    custo_cola_isopor = 0
    custo_cola_acrilico = CUSTO_COLA_ACRILICO
else:
    custo_cola_pva = 0
    custo_cola_adesiva = 0
    custo_cola_quente = 0
    custo_cola_isopor = 0
    custo_cola_acrilico = 0

custo_fita = metros_fita * PRECO_FITA_POR_M
custo_rebites = num_rebites * PRECO_REBITE_UNITARIO
custo_ima_chapa = calcular_custo_ima_chapa_automatico(tipo_tampa, largura)
custo_caixa_kraft = calcular_custo_caixa_kraft(num_caixas_por_embalagem)

# Custos adicionais (só aplicados se há serigrafia)
custo_retardador = CUSTO_RETARDADOR_VINILICO if usar_serigrafia else 0
custo_emulsao = CUSTO_EMULSAO_SENSIBILIZANTE if usar_serigrafia else 0
custo_cola_permanente = CUSTO_COLA_PERMANENTE if usar_serigrafia else 0

# Custo de frete
if tem_frete:
    if tipo_frete == "Recife":
        custo_frete = CUSTO_FRETE_RECIFE
    elif tipo_frete == "RMR":
        custo_frete = CUSTO_FRETE_RMR
    elif tipo_frete == "Interestadual":
        custo_frete = CUSTO_FRETE_INTERESTADUAL
    else:
        custo_frete = CUSTO_FRETE_RECIFE  # Default
else:
    custo_frete = 0

# Total de custos variáveis
total_custos_variaveis = (
    custo_papelao + custo_acrilico + custo_serigrafia + custo_impressao + 
    custo_revestimento + custo_cola_pva + custo_cola_adesiva + custo_cola_quente + custo_cola_isopor + 
    custo_cola_acrilico + custo_fita + custo_rebites + custo_ima_chapa + custo_caixa_kraft + 
    custo_retardador + custo_emulsao + custo_cola_permanente + custo_frete
)

# Aplicar multiplicador de complexidade
total_custos_variaveis_complexidade = aplicar_multiplicador_complexidade(
    total_custos_variaveis, tem_berco, tem_nicho
)

# Custo final
custo_final = CUSTO_FIXO_UNITARIO + total_custos_variaveis_complexidade

# Custo total do projeto
custo_total_projeto = custo_final * quantidade_caixas

# Exibição dos resultados
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Detalhamento de Custos**")
    
    # Custo fixo
    st.write(f"**Custo fixo:** R$ {CUSTO_FIXO_UNITARIO:.2f}")
    
    # Custos variáveis
    if estrutura == "Papelão":
        st.write(f"**Papelão:** R$ {custo_papelao:.2f}")
    elif estrutura == "Acrílico":
        st.write(f"**Acrílico:** R$ {custo_acrilico:.2f}")
    
    if usar_serigrafia:
        st.write(f"**Serigrafia ({num_cores_serigrafia} cores):** R$ {custo_serigrafia:.2f}")
    if tipo_impressao != "Nenhuma":
        st.write(f"**Impressão {tipo_impressao}:** R$ {custo_impressao:.2f}")
    
    # Custo de revestimento
    if estrutura == "Papelão":
        st.write(f"**Revestimento ({tipo_revestimento}):** R$ {custo_revestimento:.2f}")
    
    # Custos de cola
    if estrutura == "Papelão":
        st.write(f"**Cola PVA:** R$ {custo_cola_pva:.2f}")
        st.write(f"**Cola adesiva:** R$ {custo_cola_adesiva:.2f}")
        if usar_cola_quente:
            st.write(f"**Cola quente:** R$ {custo_cola_quente:.2f}")
        if usar_cola_isopor:
            st.write(f"**Cola de isopor:** R$ {custo_cola_isopor:.2f}")
    elif estrutura == "Acrílico":
        st.write(f"**Cola de acrílico:** R$ {custo_cola_acrilico:.2f}")
    
    # Outros custos
    if metros_fita > 0:
        st.write(f"**Fita:** R$ {custo_fita:.2f}")
    if num_rebites > 0:
        st.write(f"**Rebites:** R$ {custo_rebites:.2f}")
    if custo_ima_chapa > 0:
        st.write(f"**Imã + chapa:** R$ {custo_ima_chapa:.2f}")
    if num_caixas_por_embalagem > 1:
        st.write(f"**Caixa kraft:** R$ {custo_caixa_kraft:.2f}")
    if tem_frete:
        st.write(f"**Frete ({tipo_frete}):** R$ {custo_frete:.2f}")
    
    # Custos adicionais (só se há serigrafia)
    if usar_serigrafia:
        st.write(f"**Retardador vinílico:** R$ {custo_retardador:.2f}")
        st.write(f"**Emulsão + sensibilizante:** R$ {custo_emulsao:.2f}")
        st.write(f"**Cola permanente:** R$ {custo_cola_permanente:.2f}")
    
    st.write(f"**Total insumos:** R$ {total_custos_variaveis:.2f}")

# with col2:
#     st.markdown("**💰 Custo Final**")
    
#     # Complexidade
#     if tem_berco and tem_nicho:
#         st.write(f"**Complexidade extra (berço + nicho):** +80%")
#     elif tem_berco:
#         st.write(f"**Complexidade extra (berço):** +30%")
#     elif tem_nicho:
#         st.write(f"**Complexidade extra (nicho):** +50%")
#     else:
#         st.write("**Complexidade extra:** Nenhuma")
    
   # st.markdown("---")
   # st.markdown(f"### **Custo final unitário: R$ {custo_final:.2f}**")
   # st.markdown(f"### **Custo total do projeto: R$ {custo_total_projeto:.2f}**")
    
    # Informações adicionais
    # st.markdown("**📋 Informações Técnicas**")
    # st.write(f"**Estrutura:** {estrutura}")
    # if estrutura == "Papelão":
    #     st.write(f"**Área de papelão:** {area_papelao:.1f} cm²")
    # elif estrutura == "Acrílico":
    #     st.write(f"**Área de acrílico:** {largura * altura:.1f} cm²")
    # st.write(f"**Tipo de tampa:** {tipo_tampa}")
    # if tipo_revestimento == "Vinil UV":
    #     area_vinil_uv = (largura * altura) + (2 * largura * profundidade) + (2 * altura * profundidade)
    #     st.write(f"**Área de vinil UV:** {area_vinil_uv:.1f} cm²")

# Margem de lucro
#st.markdown("---")
#st.subheader("📈 Margem de Lucro")

#margem_lucro = st.slider("Margem de lucro (%)", min_value=0, max_value=100, value=20, step=5)
#preco_venda_unitario = custo_final * (1 + margem_lucro / 100)
#preco_venda_total = preco_venda_unitario * quantidade_caixas

#st.markdown(f"### **Preço de venda unitário: R$ {preco_venda_unitario:.2f}**")
#st.markdown(f"### **Preço total do projeto: R$ {preco_venda_total:.2f}**")

# Informações sobre o cálculo
#st.markdown("---")
#st.markdown("## 📚 Como os valores são calculados")

#st.markdown("""
### 💰 Custo Fixo
#- **R$ 26,92** por unidade (custo base de mão de obra e operacional)

### 🏗️ Estrutura da Caixa
#- **Papelão:** Permite revestimentos (vinil, papel, tecido), usa Cola PVA + Adesiva automaticamente
#- **Acrílico:** Sem revestimentos, usa apenas Cola de Acrílico

### 📦 Papelão
#- Área calculada baseada nas dimensões e tipo de tampa
#- **R$ 8,31/m²** - preço do papelão

### 🏗️ Acrílico
#- Área calculada baseada nas dimensões principais
#- **R$ 95,50/m²** - preço do acrílico

### 🎨 Insumos Gráficos
#- **Serigrafia:** R$ 1,01 por cor (disponível para ambas estruturas)
#- **Impressão Digital:** Opcional - A4: R$ 3,50, A3: R$ 5,00

### 🎨 Revestimentos (apenas para papelão)
#- **Vinil UV:** R$ 140,00/m²
#- **Papel:** R$ 15,00/m²

### 🔧 Insumos Físicos
#- **Cola PVA:** R$ 0,469 (automática para papelão)
#- **Cola adesiva:** R$ 0,058 (automática para papelão)
#- **Cola quente:** R$ 0,0125 (opcional para papelão)
#- **Cola de isopor:** R$ 0,015 (opcional para papelão)
#- **Cola de acrílico:** R$ 0,085 (automática para acrílico)
#- **Fita:** R$ 0,627/m
#- **Rebite:** R$ 0,10/un
#- **Imã + chapa:** R$ 1,58/par (automático: 1 par ≤10cm, 2 pares >10cm)
#- **Caixa kraft:** R$ 8,00 ÷ nº de caixas por embalagem

### 🔧 Custos Adicionais (só aplicados se há serigrafia)
#- **Retardador vinílico:** R$ 0,041
#- **Emulsão + sensibilizante:** R$ 0,058
#- **Cola permanente:** R$ 0,028

### 🚚 Frete
#- **Recife:** R$ 15,00 por unidade
#- **RMR:** R$ 20,00 por unidade  
#- **Interestadual:** R$ 35,00 por unidade

### ⚡ Multiplicadores de Complexidade
#- **Berço:** +30% no total variável
#- **Nicho:** +50% no total variável
#- **Berço + Nicho:** +80% no total variável

### 🧲 Regras Automáticas de Imã
#- **Tampa Imã + Largura ≤10cm:** 1 par de imã + chapa
#- **Tampa Imã + Largura >10cm:** 2 pares de imã + chapa
#- **Outros tipos:** Sem imã

### 🎨 Revestimentos por Estrutura
#- **Papelão:** Vinil adesivo, papel, tecido
#- **Acrílico:** Nenhum revestimento
#""")
