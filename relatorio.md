# Recomendação de investimento — Itapema (SC)

**Desafio Jovens Talentos AI Builder 2026 · Seazone**
Renato Cazzoletti · análise sobre dados de Airbnb e VivaReal de Itapema

---

## A recomendação, em três parágrafos

**Não comprar nenhum dos ativos deste dataset ao preço pedido.** O melhor perfil de
Itapema — apartamento de **2 quartos em Meia Praia, a menos de 400 m da praia** —
rende, na minha estimativa, **2,14% líquido ao ano** sobre o capital investido. O
CDI na data da captura dos dados era **12,25%**. Para empatar com o título público,
esse mesmo apartamento precisaria ser comprado com **82% de desconto** sobre o preço
anunciado. Isso não é uma questão de negociar melhor: o mercado de Itapema está
precificado para valorização e uso próprio, não para renda de short stay.

**O que eu recomendo que a Seazone faça é o que ela já sabe fazer melhor: originar e
operar, não comprar.** A receita da Seazone é percentual sobre volume administrado —
ela não precisa do denominador. Um apartamento de 2 quartos em Meia Praia gera
**~R$ 40 mil de receita anual**, dos quais a taxa de gestão captura ~R$ 7 mil sem
imobilizar R$ 1 milhão. O ativo que é péssimo para o proprietário continua sendo bom
para o gestor. A recomendação acionável é **captação de proprietários no eixo Meia
Praia até 400 m da orla, tipologia 2–3 quartos** — o recorte com maior RevPAN e maior
densidade de unidades comparáveis da cidade.

**Se a Seazone quiser mesmo comprar**, a única porta que fecha a conta é **compra em
bloco / lançamento com desconto de incorporador** — e aí a tese dos compactos volta
a ficar interessante, pelo motivo que explico na seção 6. No preço de tabela do
VivaReal, nenhuma célula analisada justifica o risco operacional, a iliquidez e o
trabalho de gestão que renda fixa não tem.

---

## 1. O critério de "melhor", declarado antes do resultado

O edital deixa "melhor", "perfil" e "localização" abertos. Escolhi:

```
Melhor = retorno sobre o capital investido

  Yield líquido = (Receita anual − Custos operacionais) ÷ Preço de aquisição
  Régua         = CDI (12,25% a.a., Selic em jan/2025)
```

**Por que este e não receita.** A pergunta 4 é "o que você compraria" — uma decisão de
alocação de capital, não de maximização de faturamento. Sem o denominador, 3 quartos
sempre vence studio, porque custa três vezes mais. O `VivaReal_Itapema.csv` entrega o
preço de compra, e é ele que transforma "onde tem mais receita" em "onde vale a pena
investir". **Capital tem custo de oportunidade**, e comparar com o CDI é como um comitê
de investimento brasileiro decide de verdade.

Este critério foi fixado antes de olhar o resultado e não foi ajustado depois.

---

## 2. O ativo central: estimar receita, não preço

`Price_AV_Itapema.csv` traz **preço anunciado de noites disponíveis**, não receita
realizada. Um imóvel caríssimo vazio 300 noites por ano não é bom investimento. Então:

```
Receita = ADR × Ocupação        RevPAN = receita por noite disponível
```

**De onde saiu a ocupação.** O arquivo tem 3 dias de captura (06, 07 e 20/01/2025) da
mesma janela futura. Uma noite disponível numa captura e ausente na seguinte foi,
provavelmente, reservada no intervalo.

**A armadilha que quase me pegou.** Cada captura enxerga ~90 noites *à frente da
própria data*. Se eu contasse "sumiu = reservou" sobre a união das datas, as 14 noites
que apenas saíram do horizonte da captura de 20/01 virariam reservas — número
plausível, silenciosamente inflado, e nada no código acusaria erro. A comparação só é
válida na **interseção dos horizontes: 20/01 a 06/04, 77 noites**. Como duas das três
capturas são consecutivas, existe **um único intervalo de comparação útil** (13 dias).

**Como testei se a inferência é real.** Se "sumir" fosse bloqueio do proprietário ou
manutenção — ruído aleatório —, as noites que sumiram teriam preço igual às que
sobraram. Não têm:

| noite ofertada em 06–07/01 | noites | preço mediano |
|---|---|---|
| sobrou disponível | 27.339 | R$ 641 |
| **SUMIU (reservada)** | 4.460 | **R$ 675** |

Sumiram 14,0% em 13 dias; reapareceram apenas 1,8%. **A noite que sumiu era mais cara
que a que sobrou** — assimetria de preço e de direção incompatível com bloqueio
aleatório, e compatível com reserva: as datas mais desejadas são as mais caras e as
que vendem primeiro. Isso me deu de brinde o **ADR correto**: o preço do que
efetivamente vendeu, não a média da vitrine.

**Segunda validação.** `ocupacao` (medida na captura final) e `pickup_13d` (medido
entre capturas) são construídas de dados diferentes e correlacionam **0,52**. Duas
medidas independentes apontando junto.

Resultado: **605 anúncios** com receita estimável — ocupação mediana **37,7%**, ADR
mediano **R$ 674**, RevPAN mediano **R$ 237**.

---

## 3. P1 — Qual o melhor perfil de imóvel?

| nº de quartos | n | RevPAN mediano | ADR | ocupação |
|---|---|---|---|---|
| 4+ quartos | 42 | R$ 363 | 1.275 | 0,40 |
| 3 quartos | 284 | R$ 292 | 750 | 0,40 |
| 2 quartos | 192 | R$ 207 | 573 | 0,42 |
| 1 quarto | 83 | R$ 162 | 520 | **0,31** |

Por **receita**, o RevPAN cresce com o tamanho — mas isso só diz que imóvel maior cobra
mais caro. Por **retorno sobre capital**, a ordem se inverte:

| perfil | preço de compra | receita/ano | **yield líquido** |
|---|---|---|---|
| **Meia Praia · 2 quartos** | R$ 963.000 | R$ 40.187 | **2,14%** |
| Morretes · 2 quartos | R$ 675.000 | R$ 26.756 | 1,92% |
| Centro · 2 quartos | R$ 990.000 | R$ 35.759 | 1,82% |
| Centro · 1 quarto | R$ 801.000 | R$ 24.556 | 1,61% |
| Centro · 3 quartos | R$ 1.890.000 | R$ 54.044 | 1,47% |
| Meia Praia · 3 quartos | R$ 1.694.213 | R$ 49.031 | 1,43% |
| Meia Praia · 4+ quartos | R$ 3.330.000 | R$ 61.333 | 0,85% |

**Resposta:** apartamento de **2 quartos, imóvel inteiro**. `apartamento` é também a
tipologia dominante e a única com amostra sólida (casa e hotel têm cobertura de preço
muito menor). Repare que 4+ quartos tem o **maior RevPAN e o pior yield** — é
exatamente o erro que ranquear por receita absoluta induz.

Uma observação que não esperava: **compactos têm ocupação menor (0,31), não maior.**
O compacto vende menos noites, não mais.

---

## 4. P2 — Qual a melhor localização?

**A leitura bruta engana.** Meia Praia parece muito superior ao Centro (RevPAN 269 vs
187). Controlando por número de quartos, a diferença encolhe e em parte se inverte:

| bairro | 1 quarto | 2 quartos | 3 quartos | 4+ quartos |
|---|---|---|---|---|
| Centro | 144 | 209 | **316** | – |
| Meia Praia | – | 235 | 287 | 358 |
| Morretes | – | 156 | – | – |

**Centro vence Meia Praia em 3 quartos.** A vantagem bruta de Meia Praia era, em boa
parte, efeito de composição: ela concentra 240 dos 284 imóveis de 3 quartos, o Centro
concentra os de 1 quarto. Sem esse controle eu estaria medindo tamanho e chamando de
localização.

**O que de fato explica a localização é a distância da praia, não o rótulo do bairro:**

| distância da orla | n | RevPAN mediano |
|---|---|---|
| até 200 m | 136 | **R$ 301** |
| 200–400 m | 185 | R$ 265 |
| 400–800 m | 240 | R$ 202 |
| 800 m–1,5 km | 40 | R$ 175 |

Gradiente monotônico, correlação de Spearman **−0,31** — e **−0,21 dentro de 2 quartos
apenas**, então não é artefato de tamanho. A orla foi estimada empiricamente a partir
de latitude/longitude (borda leste da mancha de anúncios por faixa de latitude).

**Resposta:** o eixo **Meia Praia até 400 m da orla**, que combina o melhor RevPAN com
a maior profundidade de oferta. Mas a variável de decisão é *distância da praia*, e
ela atravessa os bairros.

---

## 5. P3 — O que explica as melhores receitas?

| variável | correlação com RevPAN | coef. padronizado (regressão) |
|---|---|---|
| capacidade (hóspedes) | +0,37 | **+0,16** |
| nº de quartos | +0,37 | −0,01 |
| distância da praia | **−0,31** | −0,08 |
| anfitrião superhost | +0,20 | +0,15 |
| nº de fotos | +0,26 | +0,02 |
| nº de avaliações | +0,21 | −0,05 |
| nota média | +0,03 | +0,07 |

Regressão em log(RevPAN), n=605, **R² = 0,11** — baixo, e digo isso de propósito:
**as características observáveis explicam pouco da variação de receita.** A maior
parte está em fatores que o dataset não tem (qualidade do prédio, mobília, gestão de
preço). Quem prometer um modelo preditivo aqui está exagerando.

Três leituras críticas:

- **Capacidade absorve nº de quartos.** São colineares; na regressão conjunta o
  coeficiente de quartos vai a zero. O que paga é quantas pessoas cabem.
- **Associação, não causa.** Amenidades correlacionam entre si e com a qualidade geral
  do ativo — piscina pode ser proxy de "prédio bom em rua boa". Serve para **triagem
  de compra**, não para estimar efeito causal.
- **Causalidade reversa em avaliações.** Nº de reviews correlaciona com receita em boa
  parte porque **quem vende mais acumula mais reviews**. Não é alavanca de
  investimento; é consequência. Note que na regressão o coeficiente inclusive vira
  negativo, controlando pelo resto.

---

## 6. Posição sobre a tese dos compactos no Centro

> *"Apartamentos compactos (studio/1 quarto) na região do Centro seriam a aposta mais
> eficiente."* — análise interna, marcada como **não validada**.

**Testei em quatro critérios. Não sustento a tese.**

| critério | veredito | evidência |
|---|---|---|
| Studio (metade da tese) | **INVERIFICÁVEL** | 4 studios no Airbnb, 0 no Centro; `bedrooms=0` no VivaReal é "não informado" |
| Receita por unidade | **NÃO SUSTENTA** | 7º de 7 em RevPAN; ocupação 0,31 vs 0,42 |
| **Yield sobre capital** | **NÃO SUSTENTA** | 4º de 7 — 1,61% |
| Receita por m² | *sustenta parcialmente* | 1º de 7 |
| Liquidez de compra | **NÃO SUSTENTA** | 22 unidades à venda no Centro |

**Primeiro: metade da tese não é verificável.** Só existem 4 studios com receita
estimável em toda a base, **nenhum no Centro**. E no VivaReal, `bedrooms = 0` não
significa studio — a área mediana desses anúncios vai de 283 a 450 m². É código de
"não informado". Não sustento nem derrubo a perna do studio: **declaro que os dados
não respondem.** O que testei foi 1 quarto no Centro (n=69).

**Segundo, e mais interessante: a tese falha exatamente onde deveria ganhar.** Seu
argumento econômico é *o denominador é menor*. Em Itapema, não é:

| Centro | R$/m² | área | preço |
|---|---|---|---|
| **1 quarto** | **R$ 20.548** | 44 m² | R$ 890.000 |
| 2 quartos | R$ 13.068 | 85 m² | R$ 1.100.000 |
| 4+ quartos | R$ 18.734 | 200 m² | R$ 3.900.000 |

**O compacto é pequeno, mas não é barato** — prêmio de 57% por m² sobre o 2 quartos,
o metro quadrado mais caro da cidade, acima até do 4 quartos. A tese assume
implicitamente que preço acompanha área. Não acompanha: **o mercado já precificou a
escassez de compactos**, e o desconto de capital que tornaria a tese verdadeira já foi
capturado pelo vendedor. Com ocupação menor, a conta fecha negativa dos dois lados.

**A condição declarada que inverteria minha posição:** se houvesse oferta de compactos
no Centro a R$ 13.068/m² — o mesmo m² de um 2 quartos — o yield subiria de 1,61% para
~2,52% e a tese passaria a vencer o ranking. **A tese não está errada sobre o tipo de
ativo; está errada sobre o preço atual desse ativo.** Em lançamento ou compra em bloco
com desconto de incorporador, ela volta a valer — e é assim que a Seazone compra.

**O que a tese acerta:** o instinto de padronização e escala. Vinte unidades quase
idênticas no mesmo prédio têm custo marginal de operação muito menor — um enxoval, um
padrão de limpeza, uma logística de chaves. Esse raciocínio continua correto.

---

## 7. P4 — O que eu compraria, e a conta

**Ativo concreto:** apartamento de **2 quartos (~85 m²), Meia Praia, até 400 m da
orla**, imóvel inteiro.

> Os valores abaixo são a mediana **da célula Meia Praia × 2 quartos** (n=96), não do
> agregado de 2 quartos da cidade da seção 3 (ADR 573, ocupação 0,42) — Meia Praia tem
> diária um pouco menor e ocupação bem maior que a média dos 2 quartos de Itapema.

```
Receita
  ADR (noites vendidas) .................. R$      555
  Ocupação estimada ......................          48%
  RevPAN ................................. R$      235
  Receita nas 77 noites observadas ....... R$   18.084
  Receita anual (janela = 45% do ano) .... R$   40.187

Custos
  Gestão 18% + canal 3% + manutenção 5% .. R$   10.449
  Limpeza (R$150 / estadia de 4 noites) .. R$    3.083
  Condomínio (R$5,10/m² x 85m² x 12) ..... R$    5.204
  IPTU (0,091% do valor) ................. R$      876
  Total .................................. R$   19.611

Resultado
  NOI .................................... R$   20.575
  Preço pedido ........................... R$ 1.070.000
  Preço de compra (−10% negociação) ...... R$  963.000
  YIELD LÍQUIDO .......................... 2,14% a.a.
  CDI .................................... 12,25% a.a.
  ----------------------------------------------------
  DIFERENÇA .............................. −10,11 p.p.
```

**Comparação com a alternativa: o CDI ganha de lavada.** E o argumento não depende da
minha premissa de sazonalidade — testei no limite físico:

> **Teste de teto.** E se Itapema rodasse os **365 dias do ano no ritmo da alta
> temporada observada** — mesma diária de janeiro, mesma ocupação de janeiro, zero
> queda de inverno? É impossível, e serve por isso: nenhum cenário real supera. Mesmo
> assim o melhor ativo chega a **5,27% líquido**, contra 12,25% do CDI. **Não existe
> fator sazonal capaz de inverter esta comparação.**

**Preço-teto.** A pergunta útil para um comitê não é "compro ou não", é "a que preço eu
compraria". Resolvendo `NOI(P)/P = CDI`, o 2 quartos de Meia Praia empataria com o CDI
a **R$ 173.818** — **82% abaixo do pedido**. Nenhuma célula da base precisa de menos
de 82% de desconto.

**Portanto: a decisão é não comprar, e monetizar pela gestão.** Sobre os mesmos
R$ 40 mil de receita anual, a Seazone captura ~R$ 7,2 mil de taxa de gestão com
capital imobilizado zero. Vinte contratos de gestão nesse eixo valem mais para ela do
que uma unidade comprada — e a densidade geográfica (mesmo eixo, mesmo padrão) reduz
custo de operação.

**O principal risco da minha decisão** — o que a faria dar errado: **eu não observo
valorização do imóvel.** Minha conta é de renda corrente. Se Itapema valorizar 15% ao
ano, o retorno total supera o CDI e minha recomendação está errada. O dataset não
permite avaliar isso: são anúncios de um único momento, sem série histórica de preço
de venda. Declaro isso como o limite da análise, não como detalhe.

O segundo risco: **viés de sobrevivência** (seção 8) faz minha receita ser otimista.
Se ela é otimista e mesmo assim o yield não fecha, o erro reforça a conclusão em vez
de ameaçá-la.

---

## 8. Limitações e premissas

**Estas são as fragilidades reais da análise. Cada uma pode mudar um número; nenhuma
muda a conclusão principal, pelo teste de teto da seção 7.**

**Janela de dados.** 3 capturas (06, 07, 20/01/2025), duas consecutivas → **1 intervalo
de comparação útil**. Estadias de 06/01 a 20/04. Comparação restrita à interseção dos
horizontes: **77 noites, 20/01–06/04**.

**Sazonalidade.** A janela é alta temporada + ombro. O preço mediano cai de R$ 801/noite
em janeiro para R$ 471 em abril, dentro da própria janela. **Não anualizei cegamente**:
reporto a receita observada e mostro o yield em três premissas (janela = 35%/45%/55%
da receita anual) em `saidas/03_yield.md`.

**Ocupação é inferida, não observada.** Trato desaparecimento de disponibilidade como
reserva. Isso **superestima** a ocupação na presença de bloqueios do proprietário,
manutenção ou anúncio saindo do ar — não tenho como separar os casos.

**Viés de sobrevivência — a limitação mais séria.** Só **999 dos 4.441 anúncios (22,5%)**
têm dado de preço, e o recorte não é aleatório: mediana de **16 avaliações** contra
**1** nos sem preço; rating 4,93 vs 4,50; 48,6% de cobertura entre anfitriões
profissionais contra 21,6% entre os demais; apenas 2,1% entre anúncios novos. **O dado
de preço é o dos anúncios que já deram certo.** Minha receita estimada é otimista para
o mercado como um todo. Após todos os filtros, a análise roda sobre **605 anúncios =
13,6% da base**.

**Preço pedido não é preço fechado.** VivaReal traz anúncio. Apliquei **10% de desconto
de negociação** declarado.

**Valores sentinela.** `monthly_condo_fee` e `yearly_iptu` vêm poluídos com zeros e uns
(2.798 de 8.293 condomínios são ≤ R$50). Usar a mediana bruta daria condomínio de
R$ 1,00. Derivei as **taxas** no subconjunto plausível (R$ 5,10/m²/mês; 0,091% do valor
ao ano) e apliquei a todas as unidades. `bedrooms = 0` também é sentinela de "não
informado", não studio.

**Encoding.** `VivaReal_Itapema.csv` está em **latin-1**. Lido como UTF-8 — o default do
pandas — bairros acentuados viram caractere de substituição e **deixam de casar** com o
bairro do Mesh, perdendo linhas em silêncio.

**Joins.** Details→Mesh 100%, Details→Hosts 100% (após deduplicar 1.383 `owner_id`
repetidos), **Details→Price 22,5%**. Contagens antes e depois em `saidas/00_perfil.md`.

**Média vs mediana.** Uso mediana por padrão — receita de short stay tem cauda longa.

**Corte de n.** n ≥ 20 no Airbnb e n ≥ 15 no VivaReal para toda célula comentada. Toda
tabela mostra o n.

**Premissas externas ao dataset** (isoladas no topo de `analise/04_yield.py` para
qualquer leitor trocar e refazer a conta): CDI 12,25%; desconto de negociação 10%;
4 noites por estadia; gestão 18%; canal 3%; limpeza R$ 150/estadia; manutenção 5%.

**Não avalio valorização do imóvel** — só renda corrente. É a maior lacuna da análise.

---

## 9. O que eu faria com mais uma semana

1. **Ganhar mais capturas.** A limitação que mais dói é ter 1 intervalo de comparação.
   Com capturas semanais por 2 meses eu mediria a curva de pickup por antecedência e
   estimaria ocupação com muito mais confiança — hoje ela vem de 13 dias.
2. **Resolver a sazonalidade com dado, não com premissa.** Buscaria uma série anual
   (mesmo de outra praia de SC) para calibrar o fator sazonal em vez de declarar 45%.
   É a premissa mais frágil que ainda sobrevive ao teste de teto.
3. **Incluir valorização.** Cruzar preço/m² por ano de construção e por data de anúncio
   para separar renda de ganho de capital. Sem isso minha recomendação responde metade
   da pergunta de investimento.
4. **Descer do bairro para o prédio.** Com lat/long dá para agrupar anúncios por
   edifício e medir RevPAN *por prédio* — é a unidade real de originação da Seazone, e
   é onde a padronização vira dinheiro. Também permitiria estimar canibalização:
   quantas unidades cabem no mesmo bolsão antes de pressionar a própria diária.
5. **Atacar o viés de sobrevivência.** Modelar a probabilidade de um anúncio ter dado de
   preço e reponderar as estimativas, em vez de só declarar o viés.
6. **Testar o texto do anúncio.** `ad_description`, `amenities` e `house_rules` estão
   sem uso. "Vista mar" e "frente mar" no título provavelmente valem diária — é barato
   testar e entra direto na triagem de compra.

---

## Onde está cada coisa

| arquivo | conteúdo |
|---|---|
| `saidas/00_perfil.md` | perfil dos 5 arquivos, joins, janela, viés de seleção |
| `saidas/01_receita.md` | ADR × ocupação, teste de validade da inferência |
| `saidas/02_perfil_local.md` | P1, P2, P3 com n e mediana |
| `saidas/03_yield.md` | yield, sensibilidade, teste de teto, preço-teto |
| `saidas/04_tese_compactos.md` | a tese testada em 4 critérios |
| `ai-log/` | sessão completa com a IA (`.jsonl` bruto + `.md` legível) |
