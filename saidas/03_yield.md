# 03 - Yield liquido sobre capital investido

_Gerado por `analise/04_yield.py`._

## Criterio, declarado antes do resultado

```
Melhor = retorno sobre o capital investido

  Yield liquido = (Receita anual - Custos operacionais) / Preco de aquisicao
  Regua        = CDI
```

O denominador e o que torna a analise uma decisao de investimento e nao um ranking de faturamento. Sem ele eu responderia *onde tem mais receita*; com ele respondo *onde vale a pena comprar*.

## Antes de usar: dois defeitos nos dados de compra

**1. Encoding.** `VivaReal_Itapema.csv` esta em **latin-1**. Lido como UTF-8 (o default do pandas), `Alto Sao Bento` e `Sertao do Trombudo` viram caractere de substituicao e **deixam de casar** com o bairro do Mesh. Corrigido em `comum.carregar()`.

**2. Valores sentinela em condominio e IPTU.** Nao sao dados faltantes declarados - sao zeros e uns:

| campo             | nulo | igual a 0 | <= R$50 (implausivel) | plausivel (> R$50) |
|-------------------|------|-----------|-----------------------|--------------------|
| monthly_condo_fee | 2441 | 2282      | 2719                  | 2944               |
| yearly_iptu       | 2624 | 2173      | 2447                  | 3033               |

Usar a mediana bruta desses campos levaria a condominio de R$1,00 em celulas inteiras. **Solucao:** derivo a *taxa* no subconjunto plausivel e aplico a todas as unidades pela area e pelo preco.

- Condominio: **R$ 5.10/m2/mes** (mediana de 2,944 anuncios com valor plausivel)
- IPTU: **0.091% do valor do imovel ao ano** (mediana de 3,033 anuncios)

## Premissas de custo e de mercado

| item                      | valor               | origem                                       |
|---------------------------|---------------------|----------------------------------------------|
| CDI (regua de comparacao) | 12.25% a.a.         | EXTERNA - Selic em jan/2025, data da captura |
| Desconto de negociacao    | 10%                 | EXTERNA - anuncio nao e preco fechado        |
| Noites por estadia        | 4                   | EXTERNA - dimensiona a limpeza               |
| Taxa de gestao            | 18% da receita      | negocio da Seazone                           |
| Comissao de canal         | 3% da receita       | padrao Airbnb                                |
| Limpeza e enxoval         | R$ 150/estadia      | estimativa                                   |
| Manutencao e vacancia     | 5% da receita       | provisao                                     |
| Condominio                | R$ 5.10/m2/mes      | DERIVADA do VivaReal limpo                   |
| IPTU                      | 0.091% do valor/ano | DERIVADA do VivaReal limpo                   |

> As tres premissas marcadas EXTERNA nao saem do dataset. Estao isoladas no topo de `analise/04_yield.py` para que qualquer leitor troque o numero e refaca a conta.

## Cruzamento Airbnb x VivaReal

- Celulas bairro x quartos com receita estimada: **24**
- Celulas com oferta de venda: **69**
- Celulas que casaram: **23**
- Apos exigir n_airbnb >= 20 **e** n_venda >= 15: **7 celulas analisaveis**

## Ranking por yield liquido - cenario base (janela = 45% da receita anual)

| bairro     | faixa_quartos | n_airbnb | n_venda | receita_ano | preco_compra | custos_totais | noi    | yield_liquido |
|------------|---------------|----------|---------|-------------|--------------|---------------|--------|---------------|
| Meia Praia | 2 quartos     | 96       | 241     | 40,187      | 963,000      | 19,611        | 20,575 | 2.14%         |
| Morretes   | 2 quartos     | 37       | 1237    | 26,756      | 675,000      | 13,795        | 12,961 | 1.92%         |
| Centro     | 2 quartos     | 48       | 87      | 35,759      | 990,000      | 17,735        | 18,024 | 1.82%         |
| Centro     | 1 quarto      | 69       | 22      | 24,556      | 801,000      | 11,693        | 12,863 | 1.61%         |
| Centro     | 3 quartos     | 31       | 436     | 54,044      | 1,890,000    | 26,207        | 27,838 | 1.47%         |
| Meia Praia | 3 quartos     | 240      | 1670    | 49,031      | 1,694,213    | 24,770        | 24,262 | 1.43%         |
| Meia Praia | 4+ quartos    | 31       | 1377    | 61,333      | 3,330,000    | 33,190        | 28,143 | 0.85%         |

**Regua: CDI = 12.25% a.a.** Nenhuma celula deve ser comentada sem essa comparacao ao lado.

## Sensibilidade a sazonalidade - onde a decisao se inverte

A janela observada e alta temporada + ombro. Nao anualizo cegamente: mostro o yield liquido sob as tres premissas.

| bairro     | faixa_quartos | conservador | base  | otimista |
|------------|---------------|-------------|-------|----------|
| Meia Praia | 2 quartos     | 1.63%       | 2.14% | 2.93%    |
| Morretes   | 2 quartos     | 1.44%       | 1.92% | 2.67%    |
| Centro     | 2 quartos     | 1.38%       | 1.82% | 2.52%    |
| Centro     | 1 quarto      | 1.24%       | 1.61% | 2.19%    |
| Centro     | 3 quartos     | 1.11%       | 1.47% | 2.04%    |
| Meia Praia | 3 quartos     | 1.07%       | 1.43% | 2.00%    |
| Meia Praia | 4+ quartos    | 0.61%       | 0.85% | 1.21%    |

- Melhor celula no cenario base: **Meia Praia / 2 quartos** com **2.14%** liquido a.a.
- Mesmo no cenario mais otimista de sazonalidade, o topo do ranking chega a **2.93%**.
- Diferenca para o CDI no cenario base: **-10.11 p.p.**

## Teste de teto - o argumento que nao depende de nenhuma premissa sazonal

A objecao obvia ao resultado acima e *voce chutou o fator sazonal*. Entao elimino a premissa: e se Itapema rodasse **os 365 dias do ano no ritmo da alta temporada observada** - mesma diaria de janeiro, mesma ocupacao de janeiro, zero queda de inverno? E um teto fisicamente impossivel, e serve justamente por isso: nenhum cenario real pode superar.

| bairro     | faixa_quartos | revpan | receita_teto | preco_compra | yield_teto |
|------------|---------------|--------|--------------|--------------|------------|
| Meia Praia | 2 quartos     | 235    | 85,723       | 963,000      | 5.27%      |
| Morretes   | 2 quartos     | 156    | 57,073       | 675,000      | 4.91%      |
| Centro     | 2 quartos     | 209    | 76,278       | 990,000      | 4.58%      |
| Centro     | 1 quarto      | 144    | 52,380       | 801,000      | 3.91%      |
| Centro     | 3 quartos     | 316    | 115,283      | 1,890,000    | 3.73%      |
| Meia Praia | 3 quartos     | 287    | 104,589      | 1,694,213    | 3.69%      |
| Meia Praia | 4+ quartos    | 358    | 130,831      | 3,330,000    | 2.3%       |

**Teto absoluto do melhor ativo do dataset: 5.27% liquido a.a.** contra **12.25%** do CDI na data da captura (e a Selic ainda subiu para ~15% ao longo de 2025).

> O ativo mais rentavel de Itapema renderia, no limite fisico, **menos da metade** do titulo publico - sem risco operacional, sem iliquidez, sem trabalho de gestao. A conclusao nao depende do fator sazonal que eu escolhi: **nao existe fator sazonal capaz de inverter essa comparacao.**

## Preco-teto - a que preco cada ativo empataria com o CDI

Se o retorno no preco pedido nao justifica a compra, a pergunta util para um comite nao e *compro ou nao*, e sim **a que preco eu compraria**. Resolvendo `NOI(P) / P = CDI` para P (o IPTU depende de P, os demais custos nao):

```
  P_teto = (Receita - custos variaveis - limpeza - condominio) / (CDI + IPTU%)
```

| bairro     | faixa_quartos | preco_compra | preco_teto | desconto_necessario |
|------------|---------------|--------------|------------|---------------------|
| Meia Praia | 2 quartos     | 963,000      | 173,818    | 82.0%               |
| Morretes   | 2 quartos     | 675,000      | 109,997    | 83.7%               |
| Centro     | 2 quartos     | 990,000      | 153,345    | 84.5%               |
| Centro     | 1 quarto      | 801,000      | 110,131    | 86.3%               |
| Centro     | 3 quartos     | 1,890,000    | 239,495    | 87.3%               |
| Meia Praia | 3 quartos     | 1,694,213    | 209,075    | 87.7%               |
| Meia Praia | 4+ quartos    | 3,330,000    | 252,580    | 92.4%               |

> Nenhum ativo do dataset empata com o CDI sem um desconto de pelo menos **82%** sobre o preco pedido. Esse e o numero que a Seazone levaria para uma mesa de negociacao - e a ordem de grandeza mostra que nao se trata de negociar melhor, e sim de que o mercado de Itapema **nao esta precificado para renda de short stay**: esta precificado para valorizacao e uso proprio.
