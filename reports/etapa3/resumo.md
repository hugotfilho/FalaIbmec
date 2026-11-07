# Entrega 3: integração do RAG e interface

Exportação da sessão do Colab em 7 de novembro de 2026. Este resumo registra o que foi observado no desenvolvimento, sem atribuir uma acurácia geral ao protótipo.

## Implementação

- Recuperação com `PORTULAN/serafim-100m-portuguese-pt-sentence-encoder-ir` e vetores normalizados de 768 dimensões.
- Geração com `Qwen/Qwen2.5-7B-Instruct`, quantizado em NF4 de 4 bits, double quant e cálculo em float16, executado em GPU no Colab.
- Base ampliada para 280 trechos. Recuperamos somente a explicação e a fórmula da média final do Guia do Aluno Faria Lima, página 4. As orientações conflitantes sobre AS permanecem excluídas.
- Busca inicial dos três candidatos mais similares e seleção dos candidatos pertencentes ao mesmo registro de origem do primeiro colocado.
- Interface Gradio com resposta e área expansível de fontes consultadas, incluindo arquivo, página quando existente, link e trecho.
- Módulos exportados em `src/rag.py` e `src/fontes.py`. Dados e modelos são passados explicitamente às funções.

## Evidências registradas

A sessão exportada contém nove interações da interface, três testes do contexto focado e uma comparação entre contexto amplo e reduzido. São exemplos conhecidos durante os ajustes, não uma avaliação independente.

| Pergunta do teste focado | Resultado observado | Trechos enviados |
| --- | --- | --- |
| Como é calculada a nota final? | Fórmula de 40% AP1, 40% AP2 e 20% AC, coerente com o fragmento recuperado. | `r090_t001` |
| Como solicitar a carteirinha de estudante? | Procedimento com caminho do SIA, foto JPG e aviso de retirada, coerente com os trechos revisados. | `r085_t007`, `r085_t008` |
| Qual é a capital da França? | Resposta de informação insuficiente nos documentos consultados. | `r043_t001` |

Antes da seleção de contexto, a pergunta sobre nota final recebeu uma recusa mesmo com a fórmula em primeiro lugar na recuperação. O contexto incluía também dois trechos sobre CR. Com somente o registro da fórmula, a resposta apresentou o cálculo. Esse caso motivou a política de contexto focado; não demonstra que essa política seja superior para todos os tipos de pergunta.

## Casos pendentes e limitações

- “Como eu tranco uma matéria?” recebeu uma recusa com um trecho sobre matrícula/reabertura. A variante “Como excluo uma disciplina?” recuperou orientações sobre exclusão no RENOVA/requerimento. Falta avaliar sistematicamente essas diferenças de vocabulário e a sustentação das respostas, respeitando a unidade e o período.
- “Como eu consulto minhas horas AAC?” recebeu uma regra sobre aproveitamento de horas de estágio, sem responder diretamente à consulta das horas já registradas. Esse caso exige revisão de recuperação e geração.
- “Fontes consultadas” são os documentos enviados ao modelo, não citações verificadas automaticamente por afirmação.
- As fontes podem ter limitações de edição, abrangência e vigência; a recuperação parcial não confirma a vigência atual da fórmula para qualquer disciplina.
- O histórico fica visível na interface, mas cada pergunta é processada de forma independente.
- O foco no registro do primeiro resultado pode descartar complementos relevantes de outras páginas ou documentos.
- Não registramos uma revisão imutável dos pesos do Qwen na exportação; a configuração informa as versões das bibliotecas observadas.
- Ainda falta uma avaliação com perguntas independentes dos exemplos usados nos ajustes.

## Conferência local do pacote

Foram conferidos o ZIP e as dez assinaturas do manifesto; os 280 IDs e suas posições no índice; as assinaturas dos textos; a matriz `(280, 768)`, seus valores finitos e a normalização dos vetores; a identidade do pacote de base aninhado; e a compilação dos módulos Python. A inferência da LLM não foi repetida no Mac.

O registro integral `fechamento.json` e os pacotes com os textos processados permanecem locais, ignorados pelo Git. Os notebooks foram sincronizados a partir do Colab. O original do 05 terminava no modelo 3B e não continha o fluxo final; ele foi preservado no backup. A cópia de execução do 05 foi reorganizada com base v3, Qwen 7B e comparação de contexto em cinco exemplos conhecidos. Os resultados dessa nova execução ainda não foram gerados. O 06 também foi reorganizado, sem saídas inventadas; os originais do Colab e as cópias locais anteriores estão nos backups. As funções da cópia organizada correspondem às exportadas. A validação de formato, sintaxe e ordem não substitui uma nova execução integral com GPU no Colab. A exportação do 05 foi adicionalmente exercitada em uma pasta temporária com um registro de teste e sem LLM: os arquivos JSON e ZIP foram conferidos e duas execuções criaram destinos diferentes, sem sobrescrever os anteriores.
