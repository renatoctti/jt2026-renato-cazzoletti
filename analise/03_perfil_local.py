"""
03 - Perguntas 1, 2 e 3: perfil, localizacao e caracteristicas.

P1 tipologia x n de quartos x tipo de anuncio -> RevPAN (mediana + n)
P2 bairro, CONTROLANDO por n de quartos       -> senao mede tamanho e chama de local
P3 o que explica a receita                    -> correlacao + regressao interpretavel

Le : saidas/receita_por_listing.csv (gerado por 02_receita.py)
Gera: saidas/02_perfil_local.md e saidas/listings_enriquecido.csv
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import numpy as np
from comum import carregar, md_table, SAIDAS

N_MIN = 20
L = []


def w(s=""):
    L.append(str(s))


d, h, m, pr, v = carregar()
r = pd.read_csv(SAIDAS / "receita_por_listing.csv")


# ---------- distancia ate a praia ----------
def haversine(la1, lo1, la2, lo2):
    R = 6371.0
    p1, p2 = np.radians(la1), np.radians(la2)
    dp, dl = np.radians(la2 - la1), np.radians(lo2 - lo1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


geo = m[["airbnb_listing_id", "latitude", "longitude", "suburb"]].copy()
# Itapema e uma enseada voltada para LESTE: para cada faixa de latitude, a borda
# leste da mancha de anuncios aproxima a orla. Linha suavizada para tirar ruido.
geo["faixa"] = (geo.latitude / 0.004).round() * 0.004
costa = (geo.groupby("faixa").longitude.quantile(0.98)
            .rolling(3, center=True, min_periods=1).mean())
geo["lon_costa"] = geo.faixa.map(costa)
geo["dist_praia_km"] = haversine(geo.latitude, geo.longitude,
                                 geo.latitude, geo.lon_costa).round(3)

hosts = h.drop_duplicates("owner_id")[
    ["owner_id", "is_superhost", "years_host", "number_of_reviews_host"]]
base = (d.merge(geo[["airbnb_listing_id", "suburb", "latitude",
                     "longitude", "dist_praia_km"]],
                on="airbnb_listing_id", how="left")
         .merge(hosts, on="owner_id", how="left")
         .merge(r, on="airbnb_listing_id", how="inner"))
base["quartos"] = base.number_of_bedrooms.clip(upper=4)
base["faixa_quartos"] = base.quartos.map({0: "Studio", 1: "1 quarto", 2: "2 quartos",
                                          3: "3 quartos", 4: "4+ quartos"})
base["compacto"] = base.number_of_bedrooms <= 1
base.to_csv(SAIDAS / "listings_enriquecido.csv", index=False)

w("# 02 - Perguntas 1, 2 e 3\n")
w(f"_Gerado por `analise/03_perfil_local.py`. Base: {len(base)} anuncios "
  "com receita estimada._\n")
w(f"**Corte de n:** so comento celulas com **n >= {N_MIN}**. Toda tabela mostra o n. "
  "Ranking sem n e ruido apresentado como conclusao.\n")
w("**Metrica:** RevPAN = receita por noite disponivel = ADR x ocupacao. Uso "
  "**mediana** por padrao: receita de short stay tem cauda longa e um anuncio de "
  "luxo distorce a media do recorte inteiro.\n")


def agg(df, by):
    t = df.groupby(by, observed=True).agg(
        n=("revpan", "size"),
        revpan_med=("revpan", "median"),
        adr_med=("adr", "median"),
        ocup_med=("ocupacao", "median"),
        receita_77n=("receita_77n", "median")).round(2)
    return t[t.n >= N_MIN].sort_values("revpan_med", ascending=False)


# ---------- P1 ----------
w("\n## P1 - Qual o melhor perfil de imovel?\n")
w("### Por numero de quartos\n")
t1 = agg(base, "faixa_quartos")
w(md_table(t1))
w()
w("### Por tipologia (tipo de imovel)\n")
w(md_table(agg(base, "listing_type")))
w()
w("### Cruzamento tipologia x numero de quartos\n")
w(md_table(agg(base, ["listing_type", "faixa_quartos"])))
w()
w("> **O erro que a receita absoluta induz:** o RevPAN cresce com o numero de "
  "quartos porque um imovel maior cobra mais caro. Isso responde *quem fatura "
  "mais por noite*, nao *quem rende mais por real investido*. A comparacao justa "
  "exige o preco de compra no denominador - e e o que a etapa 04 faz.\n")

# ---------- P2 ----------
w("\n## P2 - Qual a melhor localizacao em termos de receita?\n")
w("### Bruto (sem controle) - a leitura enganosa\n")
w(md_table(agg(base, "suburb")))
w()
w("### Controlando por numero de quartos - a leitura correta\n")
w("Se o bairro X aparece melhor apenas porque concentra imoveis maiores, o efeito "
  "some aqui.\n")
piv = base.pivot_table(index="suburb", columns="faixa_quartos",
                       values="revpan", aggfunc="median")
cnt = base.pivot_table(index="suburb", columns="faixa_quartos",
                       values="revpan", aggfunc="size")
piv = piv.where(cnt >= N_MIN).dropna(how="all").round(0)
w(f"**RevPAN mediano por bairro x quartos** (celulas com n < {N_MIN} suprimidas):\n")
w(md_table(piv.fillna("-"), floats="{:,.0f}"))
w()
w("**n de cada celula:**\n")
w(md_table(cnt.fillna(0).astype(int)))
w()

w("### Distancia ate a praia - o regressor que o rotulo de bairro esconde\n")
w("_Orla estimada empiricamente: para cada faixa de latitude, a borda leste da "
  "mancha de anuncios (percentil 98 da longitude), suavizada. Itapema e uma "
  "enseada voltada para leste._\n")
base["faixa_praia"] = pd.cut(base.dist_praia_km, [-.01, .2, .4, .8, 1.5, 99],
                             labels=["ate 200m", "200-400m", "400-800m",
                                     "800m-1,5km", "mais de 1,5km"])
w(md_table(agg(base, "faixa_praia")))
w()
sub = base[base.dist_praia_km.notna()]
w("- Correlacao de Spearman entre distancia da praia e RevPAN: "
  f"**{sub.dist_praia_km.corr(sub.revpan, method='spearman'):.2f}**")
c2 = base[base.quartos == 2]
w(f"- Dentro de **2 quartos apenas** (n={len(c2)}), a correlacao e "
  f"**{c2.dist_praia_km.corr(c2.revpan, method='spearman'):.2f}** - o efeito nao "
  "e artefato de tamanho.\n")

# ---------- P3 ----------
w("\n## P3 - Quais caracteristicas explicam as melhores receitas?\n")
base["amenidades_n"] = base.amenities.fillna("").str.count(",") + 1
base["superhost"] = (base.is_superhost == True).astype(int)
cands = {"number_of_bedrooms": "numero de quartos",
         "number_of_guests": "capacidade (hospedes)",
         "dist_praia_km": "distancia da praia (km)",
         "star_rating": "nota media",
         "number_of_reviews": "numero de avaliacoes",
         "picture_count": "numero de fotos",
         "amenidades_n": "numero de amenidades",
         "superhost": "anfitriao superhost",
         "years_host": "anos como anfitriao",
         "cleaning_fee": "taxa de limpeza"}
cor = pd.DataFrame({
    "variavel": list(cands.values()),
    "corr_com_revpan": [base[k].corr(base.revpan, method="spearman") for k in cands],
    "n": [int(base[k].notna().sum()) for k in cands]}).round(3)
w("### Correlacao (Spearman) com RevPAN\n")
w(md_table(cor.sort_values("corr_com_revpan", key=abs, ascending=False)))
w()

# regressao interpretavel em log
X = base[list(cands)].apply(pd.to_numeric, errors="coerce")
y = np.log(base.revpan.clip(lower=1))
ok = X.notna().all(axis=1) & np.isfinite(y)
Xs = (X[ok] - X[ok].mean()) / X[ok].std().replace(0, 1)
A = np.column_stack([np.ones(int(ok.sum())), Xs.values])
beta, *_ = np.linalg.lstsq(A, y[ok].values, rcond=None)
pred = A @ beta
r2 = 1 - ((y[ok].values - pred) ** 2).sum() / ((y[ok].values - y[ok].mean()) ** 2).sum()
w(f"### Regressao linear em log(RevPAN), variaveis padronizadas "
  f"(n={int(ok.sum())}, R2 = {r2:.2f})\n")
w("Coeficiente = variacao em log(RevPAN) por **1 desvio-padrao** da variavel, "
  "mantendo as demais fixas.\n")
w(md_table(pd.DataFrame({"variavel": list(cands.values()),
                         "coef_padronizado": beta[1:].round(3)})
           .sort_values("coef_padronizado", key=abs, ascending=False)))
w()
w("> **Estes coeficientes sao associacao, nao causa.** Amenidades correlacionam "
  "entre si e com a qualidade geral do ativo - piscina pode ser proxy de *predio "
  "bom em rua boa*. O interesse aqui e **identificar sinal para triagem de "
  "compra**, nao estimar efeito causal.\n")
w("> **Causalidade reversa em avaliacoes:** numero de reviews correlaciona com "
  "receita em boa parte porque **quem vende mais acumula mais reviews**, e nao o "
  "contrario. Nao trate *conseguir reviews* como alavanca de investimento - ela e "
  "consequencia, nao causa.\n")

(SAIDAS / "02_perfil_local.md").write_text("\n".join(L), encoding="utf-8")
print("OK -> saidas/02_perfil_local.md")
print(t1.to_string())
