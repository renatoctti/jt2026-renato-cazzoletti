# 00 — Perfil dos dados

_Gerado por `analise/01_perfil.py`. Todos os numeros abaixo saem do codigo._

## 1. Tamanho e chaves


| arquivo                   | linhas | colunas | chave                | chaves unicas | duplicadas |
|---------------------------|--------|---------|----------------------|---------------|------------|
| Details_Itapema.csv       | 4441   | 35      | airbnb_listing_id    | 4441          | 0          |
| Hosts_ids_Itapema.csv     | 4440   | 11      | owner_id             | 3057          | 1383       |
| Mesh_Ids_Data_Itapema.csv | 4441   | 8       | airbnb_listing_id    | 4441          | 0          |
| Price_AV_Itapema.csv      | 118839 | 4       | listing+data+captura | 1005          | -          |
| VivaReal_Itapema.csv      | 8329   | 22      | listing_id           | 8293          | 36         |

## 2. Taxa de casamento dos joins

_Contagem antes e depois de cada join, conforme exigido para nao perder linhas em silencio._


| join                         | linhas antes | linhas depois | casamento | nota                                               |
|------------------------------|--------------|---------------|-----------|----------------------------------------------------|
| Details -> Mesh (bairro/geo) | 4441         | 4441          | 100.0%    | join limpo                                         |
| Details -> Hosts (owner_id)  | 4441         | 4441          | 100.0%    | 1383 owner_id repetidos em Hosts: deduplicar antes |
| Details -> Price (preco)     | 4441         | 999           | 22.5%     | *** GARGALO: so 22% dos anuncios tem preco ***     |

## 3. Janela de observacao do Price_AV — o fato que define o metodo


| capd       | linhas | anuncios | primeira_estadia    | ultima_estadia      |
|------------|--------|----------|---------------------|---------------------|
| 2025-01-06 | 37825  | 753      | 2025-01-06 00:00:00 | 2025-04-06 00:00:00 |
| 2025-01-07 | 38991  | 773      | 2025-01-07 00:00:00 | 2025-04-07 00:00:00 |
| 2025-01-20 | 42023  | 780      | 2025-01-20 00:00:00 | 2025-04-20 00:00:00 |

- **Apenas 3 dias de captura** — e dois deles (06 e 07/01) sao consecutivos, logo existe **1 unico intervalo de comparacao util**: 07/01 -> 20/01 (13 dias).
- Cada captura enxerga uma janela **movel** de ~90 noites a frente da propria data.
- Logo a comparacao so e valida na **intersecao** das janelas: **20/01/2025 a 06/04/2025 (77 noites)**. Fora dela, uma noite 'sumir' significa apenas que saiu do horizonte da captura, nao que foi reservada.
- Estadias observadas vao de 06/01/2025 a 20/04/2025: **alta temporada + ombro**. Nao cobre o ano; anualizar por 365 sem fator sazonal produziria ficcao.

## 4. Vies de selecao: quem tem dado de preco?

Dos 4441 anuncios do Details, **999 (22.5%) tem preco**. Esse subconjunto nao e aleatorio:


| grupo     | number_of_reviews | star_rating | picture_count |
|-----------|-------------------|-------------|---------------|
| SEM preco | 1.00              | 4.50        | 8.00          |
| COM preco | 16.00             | 4.93        | 21.00         |

**O anuncio com preco tem mediana de 16 avaliacoes; o sem preco, 1.** O recorte com preco e o dos anuncios estabelecidos e ja vendendo — vies de sobrevivencia explicito.

**Cobertura por anfitriao profissional:**

| is_professional | n    | cobertura |
|-----------------|------|-----------|
| True            | 389  | 48.6%     |
| False           | 3697 | 21.6%     |

**Cobertura por anuncio novo:**

| is_new_listing | n    | cobertura |
|----------------|------|-----------|
| False          | 2836 | 13.4%     |
| True           | 731  | 2.1%      |

**Cobertura por tipologia:**

| listing_type | n    | cobertura |
|--------------|------|-----------|
| apartamento  | 3710 | 24.6%     |
| casa         | 443  | 15.8%     |
| outros       | 245  | 6.9%      |
| hotel        | 43   | 2.3%      |

**Cobertura por bairro (n>=30):**

| suburb                  | n    | cobertura |
|-------------------------|------|-----------|
| Centro                  | 657  | 31.2%     |
| Meia Praia              | 2860 | 22.1%     |
| Morretes                | 441  | 18.8%     |
| Ilhota                  | 56   | 17.9%     |
| Casa Branca             | 88   | 17.0%     |
| Tabuleiro dos Oliveiras | 129  | 15.5%     |
| Varzea                  | 43   | 11.6%     |
| Alto Sao Bento          | 62   | 8.1%      |

## 5. Mercado de compra (VivaReal)

- 8329 anuncios de venda, 36 duplicados por listing_id.
- 100% `property_type = UNIT`; `business_types`: {'Venda': np.int64(8327), 'Ambos': np.int64(2)}.
- Preco de venda ausente em 0 linhas; condominio ausente em 2490; IPTU ausente em 2714.
- Bairros com mais oferta de compra:

| suburb                  | anuncios a venda |
|-------------------------|------------------|
| Meia Praia              | 3452             |
| Morretes                | 1777             |
| Centro                  | 1009             |
| Andorinha               | 782              |
| Castelo Branco          | 510              |
| Canto da Praia          | 131              |
| Tabuleiro dos Oliveiras | 128              |
| Jardim Praia Mar        | 104              |

> Atencao: bairro do VivaReal vem **com acento** e o do Mesh **sem** (`Alto Sao Bento` vs `Alto S~ao Bento`). Normalizar antes de cruzar.

## 6. Perguntas em aberto ao fim do perfil

- A ocupacao inferida (noite some entre capturas) sobrevive a um teste contra ruido aleatorio?
- Com 77 noites de alta/ombro, qual premissa de sazonalidade usar para anualizar — e qual a sensibilidade do yield a ela?
- O recorte de ~650 anuncios com ocupacao estimavel aguenta cortes por bairro x tipologia com n>=20?
- A tese dos compactos no Centro tem oferta de compra suficiente para ser acionavel em escala?