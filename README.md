**🎥 Vídeo (3 min):** `<COLAR AQUI O LINK DO GOOGLE DRIVE — compartilhamento em "qualquer pessoa com o link">`

# Recomendação de investimento — Itapema (SC)

**Desafio Jovens Talentos AI Builder 2026 · Seazone** — Renato Cazzoletti

---

## A recomendação, em três linhas

1. **Não comprar ao preço pedido.** O melhor perfil da cidade — **apartamento de 2
   quartos em Meia Praia, até 400 m da praia** — rende **2,14% líquido a.a.** contra
   **12,25% do CDI**. Empataria com o CDI só a **82% de desconto** sobre o anunciado.
2. **A conclusão não depende da minha premissa de sazonalidade:** mesmo que Itapema
   rodasse os 365 dias do ano no ritmo da alta temporada — impossível — o teto seria
   **5,27%**, menos da metade do CDI.
3. **O que a Seazone deve fazer é originar e operar, não comprar.** Sobre os mesmos
   ~R$ 40 mil de receita anual, a gestão captura ~R$ 7 mil **sem imobilizar capital**.
   O ativo é ruim para o proprietário e continua bom para o gestor.

**Sobre a tese dos compactos no Centro: não a sustento.** Ela falha exatamente onde
deveria ganhar — o compacto é pequeno mas **não é barato**: R$ 20.548/m² contra
R$ 13.068/m² de um 2 quartos no mesmo bairro, o m² mais caro da cidade. O mercado já
precificou a escassez. Metade da tese (studio) é **inverificável**: existem 4 studios
na base e nenhum no Centro. [Raciocínio completo →](relatorio.md)

---

## 📄 A resposta completa está em **[`relatorio.md`](relatorio.md)**

Critério adotado, as 4 perguntas respondidas, a posição sobre a tese, a conta do
retorno, as limitações e o que eu faria com mais uma semana.

---

## Como rodar

**Requisitos:** Python 3.9+ com `pandas` e `numpy`. Nada além disso — as tabelas em
markdown são geradas por código próprio, sem `tabulate`, justamente para o repositório
rodar numa máquina limpa.

```bash
pip install pandas numpy

# na raiz do repositório, na ordem:
python analise/01_perfil.py          # perfil dos 5 arquivos, joins, viés de seleção
python analise/02_receita.py         # ADR × ocupação → receita por anúncio
python analise/03_perfil_local.py    # P1 perfil, P2 localização, P3 características
python analise/04_yield.py           # yield líquido, sensibilidade, preço-teto
python analise/05_tese_compactos.py  # a tese testada em 4 critérios
```

Cada script escreve em `saidas/`. Rodam em ~20 s no total e devem ser executados nesta
ordem (02 consome a saída de 01, e assim por diante).

```bash
python analise/99_exportar_ai_log.py  # regenera ai-log/ a partir da sessão do Claude Code
```

---

## Mapa dos arquivos

| caminho | o que é |
|---|---|
| **[`relatorio.md`](relatorio.md)** | **a recomendação, o critério, a tese e as limitações** |
| [`ai-log/`](ai-log/) | sessão completa com a IA — `.jsonl` bruto + `.md` legível |
| [`ai-log/README.md`](ai-log/README.md) | índice da sessão hora a hora |
| `analise/comum.py` | utilitários: carga dos CSVs, tabela markdown, normalização de bairro |
| `analise/01_perfil.py` | → `saidas/00_perfil.md` |
| `analise/02_receita.py` | → `saidas/01_receita.md`, `saidas/receita_por_listing.csv` |
| `analise/03_perfil_local.py` | → `saidas/02_perfil_local.md`, `saidas/listings_enriquecido.csv` |
| `analise/04_yield.py` | → `saidas/03_yield.md`, `saidas/yield_por_celula.csv` |
| `analise/05_tese_compactos.py` | → `saidas/04_tese_compactos.md` |
| `saidas/` | todas as tabelas geradas — **todo número do relatório sai daqui** |
| `data/` | os 5 CSVs originais do fork, intocados |

---

## O método, em um parágrafo

`Price_AV` traz **preço anunciado**, não receita. Estimei ocupação pelo
desaparecimento de noites entre capturas, restrito à **interseção dos horizontes das
capturas** (20/01–06/04, 77 noites) — fora dela, "sumir" significa apenas "saiu da
janela da captura", e contar isso como reserva infla a ocupação em silêncio. Validei a
inferência contra um atributo que ela não usa: **as noites que sumiram estavam mais
caras que as que sobraram** (R$ 675 vs R$ 641), o que é incompatível com bloqueio
aleatório e compatível com reserva. Isso também dá o ADR correto — o preço do que
vendeu, não da vitrine. Daí: `RevPAN = ADR × ocupação`, dividido pelo preço de compra
do VivaReal, menos a estrutura de custo, comparado ao CDI.

---

## Os dados (`data/`)

Snapshot estático do mercado imobiliário de **Itapema (SC)** — Airbnb e venda (VivaReal).

| Arquivo | O que tem | Como conecta |
|---|---|---|
| `Details_Itapema.csv` | Cada anúncio de Airbnb: título, reviews, star rating, descrição, host_id, nº de quartos, tipo de imóvel | Base principal dos listings |
| `Hosts_ids_Itapema.csv` | Dados do anfitrião: nº de reviews, anos como host, superhost, taxa de resposta | Liga com Details pelo `owner_id` |
| `Mesh_Ids_Data_Itapema.csv` | Latitude/longitude + bairro de cada anúncio | Liga por listing |
| `Price_AV_Itapema.csv` | Preço por anúncio, por data de estadia e por data de captura | Liga por listing |
| `VivaReal_Itapema.csv` | Anúncios de venda: preço, condomínio, área, vendedor | Mercado de compra |

> ⚠️ Dois defeitos encontrados e tratados: `VivaReal_Itapema.csv` está em **latin-1**
> (lido como UTF-8 os bairros acentuados deixam de casar com o Mesh), e
> `monthly_condo_fee`, `yearly_iptu` e `bedrooms` carregam **valores sentinela** (0 e 1)
> que não são dados faltantes declarados. Detalhes em `saidas/03_yield.md`.

---

Enunciado original do desafio: [`index.html`](index.html) ·
[versão online](https://seazone-tech.github.io/jovens-talentos-2026-hackathon-data/)

*Seazone — Jovens Talentos AI Builder 2026*
