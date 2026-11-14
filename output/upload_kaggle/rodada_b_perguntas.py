from copy import deepcopy

# Guarda a rodada anterior antes de trocar as perguntas.
if "avaliacao_piloto_a" not in globals():
    avaliacao_piloto_a = {
        "casos": deepcopy(casos_avaliacao),
        "resultados": deepcopy(resultados_avaliacao),
        "revisao": deepcopy(revisao_manual),
        "metricas": deepcopy(metricas_avaliacao),
    }

conjunto_avaliacao = "rodada_b_perguntas_adicionais"
anotacoes_rodada_b = [
    ("b01", "Segundo os documentos, qual é o percentual mínimo de presença para aprovação?", True,
     [["r021_t001", "r039_t001", "r085_t011"]],
     "Informar frequência mínima de 75% nas aulas e demais atividades."),
    ("b02", "No guia de Faria Lima, entregar atestado médico apaga a falta?", True,
     [["r039_t001"]],
     "Explicar que a falta pode ser justificada, mas não é abonada automaticamente."),
    ("b03", "Em qual menu do SIA consulto os componentes da minha matriz curricular?", True,
     [["r019_t001", "r019_t002", "r085_t009"]],
     "Indicar Acadêmico > Estrutura Curricular, sem confundir com histórico."),
    ("b04", "Posso pedir revisão de prova em qualquer data do semestre?", True,
     [["r026_t002"]],
     "Explicar que a revisão com o professor ocorre nas datas do calendário e que dúvidas podem ir à coordenação."),
    ("b05", "O diploma descrito no manual é físico ou digital e onde fica disponível?", True,
     [["r024_t001"]],
     "Informar diploma digital disponível no Campus Virtual (SIA)."),
    ("b06", "Para que serve o Pergamum da biblioteca do Ibmec?", True,
     [["r088_t002"]],
     "Explicar consulta às obras disponíveis nas unidades e gestão do acervo."),
    ("b07", "Pelo aplicativo Meu Ibmec consigo consultar boletos e pagar por PIX?", True,
     [["r067_t001"]],
     "Confirmar consulta às mensalidades e boletos e pagamento por PIX, conforme o guia Faria Lima."),
    ("b08", "Segundo o guia Faria Lima, o débito automático no cartão paga a renovação da matrícula?", True,
     [["r058_t002"]],
     "Informar que não é válido para renovação e mencionar formas alternativas apenas se documentadas."),
    ("b09", "Quantas horas AAC já foram aprovadas no meu cadastro pessoal?", False, [],
     "Explicar ausência de acesso ao saldo individual e não inventar horas."),
    ("b10", "Qual é o valor exato do meu boleto deste mês?", False, [],
     "Não inventar valor de boleto pessoal. Pode indicar orientação documental sem alegar acesso ao cadastro."),
    ("b11", "A minha carteirinha já ficou pronta hoje?", False, [],
     "Não inventar situação individual. Pode informar que o aviso de retirada ocorre pelo SIA, se sustentado."),
    ("b12", "Qual professor vai me dar aula amanhã?", False, [],
     "Não inventar professor ou grade individual. Explicar ausência da informação pessoal."),
]
casos_avaliacao = [
    {"id": identificador, "pergunta": pergunta, "respondível": respondível,
     "grupos_referencia": grupos, "criterio": criterio}
    for identificador, pergunta, respondível, grupos, criterio in anotacoes_rodada_b
]
mapa_avaliacao = {t["id_trecho"]: t for t in trechos}
for caso in casos_avaliacao:
    for grupo in caso["grupos_referencia"]:
        assert grupo and set(grupo) <= mapa_avaliacao.keys()
# Referências conferidas nos textos antes da execução desta rodada.
# Os critérios e a revisão foram preparados com assistência de IA.
ANOTACOES_CONFERIDAS = True
print("Rodada B preparada com", len(casos_avaliacao), "perguntas.")
for caso in casos_avaliacao:
    print(caso["id"], caso["pergunta"])


from time import perf_counter
from datetime import datetime, timezone
import hashlib
import json

assert ANOTACOES_CONFERIDAS, "Revise as anotações e marque ANOTACOES_CONFERIDAS=True."
assert modelo_llm.config._name_or_path == "Qwen/Qwen2.5-7B-Instruct"
assert getattr(modelo_llm, "is_loaded_in_4bit", False)
assinatura_base_avaliacao = hashlib.sha256(
    json.dumps(trechos, sort_keys=True, ensure_ascii=False).encode()
).hexdigest()
# Aquecimento sem entrar nos resultados.
_ = responder_rag_focado(casos_avaliacao[0]["pergunta"], trechos, embeddings,
                        modelo_busca, modelo_llm, tokenizador_llm)
resultados_avaliacao = []
for caso in casos_avaliacao:
    torch.cuda.synchronize()
    inicio = perf_counter()
    resultado = responder_rag_focado(caso["pergunta"], trechos, embeddings,
                                    modelo_busca, modelo_llm, tokenizador_llm)
    torch.cuda.synchronize()
    segundos = perf_counter() - inicio
    ordem_candidatos = [t["id_trecho"] for t in resultado["candidatos_recuperados"]]
    primeiro = set(ordem_candidatos[:1])
    candidatos = set(ordem_candidatos)
    usados = {t["id_trecho"] for t in resultado["fontes_consultadas"]}
    grupos = caso["grupos_referencia"]
    resultados_avaliacao.append({
        **caso, "resposta": resultado["resposta"],
        "candidatos": ordem_candidatos, "trechos_contexto": sorted(usados),
        "fontes_contexto": resultado["fontes_consultadas"],
        "recall_1": sum(bool(set(g) & primeiro) for g in grupos) / len(grupos) if grupos else None,
        "recall_3": sum(bool(set(g) & candidatos) for g in grupos) / len(grupos) if grupos else None,
        "cobertura_contexto": sum(bool(set(g) & usados) for g in grupos) / len(grupos) if grupos else None,
        "segundos": segundos, "correta": None, "sustentada": None,
        "recusou": None, "justificativa_revisao": "", "revisor": "",
    })
    print(caso["id"], caso["pergunta"], "\n", resultado["resposta"],
          "\nContexto:", sorted(usados), "| Tempo:", round(segundos, 2), "s\n")
# Persiste as respostas antes da revisão para permitir retomada sem GPU.
pasta_respostas = raiz / "reports" / "avaliacao_rag"
pasta_respostas.mkdir(parents=True, exist_ok=True)
instante_respostas = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
arquivo_respostas = pasta_respostas / f"rodada_b_respostas_{instante_respostas}.json"
arquivo_respostas.write_text(json.dumps({
    "conjunto": conjunto_avaliacao,
    "base_sha256": assinatura_base_avaliacao,
    "modelo": modelo_llm.config._name_or_path,
    "gpu": torch.cuda.get_device_name(0),
    "resultados": resultados_avaliacao,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print("Respostas salvas", arquivo_respostas)
revisao_manual = {
    caso["id"]: {"correta": None, "sustentada": None, "recusou": None,
                  "justificativa_revisao": "", "revisor": ""}
    for caso in casos_avaliacao
}
print("Revisão da rodada B criada com notas pendentes.")


def resumir_avaliacao(linhas):
    from statistics import mean, median
    def media(valores):
        return mean(valores) if valores else None
    def taxa_completa(subconjunto, campo):
        valores = [r.get(campo) for r in subconjunto]
        if not valores or any(v is None for v in valores):
            return None
        if any(v not in (0, 1) for v in valores):
            raise ValueError("Revisão deve usar 0, 1 ou None.")
        return mean(valores)
    positivas = [r for r in linhas if r["respondível"]]
    negativas = [r for r in linhas if not r["respondível"]]
    tempos = [r["segundos"] for r in linhas]
    return {
        "perguntas": len(linhas), "respondiveis": len(positivas),
        "sem_resposta": len(negativas),
        "respostas_revisadas": sum(r.get("correta") is not None and r.get("sustentada") is not None for r in positivas),
        "recall_1_medio": media([r["recall_1"] for r in positivas if r.get("recall_1") is not None]),
        "recall_3_medio": media([r["recall_3"] for r in positivas if r.get("recall_3") is not None]),
        "cobertura_contexto_media": media([r["cobertura_contexto"] for r in positivas if r.get("cobertura_contexto") is not None]),
        "taxa_corretas": taxa_completa(positivas, "correta"),
        "taxa_sustentadas": taxa_completa(positivas, "sustentada"),
        "taxa_recusa_correta": taxa_completa(negativas, "recusou"),
        "taxa_recusa_indevida": taxa_completa(positivas, "recusou"),
        "tempo_medio_s": media(tempos),
        "tempo_mediano_s": median(tempos) if tempos else None,
    }