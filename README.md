**🎥 Vídeo (3 min): https://drive.google.com/file/d/1gwguIy2QwmltcSwvvhmZ17jQUKKpjxiJ/view?usp=sharing**

# Onde a Seazone deveria investir em Itapema — e por que a resposta é "em lugar nenhum, a esse preço"

**Desafio Jovens Talentos AI Builder 2026 · Seazone** — Renato Cazzoletti
Análise sobre 4.441 anúncios de Airbnb e 8.293 anúncios de venda em Itapema (SC).

---

## A resposta, em 30 segundos

> **Não comprar em Itapema ao preço pedido.** O melhor ativo da cidade — apartamento de
> 2 quartos em Meia Praia, até 400 m da orla — rende **2,14% líquido ao ano**. O CDI, na
> data dos dados, pagava **12,25%** sem risco operacional, sem iliquidez e sem trabalho
> de gestão.
>
> **O caminho para a Seazone é originar e operar, não comprar.** Sobre os mesmos
> ~R$ 40 mil de receita anual, a taxa de gestão captura ~R$ 7 mil **com capital
> imobilizado zero**. O ativo é ruim para o proprietário e continua ótimo para o gestor.
>
> **Sobre a tese dos compactos no Centro: não sustento** — e pelo motivo oposto ao que
> se imagina. Detalhes abaixo.

| | |
|---|---|
| **Critério adotado** | Yield líquido sobre capital investido, com o CDI como régua |
| **Melhor ativo** | 2 quartos · Meia Praia · até 400 m da praia |
| **Retorno estimado** | 2,14% líquido a.a. (1,63% a 2,93% conforme a sazonalidade) |
| **Desconto necessário para empatar com o CDI** | **82%** sobre o preço anunciado |
| **Teto físico do melhor ativo** | 5,27% — menos da metade do CDI |
| **Base analisada** | 605 anúncios com receita estimável (13,6% da base) |

📄 **Raciocínio completo, premissas e limitações em [`relatorio.md`](relatorio.md).**

---

## O ponto de partida: o dado não traz receita, traz preço

`Price_AV_Itapema.csv` tem **preço anunciado de noites disponíveis** — não receita
realizada. Tirar média de preço por bairro e chamar de "receita" é o caminho natural, e
é errado: um imóvel caríssimo vazio 300 noites por ano não é investimento.

```
Receita = ADR × Ocupação          RevPAN = receita por noite disponível
```

**A ocupação não vem pronta.** O arquivo tem 3 capturas do mesmo calendário futuro
(06, 07 e 20/01/2025). Como o Airbnb remove do calendário a noite reservada, a noite que
estava à venda numa captura e sumiu na seguinte foi, muito provavelmente, **reservada no
intervalo**.

### A armadilha que quase me pegou

Cada captura enxerga ~90 noites **à frente da própria data**. A de 06/01 vê até 06/04; a
de 20/01 vê até 20/04. Se eu contasse "sumiu = reservou" sobre a união das datas, as
**14 noites que apenas saíram do horizonte** da captura de 20/01 virariam reservas
fantasma — número plausível, silenciosamente inflado, e **nenhum erro apareceria no
código**.

Por isso a comparação vale só na **interseção dos horizontes: 20/01 a 06/04, 77 noites**.
E como duas das três capturas são consecutivas, existe **um único intervalo útil** de
comparação (13 dias) — não três.

### Como validei que a inferência é real

"Sumiu" também pode ser o dono bloqueando a agenda. Não dá para separar os casos olhando
o calendário — então testei contra um atributo que a inferência **não usou**: o preço.

| noite ofertada em 06–07/01 | noites | preço mediano |
|---|---|---|
| sobrou disponível | 27.339 | R$ 641 |
| **SUMIU (reservada)** | **4.460** | **R$ 675** |

Bloqueio de proprietário é indiferente ao preço — quem fecha a agenda para uso próprio
não escolhe a data mais cara. **Hóspede escolhe.** As noites que sumiram serem R$ 34 mais
caras é a assinatura de demanda, não de ruído. Some 14,0% em 13 dias contra apenas 1,8%
que reaparecem: fluxo fortemente numa direção só.

**Validação independente:** `ocupacao` (medida na captura final) e `pickup_13d` (medido
entre capturas) vêm de dados diferentes e correlacionam **0,52**.

**Bônus:** isso entrega o ADR correto — o preço do que **efetivamente vendeu**, não a
média da vitrine.

---

## As quatro perguntas

### 1️⃣ Melhor perfil de imóvel

| nº de quartos | n | RevPAN mediano | ADR | ocupação |
|---|---|---|---|---|
| 4+ quartos | 42 | R$ 363 | 1.275 | 0,40 |
| 3 quartos | 284 | R$ 292 | 750 | 0,40 |
| 2 quartos | 192 | R$ 207 | 573 | 0,42 |
| 1 quarto | 83 | R$ 162 | 520 | **0,31** |

Por **receita**, quanto maior melhor — mas isso só diz que imóvel grande cobra caro. Por
**retorno sobre capital**, a ordem inverte: 4+ quartos tem o **maior RevPAN e o pior
yield** (0,85%). É exatamente o erro que ranquear por receita absoluta induz.

**Resposta: apartamento de 2 quartos, imóvel inteiro.** Achado inesperado: compactos têm
ocupação **menor** (0,31 contra 0,42) — vendem menos noites, não mais.

### 2️⃣ Melhor localização

A leitura bruta diz que Meia Praia domina (RevPAN 269 vs 187 do Centro). **Controlando
por número de quartos, a história muda:**

| bairro | 1 quarto | 2 quartos | 3 quartos | 4+ quartos |
|---|---|---|---|---|
| Centro | 144 | 209 | **316** | – |
| Meia Praia | – | 235 | 287 | 358 |
| Morretes | – | 156 | – | – |

**O Centro vence Meia Praia em 3 quartos.** A vantagem bruta era efeito de composição —
Meia Praia concentra 240 dos 284 imóveis de 3 quartos, o Centro concentra os de 1 quarto.
Sem esse controle eu estaria medindo tamanho e chamando de localização.

**O que realmente explica é a distância da praia, não o rótulo do bairro:**

| distância da orla | n | RevPAN mediano |
|---|---|---|
| até 200 m | 136 | **R$ 301** |
| 200–400 m | 185 | R$ 265 |
| 400–800 m | 240 | R$ 202 |
| 800 m–1,5 km | 40 | R$ 175 |

Gradiente monotônico, Spearman **−0,31** — e **−0,21 dentro de 2 quartos apenas**, então
não é artefato de tamanho. A orla foi estimada empiricamente de latitude/longitude.

### 3️⃣ O que explica as receitas

Capacidade de hóspedes (+0,37), nº de quartos (+0,37) e distância da praia (−0,31)
lideram. Mas a regressão em log(RevPAN) dá **R² = 0,11** — e digo isso de propósito:
**as características observáveis explicam pouco.** O resto está em fatores que o dataset
não tem (qualidade do prédio, mobília, gestão de preço). Quem prometer modelo preditivo
aqui está exagerando.

Duas leituras críticas: os coeficientes são **associação, não causa** (piscina é proxy de
"prédio bom em rua boa"); e há **causalidade reversa em avaliações** — mais reviews
correlaciona com receita porque *quem vende mais acumula mais reviews*, não o contrário.

### 4️⃣ O que eu compraria

```
Receita
  ADR (noites vendidas) .................. R$      555
  Ocupação estimada ......................          48%
  Receita anual (janela = 45% do ano) .... R$   40.187
Custos
  Gestão 18% + canal 3% + manutenção 5% .. R$   10.449
  Limpeza, condomínio e IPTU ............. R$    9.162
Resultado
  NOI .................................... R$   20.575
  Preço de compra (−10% negociação) ...... R$  963.000
  YIELD LÍQUIDO .......................... 2,14% a.a.
  CDI .................................... 12,25% a.a.
```

| perfil | preço de compra | receita/ano | **yield líquido** |
|---|---|---|---|
| **Meia Praia · 2 quartos** | R$ 963.000 | R$ 40.187 | **2,14%** |
| Morretes · 2 quartos | R$ 675.000 | R$ 26.756 | 1,92% |
| Centro · 2 quartos | R$ 990.000 | R$ 35.759 | 1,82% |
| Centro · 1 quarto | R$ 801.000 | R$ 24.556 | 1,61% |
| Centro · 3 quartos | R$ 1.890.000 | R$ 54.044 | 1,47% |
| Meia Praia · 3 quartos | R$ 1.694.213 | R$ 49.031 | 1,43% |
| Meia Praia · 4+ quartos | R$ 3.330.000 | R$ 61.333 | 0,85% |

**O argumento não depende da minha premissa de sazonalidade.** Testei no limite físico:
se Itapema rodasse os **365 dias do ano no ritmo da alta temporada** — impossível — o
melhor ativo chegaria a **5,27%**. Ainda menos da metade do CDI. *Não existe fator
sazonal capaz de inverter esta comparação.*

**Preço-teto.** A pergunta útil não é "compro ou não", é "a que preço eu compraria".
Resolvendo `NOI(P)/P = CDI`: o 2 quartos de Meia Praia empataria com o CDI a
**R$ 173.818** — **82% abaixo do pedido**. Nenhuma célula precisa de menos que isso. Não
é questão de negociar melhor: **o mercado de Itapema não está precificado para renda de
short stay**, está precificado para valorização e uso próprio.

---

## 🎯 A tese dos compactos no Centro

> *"Apartamentos compactos (studio/1 quarto) na região do Centro seriam a aposta mais
> eficiente."* — análise interna, marcada como **não validada**.

Testei em quatro critérios. **Não sustento a tese.**

| critério | veredito | evidência |
|---|---|---|
| Studio (metade da tese) | **INVERIFICÁVEL** | 4 studios na base, **0 no Centro**; `bedrooms=0` no VivaReal é "não informado" |
| Receita por unidade | **NÃO SUSTENTA** | 7º de 7 em RevPAN; ocupação 0,31 vs 0,42 |
| **Yield sobre capital** | **NÃO SUSTENTA** | 4º de 7 — 1,61% |
| Receita por m² | *sustenta parcialmente* | 1º de 7 |
| Liquidez de compra | **NÃO SUSTENTA** | 22 unidades à venda no Centro |

**A tese falha exatamente onde deveria ganhar.** Seu argumento econômico é *o denominador
é menor*. Em Itapema, não é:

| Centro | R$/m² | área | preço |
|---|---|---|---|
| **1 quarto** | **R$ 20.548** | 44 m² | R$ 890.000 |
| 2 quartos | R$ 13.068 | 85 m² | R$ 1.100.000 |
| 4+ quartos | R$ 18.734 | 200 m² | R$ 3.900.000 |

**O compacto é pequeno, mas não é barato** — prêmio de 57% por m² sobre o 2 quartos, o
metro quadrado mais caro da cidade, acima até do 4 quartos. A tese assume que preço
acompanha área; não acompanha. **O mercado já precificou a escassez de compactos**, e o
desconto de capital que tornaria a tese verdadeira já foi capturado pelo vendedor.

**A condição declarada que inverteria minha posição:** se houvesse oferta de compactos no
Centro a R$ 13.068/m², o yield subiria de 1,61% para ~2,52% e a tese venceria o ranking.
**A tese não está errada sobre o tipo de ativo; está errada sobre o preço dele hoje.** Em
lançamento ou compra em bloco com desconto de incorporador, ela volta a valer — e é assim
que a Seazone compra.

---

## ⚠️ Limitações que você deve considerar ao ler

| limitação | impacto |
|---|---|
| **Viés de sobrevivência** | Só 999 de 4.441 anúncios (22,5%) têm preço, e o recorte tem mediana de **16 avaliações contra 1** dos sem preço. É o dado de quem já deu certo — minha receita é **otimista** |
| **Ocupação inferida** | Trato desaparecimento como reserva; **superestima** na presença de bloqueios do proprietário |
| **1 intervalo de comparação** | 3 capturas, duas consecutivas → 13 dias de observação |
| **Sazonalidade** | A janela é alta temporada + ombro; preço cai de R$ 801 (jan) para R$ 471 (abr) |
| **Preço pedido ≠ fechado** | Apliquei 10% de desconto de negociação declarado |
| **Não avalio valorização** | Análise é de renda corrente. É a maior lacuna — e o principal risco da recomendação |

Se a receita é otimista por construção e **mesmo assim** o yield não fecha, o viés
reforça a conclusão em vez de ameaçá-la. Bloco completo na
[seção 8 do relatório](relatorio.md).

### Dois defeitos nos dados, encontrados e tratados

**Encoding.** `VivaReal_Itapema.csv` está em **latin-1**. Lido como UTF-8 (o default do
pandas), bairros acentuados viram caractere de substituição e **deixam de casar** com o
bairro do Mesh — perdendo linhas em silêncio.

**Valores sentinela.** `monthly_condo_fee` e `yearly_iptu` vêm poluídos com zeros e uns
(**2.798 de 8.293** condomínios são ≤ R$50). A mediana bruta daria condomínio de R$ 1,00.
Derivei as *taxas* no subconjunto plausível (R$ 5,10/m²/mês; 0,091% do valor/ano).
`bedrooms = 0` também é sentinela — a área mediana desses anúncios vai de 283 a 450 m².

---

## Como rodar

**Requisitos:** Python 3.9+ com `pandas` e `numpy`. **Nada além disso** — as tabelas
markdown são geradas por código próprio, sem `tabulate`, para o repositório rodar em
máquina limpa. Testado apagando `saidas/` e regenerando do zero.

```bash
pip install pandas numpy

# na raiz do repositório, nesta ordem (cada etapa consome a anterior):
python analise/01_perfil.py          # perfil dos 5 arquivos, joins, viés de seleção
python analise/02_receita.py         # ADR × ocupação → receita por anúncio
python analise/03_perfil_local.py    # P1 perfil, P2 localização, P3 características
python analise/04_yield.py           # yield líquido, sensibilidade, teto, preço-teto
python analise/05_tese_compactos.py  # a tese testada em 4 critérios
```

Roda em ~20 s no total e escreve tudo em `saidas/`. **Todo número deste README e do
relatório sai de lá.**

```bash
python analise/99_exportar_ai_log.py  # regenera ai-log/ a partir da sessão do Claude Code
```

As premissas externas ao dataset (CDI, desconto de negociação, taxa de gestão, limpeza)
ficam **isoladas no topo de [`analise/04_yield.py`](analise/04_yield.py)** para qualquer
leitor trocar o número e refazer a conta.

---

## Mapa dos arquivos

| caminho | o que é |
|---|---|
| **[`relatorio.md`](relatorio.md)** | **a recomendação completa: critério, 4 perguntas, tese, limitações, o que eu faria com mais uma semana** |
| [`ai-log/`](ai-log/) | sessão completa com a IA — `.jsonl` bruto (prova) + `.md` legível |
| [`ai-log/README.md`](ai-log/README.md) | **índice da sessão hora a hora**, com as 5 viradas do dia e onde o senso crítico aparece |
| `analise/comum.py` | carga dos CSVs, tabela markdown, normalização de bairro |
| `analise/01_perfil.py` | → `saidas/00_perfil.md` |
| `analise/02_receita.py` | → `saidas/01_receita.md` + `receita_por_listing.csv` |
| `analise/03_perfil_local.py` | → `saidas/02_perfil_local.md` + `listings_enriquecido.csv` |
| `analise/04_yield.py` | → `saidas/03_yield.md` + `yield_por_celula.csv` |
| `analise/05_tese_compactos.py` | → `saidas/04_tese_compactos.md` |
| `saidas/` | todas as tabelas geradas |
| `data/` | os 5 CSVs originais do fork, intocados |

---

## Os dados (`data/`)

Snapshot estático do mercado imobiliário de **Itapema (SC)** — Airbnb e venda (VivaReal).

| Arquivo | O que tem | Como conecta | Casamento |
|---|---|---|---|
| `Details_Itapema.csv` | 4.441 anúncios de Airbnb: título, reviews, rating, descrição, quartos, tipo | Base principal | — |
| `Hosts_ids_Itapema.csv` | Anfitrião: reviews, anos como host, superhost, taxa de resposta | por `owner_id` | 100% |
| `Mesh_Ids_Data_Itapema.csv` | Latitude/longitude + bairro | por listing | 100% |
| `Price_AV_Itapema.csv` | Preço por anúncio, data de estadia e data de captura | por listing | **22,5%** ⚠️ |
| `VivaReal_Itapema.csv` | 8.293 anúncios de venda: preço, condomínio, área, vendedor | mercado de compra | — |

O casamento de 22,5% do `Price_AV` é **o gargalo da análise** e a origem do viés de
sobrevivência. Contagens antes e depois de cada join em
[`saidas/00_perfil.md`](saidas/00_perfil.md).

---

## Como a IA foi usada

Claude Code desde o minuto zero, **antes de abrir o primeiro CSV** — a sessão inteira
está em [`ai-log/`](ai-log/), sem cortes, com o `.jsonl` bruto ao lado do `.md` legível.

O [índice da sessão](ai-log/README.md) marca as cinco viradas do dia e traz uma seção
**"onde o senso crítico aparece"**, apontando os momentos em que o resultado da IA não
foi aceito de primeira: a armadilha do horizonte móvel, o teste da ocupação contra ruído
aleatório, a recusa de uma dependência que só existiria na minha máquina, o condomínio
mediano de R$ 1, e a decisão de declarar metade da tese inverificável em vez de produzir
um número com n de 4.

**A escolha do critério e a posição sobre a tese foram minhas.** A IA calculou; a decisão
foi tomada e é defendida no vídeo.

---

Enunciado original: [`index.html`](index.html) ·
[versão online](https://seazone-tech.github.io/jovens-talentos-2026-hackathon-data/)

*Seazone — Jovens Talentos AI Builder 2026*
