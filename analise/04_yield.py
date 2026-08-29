"""
04 - Yield liquido sobre capital: onde VALE A PENA investir.

Cruza a receita estimada (Airbnb) com o preco de compra (VivaReal) por
celula bairro x numero de quartos, desconta a estrutura de custo e compara
com o CDI.

Le  : saidas/listings_enriquecido.csv (03_perfil_local.py)
Gera: saidas/03_yield.md e saidas/yield_por_celula.csv
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import numpy as np
from comum import carregar, md_table, normalizar_bairro, SAIDAS, JANELA_N

# ------------------------------------------------------------------
# PREMISSAS - todas declaradas, nenhuma escondida.
# As tres primeiras sao EXTERNAS ao dataset; as demais saem do proprio dado.
# ------------------------------------------------------------------
# Selic/CDI no momento da captura dos dados (jan/2025). Uso a taxa da data do
# dado, nao o pico do ano, para nao inflar artificialmente a regua.
CDI = 0.1225
SELIC_PICO_2025 = 0.15       # a Selic subiu ao longo de 2025; o gap so aumenta
DESCONTO_NEGOCIACAO = 0.10   # imovel no Brasil fecha abaixo do pedido
NOITES_POR_ESTADIA = 4.0     # para dimensionar o custo de limpeza

TAXA_GESTAO = 0.18           # servico da propria Seazone (~15-20% da receita)
COMISSAO_CANAL = 0.03        # padrao Airbnb no lado do anfitriao
LIMPEZA_POR_ESTADIA = 150.0
PROVISAO_MANUTENCAO = 0.05   # colchao sobre a receita

# Cenarios de sazonalidade: quanto da receita ANUAL cai nas 77 noites
# observadas (20/01 a 06/04 = alta temporada + ombro).
CENARIOS = {"conservador (janela = 55% do ano)": 0.55,
            "base (janela = 45% do ano)": 0.45,
            "otimista (janela = 35% do ano)": 0.35}
CEN_BASE = "base (janela = 45% do ano)"

N_MIN_AIRBNB = 20
N_MIN_VENDA = 15

L = []


def w(s=""):
    L.append(str(s))


d, h, m, pr, v = carregar()
base = pd.read_csv(SAIDAS / "listings_enriquecido.csv")
base["bairro"] = normalizar_bairro(base.suburb)

# ---------- lado da compra ----------
v = v.drop_duplicates("listing_id").copy()
for c_ in ["sale_price", "monthly_condo_fee", "yearly_iptu", "usable_area", "bedrooms"]:
    v[c_] = pd.to_numeric(v[c_], errors="coerce")
v["bairro"] = normalizar_bairro(v.suburb)
v = v[v.sale_price.between(80_000, 20_000_000) & v.bedrooms.between(0, 6)
      & v.usable_area.between(20, 600)]
v["quartos"] = v.bedrooms.clip(upper=4)

w("# 03 - Yield liquido sobre capital investido\n")
w("_Gerado por `analise/04_yield.py`._\n")
w("## Criterio, declarado antes do resultado\n")
w("```\nMelhor = retorno sobre o capital investido\n\n"
  "  Yield liquido = (Receita anual - Custos operacionais) / Preco de aquisicao\n"
  "  Regua        = CDI\n```\n")
w("O denominador e o que torna a analise uma decisao de investimento e nao um "
  "ranking de faturamento. Sem ele eu responderia *onde tem mais receita*; com "
  "ele respondo *onde vale a pena comprar*.\n")

# ---------- qualidade dos campos de custo ----------
w("## Antes de usar: dois defeitos nos dados de compra\n")
w("**1. Encoding.** `VivaReal_Itapema.csv` esta em **latin-1**. Lido como UTF-8 "
  "(o default do pandas), `Alto Sao Bento` e `Sertao do Trombudo` viram "
  "caractere de substituicao e **deixam de casar** com o bairro do Mesh. "
  "Corrigido em `comum.carregar()`.\n")
w("**2. Valores sentinela em condominio e IPTU.** Nao sao dados faltantes "
  "declarados - sao zeros e uns:\n")
q = pd.DataFrame({
    "campo": ["monthly_condo_fee", "yearly_iptu"],
    "nulo": [int(v.monthly_condo_fee.isna().sum()), int(v.yearly_iptu.isna().sum())],
    "igual a 0": [int((v.monthly_condo_fee == 0).sum()),
                  int((v.yearly_iptu == 0).sum())],
    "<= R$50 (implausivel)": [int((v.monthly_condo_fee <= 50).sum()),
                              int((v.yearly_iptu <= 50).sum())],
    "plausivel (> R$50)": [int((v.monthly_condo_fee > 50).sum()),
                           int((v.yearly_iptu > 50).sum())]})
w(md_table(q))
w("\nUsar a mediana bruta desses campos levaria a condominio de R$1,00 em "
  "celulas inteiras. **Solucao:** derivo a *taxa* no subconjunto plausivel e "
  "aplico a todas as unidades pela area e pelo preco.\n")
cok = v[v.monthly_condo_fee > 50]
iok = v[v.yearly_iptu > 50]
CONDO_M2 = float((cok.monthly_condo_fee / cok.usable_area).median())
IPTU_PCT = float((iok.yearly_iptu / iok.sale_price).median())
w(f"- Condominio: **R$ {CONDO_M2:.2f}/m2/mes** (mediana de {len(cok):,} anuncios "
  "com valor plausivel)")
w(f"- IPTU: **{IPTU_PCT*100:.3f}% do valor do imovel ao ano** "
  f"(mediana de {len(iok):,} anuncios)\n")

w("## Premissas de custo e de mercado\n")
w(md_table(pd.DataFrame([
    ["CDI (regua de comparacao)", f"{CDI*100:.2f}% a.a.",
     "EXTERNA - Selic em jan/2025, data da captura"],
    ["Desconto de negociacao", f"{DESCONTO_NEGOCIACAO*100:.0f}%",
     "EXTERNA - anuncio nao e preco fechado"],
    ["Noites por estadia", f"{NOITES_POR_ESTADIA:.0f}",
     "EXTERNA - dimensiona a limpeza"],
    ["Taxa de gestao", f"{TAXA_GESTAO*100:.0f}% da receita", "negocio da Seazone"],
    ["Comissao de canal", f"{COMISSAO_CANAL*100:.0f}% da receita", "padrao Airbnb"],
    ["Limpeza e enxoval", f"R$ {LIMPEZA_POR_ESTADIA:.0f}/estadia", "estimativa"],
    ["Manutencao e vacancia", f"{PROVISAO_MANUTENCAO*100:.0f}% da receita", "provisao"],
    ["Condominio", f"R$ {CONDO_M2:.2f}/m2/mes", "DERIVADA do VivaReal limpo"],
    ["IPTU", f"{IPTU_PCT*100:.3f}% do valor/ano", "DERIVADA do VivaReal limpo"],
], columns=["item", "valor", "origem"])))
w("\n> As tres premissas marcadas EXTERNA nao saem do dataset. Estao isoladas no "
  "topo de `analise/04_yield.py` para que qualquer leitor troque o numero e "
  "refaca a conta.\n")

# ---------- celulas ----------
air = (base.groupby(["bairro", "faixa_quartos"])
           .agg(n_airbnb=("revpan", "size"), receita_77n=("receita_77n", "median"),
                revpan=("revpan", "median"), adr=("adr", "median"),
                ocupacao=("ocupacao", "median")).reset_index())
mapa = {0: "Studio", 1: "1 quarto", 2: "2 quartos", 3: "3 quartos", 4: "4+ quartos"}
v["faixa_quartos"] = v.quartos.map(mapa)
ven = (v.groupby(["bairro", "faixa_quartos"])
        .agg(n_venda=("sale_price", "size"), preco_pedido=("sale_price", "median"),
             area=("usable_area", "median")).reset_index())

c = air.merge(ven, on=["bairro", "faixa_quartos"], how="inner")
w("## Cruzamento Airbnb x VivaReal\n")
w(f"- Celulas bairro x quartos com receita estimada: **{len(air)}**")
w(f"- Celulas com oferta de venda: **{len(ven)}**")
w(f"- Celulas que casaram: **{len(c)}**")
c = c[(c.n_airbnb >= N_MIN_AIRBNB) & (c.n_venda >= N_MIN_VENDA)].copy()
w(f"- Apos exigir n_airbnb >= {N_MIN_AIRBNB} **e** n_venda >= {N_MIN_VENDA}: "
  f"**{len(c)} celulas analisaveis**\n")

# ---------- economia ----------
c["preco_compra"] = c.preco_pedido * (1 - DESCONTO_NEGOCIACAO)
c["condominio_ano"] = CONDO_M2 * c.area * 12
c["iptu_ano"] = IPTU_PCT * c.preco_compra

linhas = []
for nome, fator in CENARIOS.items():
    x = c.copy()
    x["cenario"] = nome
    x["receita_ano"] = x.receita_77n / fator
    x["noites_vendidas_ano"] = (x.ocupacao * JANELA_N) / fator
    x["custo_limpeza"] = x.noites_vendidas_ano / NOITES_POR_ESTADIA * LIMPEZA_POR_ESTADIA
    x["custo_variavel"] = x.receita_ano * (TAXA_GESTAO + COMISSAO_CANAL
                                           + PROVISAO_MANUTENCAO)
    x["custos_totais"] = (x.custo_variavel + x.custo_limpeza
                          + x.condominio_ano + x.iptu_ano)
    x["noi"] = x.receita_ano - x.custos_totais
    x["yield_bruto"] = x.receita_ano / x.preco_compra
    x["yield_liquido"] = x.noi / x.preco_compra
    linhas.append(x)
res = pd.concat(linhas, ignore_index=True)
res.to_csv(SAIDAS / "yield_por_celula.csv", index=False)

rb = res[res.cenario == CEN_BASE].sort_values("yield_liquido", ascending=False)

w("## Ranking por yield liquido - cenario base (janela = 45% da receita anual)\n")
tab = rb[["bairro", "faixa_quartos", "n_airbnb", "n_venda", "receita_ano",
          "preco_compra", "custos_totais", "noi", "yield_liquido"]].reset_index(drop=True)
for col in ["receita_ano", "preco_compra", "custos_totais", "noi"]:
    tab[col] = tab[col].round(0)
tab["yield_liquido"] = (tab.yield_liquido * 100).round(2).astype(str) + "%"
w(md_table(tab, floats="{:,.0f}"))
w(f"\n**Regua: CDI = {CDI*100:.2f}% a.a.** Nenhuma celula deve ser comentada sem "
  "essa comparacao ao lado.\n")

w("## Sensibilidade a sazonalidade - onde a decisao se inverte\n")
w("A janela observada e alta temporada + ombro. Nao anualizo cegamente: mostro o "
  "yield liquido sob as tres premissas.\n")
piv = res.pivot_table(index=["bairro", "faixa_quartos"], columns="cenario",
                      values="yield_liquido")
piv = (piv * 100).reindex(columns=list(CENARIOS)).sort_values(CEN_BASE,
                                                              ascending=False)
piv.columns = [k.split("(")[0].strip() for k in piv.columns]
w(md_table(piv.map(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")))
melhor = rb.iloc[0]
otim = res[res.cenario == "otimista (janela = 35% do ano)"].yield_liquido.max()
w(f"\n- Melhor celula no cenario base: **{melhor.bairro} / {melhor.faixa_quartos}** "
  f"com **{melhor.yield_liquido*100:.2f}%** liquido a.a.")
w(f"- Mesmo no cenario mais otimista de sazonalidade, o topo do ranking chega a "
  f"**{otim*100:.2f}%**.")
w(f"- Diferenca para o CDI no cenario base: **{(melhor.yield_liquido-CDI)*100:+.2f} p.p.**\n")

# ---------- teste de teto: tira a sazonalidade da discussao ----------
w("## Teste de teto - o argumento que nao depende de nenhuma premissa sazonal\n")
w("A objecao obvia ao resultado acima e *voce chutou o fator sazonal*. Entao "
  "elimino a premissa: e se Itapema rodasse **os 365 dias do ano no ritmo da alta "
  "temporada observada** - mesma diaria de janeiro, mesma ocupacao de janeiro, "
  "zero queda de inverno? E um teto fisicamente impossivel, e serve justamente "
  "por isso: nenhum cenario real pode superar.\n")
t = c.copy()
t["receita_teto"] = t.revpan * 365
t["noites_teto"] = t.ocupacao * 365
t["noi_teto"] = (t.receita_teto * (1 - TAXA_GESTAO - COMISSAO_CANAL - PROVISAO_MANUTENCAO)
                 - t.condominio_ano - t.iptu_ano
                 - t.noites_teto / NOITES_POR_ESTADIA * LIMPEZA_POR_ESTADIA)
t["yield_teto"] = t.noi_teto / t.preco_compra
tt = (t.sort_values("yield_teto", ascending=False)
       [["bairro", "faixa_quartos", "revpan", "receita_teto",
         "preco_compra", "yield_teto"]].reset_index(drop=True))
tt["revpan"] = tt.revpan.round(0)
tt["receita_teto"] = tt.receita_teto.round(0)
tt["preco_compra"] = tt.preco_compra.round(0)
tt["yield_teto"] = (tt.yield_teto * 100).round(2).astype(str) + "%"
w(md_table(tt, floats="{:,.0f}"))
teto = t.yield_teto.max()
w(f"\n**Teto absoluto do melhor ativo do dataset: {teto*100:.2f}% liquido a.a.** "
  f"contra **{CDI*100:.2f}%** do CDI na data da captura "
  f"(e a Selic ainda subiu para ~{SELIC_PICO_2025*100:.0f}% ao longo de 2025).\n")
w(f"> O ativo mais rentavel de Itapema renderia, no limite fisico, "
  f"**menos da metade** do titulo publico - sem risco operacional, sem "
  "iliquidez, sem trabalho de gestao. A conclusao nao depende do fator "
  "sazonal que eu escolhi: **nao existe fator sazonal capaz de inverter "
  "essa comparacao.**\n")

# ---------- preco-teto: a que preco o ativo passaria a valer a pena ----------
w("## Preco-teto - a que preco cada ativo empataria com o CDI\n")
w("Se o retorno no preco pedido nao justifica a compra, a pergunta util para um "
  "comite nao e *compro ou nao*, e sim **a que preco eu compraria**. Resolvendo "
  "`NOI(P) / P = CDI` para P (o IPTU depende de P, os demais custos nao):\n")
w("```\n  P_teto = (Receita - custos variaveis - limpeza - condominio) / (CDI + IPTU%)\n```\n")
pt = res[res.cenario == CEN_BASE].copy()
pt["preco_teto"] = ((pt.receita_ano - pt.custo_variavel - pt.custo_limpeza
                     - pt.condominio_ano) / (CDI + IPTU_PCT))
pt["desconto_necessario"] = 1 - pt.preco_teto / pt.preco_compra
pt = pt.sort_values("desconto_necessario").reset_index(drop=True)
ptx = pt[["bairro", "faixa_quartos", "preco_compra", "preco_teto",
          "desconto_necessario"]].copy()
ptx["preco_compra"] = ptx.preco_compra.round(0)
ptx["preco_teto"] = ptx.preco_teto.round(0)
ptx["desconto_necessario"] = (ptx.desconto_necessario * 100).round(1).astype(str) + "%"
w(md_table(ptx, floats="{:,.0f}"))
w(f"\n> Nenhum ativo do dataset empata com o CDI sem um desconto de pelo menos "
  f"**{pt.desconto_necessario.min()*100:.0f}%** sobre o preco pedido. Esse e o "
  "numero que a Seazone levaria para uma mesa de negociacao - e a ordem de "
  "grandeza mostra que nao se trata de negociar melhor, e sim de que o mercado "
  "de Itapema **nao esta precificado para renda de short stay**: esta "
  "precificado para valorizacao e uso proprio.\n")

(SAIDAS / "03_yield.md").write_text("\n".join(L), encoding="utf-8")
print("OK -> saidas/03_yield.md")
print(tab.to_string(index=False))
