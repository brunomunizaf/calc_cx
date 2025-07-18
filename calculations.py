import math
from itertools import permutations
from constants import *

def calcular_area_papelao(largura, altura, profundidade, tipo_tampa):
    """Calcula a área total de papelão necessária baseada no tipo de tampa"""
    area_base = largura * altura
    
    if tipo_tampa == "Tampa Solta":
        # Base + 4 laterais + tampa
        area_laterais = 2 * (largura * profundidade) + 2 * (altura * profundidade)
        area_tampa = largura * altura
        return area_base + area_laterais + area_tampa
    
    elif tipo_tampa == "Tampa Livro":
        # Base + 4 laterais + tampa (tampa conectada)
        area_laterais = 2 * (largura * profundidade) + 2 * (altura * profundidade)
        area_tampa = largura * altura
        return area_base + area_laterais + area_tampa
    
    elif tipo_tampa == "Tampa Luva":
        # Base + 4 laterais + tampa + aba lateral
        area_laterais = 2 * (largura * profundidade) + 2 * (altura * profundidade)
        area_tampa = largura * altura
        area_aba = largura * profundidade  # Aba lateral
        return area_base + area_laterais + area_tampa + area_aba
    
    elif tipo_tampa == "Tampa Imã":
        # Base + 4 laterais + tampa + área para imã
        area_laterais = 2 * (largura * profundidade) + 2 * (altura * profundidade)
        area_tampa = largura * altura
        area_ima = largura * 2  # Área para imã (2cm de altura)
        return area_base + area_laterais + area_tampa + area_ima
    
    else:
        return area_base

def calcular_custo_papelao(largura, altura):
    """Calcula o custo do papelão baseado na área"""
    area_m2 = (largura * altura) / 10000  # Converter cm² para m²
    return area_m2 * PRECO_PAPELAO_POR_M2

def calcular_custo_vinil_uv(largura_vinil, altura_vinil):
    """Calcula o custo do vinil UV baseado na área"""
    area_m2 = (largura_vinil * altura_vinil) / 10000
    return area_m2 * CUSTO_VINIL_UV_POR_M2

def calcular_custo_acrilico(largura_acrilico, altura_acrilico):
    """Calcula o custo do acrílico baseado na área"""
    area_m2 = (largura_acrilico * altura_acrilico) / 10000
    return area_m2 * PRECO_ACRILICO_POR_M2

def calcular_custo_ima_chapa_automatico(tipo_tampa, largura):
    """Calcula automaticamente o custo de imã + chapa baseado no tipo de tampa"""
    if tipo_tampa == "Tampa Imã":
        # Regra: 1 par se largura ≤ 10cm, 2 pares se > 10cm
        num_pares = 1 if largura <= 10 else 2
        return num_pares * PRECO_IMA_CHAPA_PAR
    return 0

def calcular_max_caixas_por_embalagem(largura, altura, profundidade):
    """Calcula o número máximo de caixas que cabem na embalagem 50x50x60"""
    # Dimensões da caixa de papelão ondulado
    embalagem_largura = 50
    embalagem_altura = 50
    embalagem_profundidade = 60
    
    # Verificar se alguma dimensão da caixa é maior que a dimensão correspondente da embalagem
    # (considerando todas as rotações possíveis)
    caixa_dims = [largura, altura, profundidade]
    embalagem_dims = [embalagem_largura, embalagem_altura, embalagem_profundidade]
    
    # Verificar se a caixa cabe em alguma rotação
    cabe_em_alguma_rotacao = False
    for dims in permutations(caixa_dims):
        l, a, p = dims
        if l <= embalagem_largura and a <= embalagem_altura and p <= embalagem_profundidade:
            cabe_em_alguma_rotacao = True
            break
    
    # Se não cabe em nenhuma rotação, retorna 0
    if not cabe_em_alguma_rotacao:
        return 0
    
    max_caixas = 0
    
    # Testar todas as 6 rotações possíveis (3! = 6)
    for dims in permutations(caixa_dims):
        l, a, p = dims
        
        # Calcular quantas caixas cabem em cada direção
        num_largura = embalagem_largura // l
        num_altura = embalagem_altura // a
        num_profundidade = embalagem_profundidade // p
        
        # Total de caixas para esta rotação
        total_esta_rotacao = num_largura * num_altura * num_profundidade
        
        if total_esta_rotacao > max_caixas:
            max_caixas = total_esta_rotacao
    
    return max_caixas

def calcular_custo_caixa_papelao(num_caixas_por_embalagem):
    """Calcula o custo da caixa de papelão ondulado por unidade"""
    if num_caixas_por_embalagem > 0:
        return PRECO_CAIXA_PAPELAO / num_caixas_por_embalagem
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

def calcular_planificacao_tampa_solta(largura, altura, profundidade):
    """
    Calcula a planificação para caixas com tampa solta
    Retorna: (area_base, area_tampa, caixas_por_chapa, chapas_necessarias)
    """
    # Converter dimensões da caixa para mm
    largura_mm = largura * 10
    altura_mm = altura * 10
    profundidade_mm = profundidade * 10
    
    # Cálculo da base planificada
    largura_base_planificada = largura_mm + 2 * profundidade_mm
    altura_base_planificada = altura_mm + 2 * profundidade_mm
    area_base_planificada = largura_base_planificada * altura_base_planificada
    
    # Cálculo da tampa solta
    # Profundidade da tampa é fixa em 25mm
    profundidade_tampa_mm = 25
    
    # Largura e altura da face central da tampa (maior que a base em 3×espessura)
    largura_tampa = largura_mm + 3 * ESPESSURA_PAPELAO_MM
    altura_tampa = altura_mm + 3 * ESPESSURA_PAPELAO_MM
    
    # Planificação da tampa
    largura_tampa_planificada = largura_tampa + 2 * profundidade_tampa_mm
    altura_tampa_planificada = altura_tampa + 2 * profundidade_tampa_mm
    area_tampa_planificada = largura_tampa_planificada * altura_tampa_planificada
    
    # Calcular quantas caixas completas cabem em uma chapa
    # Área disponível na chapa (descontando margens)
    area_disponivel = (CHAPA_LARGURA_MM - MARGEM_MM) * (CHAPA_ALTURA_MM - MARGEM_MM)
    
    # Área necessária para uma caixa completa (base + tampa)
    area_caixa_completa = area_base_planificada + area_tampa_planificada
    
    # Número de caixas que cabem em uma chapa
    caixas_por_chapa = int(area_disponivel / area_caixa_completa)
    
    return {
        'area_base_mm2': area_base_planificada,
        'area_tampa_mm2': area_tampa_planificada,
        'area_caixa_completa_mm2': area_caixa_completa,
        'caixas_por_chapa': caixas_por_chapa,
        'dimensoes_base': (largura_base_planificada, altura_base_planificada),
        'dimensoes_tampa': (largura_tampa_planificada, altura_tampa_planificada)
    }

def calcular_planificacao_tampa_livro(largura, altura, profundidade):
    """
    Calcula a planificação para caixas com tampa-livro
    Retorna: (area_planificada, caixas_por_chapa, chapas_necessarias)
    """
    # Converter dimensões da caixa para mm
    largura_mm = largura * 10
    altura_mm = altura * 10
    profundidade_mm = profundidade * 10
    
    # Cálculo da planificação da tampa-livro
    # Largura planificada = largura da base + 2 × profundidade
    largura_planificada = largura_mm + 2 * profundidade_mm
    
    # Altura planificada = 2 × altura + profundidade
    altura_planificada = 2 * altura_mm + profundidade_mm
    
    # Área planificada
    area_planificada = largura_planificada * altura_planificada
    
    # Calcular quantas caixas cabem por chapa
    # Colunas por chapa = parte inteira de: 1040 ÷ (largura planificada + margem)
    colunas_por_chapa = int(CHAPA_LARGURA_MM / (largura_planificada + MARGEM_MM))
    
    # Linhas por chapa = parte inteira de: 860 ÷ (altura planificada + margem)
    linhas_por_chapa = int(CHAPA_ALTURA_MM / (altura_planificada + MARGEM_MM))
    
    # Caixas por chapa = colunas × linhas
    caixas_por_chapa = colunas_por_chapa * linhas_por_chapa
    
    return {
        'area_planificada_mm2': area_planificada,
        'caixas_por_chapa': caixas_por_chapa,
        'dimensoes_planificacao': (largura_planificada, altura_planificada),
        'colunas_por_chapa': colunas_por_chapa,
        'linhas_por_chapa': linhas_por_chapa
    }

def calcular_planificacao_tampa_ima(largura, altura, profundidade):
    """
    Calcula a planificação para caixas com tampa-imã
    Retorna: (area_base, area_tampa, area_ima, caixas_por_chapa)
    """
    # Converter dimensões da caixa para mm
    largura_mm = largura * 10
    altura_mm = altura * 10
    profundidade_mm = profundidade * 10
    
    # Cálculo da base planificada
    largura_base_planificada = largura_mm + 2 * profundidade_mm
    altura_base_planificada = altura_mm + 2 * profundidade_mm
    area_base_planificada = largura_base_planificada * altura_base_planificada
    
    # Cálculo da tampa com imã
    # Profundidade da tampa é fixa em 25mm
    profundidade_tampa_mm = 25
    
    # Largura e altura da face central da tampa (maior que a base em 3×espessura)
    largura_tampa = largura_mm + 3 * ESPESSURA_PAPELAO_MM
    altura_tampa = altura_mm + 3 * ESPESSURA_PAPELAO_MM
    
    # Planificação da tampa
    largura_tampa_planificada = largura_tampa + 2 * profundidade_tampa_mm
    altura_tampa_planificada = altura_tampa + 2 * profundidade_tampa_mm
    area_tampa_planificada = largura_tampa_planificada * altura_tampa_planificada
    
    # Cálculo da área para imã (2cm de altura)
    altura_ima_mm = 20  # 2cm
    area_ima_planificada = largura_mm * altura_ima_mm
    
    # Calcular quantas caixas completas cabem em uma chapa
    # Área disponível na chapa (descontando margens)
    area_disponivel = (CHAPA_LARGURA_MM - MARGEM_MM) * (CHAPA_ALTURA_MM - MARGEM_MM)
    
    # Área necessária para uma caixa completa (base + tampa + imã)
    area_caixa_completa = area_base_planificada + area_tampa_planificada + area_ima_planificada
    
    # Número de caixas que cabem em uma chapa
    caixas_por_chapa = int(area_disponivel / area_caixa_completa)
    
    return {
        'area_base_mm2': area_base_planificada,
        'area_tampa_mm2': area_tampa_planificada,
        'area_ima_mm2': area_ima_planificada,
        'area_caixa_completa_mm2': area_caixa_completa,
        'caixas_por_chapa': caixas_por_chapa,
        'dimensoes_base': (largura_base_planificada, altura_base_planificada),
        'dimensoes_tampa': (largura_tampa_planificada, altura_tampa_planificada),
        'dimensoes_ima': (largura_mm, altura_ima_mm)
    }

def calcular_planificacao_tampa_luva(largura, altura, profundidade):
    """
    Calcula a planificação para caixas com tampa-luva
    Retorna: (area_base, area_tampa, area_aba, caixas_por_chapa)
    """
    # Converter dimensões da caixa para mm
    largura_mm = largura * 10
    altura_mm = altura * 10
    profundidade_mm = profundidade * 10
    
    # Cálculo da base planificada
    largura_base_planificada = largura_mm + 2 * profundidade_mm
    altura_base_planificada = altura_mm + 2 * profundidade_mm
    area_base_planificada = largura_base_planificada * altura_base_planificada
    
    # Cálculo da tampa com luva
    # Profundidade da tampa é fixa em 25mm
    profundidade_tampa_mm = 25
    
    # Largura e altura da face central da tampa (maior que a base em 3×espessura)
    largura_tampa = largura_mm + 3 * ESPESSURA_PAPELAO_MM
    altura_tampa = altura_mm + 3 * ESPESSURA_PAPELAO_MM
    
    # Planificação da tampa
    largura_tampa_planificada = largura_tampa + 2 * profundidade_tampa_mm
    altura_tampa_planificada = altura_tampa + 2 * profundidade_tampa_mm
    area_tampa_planificada = largura_tampa_planificada * altura_tampa_planificada
    
    # Cálculo da aba lateral (largura × profundidade)
    area_aba_planificada = largura_mm * profundidade_mm
    
    # Calcular quantas caixas completas cabem em uma chapa
    # Área disponível na chapa (descontando margens)
    area_disponivel = (CHAPA_LARGURA_MM - MARGEM_MM) * (CHAPA_ALTURA_MM - MARGEM_MM)
    
    # Área necessária para uma caixa completa (base + tampa + aba)
    area_caixa_completa = area_base_planificada + area_tampa_planificada + area_aba_planificada
    
    # Número de caixas que cabem em uma chapa
    caixas_por_chapa = int(area_disponivel / area_caixa_completa)
    
    return {
        'area_base_mm2': area_base_planificada,
        'area_tampa_mm2': area_tampa_planificada,
        'area_aba_mm2': area_aba_planificada,
        'area_caixa_completa_mm2': area_caixa_completa,
        'caixas_por_chapa': caixas_por_chapa,
        'dimensoes_base': (largura_base_planificada, altura_base_planificada),
        'dimensoes_tampa': (largura_tampa_planificada, altura_tampa_planificada),
        'dimensoes_aba': (largura_mm, profundidade_mm)
    } 