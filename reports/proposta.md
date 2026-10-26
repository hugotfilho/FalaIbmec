# Chatbot de FAQ acadêmico do Ibmec Faria Lima

**Instituição:** Ibmec, São Paulo, Faria Lima  
**Curso:** Ciência de Dados e Inteligência Artificial  
**Integrantes:** Caio Jardim e Hugo Toledo

## Problema, público-alvo e justificativa

Alunos de graduação precisam consultar diferentes guias, manuais e páginas institucionais para encontrar orientações sobre matrícula, sistemas, biblioteca e estágio. A distribuição das informações dificulta a busca e exige atenção à unidade, ao semestre e à versão dos documentos.

Propomos um chatbot de perguntas frequentes para alunos de graduação do Ibmec Faria Lima, fundamentado em fontes oficiais selecionadas. A aplicação deverá apresentar referências e informar quando não encontrar suporte suficiente. O tema permite aplicar Processamento de Linguagem Natural a uma necessidade próxima da rotina do grupo e discutir qualidade, procedência e limites dos dados.

## Objetivos

**Objetivo geral:** desenvolver e avaliar um protótipo que responda a perguntas acadêmicas cobertas pelo corpus, indicando as fontes utilizadas.

**Objetivos específicos:** preparar documentos preservando arquivo, página e referência; reconhecer instituição, unidade e termos acadêmicos nas perguntas; recuperar trechos por similaridade semântica; gerar respostas fundamentadas nos trechos recuperados; e avaliar entidades, recuperação e respostas.

## Dados e escopo

A coleta inicial reúne quatro PDFs e 14 páginas HTML institucionais. A extração produziu 130 registros: páginas dos guias e do manual, registros mensais do calendário e páginas HTML. Na curadoria da versão 3, foram selecionados 89 registros de nove fontes, com 41 exclusões justificadas. Esses registros ainda serão divididos em trechos para recuperação.

O processamento preservou os textos originais e normalizou espaços em uma coluna separada. Foram retirados determinados sumários, capas, divisórias, conteúdos redundantes e registros com contatos ou horários não confirmados. Duas páginas com diferença na condição de realização da Avaliação Substitutiva foram separadas. O calendário foi extraído por regiões mensais para preservar datas e eventos.

A base é delimitada pelos documentos coletados. Edições internas não identificadas e limitações de vigência permanecem documentadas. O protótipo não será atendimento oficial nem acessará notas, pagamentos ou dados pessoais nos sistemas internos.

## Técnicas e tecnologias

Utilizaremos Python e Jupyter, com PyMuPDF e Beautiful Soup na extração. O experimento inicial de NER utiliza spaCy: um modelo pré-treinado em português foi observado e um pipeline separado recebeu regras EntityRuler para instituição, unidade e termos como matrícula, estágio e carteirinha. Essas regras não constituem um modelo treinado pelo grupo.

A recuperação prevê embeddings multilíngues com Sentence Transformers e comparação de similaridade. Na abordagem RAG, os trechos recuperados serão fornecidos a um modelo de linguagem, ainda a selecionar conforme recursos e custos. A interface prevista é Streamlit.

Conforme a adaptação de escopo informada pelo grupo, a entrega inicial reúne proposta e NER. Não estão previstos sentimentos ou treinamento de uma rede separada do zero. O Transformer pré-treinado será o componente neural da busca.

## Avaliação, estado atual e responsabilidade

O NER será avaliado por precisão, revocação e F1 com correspondência exata de posição e rótulo. Para recuperação, prevemos Recall@3 com perguntas e trechos relevantes anotados e, se viável, comparação com busca lexical. As respostas serão avaliadas quanto à correção, sustentação documental, referências e reconhecimento de ausência de informação.

Extração, curadoria e um piloto sintético de NER já foram executados. A revisão humana das anotações ainda precisa ser registrada. Divisão em trechos, busca, RAG e interface ainda não foram implementados; não há resultados dessas etapas.

As cópias das fontes permanecerão locais até análise das condições de redistribuição. O uso de IA no apoio à programação, documentação e exemplos será informado. Os integrantes revisarão as entregas e deverão explicar o código, as escolhas e as limitações.
