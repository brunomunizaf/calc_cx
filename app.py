import math
import streamlit as st

# Funções de cálculo

def calcular_area_cachepot_base(largura, altura, profundidade):
    area_base = largura * altura
    area_laterais = 2 * (largura * profundidade) + 2 * (altura * profundidade)
    return area_base + area_laterais

def calcular_area_tampa_cachepot(largura, altura):
    folga = 1.0
    profundidade = 3.0
    largura_tampa = largura + folga
    altura_tampa = altura + folga
    area_base = largura_tampa * altura_tampa
    area_laterais = 2 * largura_tampa * profundidade + 2 * altura_tampa * profundidade
    return area_base + area_laterais

def calcular_area_tampa_livro(largura, altura, profundidade):
    folga = 2.0
    largura_folga = largura + folga
    altura_folga = altura + folga
    area_placas = 2 * (largura_folga * altura_folga)
    area_lombada = profundidade * altura_folga
    return area_placas + area_lombada

def calcular_area_tampa_ima(largura, altura, profundidade):
    area_livro = calcular_area_tampa_livro(largura, altura, profundidade)
    folga = 2.0
    altura_folga = altura + folga
    altura_lingua = profundidade - 0.5
    area_lingua = altura_lingua * altura_folga
    return area_livro + area_lingua

def calcular_rendimento_por_placa(largura_planificada, altura_planificada, gap=0.5, largura_placa=104.0, altura_placa=86.0):
    caixas_por_linha = math.floor((largura_placa + gap) / (largura_planificada + gap))
    caixas_por_coluna = math.floor((altura_placa + gap) / (altura_planificada + gap))
    return caixas_por_linha * caixas_por_coluna

def calcular_quantidade_placas(quantidade_caixas, rendimento_por_placa):
    return math.ceil(quantidade_caixas / rendimento_por_placa)

def calcular_custo_total_papelao(quantidade_placas, preco_por_placa):
    return quantidade_placas * preco_por_placa

def calcular_custo_total_papel(area_total_cm2, preco_folha, largura_folha=66.0, altura_folha=96.0):
    area_folha_cm2 = largura_folha * altura_folha
    area_total_ambos_lados = area_total_cm2 * 2
    folhas_necessarias = math.ceil(area_total_ambos_lados / area_folha_cm2)
    return folhas_necessarias * preco_folha, folhas_necessarias

# App Streamlit

st.set_page_config(page_title="Cálculo de Custo de Caixa Cartonada")
st.title("🧮 Cálculo de Custo - Caixa Cartonada")

col1, col2, col3 = st.columns(3)
with col1:
    largura = st.number_input("Largura da base (cm)", value=20.0)
with col2:
    altura = st.number_input("Altura da base (cm)", value=15.0)
with col3:
    profundidade = st.number_input("Profundidade da caixa (cm)", value=10.0)

quantidade_caixas = st.number_input("Quantidade de caixas", value=50)
preco_por_placa = st.number_input("Preço da placa de papelão (R$)", value=15.0)
preco_folha_papel = st.number_input("Preço da folha de papel (R$)", value=5.0)

mao_obra_unitaria = st.number_input("Custo fixo de mão de obra por caixa (R$)", value=2.00)
custo_energia_unitario = st.number_input("Custo fixo de energia por caixa (R$)", value=0.30)
custo_impressao_unitario = st.number_input("Custo fixo de impressão por caixa (R$)", value=1.20)
custo_ima_chapa_unitario = st.number_input("Custo de imã + chapa por caixa (R$)", value=2.00)

tipo_tampa = st.selectbox("Tipo de tampa", ["cachepot", "livro", "ima"])

area_base = calcular_area_cachepot_base(largura, altura, profundidade)

if tipo_tampa == "cachepot":
    area_tampa = calcular_area_tampa_cachepot(largura, altura)
elif tipo_tampa == "livro":
    area_tampa = calcular_area_tampa_livro(largura, altura, profundidade)
elif tipo_tampa == "ima":
    area_tampa = calcular_area_tampa_ima(largura, altura, profundidade)
else:
    st.error("Tipo de tampa inválido.")
    st.stop()

area_total = area_base + area_tampa
largura_planificada = largura + 2 * profundidade
altura_planificada = altura + 2 * profundidade

rendimento = calcular_rendimento_por_placa(largura_planificada, altura_planificada)
quantidade_placas = calcular_quantidade_placas(quantidade_caixas, rendimento)
custo_total_papelao = calcular_custo_total_papelao(quantidade_placas, preco_por_placa)
custo_unitario_papelao = custo_total_papelao / quantidade_caixas if quantidade_caixas else 0

custo_total_papel, folhas_necessarias = calcular_custo_total_papel(area_total * quantidade_caixas, preco_folha_papel)
custo_unitario_papel = custo_total_papel / quantidade_caixas if quantidade_caixas else 0

custo_unitario_cola = 0.50
custo_total_cola = custo_unitario_cola * quantidade_caixas

custo_total_mao_obra = mao_obra_unitaria * quantidade_caixas
custo_total_energia = custo_energia_unitario * quantidade_caixas
custo_total_impressao = custo_impressao_unitario * quantidade_caixas
custo_total_ima = custo_ima_chapa_unitario * quantidade_caixas

custo_total_geral = custo_total_papelao + custo_total_papel + custo_total_cola + custo_total_mao_obra + custo_total_energia + custo_total_impressao + custo_total_ima
custo_unitario_geral = custo_total_geral / quantidade_caixas if quantidade_caixas else 0

# Entrada de margem de lucro
margem_lucro_percentual = st.number_input("Margem de lucro desejada (%)", value=20.0)
preco_venda_unitario = custo_unitario_geral * (1 + margem_lucro_percentual / 100)
preco_venda_total = preco_venda_unitario * quantidade_caixas

# Resultados
st.markdown("---")
st.subheader("📊 Papelão")
st.write(f"**Área total por caixa:** {area_total / 10_000:.3f} m²")
st.write(f"**Rendimento por placa:** {rendimento} caixas")
st.write(f"**Placas necessárias:** {quantidade_placas}")
st.write(f"**Custo total de papelão:** R${custo_total_papelao:.2f}")
st.write(f"**Custo unitário de papelão:** R${custo_unitario_papelao:.2f}")

st.markdown("---")
st.subheader("📊 Papel")
st.write(f"**Folhas necessárias:** {folhas_necessarias}")
st.write(f"**Custo total de papel (interno + externo):** R${custo_total_papel:.2f}")
st.write(f"**Custo unitário de papel:** R${custo_unitario_papel:.2f}")

st.markdown("---")
st.subheader("📊 Cola")
st.write(f"**Custo total de cola (fixo):** R${custo_total_cola:.2f}")
st.write(f"**Custo unitário de cola:** R${custo_unitario_cola:.2f}")

st.markdown("---")
st.subheader("📊 Mão de Obra")
st.write(f"**Custo total de mão de obra:** R${custo_total_mao_obra:.2f}")
st.write(f"**Custo unitário de mão de obra:** R${mao_obra_unitaria:.2f}")

st.markdown("---")
st.subheader("📊 Energia, Impressão e Imã")
st.write(f"**Custo total de energia:** R${custo_total_energia:.2f}")
st.write(f"**Custo total de impressão:** R${custo_total_impressao:.2f}")
st.write(f"**Custo total de imã + chapa:** R${custo_total_ima:.2f}")

st.markdown("---")
st.subheader("💰 Custo Total")
st.write(f"**Custo total do projeto:** R${custo_total_geral:.2f}")
st.write(f"**Custo total unitário por caixa:** R${custo_unitario_geral:.2f}")

st.markdown("---")
st.subheader("📈 Preço com Lucro")
st.write(f"**Preço de venda unitário com {margem_lucro_percentual:.1f}% de lucro:** R${preco_venda_unitario:.2f}")
st.write(f"**Preço total com lucro:** R${preco_venda_total:.2f}")

st.markdown("---")
st.write("Obs: Os valores acima são aproximações grosseiras.")

st.markdown("## 🧾 Como os valores são calculados")
st.markdown("""
### 📦 Papelão
- Calculamos a área total da caixa (base + laterais + tampa).
- Verificamos quantas caixas cabem em uma placa de papelão.
- Multiplicamos a quantidade de placas pelo valor unitário da placa.

### 🧻 Papel (Revestimento Interno + Externo)
- Calculamos a área da caixa e multiplicamos por 2 (interno + externo).
- Dividimos pela área de uma folha de papel (66x96cm).
- Multiplicamos o número de folhas pelo preço unitário da folha.

### 🧴 Cola
- Valor inserido manualmente por unidade de caixa.

### 🛠️ Mão de Obra
- Valor informado por unidade, estimado com base no custo para montar cada caixa.

### ⚡ Energia
- Valor estimado por unidade de caixa, referente ao uso de máquinas.

### 🖨️ Impressão
- Valor fixo inserido por unidade de caixa (UV, hot stamp, etc.).

### 🧲 Imã + Chapa
- Valor fixo por caixa para modelos que incluem esse acabamento.

### 💰 Margem de Lucro
- O lucro é calculado sobre o custo total unitário.
- Você informa o percentual desejado e o sistema calcula o preço de venda.
""")
