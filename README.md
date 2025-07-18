# 📦 Calculadora de Custo de Produção | Touché

Aplicação Streamlit para cálculo de custos de produção de caixas personalizadas.

## 🏗️ Estrutura do Projeto

O projeto foi organizado em módulos para melhor manutenibilidade e legibilidade:

### 📁 Arquivos Principais

- **`app.py`** - Arquivo principal da aplicação Streamlit
- **`constants.py`** - Todas as constantes de preços e configurações
- **`calculations.py`** - Funções de cálculo e lógica de negócio
- **`ui_components.py`** - Componentes de interface e exibição

### 🔧 Módulos

#### `constants.py`
Contém todas as constantes utilizadas na aplicação:
- Preços dos materiais (papelão, acrílico, colas, etc.)
- Custos de impressão e serigrafia
- Multiplicadores de complexidade
- Dimensões das chapas de papelão
- Configurações de produção

#### `calculations.py`
Funções de cálculo e lógica de negócio:
- **`calcular_area_papelao()`** - Calcula área de papelão por tipo de tampa
- **`calcular_custo_papelao()`** - Calcula custo do papelão
- **`calcular_planificacao_tampa_solta()`** - Planificação para tampa solta
- **`calcular_planificacao_tampa_livro()`** - Planificação para tampa-livro
- **`calcular_max_caixas_por_embalagem()`** - Algoritmo 3D de empacotamento
- **`aplicar_multiplicador_complexidade()`** - Aplica multiplicadores de berço/nicho
- **`determinar_colas_automaticas()`** - Determina colas baseado na estrutura

#### `ui_components.py`
Componentes de interface e exibição:
- **`display_fixed_costs_section()`** - Seção de custos fixos
- **`display_planification_section()`** - Seção de planificação de chapas
- **`display_cost_breakdown()`** - Detalhamento completo dos custos

#### `app.py`
Arquivo principal que:
- Define a interface do usuário
- Coordena os cálculos entre módulos
- Exibe os resultados finais

## 🚀 Como Executar

```bash
streamlit run app.py
```

## 📊 Funcionalidades

### 🎯 Cálculo de Custos
- **Custos fixos** - Aluguel, energia, água, pessoal, etc.
- **Custos variáveis** - Materiais, impressão, colas, embalagem
- **Multiplicadores de complexidade** - Berço (+30%), Nicho (+50%)

### 📐 Planificação de Chapas
- **Tampa Solta** - Base e tampa separadas
- **Tampa-Livro** - Peça única articulada
- **Otimização** - Calcula quantas caixas cabem por chapa (1040×860mm)

### 🏗️ Tipos de Estrutura
- **Papelão** - Permite revestimentos (Vinil UV, Papel)
- **Acrílico** - Sem revestimentos, apenas cola de acrílico

### 🎨 Insumos Gráficos
- **Serigrafia** - R$ 1,01 por cor por impressão
- **Impressão Digital** - A4 (R$ 3,50) ou A3 (R$ 5,00)

### 📦 Embalagem
- **Caixas de papelão ondulado** - 50×50×60cm (R$ 31,00)
- **Algoritmo 3D** - Calcula máximo de caixas por embalagem com rotação

## 🔧 Configurações

### Margens de Planificação
- **Margem entre peças**: 0.5cm (5mm)
- **Dimensões da chapa**: 1040mm × 860mm

### Produção Mensal
- **Base para custo fixo unitário**: 1000 caixas/mês

## 📈 Vantagens da Estrutura Modular

1. **Manutenibilidade** - Fácil atualização de preços em `constants.py`
2. **Testabilidade** - Funções isoladas em `calculations.py`
3. **Reutilização** - Componentes UI reutilizáveis
4. **Legibilidade** - Código organizado e bem documentado
5. **Escalabilidade** - Fácil adição de novos tipos de caixa

## 🛠️ Tecnologias

- **Streamlit** - Interface web
- **Python** - Lógica de negócio
- **Matemática** - Cálculos de área, volume e otimização 