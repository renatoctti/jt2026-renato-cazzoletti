"""Utilitarios compartilhados. Zero dependencias alem de pandas/numpy —
o repositorio precisa rodar em maquina limpa."""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "data"
SAIDAS = RAIZ / "saidas"

# Janela de comparacao valida = intersecao dos horizontes das capturas.
# Ver saidas/00_perfil.md secao 3.
JANELA_INI = pd.Timestamp("2025-01-20")
JANELA_FIM = pd.Timestamp("2025-04-06")
JANELA_N = (JANELA_FIM - JANELA_INI).days + 1  # 77 noites


def md_table(df, floats="{:,.2f}"):
    """DataFrame -> tabela markdown, sem depender de `tabulate`.

    Regra de indice: um indice INTEIRO e sem nome nao carrega informacao (e o
    residuo de um sort ou de um filtro) e por isso e descartado. Ja um indice
    nomeado, um MultiIndex ou um indice de rotulos de texto (os nomes das
    estatisticas de `describe()`, por exemplo) sao dados e viram coluna.
    """
    df = df.copy()
    lixo = (df.index.name is None
            and not isinstance(df.index, pd.MultiIndex)
            and pd.api.types.is_integer_dtype(df.index))
    if lixo:
        df = df.reset_index(drop=True)
    else:
        df = df.reset_index()
    def fmt(x):
        if isinstance(x, float):
            return floats.format(x)
        return "" if x is None else str(x)
    cols = [str(c) for c in df.columns]
    linhas = [[fmt(x) for x in row] for row in df.itertuples(index=False)]
    larg = [max(len(cols[i]), *(len(l[i]) for l in linhas)) if linhas else len(cols[i])
            for i in range(len(cols))]
    def linha(vals):
        return "| " + " | ".join(v.ljust(larg[i]) for i, v in enumerate(vals)) + " |"
    return "\n".join([linha(cols), "|" + "|".join("-" * (w + 2) for w in larg) + "|",
                      *(linha(l) for l in linhas)])


def carregar():
    """Carrega os 5 arquivos com os tipos ja tratados.

    VivaReal_Itapema.csv esta em **latin-1**, nao em UTF-8. Lido com o default
    do pandas, todo bairro acentuado vira caractere de substituicao
    ('Alto S?o Bento') e deixa de casar com o bairro do Mesh.
    """
    d = pd.read_csv(DADOS / "Details_Itapema.csv", low_memory=False)
    h = pd.read_csv(DADOS / "Hosts_ids_Itapema.csv")
    m = pd.read_csv(DADOS / "Mesh_Ids_Data_Itapema.csv")
    pr = pd.read_csv(DADOS / "Price_AV_Itapema.csv")
    v = pd.read_csv(DADOS / "VivaReal_Itapema.csv", low_memory=False,
                    encoding="latin-1")
    pr["date"] = pd.to_datetime(pr["date"])
    pr["captura"] = pd.to_datetime(pr["aquisition_date"]).dt.normalize()
    return d, h, m, pr, v


def normalizar_bairro(s):
    """Mesh traz o bairro sem acento; VivaReal com acento e as vezes em caixa
    alta ('CENTRO'). Remove acento e padroniza caixa nos DOIS lados para
    permitir o cruzamento. Preposicoes ficam minusculas para 'Canto Da Praia'
    casar com 'Canto da Praia'."""
    import unicodedata
    peq = {"da", "de", "do", "das", "dos", "e"}

    def n(x):
        if not isinstance(x, str):
            return None
        x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode()
        p = [w.lower() for w in x.split()]
        return " ".join(w if i and w in peq else w.capitalize()
                        for i, w in enumerate(p)) or None
    return s.map(n)
