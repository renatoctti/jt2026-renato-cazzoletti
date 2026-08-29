"""
05 - A tese dos compactos no Centro, testada em quatro criterios.

A tese interna: "apartamentos compactos (studio/1 quarto) na regiao do Centro
seriam a aposta mais eficiente". Ela e marcada como NAO VALIDADA, entao o
trabalho aqui e valida-la, nao acata-la.

Testes:
  A. Receita absoluta por unidade
  B. Yield sobre capital investido  <- criterio que adotei
  C. Receita por m2
  D. Liquidez: existe oferta de compra para montar posicao?
  + o mecanismo: por que o resultado sai como sai

Le  : saidas/listings_enriquecido.csv, saidas/yield_por_celula.csv
Gera: saidas/04_tese_compactos.md
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import numpy as np
from comum import carregar, md_table, normalizar_bairro, SAIDAS

CEN_BASE = "base (janela = 45% do ano)"
L = []


def w(s=""):
    L.append(str(s))


d, h, m, pr, v = carregar()
base = pd.read_csv(SAIDAS / "listings_enriquecido.csv")
base["bairro"] = normalizar_bairro(base.suburb)
yc = pd.read_csv(SAIDAS / "yield_por_celula.csv")
yb = yc[yc.cenario == CEN_BASE].copy()

v = v.drop_duplicates("listing_id").copy()
for c_ in ["sale_price", "bedrooms", "usable_area"]:
    v[c_] = pd.to_numeric(v[c_], errors="coerce")
v["bairro"] = normalizar_bairro(v.suburb)
v = v[v.sale_price.between(80_000, 20_000_000) & v.usable_area.between(20, 600)]
v["rs_m2"] = v.sale_price / v.usable_area
v["quartos"] = v.bedrooms.clip(upper=4)

w("# 04 - A tese dos compactos no Centro\n")
w("_Gerado por `analise/05_tese_compactos.py`._\n")
w("> **A tese, como recebida:** *apartamentos compactos (studio/1 quarto) na "
  "regiao do Centro seriam a aposta mais eficiente para a Seazone.* Vem marcada "
  "como analise preliminar interna **ainda nao validada**. Trato como hipotese a "
  "testar, nao como orientacao a seguir.\n")

# ---------- 0. a perna do studio ----------
w("## 0. Antes de testar: metade da tese nao e verificavel\n")
w("A tese fala em *studio/1 quarto*. Os dois lados do dado se comportam muito "
  "diferente nessas duas categorias.\n")
st_air = base[base.faixa_quartos == "Studio"]
n_st_centro = len(st_air[st_air.bairro == "Centro"])
n_1q_centro = len(base[(base.bairro == "Centro") & (base.faixa_quartos == "1 quarto")])
w(f"**Lado Airbnb:** dos {len(base)} anuncios com receita estimavel, apenas "
  f"**{len(st_air)} sao studio** - e **{n_st_centro} no Centro**. "
  "Nao existe amostra para estimar receita de studio no Centro.\n")
z = v[v.bedrooms == 0].groupby("bairro").usable_area.agg(n="size", area_mediana="median")
z = z[z.n >= 5].sort_values("area_mediana", ascending=False)
w("**Lado VivaReal:** `bedrooms = 0` **nao significa studio**. A area mediana "
  "desses anuncios denuncia o campo:\n")
w(md_table(z.round(0), floats="{:,.0f}"))
w("\nUm *studio* de 283 a 450 m2 nao existe. `bedrooms = 0` no VivaReal e codigo "
  "de **nao informado**, nao de studio - o mesmo padrao de valor sentinela ja "
  "encontrado em condominio e IPTU.\n")
w("> **Consequencia:** a perna *studio* da tese e **inverificavel** com estes "
  "dados, nos dois lados. Nao a sustento nem a derrubo: declaro que nao da para "
  "responder. O que testo a seguir e a perna verificavel - **1 quarto no Centro**, "
  f"com n = {n_1q_centro} anuncios de Airbnb.\n")

# ---------- A. receita ----------
w("## A. Criterio 1 - receita absoluta por unidade\n")
ta = (base.groupby(["bairro", "faixa_quartos"])
          .agg(n=("revpan", "size"), revpan=("revpan", "median"),
               adr=("adr", "median"), ocupacao=("ocupacao", "median"))
          .reset_index())
ta = ta[ta.n >= 20].sort_values("revpan", ascending=False).reset_index(drop=True)
ta["destaque"] = np.where((ta.bairro == "Centro") & (ta.faixa_quartos == "1 quarto"),
                          "<-- A TESE", "")
w(md_table(ta.round(2)))
tese_rev = ta[(ta.bairro == "Centro") & (ta.faixa_quartos == "1 quarto")]
pos = int(tese_rev.index[0]) + 1
w(f"\n**Veredito A: a tese perde.** Compacto no Centro e o **{pos}o de {len(ta)}** "
  "em RevPAN. Nao e so a diaria menor: a **ocupacao tambem e menor** "
  f"({float(tese_rev.ocupacao.iloc[0]):.2f} contra "
  f"{ta[ta.faixa_quartos=='2 quartos'].ocupacao.median():.2f} dos 2 quartos). "
  "O compacto vende menos noites, nao mais.\n")

# ---------- B. yield ----------
w("## B. Criterio 2 - yield liquido sobre capital (o criterio que adotei)\n")
w("Este e o teste que importa: e aqui que a tese *deveria* vencer, porque o "
  "denominador de um compacto e menor.\n")
tb = yb.sort_values("yield_liquido", ascending=False).reset_index(drop=True)
tb["destaque"] = np.where((tb.bairro == "Centro") & (tb.faixa_quartos == "1 quarto"),
                          "<-- A TESE", "")
tbx = tb[["bairro", "faixa_quartos", "n_airbnb", "n_venda", "preco_compra",
          "receita_ano", "yield_liquido", "destaque"]].copy()
tbx["preco_compra"] = tbx.preco_compra.round(0)
tbx["receita_ano"] = tbx.receita_ano.round(0)
tbx["yield_liquido"] = (tbx.yield_liquido * 100).round(2).astype(str) + "%"
w(md_table(tbx, floats="{:,.0f}"))
lin = tb[(tb.bairro == "Centro") & (tb.faixa_quartos == "1 quarto")]
posb = int(lin.index[0]) + 1
y_tese = float(lin.yield_liquido.iloc[0])
w(f"\n**Veredito B: a tese tambem perde.** Compacto no Centro rende "
  f"**{y_tese*100:.2f}%** liquido a.a. e fica em **{posb}o de {len(tb)}**, atras "
  "de 2 quartos em Meia Praia, Morretes e no proprio Centro.\n")

# ---------- mecanismo ----------
w("### Por que a tese falha justamente onde deveria ganhar\n")
w("O argumento economico da tese e *o denominador e menor*. Em Itapema ele nao e:\n")
mec = (v[v.bedrooms >= 1].groupby(["bairro", "quartos"])
         .agg(n=("rs_m2", "size"), rs_m2=("rs_m2", "median"),
              area=("usable_area", "median"), preco=("sale_price", "median")))
mec = mec[mec.n >= 20].reset_index()
mec = mec[mec.bairro.isin(["Centro", "Meia Praia", "Morretes"])]
w(md_table(mec.round(0), floats="{:,.0f}"))
c1 = float(mec[(mec.bairro == "Centro") & (mec.quartos == 1)].rs_m2.iloc[0])
c2 = float(mec[(mec.bairro == "Centro") & (mec.quartos == 2)].rs_m2.iloc[0])
w(f"\n**O compacto e pequeno, mas nao e barato.** Um quarto no Centro custa "
  f"**R$ {c1:,.0f}/m2** contra **R$ {c2:,.0f}/m2** de um 2 quartos no mesmo bairro "
  f"- um premio de **{(c1/c2-1)*100:.0f}%**. E o metro quadrado mais caro da cidade, "
  "acima ate do 4 quartos.\n")
w("> A tese assume implicitamente que preco acompanha area. Nao acompanha: o "
  "mercado de Itapema **ja precifica** a escassez de compactos. O desconto de "
  "capital que tornaria a tese verdadeira **ja foi capturado pelo vendedor** - e "
  "com ocupacao menor, a conta fecha negativa nos dois lados.\n")

# ---------- C. receita por m2 ----------
w("## C. Criterio 3 - receita por m2\n")
w("Unico criterio em que a tese tem chance real: a diaria nao cai "
  "proporcionalmente a area.\n")
tc = yb.copy()
tc["receita_m2_ano"] = tc.receita_ano / tc.area
tc = tc.sort_values("receita_m2_ano", ascending=False).reset_index(drop=True)
tc["destaque"] = np.where((tc.bairro == "Centro") & (tc.faixa_quartos == "1 quarto"),
                          "<-- A TESE", "")
tcx = tc[["bairro", "faixa_quartos", "area", "receita_ano", "receita_m2_ano",
          "destaque"]].copy()
for col in ["area", "receita_ano", "receita_m2_ano"]:
    tcx[col] = tcx[col].round(0)
w(md_table(tcx, floats="{:,.0f}"))
posc = int(tc[(tc.bairro == "Centro") & (tc.faixa_quartos == "1 quarto")].index[0]) + 1
w(f"\n**Veredito C: aqui a tese acerta parcialmente** - o compacto sobe para "
  f"**{posc}o de {len(tc)}** em receita por m2. Confirma a intuicao de que o "
  "compacto usa melhor a area. **Mas receita por m2 nao paga o investidor**: "
  "quem compra desembolsa o preco do imovel, nao o preco do metro quadrado. "
  "Como o m2 do compacto e o mais caro da cidade, a vantagem em produtividade "
  "de area nao chega ao retorno.\n")

# ---------- D. liquidez ----------
w("## D. Criterio 4 - liquidez: da para montar posicao?\n")
w("A Seazone nao compra uma unidade: ela origina predios e opera portfolio. "
  "Uma tese verdadeira em teoria mas com cinco unidades a venda e irrelevante "
  "na pratica.\n")
liq = (v[v.bedrooms <= 1].groupby(["bairro", "bedrooms"])
         .agg(unidades_a_venda=("sale_price", "size"),
              preco_mediano=("sale_price", "median"),
              area_mediana=("usable_area", "median")).reset_index())
liq = liq[liq.unidades_a_venda >= 3].sort_values("unidades_a_venda", ascending=False)
w(md_table(liq.round(0), floats="{:,.0f}"))
n_c1 = int(v[(v.bairro == "Centro") & (v.bedrooms == 1)].shape[0])
n_m2 = int(v[(v.bairro == "Meia Praia") & (v.bedrooms == 2)].shape[0])
w(f"\n**Veredito D: a tese e rasa tambem na oferta.** Existem **{n_c1} unidades de "
  f"1 quarto a venda no Centro** - contra {n_m2} de 2 quartos em Meia Praia. "
  "Mesmo se a tese estivesse certa, nao daria para montar um portfolio "
  "relevante sem pressionar o proprio preco de compra.\n")

# ---------- veredito ----------
w("## Veredito final sobre a tese\n")
w(md_table(pd.DataFrame([
    ["Studio (metade da tese)", "INVERIFICAVEL",
     f"{len(st_air)} studios no Airbnb; bedrooms=0 no VivaReal e 'nao informado'"],
    ["A. Receita por unidade", "NAO SUSTENTA",
     f"{pos}o de {len(ta)} em RevPAN; ocupacao menor, nao maior"],
    ["B. Yield sobre capital", "NAO SUSTENTA",
     f"{posb}o de {len(tb)}; o m2 do compacto e o mais caro da cidade"],
    ["C. Receita por m2", "SUSTENTA PARCIALMENTE",
     f"{posc}o de {len(tc)}, mas nao e o que paga o investidor"],
    ["D. Liquidez de compra", "NAO SUSTENTA",
     f"{n_c1} unidades a venda no Centro"],
], columns=["criterio", "veredito", "evidencia"])))
w()
w("**Minha posicao:** *nao sustento a tese.* Ela e verdadeira apenas no criterio "
  "de receita por m2 - que mede produtividade de area, nao retorno sobre capital. "
  "No criterio que adotei, retorno sobre o capital investido, o compacto no Centro "
  f"fica em {posb}o lugar de {len(tb)}, e falha pelo motivo oposto ao que a tese "
  "supoe: **nao porque renda pouco, mas porque custa caro demais por metro "
  "quadrado**. O mercado ja precificou a escassez de compactos.\n")
w("**A condicao que inverteria minha posicao,** declarada: se aparecesse oferta de "
  f"compactos no Centro a **R$ {c2:,.0f}/m2** - o mesmo m2 de um 2 quartos - o yield "
  f"do compacto subiria de {y_tese*100:.2f}% para cerca de "
  f"{y_tese*100*c1/c2:.2f}% e a tese passaria a vencer. "
  "Ou seja: a tese nao esta errada sobre o *tipo de ativo*, esta errada sobre o "
  "*preco atual* desse ativo. Em lancamento ou compra em bloco com desconto, ela "
  "volta a valer - e e assim que a Seazone compra.\n")
w("> **O que a tese acerta:** o instinto de padronizacao e escala. Unidades "
  "compactas quase identicas no mesmo predio tem custo marginal de operacao muito "
  "menor. Esse raciocinio esta correto e permanece valido - apenas nao no preco "
  "pedido hoje no Centro.\n")

(SAIDAS / "04_tese_compactos.md").write_text("\n".join(L), encoding="utf-8")
print("OK -> saidas/04_tese_compactos.md")
print(f"veredito: receita {pos}o/{len(ta)} | yield {posb}o/{len(tb)} | "
      f"receita_m2 {posc}o/{len(tc)} | {n_c1} unidades 1q a venda no Centro")
