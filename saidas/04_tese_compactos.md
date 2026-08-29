# 04 - A tese dos compactos no Centro

_Gerado por `analise/05_tese_compactos.py`._

> **A tese, como recebida:** *apartamentos compactos (studio/1 quarto) na regiao do Centro seriam a aposta mais eficiente para a Seazone.* Vem marcada como analise preliminar interna **ainda nao validada**. Trato como hipotese a testar, nao como orientacao a seguir.

## 0. Antes de testar: metade da tese nao e verificavel

A tese fala em *studio/1 quarto*. Os dois lados do dado se comportam muito diferente nessas duas categorias.

**Lado Airbnb:** dos 605 anuncios com receita estimavel, apenas **4 sao studio** - e **0 no Centro**. Nao existe amostra para estimar receita de studio no Centro.

**Lado VivaReal:** `bedrooms = 0` **nao significa studio**. A area mediana desses anuncios denuncia o campo:

| bairro             | n  | area_mediana |
|--------------------|----|--------------|
| Ilhota             | 5  | 450          |
| Casa Branca        | 13 | 331          |
| Alto Sao Bento     | 8  | 303          |
| Morretes           | 88 | 283          |
| Sertao do Trombudo | 12 | 247          |
| Meia Praia         | 28 | 140          |
| Andorinha          | 7  | 104          |
| Castelo Branco     | 6  | 90           |

Um *studio* de 283 a 450 m2 nao existe. `bedrooms = 0` no VivaReal e codigo de **nao informado**, nao de studio - o mesmo padrao de valor sentinela ja encontrado em condominio e IPTU.

> **Consequencia:** a perna *studio* da tese e **inverificavel** com estes dados, nos dois lados. Nao a sustento nem a derrubo: declaro que nao da para responder. O que testo a seguir e a perna verificavel - **1 quarto no Centro**, com n = 69 anuncios de Airbnb.

## A. Criterio 1 - receita absoluta por unidade

| bairro     | faixa_quartos | n   | revpan | adr      | ocupacao | destaque   |
|------------|---------------|-----|--------|----------|----------|------------|
| Meia Praia | 4+ quartos    | 31  | 358.44 | 1,200.00 | 0.40     |            |
| Centro     | 3 quartos     | 31  | 315.84 | 825.00   | 0.38     |            |
| Meia Praia | 3 quartos     | 240 | 286.55 | 750.00   | 0.40     |            |
| Meia Praia | 2 quartos     | 96  | 234.86 | 554.75   | 0.48     |            |
| Centro     | 2 quartos     | 48  | 208.98 | 768.75   | 0.36     |            |
| Morretes   | 2 quartos     | 37  | 156.36 | 477.67   | 0.31     |            |
| Centro     | 1 quarto      | 69  | 143.51 | 502.00   | 0.30     | <-- A TESE |

**Veredito A: a tese perde.** Compacto no Centro e o **7o de 7** em RevPAN. Nao e so a diaria menor: a **ocupacao tambem e menor** (0.30 contra 0.36 dos 2 quartos). O compacto vende menos noites, nao mais.

## B. Criterio 2 - yield liquido sobre capital (o criterio que adotei)

Este e o teste que importa: e aqui que a tese *deveria* vencer, porque o denominador de um compacto e menor.

| bairro     | faixa_quartos | n_airbnb | n_venda | preco_compra | receita_ano | yield_liquido | destaque   |
|------------|---------------|----------|---------|--------------|-------------|---------------|------------|
| Meia Praia | 2 quartos     | 96       | 241     | 963,000      | 40,187      | 2.14%         |            |
| Morretes   | 2 quartos     | 37       | 1237    | 675,000      | 26,756      | 1.92%         |            |
| Centro     | 2 quartos     | 48       | 87      | 990,000      | 35,759      | 1.82%         |            |
| Centro     | 1 quarto      | 69       | 22      | 801,000      | 24,556      | 1.61%         | <-- A TESE |
| Centro     | 3 quartos     | 31       | 436     | 1,890,000    | 54,044      | 1.47%         |            |
| Meia Praia | 3 quartos     | 240      | 1670    | 1,694,213    | 49,031      | 1.43%         |            |
| Meia Praia | 4+ quartos    | 31       | 1377    | 3,330,000    | 61,333      | 0.85%         |            |

**Veredito B: a tese tambem perde.** Compacto no Centro rende **1.61%** liquido a.a. e fica em **4o de 7**, atras de 2 quartos em Meia Praia, Morretes e no proprio Centro.

### Por que a tese falha justamente onde deveria ganhar

O argumento economico da tese e *o denominador e menor*. Em Itapema ele nao e:

| bairro     | quartos | n    | rs_m2  | area | preco     |
|------------|---------|------|--------|------|-----------|
| Centro     | 1       | 22   | 20,548 | 44   | 890,000   |
| Centro     | 2       | 87   | 13,068 | 85   | 1,100,000 |
| Centro     | 3       | 436  | 15,789 | 131  | 2,100,000 |
| Centro     | 4       | 440  | 18,734 | 200  | 3,900,000 |
| Meia Praia | 1       | 59   | 21,250 | 40   | 880,000   |
| Meia Praia | 2       | 241  | 12,826 | 85   | 1,070,000 |
| Meia Praia | 3       | 1670 | 14,920 | 129  | 1,882,459 |
| Meia Praia | 4       | 1380 | 18,617 | 190  | 3,700,000 |
| Morretes   | 1       | 49   | 12,889 | 44   | 600,000   |
| Morretes   | 2       | 1237 | 11,111 | 69   | 750,000   |
| Morretes   | 3       | 306  | 8,333  | 100  | 790,000   |
| Morretes   | 4       | 69   | 25,435 | 186  | 5,500,000 |

**O compacto e pequeno, mas nao e barato.** Um quarto no Centro custa **R$ 20,548/m2** contra **R$ 13,068/m2** de um 2 quartos no mesmo bairro - um premio de **57%**. E o metro quadrado mais caro da cidade, acima ate do 4 quartos.

> A tese assume implicitamente que preco acompanha area. Nao acompanha: o mercado de Itapema **ja precifica** a escassez de compactos. O desconto de capital que tornaria a tese verdadeira **ja foi capturado pelo vendedor** - e com ocupacao menor, a conta fecha negativa nos dois lados.

## C. Criterio 3 - receita por m2

Unico criterio em que a tese tem chance real: a diaria nao cai proporcionalmente a area.

| bairro     | faixa_quartos | area | receita_ano | receita_m2_ano | destaque   |
|------------|---------------|------|-------------|----------------|------------|
| Centro     | 1 quarto      | 44   | 24,556      | 564            | <-- A TESE |
| Meia Praia | 2 quartos     | 85   | 40,187      | 473            |            |
| Centro     | 2 quartos     | 85   | 35,759      | 421            |            |
| Centro     | 3 quartos     | 131  | 54,044      | 413            |            |
| Morretes   | 2 quartos     | 69   | 26,756      | 388            |            |
| Meia Praia | 3 quartos     | 129  | 49,031      | 380            |            |
| Meia Praia | 4+ quartos    | 190  | 61,333      | 323            |            |

**Veredito C: aqui a tese acerta parcialmente** - o compacto sobe para **1o de 7** em receita por m2. Confirma a intuicao de que o compacto usa melhor a area. **Mas receita por m2 nao paga o investidor**: quem compra desembolsa o preco do imovel, nao o preco do metro quadrado. Como o m2 do compacto e o mais caro da cidade, a vantagem em produtividade de area nao chega ao retorno.

## D. Criterio 4 - liquidez: da para montar posicao?

A Seazone nao compra uma unidade: ela origina predios e opera portfolio. Uma tese verdadeira em teoria mas com cinco unidades a venda e irrelevante na pratica.

| bairro             | bedrooms | unidades_a_venda | preco_mediano | area_mediana |
|--------------------|----------|------------------|---------------|--------------|
| Morretes           | 0        | 88               | 650,000       | 283          |
| Meia Praia         | 1        | 59               | 880,000       | 40           |
| Morretes           | 1        | 49               | 600,000       | 44           |
| Meia Praia         | 0        | 28               | 1,656,250     | 140          |
| Centro             | 1        | 22               | 890,000       | 44           |
| Casa Branca        | 0        | 13               | 810,000       | 331          |
| Andorinha          | 1        | 13               | 750,000       | 48           |
| Sertao do Trombudo | 0        | 12               | 390,000       | 247          |
| Alto Sao Bento     | 0        | 8                | 375,000       | 303          |
| Andorinha          | 0        | 7                | 2,197,000     | 104          |
| Canto da Praia     | 1        | 7                | 780,000       | 50           |
| Castelo Branco     | 0        | 6                | 1,636,924     | 90           |
| Ilhota             | 0        | 5                | 1,200,000     | 450          |
| Ilhota             | 1        | 5                | 220,000       | 38           |
| Jardim Praia Mar   | 1        | 5                | 740,000       | 62           |
| Sertao do Trombudo | 1        | 4                | 790,000       | 78           |
| Centro             | 0        | 3                | 2,145,000     | 123          |

**Veredito D: a tese e rasa tambem na oferta.** Existem **22 unidades de 1 quarto a venda no Centro** - contra 241 de 2 quartos em Meia Praia. Mesmo se a tese estivesse certa, nao daria para montar um portfolio relevante sem pressionar o proprio preco de compra.

## Veredito final sobre a tese

| criterio                | veredito              | evidencia                                                     |
|-------------------------|-----------------------|---------------------------------------------------------------|
| Studio (metade da tese) | INVERIFICAVEL         | 4 studios no Airbnb; bedrooms=0 no VivaReal e 'nao informado' |
| A. Receita por unidade  | NAO SUSTENTA          | 7o de 7 em RevPAN; ocupacao menor, nao maior                  |
| B. Yield sobre capital  | NAO SUSTENTA          | 4o de 7; o m2 do compacto e o mais caro da cidade             |
| C. Receita por m2       | SUSTENTA PARCIALMENTE | 1o de 7, mas nao e o que paga o investidor                    |
| D. Liquidez de compra   | NAO SUSTENTA          | 22 unidades a venda no Centro                                 |

**Minha posicao:** *nao sustento a tese.* Ela e verdadeira apenas no criterio de receita por m2 - que mede produtividade de area, nao retorno sobre capital. No criterio que adotei, retorno sobre o capital investido, o compacto no Centro fica em 4o lugar de 7, e falha pelo motivo oposto ao que a tese supoe: **nao porque renda pouco, mas porque custa caro demais por metro quadrado**. O mercado ja precificou a escassez de compactos.

**A condicao que inverteria minha posicao,** declarada: se aparecesse oferta de compactos no Centro a **R$ 13,068/m2** - o mesmo m2 de um 2 quartos - o yield do compacto subiria de 1.61% para cerca de 2.52% e a tese passaria a vencer. Ou seja: a tese nao esta errada sobre o *tipo de ativo*, esta errada sobre o *preco atual* desse ativo. Em lancamento ou compra em bloco com desconto, ela volta a valer - e e assim que a Seazone compra.

> **O que a tese acerta:** o instinto de padronizacao e escala. Unidades compactas quase identicas no mesmo predio tem custo marginal de operacao muito menor. Esse raciocinio esta correto e permanece valido - apenas nao no preco pedido hoje no Centro.
