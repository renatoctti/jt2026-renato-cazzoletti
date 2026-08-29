"""
Exporta a sessao do Claude Code para ai-log/ em dois formatos:
  - sessao-completa.jsonl : copia bruta, integral, prova de autenticidade
  - sessao-completa.md    : transcricao legivel (o que o corretor le)

Uso:  python analise/99_exportar_ai_log.py
Nao edita, nao filtra e nao seleciona trechos: exporta a sessao inteira,
conforme exigido pelo edital.
"""
import json, shutil, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SESS = Path.home() / ".claude" / "projects" / \
    "d--Users-User-Desktop-desafio-seazone-jt2026-renato-cazzoletti"
OUT = PROJ / "ai-log"
OUT.mkdir(exist_ok=True)

jsonls = sorted(SESS.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
if not jsonls:
    sys.exit(f"Nenhuma sessao encontrada em {SESS}")

MAXLEN = 3000  # truncamento apenas de SAIDA DE FERRAMENTA muito longa (dump de CSV)


def blocos(content):
    """Normaliza content (str ou lista de blocos) em uma lista de blocos."""
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return content if isinstance(content, list) else []


def render(rows):
    out = []
    for o in rows:
        t = o.get("type")
        if t not in ("user", "assistant"):
            continue
        msg = o.get("message") or {}
        if not isinstance(msg, dict):
            continue
        ts = (o.get("timestamp") or "")[:19].replace("T", " ")
        who = "USUARIO" if msg.get("role") == "user" else "CLAUDE"
        partes = []
        for b in blocos(msg.get("content")):
            bt = b.get("type")
            if bt == "text" and b.get("text", "").strip():
                partes.append(b["text"].rstrip())
            elif bt == "thinking" and b.get("thinking", "").strip():
                partes.append("> **[raciocinio interno]**\n> " +
                              b["thinking"].rstrip().replace("\n", "\n> "))
            elif bt == "tool_use":
                inp = json.dumps(b.get("input", {}), ensure_ascii=False, indent=2)
                partes.append(f"**-> ferramenta `{b.get('name')}`**\n```json\n{inp}\n```")
            elif bt == "tool_result":
                c = b.get("content")
                if isinstance(c, list):
                    c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                c = str(c or "")
                if len(c) > MAXLEN:
                    c = c[:MAXLEN] + f"\n... [saida truncada: +{len(c)-MAXLEN} caracteres]"
                partes.append(f"**<- resultado**\n```\n{c}\n```")
        if partes:
            out.append(f"\n\n### {who} · {ts}\n\n" + "\n\n".join(partes))
    return out


partes_md, total = [], 0
for jf in jsonls:
    rows = []
    for line in jf.open(encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    total += len(rows)
    shutil.copy2(jf, OUT / ("sessao-completa.jsonl" if len(jsonls) == 1
                            else f"sessao-{jf.stem[:8]}.jsonl"))
    partes_md.append(f"\n\n---\n\n## Sessao `{jf.stem}`\n"
                     f"_{len(rows)} registros brutos_\n")
    partes_md += render(rows)

header = (
    "# ai-log — transcricao completa da sessao\n\n"
    "Desafio Jovens Talentos AI Builder 2026 — Seazone · Itapema (SC)\n\n"
    "Gerado por `analise/99_exportar_ai_log.py`. **Sessao inteira, sem cortes "
    "nem curadoria.** Apenas saidas de ferramenta com mais de "
    f"{MAXLEN} caracteres (dumps de CSV) aparecem truncadas, com o numero de "
    "caracteres omitidos indicado.\n\n"
    "O `.jsonl` ao lado e a copia bruta e integral, exatamente como o Claude "
    "Code a gravou.\n"
)
(OUT / "sessao-completa.md").write_text(header + "".join(partes_md), encoding="utf-8")
print(f"OK  {len(jsonls)} sessao(oes), {total} registros -> {OUT}")
for f in sorted(OUT.iterdir()):
    print(f"    {f.name:28s} {f.stat().st_size/1024:8.1f} KB")
