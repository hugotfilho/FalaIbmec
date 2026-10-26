# Chatbot de FAQ acadêmico do Ibmec Faria Lima

**Instituição:** Ibmec, São Paulo, Faria Lima  
**Curso:** Ciência de Dados e Inteligência Artificial  
**Integrantes:** Caio Jardim e Hugo Toledo

## Problema e público-alvo

Precisamos consultar diferentes guias, manuais e páginas institucionais para encontrar informações sobre matrícula, acesso aos sistemas, biblioteca e estágio. Como essas informações estão distribuídas em várias fontes, podemos ter dificuldade para localizar a orientação adequada à nossa unidade e ao período letivo.

Propomos um chatbot de perguntas frequentes para alunos de graduação do Ibmec Faria Lima. Pretendemos reunir a consulta a essas informações em uma interface na qual poderemos fazer perguntas em linguagem natural e receber respostas acompanhadas das fontes utilizadas.

## Justificativa

Escolhemos esse tema por vivenciarmos essa dificuldade na nossa rotina acadêmica. Com o projeto, queremos facilitar o acesso às orientações institucionais e aplicar técnicas de Processamento de Linguagem Natural a um problema próximo da nossa realidade. Buscaremos apresentar respostas fundamentadas nos documentos e indicar quando não encontrarmos informação suficiente.

## Objetivos

**Objetivo geral:** desenvolver e avaliar um protótipo de chatbot que responda a dúvidas acadêmicas com base nos documentos selecionados, indicando as fontes consultadas.

**Objetivos específicos:** organizar e preparar os textos; identificar instituição, unidade e termos acadêmicos nas perguntas; recuperar trechos relacionados à dúvida; gerar respostas com base nesses trechos; e avaliar a identificação de entidades, a recuperação e as respostas.

## Dados

Utilizaremos guias, manual do aluno, calendário acadêmico e páginas institucionais do Ibmec. Reunimos inicialmente quatro PDFs e 14 arquivos HTML, dos quais extraímos 130 registros. Após a curadoria, selecionamos 89 registros de nove fontes e documentamos 41 exclusões.

Preservamos os textos originais e registramos as referências e as limitações das fontes. Para a busca, utilizaremos os textos preparados e os dividiremos em trechos. Limitaremos as respostas aos assuntos cobertos por esses documentos, considerando a unidade e o período quando identificados.

## Tecnologias e técnicas de PLN previstas

Utilizaremos Python e Jupyter nos experimentos, PyMuPDF na extração dos PDFs e Beautiful Soup no processamento dos HTMLs. Para reconhecer entidades, utilizaremos spaCy, observando o modelo pré-treinado em português e adaptando regras com EntityRuler para instituição, unidade e termos acadêmicos.

Na busca semântica, utilizaremos embeddings de um Transformer pré-treinado com Sentence Transformers. Integraremos a recuperação a um modelo de linguagem por meio de RAG, para gerar respostas apoiadas nos trechos encontrados. Selecionaremos esse modelo conforme os recursos disponíveis e construiremos a interface do protótipo com Streamlit.
