# 01 — Estimativa de receita (ADR x Ocupacao)

_Gerado por `analise/02_receita.py`._

**Janela de comparacao:** 20/01/2025 a 06/04/2025 = **77 noites** (intersecao dos horizontes das capturas).

## Funil de anuncios

| etapa                                   | anuncios | % do Details |
|-----------------------------------------|----------|--------------|
| anuncios no Details                     | 4441     | 100.0%       |
| com alguma linha em Price_AV            | 1005     | 22.6%        |
| ofertando na janela em 06-07/01         | 881      | 19.8%        |
| ofertando na janela em 20/01            | 776      | 17.5%        |
| presentes nas DUAS capturas (ativos)    | 656      | 14.8%        |
| com >= 20 noites observadas (elegiveis) | 605      | 13.6%        |

## Teste de validade: 'sumiu' e demanda ou bloqueio do proprietario?

Se o desaparecimento fosse bloqueio/manutencao (ruido aleatorio), o preco das noites que sumiram seria igual ao das que sobraram. Comparando com um atributo que a inferencia **nao usou**:

| noite ofertada em 06-07/01 | noites | preco_mediano | preco_medio |
|----------------------------|--------|---------------|-------------|
| sobrou disponivel          | 27339  | 641.00        | 723.80      |
| SUMIU (reservada)          | 4460   | 675.00        | 700.70      |

- Sumiram **4,460 noites-anuncio (14.0%)** em 13 dias; reapareceram apenas **568 (1.8%)**.
- A noite que sumiu era **R$ 34 mais cara** que a que sobrou (mediana). Assimetria de preco e de direcao e **incompativel com bloqueio aleatorio** e compativel com reserva: as datas mais desejadas sao as mais caras e as que vendem primeiro.
- **Premissa declarada:** trato desaparecimento de disponibilidade como reserva. Isso **superestima** a ocupacao na presenca de bloqueios do proprietario, e nao tenho como separar os dois casos.

## Construcao das metricas por anuncio (n = 605)

| metrica | definicao |
|---|---|
| `ocupacao` | 1 - (noites ainda ofertadas em 20/01 na janela) / 77. Nivel de ocupacao observado. |
| `pickup_13d` | fracao das noites ofertadas em 06-07/01 que sumiram ate 20/01. Velocidade de venda. |
| `adr` | **mediana do preco das noites que efetivamente sumiram** — o preco do que vendeu, nao da vitrine. |
| `revpan` | `adr x ocupacao` = receita por noite disponivel. |
| `receita_77n` | `revpan x 77` = receita estimada na janela observada. |

- 185 anuncios (30.6%) nao venderam nenhuma noite no intervalo; para eles uso a mediana das noites ofertadas como ADR (premissa declarada, conservadora quanto ao mix).
- **Coerencia interna:** `ocupacao` e `pickup_13d` sao construidas de capturas diferentes e correlacionam **0.52**. Duas medidas independentes apontando junto — a ocupacao esta medindo demanda, nao ruido.

## Distribuicao das estimativas

| estatistica | adr      | ocupacao | pickup_13d | revpan   | receita_77n |
|-------------|----------|----------|------------|----------|-------------|
| count       | 605.00   | 605.00   | 605.00     | 605.00   | 605.00      |
| mean        | 726.48   | 0.40     | 0.14       | 272.57   | 20,987.85   |
| std         | 346.15   | 0.21     | 0.16       | 182.57   | 14,057.54   |
| min         | 165.00   | 0.00     | 0.00       | 0.00     | 0.00        |
| 10%         | 385.20   | 0.13     | 0.00       | 87.71    | 6,754.00    |
| 25%         | 500.00   | 0.25     | 0.00       | 149.35   | 11,500.00   |
| 50%         | 674.00   | 0.38     | 0.11       | 237.04   | 18,252.00   |
| 75%         | 850.00   | 0.56     | 0.22       | 353.25   | 27,200.00   |
| 90%         | 1,096.00 | 0.69     | 0.35       | 487.79   | 37,560.00   |
| max         | 3,500.00 | 0.96     | 0.92       | 1,246.75 | 96,000.00   |

**Sanidade da ocupacao** (massa em 0% ou 100% indicaria regra quebrada):

| ocupacao | anuncios |
|----------|----------|
| 0%       | 7        |
| 0-20%    | 108      |
| 20-40%   | 203      |
| 40-60%   | 168      |
| 60-80%   | 97       |
| 80-99%   | 22       |
| 100%     | 0        |

Nenhum anuncio em 100% e apenas 7 em 0%: a regra discrimina, nao satura.
