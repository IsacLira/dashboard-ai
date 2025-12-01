# Analytics Agent - Queries de Teste

Este documento descreve as diferentes queries disponíveis para testar o agente de analytics.

## Como Usar

No arquivo `analytics_agent.py`, altere a linha:
```python
query = query_complex  # Altere para testar diferentes queries
```

Substitua `query_complex` por qualquer uma das queries abaixo.

## Queries Disponíveis

### 1. `query_basic` - Análise Estatística Básica
**Nível:** Iniciante  
**Testa:** Agregações simples, estatísticas descritivas

Calcula métricas estatísticas básicas (média, mediana, moda, variância, desvio padrão) de vendas por categoria.

### 2. `query_temporal` - Análise Temporal e Tendências
**Nível:** Intermediário  
**Testa:** Manipulação de datas, análise de séries temporais, sazonalidade

Analisa a evolução das vendas ao longo do tempo, identifica padrões sazonais e compara crescimento ano a ano.

### 3. `query_segmentation` - Análise de Segmentação e Correlação
**Nível:** Intermediário/Avançado  
**Testa:** Correlações, cálculos de margem, análise multi-dimensional

Explora relações entre variáveis (desconto vs lucro), calcula margens de lucro e analisa performance por segmento e região.

### 4. `query_products` - Análise de Performance de Produtos
**Nível:** Intermediário  
**Testa:** Rankings, filtros condicionais, análise de impacto

Identifica produtos mais vendidos, analisa margens de lucro e avalia impacto de descontos na lucratividade.

### 5. `query_geographic` - Análise Geográfica e de Clientes
**Nível:** Intermediário  
**Testa:** Agregações geográficas, análise de clientes, comparações regionais

Analisa performance por localização geográfica e identifica clientes mais valiosos.

### 6. `query_complex` - Análise Multi-dimensional Complexa
**Nível:** Avançado  
**Testa:** Agregações complexas, cálculos de ROI, rankings compostos

Realiza análise sofisticada combinando múltiplas dimensões (Category + Segment), calcula ROI e cria rankings baseados em múltiplos critérios.

## Exemplo de Execução

```bash
cd backend
source venv/bin/activate
export GOOGLE_API_KEY=your_key_here
python analytics_agent.py
```

## Capacidades Testadas

- ✅ Agregações (sum, mean, median, mode, var, std)
- ✅ Manipulação de datas e análise temporal
- ✅ Correlações estatísticas
- ✅ Filtros e condições complexas
- ✅ Rankings e top-N
- ✅ Cálculos de métricas de negócio (margem, ROI)
- ✅ Análise multi-dimensional (groupby com múltiplas colunas)
- ✅ Comparações entre grupos
