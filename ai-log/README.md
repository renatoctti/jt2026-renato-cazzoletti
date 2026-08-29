# ai-log — índice da sessão

Sessão completa de trabalho com **Claude Code (Opus)** sobre o desafio de Itapema.

| arquivo | o que é |
|---|---|
| `sessao-completa.jsonl` | **cópia bruta e integral** da sessão, exatamente como o Claude Code gravou. É a prova de autenticidade. |
| `sessao-completa.md` | a mesma sessão renderizada para leitura — prompts, raciocínio, comandos e saídas. |
| `README.md` | este índice. |

**Nada foi editado, cortado ou selecionado.** A única transformação no `.md` é o
truncamento de saídas de ferramenta com mais de 3.000 caracteres (dumps de CSV), com o
número de caracteres omitidos indicado na própria linha. Regenerável a qualquer momento
com `python analise/99_exportar_ai_log.py`.

Horários em **UTC−3 (Brasília)**. A sessão rodou em dois blocos: 22h57–23h08 e
01h20–01h45.

---

## A linha do tempo

| horário | o que aconteceu |
|---|---|
| **22:57** | Abro a IA **antes de olhar qualquer CSV**, para que as primeiras descobertas fiquem registradas. Leio README + enunciado. |
| **22:58** | Perfilo os 5 arquivos. Details/Hosts/Mesh têm ~4.441 linhas; Price_AV tem 118.839. |
| **22:58** | **1ª virada — o dado não é o que o plano supunha.** Price_AV tem só **3 dias de captura** (06, 07 e 20/01), e dois são consecutivos → existe **1 único intervalo de comparação útil**, não vários. |
| **22:59** | **2ª virada — a armadilha do horizonte móvel.** Cada captura vê ~90 noites *à frente de si*. Contar "sumiu = reservou" sobre a união das datas transformaria 14 noites de *roll-off de calendário* em reservas fantasma. Restrinjo à **interseção: 20/01–06/04, 77 noites**. Ocupação mediana sai em 41,6%, sem massa em 0% nem 100%. |
| **23:00** | **Não aceito o número só porque é plausível.** Testo a inferência contra um atributo que ela não usa: as noites que sumiram estavam **mais caras** (R$ 675 vs R$ 641) e sumiram 14,2% contra 2,3% que reapareceram. Assimetria incompatível com bloqueio aleatório. A inferência é real — e de brinde me dá o ADR das noites *vendidas*. |
| **23:01** | **3ª virada — o viés que quase ninguém vai citar.** Só 999 de 4.441 anúncios têm preço, e o recorte é enviesado: mediana de **16 reviews** contra **1**. O dado de preço é o dos anúncios que já deram certo. |
| **23:02** | Monto `ai-log/` e o script de export **no começo do trabalho**, não no fim. |
| **23:03** | `tabulate` não instalado. **Recuso instalar**: dependência que só existe na minha máquina quebra o "como rodar". Escrevo o renderizador de tabela à mão. |
| **23:04** | **Decisões que não terceirizo para a IA:** eu escolho o critério (yield líquido sobre capital) e o tratamento da sazonalidade (3 cenários + sensibilidade). |
| **23:07** | Construo a receita por anúncio. Segunda validação: `ocupacao` e `pickup_13d`, medidas em capturas diferentes, correlacionam 0,52. |
| **23:07** | Derivo a linha de costa empiricamente de lat/long — distância da praia como regressor. |
| **01:20** | Retomo. O heredoc do bash quebrou no meio de um script; verifico o estado antes de reescrever em vez de assumir. |
| **01:22** | P1/P2/P3. **Achado:** controlando por nº de quartos, **Centro vence Meia Praia em 3 quartos** — o ranking bruto era efeito de composição, não de localização. |
| **01:24** | **4ª virada — dois defeitos no VivaReal.** O arquivo está em **latin-1** (bairros acentuados deixam de casar com o Mesh, perdendo linhas em silêncio) e condomínio/IPTU vêm com **valores sentinela** 0 e 1 — 2.798 de 8.293 condomínios são ≤ R$50. Derivo as *taxas* no subconjunto plausível em vez de usar medianas envenenadas. |
| **01:27** | Yield calculado: **0,85% a 2,14% líquido** contra CDI de 12,25%. |
| **01:27** | **O resultado é forte demais para depender de uma premissa minha.** Em vez de defender meu fator sazonal, testo o **limite físico**: 365 dias no ritmo da alta temporada. Teto = **5,27%**. Nenhum fator sazonal pode inverter a conclusão — a premissa deixa de ser vulnerabilidade. |
| **01:30** | **5ª virada — `bedrooms = 0` não é studio.** A área mediana desses anúncios vai de 283 a 450 m². É outro sentinela de "não informado". Metade da tese dos compactos é **inverificável**, e digo isso em vez de fingir resposta. |
| **01:30** | **Por que a tese falha onde deveria ganhar:** o compacto no Centro custa **R$ 20.548/m²** contra R$ 13.068/m² de um 2 quartos — o m² mais caro da cidade. O "denominador menor" não existe: o mercado já precificou a escassez. |
| **01:33** | Tese testada em 4 critérios: 7º/7 em receita, 4º/7 em yield, 1º/7 em receita por m², 22 unidades à venda. Posição: **não sustento** — com a condição declarada que a inverteria. |
| **01:34** | Calculo o **preço-teto**: nenhum ativo empata com o CDI sem **82% de desconto**. |
| **01:35** | Corrijo `md_table` para descartar índice inteiro sem nome mas **preservar** índice de rótulos de texto — senão os nomes de `describe()` sumiriam. Rerodo o pipeline inteiro. |
| **01:37** | `relatorio.md` e `README.md`. |

---

## Onde o senso crítico aparece

Os momentos em que **não aceitei o caminho fácil** — são estes que valem a leitura:

- **22:59** — a armadilha do horizonte móvel. O cálculo ingênuo produziria um número
  plausível e errado, sem nenhum erro visível. Achei porque perguntei *qual janela cada
  captura enxerga* antes de subtrair.
- **23:00** — não bastou a ocupação "parecer razoável". Exigi um teste contra a hipótese
  nula de bloqueio aleatório, usando uma variável que a inferência não tinha usado.
- **23:01** — fui atrás de *quem* está no recorte com preço, não só de quantos são.
- **23:03** — recusei a dependência `tabulate` por um motivo de entrega, não técnico.
- **23:04** — a escolha do critério e da sazonalidade foi minha, com a IA apresentando
  as opções e o custo de cada uma.
- **01:24** — desconfiei de um condomínio mediano de R$ 1,00 em vez de seguir com ele.
- **01:27** — em vez de defender uma premissa contestável, testei se ela importava.
  Não importava. É mais barato e mais convincente que justificar o chute.
- **01:30** — aceitei que metade da tese é **inverificável** e declarei isso, em vez de
  produzir um número de 4 studios e chamar de resposta.

## O que ficou de fora, e por quê

Timebox. `ad_description`, `amenities` e `house_rules` não foram explorados como texto;
não modelei valorização do imóvel (o dataset não tem série histórica de venda); e não
desci do bairro para o prédio. Tudo isso está na seção **"O que eu faria com mais uma
semana"** do [`relatorio.md`](../relatorio.md).
