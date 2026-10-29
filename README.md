# Chatbot FAQ do Ibmec | Projeto de PLN

Projeto de um assistente para responder a dúvidas acadêmicas de alunos de graduação do Ibmec Faria Lima, consultando documentos institucionais e indicando as fontes utilizadas.

**Curso:** Ciência de Dados e Inteligência Artificial  
**Integrantes:** Caio Jardim e Hugo Toledo  
**Unidade:** Ibmec Faria Lima, São Paulo

## Estado atual

A extração dos textos, a curadoria do corpus e o experimento inicial de reconhecimento de entidades foram concluídos. O RAG e a interface ainda serão implementados.

A entrega inicial reúne a [proposta do projeto](reports/proposta.md) e o [experimento básico de NER](notebooks/03_ner_basico.ipynb), conforme a adaptação de escopo autorizada pelo professor.

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

A curadoria não confirma a vigência de todas as regras acadêmicas. As limitações de edição, período e unidade permanecem documentadas para orientar o uso dos dados.

Os materiais originais e os textos processados são mantidos localmente e ignorados pelo Git. A reprodução das etapas de extração e curadoria exige esses arquivos.

## Notebooks

| Notebook | Conteúdo |
| --- | --- |
| [01_extracao_textos.ipynb](notebooks/01_extracao_textos.ipynb) | Extração e inspeção de textos de PDFs e HTMLs. |
| [02_revisao_corpus.ipynb](notebooks/02_revisao_corpus.ipynb) | Revisão das fontes, exclusões, sobreposições e consolidação do corpus. |
| [03_ner_basico.ipynb](notebooks/03_ner_basico.ipynb) | Observação do modelo pré-treinado, regras de entidades, avaliação e reprodução dos resultados. |

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

## Execução dos experimentos

Abra os notebooks no Jupyter ou no VS Code e execute as células na ordem. Os notebooks 01 e 02 dependem dos materiais locais em `data/raw/` e dos arquivos gerados em `data/processed/`.

Para o experimento de NER, instale as dependências no ambiente Python utilizado pelo kernel:

```bash
python -m pip install spacy==3.8.16 jupyter ipykernel
python -m spacy download pt_core_news_sm-3.8.0 --direct
```

O notebook 03 usa exemplos sintéticos e não depende do corpus local. A célula de exportação protege os resultados existentes e interrompe a gravação quando os CSVs já estão presentes. Para conferir os resultados versionados, utilize a célula final de reprodução; para gerar uma nova exportação, escolha outra pasta de resultados.

Ainda não há aplicação de chatbot executável.

## Desenvolvimento previsto

O fluxo planejado é:

**Pergunta → reconhecimento de entidades → recuperação de trechos → geração de resposta com fontes.**

- **Busca semântica:** embeddings de um Transformer pré-treinado, com Sentence Transformers.
- **RAG:** fornecimento dos trechos recuperados a um modelo de linguagem, ainda a selecionar.
- **Interface:** protótipo com Streamlit.
- **Avaliação:** Recall@3 para recuperação e revisão de correção, sustentação documental e referências das respostas. Quando viável, comparação com uma busca lexical simples.

As entidades só deverão restringir a recuperação quando o reconhecimento e os metadados forem confiáveis. A análise de sentimentos e o treinamento de uma rede neural separada do zero não fazem parte do escopo aprovado.

## Próximas etapas

1. Registrar a revisão humana das anotações e ampliar a avaliação do NER com casos independentes.
2. Dividir os documentos em trechos, preservando as referências e os metadados.
3. Implementar e avaliar a recuperação por similaridade semântica.
4. Integrar o modelo de linguagem e a interface.
5. Avaliar as respostas e documentar os resultados e as limitações.

## Transparência e uso das fontes

O projeto utiliza apoio de IA na programação, documentação e elaboração de exemplos. Os integrantes são responsáveis por revisar as entregas e explicar o código e as decisões adotadas.

O acesso público a um documento não implica autorização automática para redistribuí-lo. Os materiais institucionais e os textos extraídos permanecem locais até a análise das condições de uso.
