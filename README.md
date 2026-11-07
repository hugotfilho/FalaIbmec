# Chatbot FAQ do Ibmec | Projeto de PLN

Projeto de um assistente para responder a dúvidas acadêmicas de alunos de graduação do Ibmec Faria Lima, consultando documentos institucionais e indicando as fontes utilizadas.

**Curso:** Ciência de Dados e Inteligência Artificial  
**Integrantes:** Caio Jardim e Hugo Toledo  
**Unidade:** Ibmec Faria Lima, São Paulo

## Estado atual

Implementamos a extração e curadoria, o NER por regras com filtros de contexto, a busca semântica com Transformer e um protótipo de RAG com interface Gradio, executado no Colab.

A versão usada na interface contém **280 trechos**, embeddings de **768 dimensões** com Serafim e geração com **Qwen2.5-7B-Instruct em 4 bits**. As fontes consultadas são mostradas com documento, página quando houver, link e trecho. O histórico visual ainda não é usado para interpretar a pergunta seguinte.

Os resultados são pilotos de desenvolvimento. Há casos pendentes sobre exclusão de disciplina e consulta de horas AAC; consulte o [fechamento da etapa 3](reports/etapa3/resumo.md). Os notebooks 05 e 06 foram organizados como cópias de execução, sem saídas inventadas; os originais do Colab estão preservados em um ZIP local. O 05 integra e compara as políticas de contexto, e o 06 apresenta a interface. A organização passou em validação estrutural, mas ainda deve ser executada integralmente em uma sessão nova do Colab.

A entrega inicial reuniu a [proposta do projeto](reports/proposta.md) e o [experimento de NER](notebooks/03_ner.ipynb), conforme a adaptação de escopo autorizada pelo professor.

## Objetivo e escopo

Facilitar a consulta a orientações sobre matrícula, acesso aos sistemas, biblioteca, estágio e outros assuntos cobertos pelas fontes selecionadas. O protótipo deverá apresentar referências e informar quando os documentos não forem suficientes para responder.

O projeto não é um canal oficial de atendimento do Ibmec e não acessará notas, pagamentos ou dados pessoais nos sistemas internos.

## Preparação dos dados

A coleta inicial reuniu quatro PDFs e 14 arquivos HTML institucionais. A extração produziu 130 registros, organizados por página de PDF, região mensal do calendário ou arquivo HTML.

A versão 3 do corpus contém **89 registros de nove fontes**, com **41 exclusões documentadas**. Todos os registros originais foram contabilizados. A curadoria incluiu:

- Retirada de capas, divisórias, sumários e determinados conteúdos redundantes.
- Separação de conteúdos com divergências, prazos específicos e informações cuja atualidade não foi confirmada.
- Registro de títulos, referências, abrangência e limitações das fontes.
- Normalização de espaços em uma coluna separada, preservando os textos originais.

Na preparação para o RAG, geramos inicialmente 279 trechos desses registros, respeitando palavras completas e o limite de tokens do Serafim. Depois recuperamos somente a explicação e a fórmula da média final do Guia do Aluno Faria Lima, página 4, elevando a base de trechos v3 para **280**. Essa página havia sido excluída integralmente por divergência nas orientações sobre AS; o trecho conflitante permanece fora da busca. O corpus v3 original e seus registros de exclusão foram preservados, com a recuperação parcial documentada separadamente.

A curadoria não confirma a vigência de todas as regras acadêmicas. As limitações de edição, período e unidade permanecem documentadas para orientar o uso dos dados.

Os materiais originais e os textos processados são mantidos localmente e ignorados pelo Git. A reprodução das etapas de extração e curadoria exige esses arquivos.

## Notebooks

| Notebook | Conteúdo |
| --- | --- |
| [01_extracao_textos.ipynb](notebooks/01_extracao_textos.ipynb) | Extração e inspeção de textos de PDFs e HTMLs. |
| [02_revisao_corpus.ipynb](notebooks/02_revisao_corpus.ipynb) | Revisão das fontes, exclusões, sobreposições e consolidação do corpus. |
| [03_ner.ipynb](notebooks/03_ner.ipynb) | Observação do modelo pré-treinado, regras, filtros de contexto, avaliação e reprodução. |
| [04_preparacao_trechos.ipynb](notebooks/04_preparacao_trechos.ipynb) | Divisão em trechos, embeddings com Serafim, busca semântica e piloto de recuperação. |
| [05_integracao_rag.ipynb](notebooks/05_integracao_rag.ipynb) | Integração e comparação de contexto amplo e focado, com base v3 e Qwen 7B em 4 bits. O original de desenvolvimento está preservado no backup. |
| [06_interface_chatbot.ipynb](notebooks/06_interface_chatbot.ipynb) | Cópia organizada para carregar a base e modelos e abrir a interface. Os diagnósticos históricos permanecem no original preservado. |

## Experimento básico de NER

Primeiro observamos o comportamento do modelo em português `pt_core_news_sm`. Em seguida, criamos um pipeline separado com `spacy.blank("pt")` e `EntityRuler`, usando 12 padrões e comparação sem distinção entre maiúsculas e minúsculas.

| Categoria do projeto | Exemplos |
| --- | --- |
| `INSTITUICAO` | Ibmec |
| `UNIDADE` | Faria Lima |
| `SERVICO_ACADEMICO` | matrícula, estágio, carteirinha e variantes previstas nas regras |

A categoria `SERVICO_ACADEMICO` representa termos do domínio acadêmico definidos pelo projeto. O grupo não treinou um modelo estatístico de NER.

### Resultados do piloto

A abordagem avaliada foi o **EntityRuler**, em oito frases sintéticas, com correspondência exata da posição dos caracteres e do rótulo da entidade.

| Métrica global (micro) | Resultado |
| --- | ---: |
| Verdadeiros positivos | 9 |
| Falsos positivos | 2 |
| Falsos negativos | 0 |
| Precisão | 81,82% |
| Revocação | 100,00% |
| F1 | 90,00% |

Os dois falsos positivos ocorreram em “O sistema matricula os alunos automaticamente” e “Eu estagio em uma empresa parceira”. As regras reconheceram formas verbais como serviços acadêmicos, mostrando uma limitação da correspondência literal.

Os exemplos foram elaborados com conhecimento das regras e apoio de IA. Esse piloto não constitui uma avaliação independente nem permite concluir o desempenho em perguntas reais. A revisão humana das anotações ainda não foi registrada.

Os [arquivos do experimento](reports/ner_basico_v1/) incluem padrões, casos, entidades de referência e previstas, métricas e configuração. As previsões salvas foram reproduzidas nos oito casos. Foram utilizados spaCy **3.8.16** e modelo **3.8.0**.

### Evolução do NER

Acrescentamos um filtro para as formas ambíguas `matricula` e `estagio`, usando a análise gramatical do spaCy e o pronome `eu` imediatamente anterior. Nos mesmos oito casos sintéticos de comparação, a v1 apresentou VP=9, FP=2, FN=0 e F1=90,00%; a v2 apresentou VP=9, FP=1, FN=0 e F1=94,74%. O erro restante ocorreu em “Eu também estagio em uma empresa”. Os [resultados da comparação](reports/ner_contexto_v2/comparacao.csv) permanecem separados dos do piloto inicial. Esses testes não estimam desempenho geral.

## Execução dos experimentos

Abra os notebooks no Jupyter ou no VS Code e execute as células na ordem. Os notebooks 01 e 02 dependem dos materiais locais em `data/raw/` e dos arquivos gerados em `data/processed/`.

Para o experimento de NER, instale as dependências no ambiente Python utilizado pelo kernel:

```bash
python -m pip install spacy==3.8.16 jupyter ipykernel
python -m spacy download pt_core_news_sm-3.8.0 --direct
```

O notebook 03 usa exemplos sintéticos e não depende do corpus local. A célula de exportação protege os resultados existentes e interrompe a gravação quando os CSVs já estão presentes. Para conferir os resultados versionados, utilize a célula final de reprodução; para gerar uma nova exportação, escolha outra pasta de resultados.

### RAG e interface no Colab

O ambiente observado está registrado em [requirements-colab.txt](requirements-colab.txt). O PyTorch com CUDA é fornecido pelo Colab; a versão usada consta no registro local da sessão. A execução do Qwen quantizado foi realizada em GPU NVIDIA T4; não foi verificada no Mac.

1. Abra no Colab a versão atualizada do notebook 06 e selecione GPU T4, quando disponível.
2. Use o pacote local `base_rag_v3.zip` na célula de upload e extraia seus quatro arquivos para `/content/projeto-pln`.
3. Execute as células de instalação, validação da base e carregamento do Serafim e do Qwen 7B em 4 bits.
4. Execute as funções e a interface Gradio. O link de compartilhamento é temporário e depende da sessão ativa.
5. Baixe os arquivos gerados e os notebooks antes de encerrar a sessão. Arquivos em `/content` não são persistentes.

O notebook 05 organizado usa a base v3 e o Qwen 7B em 4 bits para comparar as duas políticas de contexto em cinco exemplos de desenvolvimento. A exportação cria uma pasta nova por execução e mantém a revisão humana como pendente. As tentativas com 1.5B e 3B e os diagnósticos antigos ficam no original preservado. Para abrir a interface diretamente, utilize o notebook 06.

Os [módulos do RAG e de fontes](src/README.md) foram exportados da sessão em funcionamento. Recebem os dados e modelos explicitamente; importá-los não carrega a LLM nem inicia a interface.

## Arquitetura do protótipo

O fluxo implementado é:

**Pergunta → embedding → busca dos três candidatos → contexto focado → geração → resposta e fontes consultadas.**

O NER permanece como experimento separado. Ainda não é usado como filtro da busca nem como classificador de intenção.

- **Busca semântica:** Serafim para português, vetores normalizados e produto escalar com NumPy.
- **Contexto focado:** entre os três candidatos, selecionamos os que pertencem ao mesmo registro de origem do primeiro colocado. A política pode prejudicar perguntas que exigem fontes diferentes.
- **Geração:** Qwen2.5-7B-Instruct, NF4 de 4 bits, sem amostragem e até 384 novos tokens.
- **Interface:** Gradio, com fontes obtidas dos metadados, separadas do texto gerado. “Fontes consultadas” não comprova automaticamente a sustentação de cada afirmação.
- **Avaliação:** o piloto de recuperação anterior, com a base de 279 trechos, obteve Recall@3 médio de 100% sobre as referências anotadas em quatro perguntas sintéticas. Uma quinta ficou sem referência naquela base. O gabarito não era exaustivo, e esse valor não deve ser atribuído à nova base ou ao chatbot como um todo. Os testes do RAG e seus erros estão documentados no fechamento da etapa 3.

As entidades só deverão restringir a recuperação quando o reconhecimento e os metadados forem confiáveis. A análise de sentimentos e o treinamento de uma rede neural separada do zero não fazem parte do escopo aprovado.

## Próximas etapas

1. Conferir os notebooks 05 e 06 organizados em uma sessão nova do Colab; a validação local não repetiu a inferência em GPU.
2. Avaliar perguntas independentes das usadas nos ajustes, incluindo casos sem resposta e variações de vocabulário.
3. Revisar os casos de trancamento de disciplina e consulta de horas AAC, distinguindo recuperação, contexto e geração.
4. Comparar a política de contexto focado com alternativas e verificar a sustentação das respostas nas fontes.
5. Finalizar relatório, avaliação e apresentação.

## Transparência e uso das fontes

O projeto utiliza apoio de IA na programação, documentação e elaboração de exemplos. Os integrantes são responsáveis por revisar as entregas e explicar o código e as decisões adotadas.

O acesso público a um documento não implica autorização automática para redistribuí-lo. Os materiais institucionais e os textos extraídos permanecem locais até a análise das condições de uso.

## Referência das aulas

O fluxo de integração foi desenvolvido usando como referência as [aulas de Chatbot RAG do professor Anderson Vanin](https://github.com/ProfAndersonVanin/Chatbot_RAG). Adaptamos a base para os documentos do Ibmec, a busca para Serafim e NumPy, o gerador para Qwen 7B em 4 bits e a seleção de contexto para a política por registro. As versões menores e os filtros que falharam fazem parte do desenvolvimento, não da configuração final da interface.
