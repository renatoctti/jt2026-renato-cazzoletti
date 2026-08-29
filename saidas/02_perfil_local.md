# 02 - Perguntas 1, 2 e 3

_Gerado por `analise/03_perfil_local.py`. Base: 605 anuncios com receita estimada._

**Corte de n:** so comento celulas com **n >= 20**. Toda tabela mostra o n. Ranking sem n e ruido apresentado como conclusao.

**Metrica:** RevPAN = receita por noite disponivel = ADR x ocupacao. Uso **mediana** por padrao: receita de short stay tem cauda longa e um anuncio de luxo distorce a media do recorte inteiro.


## P1 - Qual o melhor perfil de imovel?

### Por numero de quartos

| faixa_quartos | n   | revpan_med | adr_med  | ocup_med | receita_77n |
|---------------|-----|------------|----------|----------|-------------|
| 4+ quartos    | 42  | 362.82     | 1,275.00 | 0.40     | 27,937.50   |
| 3 quartos     | 284 | 291.56     | 750.00   | 0.40     | 22,450.00   |
| 2 quartos     | 192 | 207.13     | 572.50   | 0.42     | 15,949.25   |
| 1 quarto      | 83  | 162.08     | 520.00   | 0.31     | 12,480.00   |

### Por tipologia (tipo de imovel)

| listing_type | n   | revpan_med | adr_med | ocup_med | receita_77n |
|--------------|-----|------------|---------|----------|-------------|
| apartamento  | 590 | 236.04     | 674.00  | 0.38     | 18,175.00   |

### Cruzamento tipologia x numero de quartos

| listing_type | faixa_quartos | n   | revpan_med | adr_med  | ocup_med | receita_77n |
|--------------|---------------|-----|------------|----------|----------|-------------|
| apartamento  | 4+ quartos    | 33  | 358.44     | 1,100.00 | 0.51     | 27,600.00   |
| apartamento  | 3 quartos     | 284 | 291.56     | 750.00   | 0.40     | 22,450.00   |
| apartamento  | 2 quartos     | 186 | 212.64     | 579.00   | 0.42     | 16,373.50   |
| apartamento  | 1 quarto      | 83  | 162.08     | 520.00   | 0.31     | 12,480.00   |

> **O erro que a receita absoluta induz:** o RevPAN cresce com o numero de quartos porque um imovel maior cobra mais caro. Isso responde *quem fatura mais por noite*, nao *quem rende mais por real investido*. A comparacao justa exige o preco de compra no denominador - e e o que a etapa 04 faz.


## P2 - Qual a melhor localizacao em termos de receita?

### Bruto (sem controle) - a leitura enganosa

| suburb     | n   | revpan_med | adr_med | ocup_med | receita_77n |
|------------|-----|------------|---------|----------|-------------|
| Meia Praia | 384 | 268.84     | 700.00  | 0.42     | 20,700.75   |
| Centro     | 151 | 187.01     | 627.00  | 0.34     | 14,400.00   |
| Morretes   | 49  | 185.71     | 554.25  | 0.34     | 14,300.00   |

### Controlando por numero de quartos - a leitura correta

Se o bairro X aparece melhor apenas porque concentra imoveis maiores, o efeito some aqui.

**RevPAN mediano por bairro x quartos** (celulas com n < 20 suprimidas):

| suburb     | 1 quarto | 2 quartos | 3 quartos | 4+ quartos | Studio |
|------------|----------|-----------|-----------|------------|--------|
| Centro     | 144      | 209       | 316       | -          | -      |
| Meia Praia | -        | 235       | 287       | 358        | -      |
| Morretes   | -        | 156       | -         | -          | -      |

**n de cada celula:**

| suburb                  | 1 quarto | 2 quartos | 3 quartos | 4+ quartos | Studio |
|-------------------------|----------|-----------|-----------|------------|--------|
| Canto da Praia          | 0        | 2         | 1         | 0          | 0      |
| Casa Branca             | 0        | 2         | 1         | 0          | 0      |
| Centro                  | 69       | 48        | 31        | 3          | 0      |
| Ilhota                  | 0        | 0         | 0         | 1          | 0      |
| Meia Praia              | 13       | 96        | 240       | 31         | 4      |
| Morretes                | 1        | 37        | 9         | 2          | 0      |
| Sertao do Trombudo      | 0        | 0         | 0         | 1          | 0      |
| Sertaozinho             | 0        | 0         | 0         | 2          | 0      |
| Tabuleiro dos Oliveiras | 0        | 7         | 2         | 1          | 0      |
| Varzea                  | 0        | 0         | 0         | 1          | 0      |

### Distancia ate a praia - o regressor que o rotulo de bairro esconde

_Orla estimada empiricamente: para cada faixa de latitude, a borda leste da mancha de anuncios (percentil 98 da longitude), suavizada. Itapema e uma enseada voltada para leste._

| faixa_praia | n   | revpan_med | adr_med | ocup_med | receita_77n |
|-------------|-----|------------|---------|----------|-------------|
| ate 200m    | 136 | 301.11     | 715.88  | 0.45     | 23,185.50   |
| 200-400m    | 185 | 264.94     | 700.00  | 0.40     | 20,400.00   |
| 400-800m    | 240 | 201.96     | 627.75  | 0.36     | 15,551.00   |
| 800m-1,5km  | 40  | 175.00     | 575.00  | 0.33     | 13,474.75   |

- Correlacao de Spearman entre distancia da praia e RevPAN: **-0.31**
- Dentro de **2 quartos apenas** (n=192), a correlacao e **-0.21** - o efeito nao e artefato de tamanho.


## P3 - Quais caracteristicas explicam as melhores receitas?

### Correlacao (Spearman) com RevPAN

| variavel                | corr_com_revpan | n   |
|-------------------------|-----------------|-----|
| numero de quartos       | 0.37            | 605 |
| capacidade (hospedes)   | 0.37            | 605 |
| distancia da praia (km) | -0.31           | 605 |
| numero de fotos         | 0.26            | 605 |
| taxa de limpeza         | 0.21            | 605 |
| numero de avaliacoes    | 0.21            | 605 |
| anfitriao superhost     | 0.20            | 605 |
| numero de amenidades    | 0.10            | 605 |
| anos como anfitriao     | 0.04            | 605 |
| nota media              | 0.03            | 605 |

### Regressao linear em log(RevPAN), variaveis padronizadas (n=605, R2 = 0.11)

Coeficiente = variacao em log(RevPAN) por **1 desvio-padrao** da variavel, mantendo as demais fixas.

| variavel                | coef_padronizado |
|-------------------------|------------------|
| capacidade (hospedes)   | 0.16             |
| anfitriao superhost     | 0.15             |
| anos como anfitriao     | 0.11             |
| numero de amenidades    | 0.09             |
| distancia da praia (km) | -0.08            |
| nota media              | 0.07             |
| numero de avaliacoes    | -0.05            |
| taxa de limpeza         | 0.05             |
| numero de fotos         | 0.02             |
| numero de quartos       | -0.01            |

> **Estes coeficientes sao associacao, nao causa.** Amenidades correlacionam entre si e com a qualidade geral do ativo - piscina pode ser proxy de *predio bom em rua boa*. O interesse aqui e **identificar sinal para triagem de compra**, nao estimar efeito causal.

> **Causalidade reversa em avaliacoes:** numero de reviews correlaciona com receita em boa parte porque **quem vende mais acumula mais reviews**, e nao o contrario. Nao trate *conseguir reviews* como alavanca de investimento - ela e consequencia, nao causa.
