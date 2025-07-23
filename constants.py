# Constantes de preços e custos

# Preços dos materiais principais
PRECO_PAPELAO_POR_M2 = 8.31  # R$ 8,31/m²
PRECO_ACRILICO_POR_M2 = 95.50  # R$ 95,50/m²

# Custos de impressão
CUSTO_SERIGRAFIA_POR_COR = 1.01  # R$ 1,01 por cor por impressão
CUSTO_IMPRESSAO_A4 = 3.50  # R$ 3,50 por unidade
CUSTO_IMPRESSAO_A3 = 5.00  # R$ 5,00 por unidade

# Custos de revestimento
CUSTO_VINIL_UV_POR_M2 = 140.0  # R$ 140,00/m²
CUSTO_PAPEL_POR_M2 = 15.0  # R$ 15,00/m²

# Custos de cola
CUSTO_COLA_PVA = 0.02  # R$ 0,02/ml
CUSTO_COLA_ADESIVA = 0.02  # R$ 0,02/ml
CUSTO_COLA_QUENTE = 0.0125  # R$ 0,0125/ml
CUSTO_COLA_ISOPOR = 0.015  # R$ 0,015/ml
CUSTO_COLA_ACRILICO = 0.085  # R$ 0,085/ml

ML_COLA_PVA_POR_M2 = 120  # ml de cola PVA por metro quadrado
ML_COLA_ADESIVA_POR_M = 10  # ml de cola adesiva por metro linear (perímetro)

# Custos de embalagem e acessórios
PRECO_FITA_POR_M = 0.627  # R$ 0,627/m
PRECO_REBITE_UNITARIO = 0.10  # R$ 0,10/un
PRECO_IMA_CHAPA_PAR = 1.58  # R$ 1,58/par
PRECO_CAIXA_PAPELAO = 12.0  # Caixa de papelão ondulado 50x35x35

# Custos adicionais (só aplicados se há serigrafia)
CUSTO_RETARDADOR_VINILICO = 0.041  # R$ 0,041 por unidade
CUSTO_EMULSAO_SENSIBILIZANTE = 0.058  # R$ 0,058 por unidade
CUSTO_COLA_PERMANENTE = 0.028  # R$ 0,028 por unidade

# Multiplicadores de complexidade
MULTIPLICADOR_BERCO = 1.30  # +30%
MULTIPLICADOR_AMBOS = 1.50  # +50% (berço + nicho)

# Dimensões das chapas de papelão
CHAPA_LARGURA_MM = 1040
CHAPA_ALTURA_MM = 860
MARGEM_MM = 5  # 0.5cm de margem entre planificações

# Espessura do papelão
ESPESSURA_PAPELAO_MM = 1.9

# Produção mensal para cálculo de custo fixo unitário
CAIXAS_POR_MES = 1000 