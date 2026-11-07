from html import escape
from urllib.parse import urlparse

def formatar_fontes(fontes):
    blocos = []

    for numero, fonte in enumerate(fontes, start=1):
        titulo = fonte.get("titulo") or fonte["arquivo"]

        detalhes = [
            f"<h3>{numero}. {escape(titulo)}</h3>",
            f"<p>Arquivo: {escape(fonte['arquivo'])}</p>",
        ]

        if fonte.get("pagina"):
            detalhes.append(
                f"<p>Página: {escape(str(fonte['pagina']))}</p>"
            )

        if fonte.get("periodo_documentado"):
            detalhes.append(
                f"<p>Período: {escape(fonte['periodo_documentado'])}</p>"
            )

        url = (
            fonte.get("url_documento")
            or fonte.get("url_referencia")
            or fonte.get("url")
        )

        if url and urlparse(url).scheme in {"http", "https"}:
            detalhes.append(
                f'<p><a href="{escape(url, quote=True)}" '
                'target="_blank" rel="noopener noreferrer">'
                "Abrir fonte</a></p>"
            )

        detalhes.append(
            '<blockquote style="white-space: pre-wrap;">'
            + escape(fonte["texto_trecho"])
            + "</blockquote>"
        )

        blocos.append("\n".join(detalhes))

    return "\n<hr>\n".join(blocos)
