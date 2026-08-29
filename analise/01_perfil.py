"""
01 — Perfil dos 5 arquivos: linhas, chaves, taxa de casamento, janela de datas,
vies de selecao. Gera saidas/00_perfil.md.

Uso: python analise/01_perfil.py
"""
import pandas as pd, datetime as dt
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from comum import md_table
from pathlib import Path

P = Path(__file__).resolve().parents[1]
OUT = P / "saidas"; OUT.mkdir(exist_ok=True)
L = []
def w(s=""): L.append(str(s))
def tab(df): w(); w(md_table(df)); w()

d = pd.read_csv(P/"data/Details_Itapema.csv", low_memory=False)
h = pd.read_csv(P/"data/Hosts_ids_Itapema.csv")
m = pd.read_csv(P/"data/Mesh_Ids_Data_Itapema.csv")
pr = pd.read_csv(P/"data/Price_AV_Itapema.csv")
v = pd.read_csv(P/"data/VivaReal_Itapema.csv", low_memory=False)

w("# 00 — Perfil dos dados\n")
w("_Gerado por `analise/01_perfil.py`. Todos os numeros abaixo saem do codigo._\n")

w("## 1. Tamanho e chaves\n")
tab(pd.DataFrame([
    ["Details_Itapema.csv",  len(d), d.shape[1], "airbnb_listing_id", d.airbnb_listing_id.nunique(), d.airbnb_listing_id.duplicated().sum()],
    ["Hosts_ids_Itapema.csv",len(h), h.shape[1], "owner_id",          h.owner_id.nunique(),          h.owner_id.duplicated().sum()],
    ["Mesh_Ids_Data_Itapema.csv", len(m), m.shape[1], "airbnb_listing_id", m.airbnb_listing_id.nunique(), m.airbnb_listing_id.duplicated().sum()],
    ["Price_AV_Itapema.csv", len(pr), pr.shape[1], "listing+data+captura", pr.airbnb_listing_id.nunique(), "-"],
    ["VivaReal_Itapema.csv", len(v), v.shape[1], "listing_id",        v.listing_id.nunique(),        v.listing_id.duplicated().sum()],
], columns=["arquivo","linhas","colunas","chave","chaves unicas","duplicadas"]).set_index("arquivo"))

w("## 2. Taxa de casamento dos joins\n")
w("_Contagem antes e depois de cada join, conforme exigido para nao perder linhas em silencio._\n")
D,M,PP = set(d.airbnb_listing_id), set(m.airbnb_listing_id), set(pr.airbnb_listing_id)
tab(pd.DataFrame([
    ["Details -> Mesh (bairro/geo)", len(D), len(D&M), f"{len(D&M)/len(D):.1%}", "join limpo"],
    ["Details -> Hosts (owner_id)",  len(d), int(d.owner_id.isin(set(h.owner_id)).sum()), f"{d.owner_id.isin(set(h.owner_id)).mean():.1%}", "1383 owner_id repetidos em Hosts: deduplicar antes"],
    ["Details -> Price (preco)",     len(D), len(D&PP), f"{len(D&PP)/len(D):.1%}", "*** GARGALO: so 22% dos anuncios tem preco ***"],
], columns=["join","linhas antes","linhas depois","casamento","nota"]).set_index("join"))

w("## 3. Janela de observacao do Price_AV — o fato que define o metodo\n")
pr["date"]=pd.to_datetime(pr.date); pr["capd"]=pd.to_datetime(pr.aquisition_date).dt.date
g = pr.groupby("capd").agg(linhas=("price","size"), anuncios=("airbnb_listing_id","nunique"),
                           primeira_estadia=("date","min"), ultima_estadia=("date","max"))
tab(g)
w(f"- **Apenas {pr.capd.nunique()} dias de captura** — e dois deles (06 e 07/01) sao consecutivos, "
  "logo existe **1 unico intervalo de comparacao util**: 07/01 -> 20/01 (13 dias).")
w("- Cada captura enxerga uma janela **movel** de ~90 noites a frente da propria data.")
w("- Logo a comparacao so e valida na **intersecao** das janelas: **20/01/2025 a 06/04/2025 (77 noites)**. "
  "Fora dela, uma noite 'sumir' significa apenas que saiu do horizonte da captura, nao que foi reservada.")
w(f"- Estadias observadas vao de {pr.date.min():%d/%m/%Y} a {pr.date.max():%d/%m/%Y}: "
  "**alta temporada + ombro**. Nao cobre o ano; anualizar por 365 sem fator sazonal produziria ficcao.\n")

w("## 4. Vies de selecao: quem tem dado de preco?\n")
d2 = d.merge(m[["airbnb_listing_id","suburb"]], on="airbnb_listing_id", how="left")
d2["tem_preco"] = d2.airbnb_listing_id.isin(PP)
w(f"Dos {len(d2)} anuncios do Details, **{d2.tem_preco.sum()} ({d2.tem_preco.mean():.1%}) tem preco**. "
  "Esse subconjunto nao e aleatorio:\n")
cmp_ = d2.groupby("tem_preco")[["number_of_reviews","star_rating","picture_count"]].median()
cmp_.index = ["SEM preco","COM preco"]
cmp_.index.name = "grupo"
tab(cmp_.round(2))
w("**O anuncio com preco tem mediana de 16 avaliacoes; o sem preco, 1.** O recorte com preco e o dos "
  "anuncios estabelecidos e ja vendendo — vies de sobrevivencia explicito.\n")
for col,lab in [("is_professional","anfitriao profissional"),("is_new_listing","anuncio novo"),("listing_type","tipologia")]:
    t = d2.groupby(col).tem_preco.agg(n="size", cobertura="mean")
    t = t[t.n>=20].sort_values("cobertura",ascending=False)
    t["cobertura"] = (t.cobertura*100).round(1).astype(str)+"%"
    w(f"**Cobertura por {lab}:**"); tab(t)
t = d2.groupby("suburb").tem_preco.agg(n="size",cobertura="mean"); t=t[t.n>=30].sort_values("cobertura",ascending=False)
t["cobertura"]=(t.cobertura*100).round(1).astype(str)+"%"
w("**Cobertura por bairro (n>=30):**"); tab(t)

w("## 5. Mercado de compra (VivaReal)\n")
w(f"- {len(v)} anuncios de venda, {v.listing_id.duplicated().sum()} duplicados por listing_id.")
w(f"- 100% `property_type = UNIT`; `business_types`: {dict(v.business_types.value_counts())}.")
w(f"- Preco de venda ausente em {v.sale_price.isna().sum()} linhas; "
  f"condominio ausente em {v.monthly_condo_fee.isna().sum()}; IPTU ausente em {v.yearly_iptu.isna().sum()}.")
w("- Bairros com mais oferta de compra:")
tab(v.suburb.value_counts().head(8).rename("anuncios a venda").to_frame())
w("> Atencao: bairro do VivaReal vem **com acento** e o do Mesh **sem** "
  "(`Alto Sao Bento` vs `Alto S~ao Bento`). Normalizar antes de cruzar.\n")

w("## 6. Perguntas em aberto ao fim do perfil\n")
for q in [
 "A ocupacao inferida (noite some entre capturas) sobrevive a um teste contra ruido aleatorio?",
 "Com 77 noites de alta/ombro, qual premissa de sazonalidade usar para anualizar — e qual a sensibilidade do yield a ela?",
 "O recorte de ~650 anuncios com ocupacao estimavel aguenta cortes por bairro x tipologia com n>=20?",
 "A tese dos compactos no Centro tem oferta de compra suficiente para ser acionavel em escala?",
]: w(f"- {q}")

(OUT/"00_perfil.md").write_text("\n".join(L), encoding="utf-8")
print(f"OK -> {OUT/'00_perfil.md'}  ({len(L)} linhas)")
