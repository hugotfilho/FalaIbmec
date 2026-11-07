def responder_rag(
    pergunta,
    trechos,
    embeddings,
    modelo_busca,
    modelo_llm,
    tokenizador_llm,
    k=3,
):
    import re
    import numpy as np
    import torch

    if not pergunta.strip():
        raise ValueError("Digite uma pergunta.")

    assert 1 <= k <= len(trechos)

    vetor = modelo_busca.encode(
        pergunta,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    pontuacoes = embeddings @ vetor
    indices = np.argsort(-pontuacoes)[:k]

    encontrados = [
        {
            **trechos[int(indice)],
            "similaridade": float(pontuacoes[indice]),
        }
        for indice in indices
    ]

    blocos = []

    for numero, trecho in enumerate(encontrados, start=1):
        metadados = [
            f"[{numero}] Arquivo: {trecho['arquivo']}",
            f"Trecho: {trecho['id_trecho']}",
        ]

        for campo, descricao in {
            "pagina": "Página",
            "mes": "Mês",
            "abrangencia_documentada": "Abrangência",
            "periodo_documentado": "Período",
            "limites_uso": "Limitações",
        }.items():
            if trecho.get(campo):
                metadados.append(f"{descricao}: {trecho[campo]}")

        blocos.append(
            "\n".join(metadados)
            + "\nConteúdo:\n"
            + trecho["texto_trecho"]
        )

    prompt = """
Responda à PERGUNTA em português brasileiro, de forma natural e breve,
usando exclusivamente as informações dos DOCUMENTOS.

Preserve os nomes dos menus e procedimentos.
Não invente etapas, documentos exigidos, botões ou explicações de siglas.
Respeite as limitações de abrangência e vigência das fontes.

Não escreva URLs nem marcadores de referência.
O sistema exibirá separadamente os documentos consultados.

Se os documentos não contiverem informação para responder, diga:
"Não encontrei informação suficiente nos documentos consultados."
""".strip()

    contexto = "\n\n".join(blocos)

    mensagens = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": f"DOCUMENTOS:\n{contexto}\n\nPERGUNTA:\n{pergunta}",
        },
    ]

    entradas = tokenizador_llm.apply_chat_template(
        mensagens,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    ).to(modelo_llm.get_input_embeddings().weight.device)

    tamanho_entrada = entradas["input_ids"].shape[1]

    assert (
        tamanho_entrada + 384
        <= modelo_llm.config.max_position_embeddings
    ), "A entrada excede o contexto disponível."

    with torch.inference_mode():
        saida = modelo_llm.generate(
            **entradas,
            max_new_tokens=384,
            do_sample=False,
            pad_token_id=tokenizador_llm.eos_token_id,
        )

    resposta = tokenizador_llm.decode(
        saida[0, tamanho_entrada:],
        skip_special_tokens=True,
    ).strip()

    conteudo = re.sub(r"\[[\d,\s]+\]", "", resposta)
    tem_conteudo = bool(re.search(r"[A-Za-zÀ-ÿ]", conteudo))

    return {
        "pergunta": pergunta,
        "resposta": (
            resposta if tem_conteudo
            else "Não consegui gerar uma resposta válida."
        ),
        "saida_original": resposta,
        "fontes_consultadas": encontrados,
        "modo": "gerada" if tem_conteudo else "revisar",
    }


def responder_rag_focado(
    pergunta,
    trechos,
    embeddings,
    modelo_busca,
    modelo_llm,
    tokenizador_llm,
    k=3,
):
    import numpy as np

    if not pergunta.strip():
        raise ValueError("Digite uma pergunta.")

    assert 1 <= k <= len(trechos)

    vetor = modelo_busca.encode(
        pergunta,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    pontuacoes = embeddings @ vetor
    candidatos = np.argsort(-pontuacoes)[:k]

    registro_principal = trechos[
        int(candidatos[0])
    ]["id_registro"]

    selecionados = [
        int(indice)
        for indice in candidatos
        if trechos[int(indice)]["id_registro"] == registro_principal
    ]

    resultado = responder_rag(
        pergunta,
        [trechos[indice] for indice in selecionados],
        embeddings[selecionados],
        modelo_busca,
        modelo_llm,
        tokenizador_llm,
        k=len(selecionados),
    )

    resultado["politica_contexto"] = "mesmo_registro_do_primeiro_resultado"
    resultado["candidatos_recuperados"] = [
        {
            "id_trecho": trechos[int(indice)]["id_trecho"],
            "similaridade": float(pontuacoes[indice]),
        }
        for indice in candidatos
    ]

    return resultado
