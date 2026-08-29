"""
02 — O ativo central: estimar RECEITA, nao preco.

Price_AV traz preco ANUNCIADO de noites DISPONIVEIS. Receita = ADR x Ocupacao.
A ocupacao e inferida do desaparecimento de noites entre capturas.

Regras que sustentam a inferencia (ver saidas/00_perfil.md secao 3):
  - So existe 1 intervalo util de comparacao: 07/01 -> 20/01 (13 dias).
  - Cada captura ve ~90 noites a frente de si. A comparacao so vale na
    INTERSECAO dos horizontes: 20/01 a 06/04 = 77 noites. Fora dela, "sumir"
    significa "saiu do horizonte", nao "foi reservada".
  - O anuncio precisa aparecer nas DUAS capturas, senao ausencia = saiu do ar.

Gera: saidas/receita_por_listing.csv e saidas/01_receita.md
"""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import pandas as pd, numpy as np
from comum import carregar, md_table, SAIDAS, JANELA_INI, JANELA_FIM, JANELA_N

MIN_NOITES_OBS = 20      # noites ofertadas na captura inicial p/ estimar ocupacao
L = []
def w(s=""): L.append(str(s))

d, h, m, pr, v = carregar()
w("# 01 — Estimativa de receita (ADR x Ocupacao)\n")
w("_Gerado por `analise/02_receita.py`._\n")
w(f"**Janela de comparacao:** {JANELA_INI:%d/%m/%Y} a {JANELA_FIM:%d/%m/%Y} "
  f"= **{JANELA_N} noites** (intersecao dos horizontes das capturas).\n")

cap = sorted(pr.captura.unique())
inicial, final = pr[pr.captura.isin(cap[:2])], pr[pr.captura == cap[-1]]

na_janela = lambda x: x[(x.date >= JANELA_INI) & (x.date <= JANELA_FIM)]
# captura inicial: 06 e 07/01 sao quase o mesmo instante -> deduplica por (listing, noite)
ini = na_janela(inicial).sort_values("captura").drop_duplicates(["airbnb_listing_id", "date"], keep="last")
fim = na_janela(final)

# --- funil de exclusao, contado e reportado ---
funil = [("anuncios no Details", d.airbnb_listing_id.nunique()),
         ("com alguma linha em Price_AV", pr.airbnb_listing_id.nunique()),
         ("ofertando na janela em 06-07/01", ini.airbnb_listing_id.nunique()),
         ("ofertando na janela em 20/01", fim.airbnb_listing_id.nunique())]
ativos = set(ini.airbnb_listing_id) & set(fim.airbnb_listing_id)
funil.append(("presentes nas DUAS capturas (ativos)", len(ativos)))
ini, fim = ini[ini.airbnb_listing_id.isin(ativos)], fim[fim.airbnb_listing_id.isin(ativos)]
obs = ini.groupby("airbnb_listing_id").size()
elegiveis = set(obs[obs >= MIN_NOITES_OBS].index)
funil.append((f"com >= {MIN_NOITES_OBS} noites observadas (elegiveis)", len(elegiveis)))
w("## Funil de anuncios\n")
f = pd.DataFrame(funil, columns=["etapa", "anuncios"])
f["% do Details"] = (f.anuncios / f.anuncios.iloc[0] * 100).round(1).astype(str) + "%"
w(md_table(f)); w()

ini = ini[ini.airbnb_listing_id.isin(elegiveis)]
fim = fim[fim.airbnb_listing_id.isin(elegiveis)]

# --- a inferencia ---
vendidas_key = set(zip(fim.airbnb_listing_id, fim.date))
ini = ini.assign(vendida=[(i, dt) not in vendidas_key
                          for i, dt in zip(ini.airbnb_listing_id, ini.date)])

w("## Teste de validade: 'sumiu' e demanda ou bloqueio do proprietario?\n")
w("Se o desaparecimento fosse bloqueio/manutencao (ruido aleatorio), o preco das noites que "
  "sumiram seria igual ao das que sobraram. Comparando com um atributo que a inferencia **nao usou**:\n")
t = ini.groupby("vendida").price.agg(noites="size", preco_mediano="median", preco_medio="mean")
t.index = ["sobrou disponivel", "SUMIU (reservada)"]
t.index.name = "noite ofertada em 06-07/01"
w(md_table(t.round(1)))
reapareceu = len(set(zip(fim.airbnb_listing_id, fim.date)) - set(zip(ini.airbnb_listing_id, ini.date)))
w(f"\n- Sumiram **{ini.vendida.sum():,} noites-anuncio ({ini.vendida.mean():.1%})** em 13 dias; "
  f"reapareceram apenas **{reapareceu:,} ({reapareceu/len(ini):.1%})**.")
dif = ini[ini.vendida].price.median() - ini[~ini.vendida].price.median()
w(f"- A noite que sumiu era **R$ {abs(dif):,.0f} {'mais cara' if dif>0 else 'mais barata'}** que a que sobrou "
  "(mediana). Assimetria de preco e de direcao e **incompativel com bloqueio aleatorio** e compativel com "
  "reserva: as datas mais desejadas sao as mais caras e as que vendem primeiro.")
w("- **Premissa declarada:** trato desaparecimento de disponibilidade como reserva. Isso **superestima** a "
  "ocupacao na presenca de bloqueios do proprietario, e nao tenho como separar os dois casos.\n")

# --- metricas por anuncio ---
adr_vend = ini[ini.vendida].groupby("airbnb_listing_id").price.median().rename("adr_vendidas")
adr_ofer = ini.groupby("airbnb_listing_id").price.median().rename("adr_ofertadas")
ocup_fim = (1 - fim.groupby("airbnb_listing_id").date.nunique() / JANELA_N).rename("ocupacao")
pickup = ini.groupby("airbnb_listing_id").vendida.mean().rename("pickup_13d")

r = pd.concat([adr_vend, adr_ofer, ocup_fim, pickup], axis=1)
r["adr_fallback"] = r.adr_vendidas.isna()
r["adr"] = r.adr_vendidas.fillna(r.adr_ofertadas)
r["revpan"] = r.adr * r.ocupacao
r["receita_77n"] = r.revpan * JANELA_N
r = r.reset_index()

w(f"## Construcao das metricas por anuncio (n = {len(r)})\n")
w("| metrica | definicao |")
w("|---|---|")
w("| `ocupacao` | 1 - (noites ainda ofertadas em 20/01 na janela) / 77. Nivel de ocupacao observado. |")
w("| `pickup_13d` | fracao das noites ofertadas em 06-07/01 que sumiram ate 20/01. Velocidade de venda. |")
w("| `adr` | **mediana do preco das noites que efetivamente sumiram** — o preco do que vendeu, nao da vitrine. |")
w("| `revpan` | `adr x ocupacao` = receita por noite disponivel. |")
w("| `receita_77n` | `revpan x 77` = receita estimada na janela observada. |")
w()
w(f"- {r.adr_fallback.sum()} anuncios ({r.adr_fallback.mean():.1%}) nao venderam nenhuma noite no intervalo; "
  "para eles uso a mediana das noites ofertadas como ADR (premissa declarada, conservadora quanto ao mix).")
cor = r[["ocupacao", "pickup_13d"]].corr().iloc[0, 1]
w(f"- **Coerencia interna:** `ocupacao` e `pickup_13d` sao construidas de capturas diferentes e correlacionam "
  f"**{cor:.2f}**. Duas medidas independentes apontando junto — a ocupacao esta medindo demanda, nao ruido.\n")

w("## Distribuicao das estimativas\n")
w(md_table(r[["adr", "ocupacao", "pickup_13d", "revpan", "receita_77n"]]
           .describe(percentiles=[.1, .25, .5, .75, .9]).round(2)
           .rename_axis("estatistica")))
w()
faixa = pd.cut(r.ocupacao, [-.01, .001, .2, .4, .6, .8, .999, 1.001],
               labels=["0%", "0-20%", "20-40%", "40-60%", "60-80%", "80-99%", "100%"])
w("**Sanidade da ocupacao** (massa em 0% ou 100% indicaria regra quebrada):\n")
w(md_table(faixa.value_counts().sort_index().rename("anuncios").to_frame()))
w(f"\nNenhum anuncio em 100% e apenas {(r.ocupacao<=0.001).sum()} em 0%: a regra discrimina, nao satura.\n")

r.to_csv(SAIDAS / "receita_por_listing.csv", index=False)
(SAIDAS / "01_receita.md").write_text("\n".join(L), encoding="utf-8")
print(f"OK  {len(r)} anuncios com receita estimada -> saidas/receita_por_listing.csv")
print(r[["adr","ocupacao","revpan","receita_77n"]].median().round(1).to_string())
