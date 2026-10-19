# Chatbot FAQ do Ibmec — Projeto de PLN

Assistente acadêmico que consulta documentos oficiais do Ibmec para responder a dúvidas em linguagem natural, com indicação das fontes.

**Curso:** Ciência de Dados e Inteligência Artificial  
**Integrantes:** Caio Jardim e Hugo Toledo  
**Unidade:** a definir.

## Status

Estrutura inicial e proposta em elaboração. A aplicação e os experimentos ainda não foram implementados. Não há resultados de avaliação disponíveis.

## Objetivo e escopo

Facilitar a consulta a orientações acadêmicas, inicialmente para uma unidade e um conjunto limitado de documentos. O escopo inclui acesso aos sistemas, documentos e serviços acadêmicos, conforme a cobertura das fontes selecionadas.

O protótipo não consultará notas, pagamentos ou dados pessoais nos sistemas internos. Não é um canal oficial de atendimento do Ibmec.

## Técnicas de PLN

- **Transformer pré-treinado:** produzir embeddings das perguntas e dos documentos para busca semântica. Transformers são redes neurais; não está previsto treinar uma rede separada do zero.
- **NER:** identificar entidades úteis, como instituições e unidades. Cursos e disciplinas poderão exigir adaptação com regras ou listas de nomes. A abordagem será escolhida e avaliada durante os experimentos.
- **RAG:** recuperar trechos e fornecê-los a um modelo de linguagem para elaborar uma resposta com fontes. Quando não houver suporte nos documentos, informar a limitação.

A análise de sentimentos e o treinamento de uma rede separada foram retirados do escopo após a orientação do professor de utilizar apenas os componentes necessários. O alinhamento dos marcos do cronograma com esse escopo deve ser confirmado pelo grupo.

## Fluxo previsto

Pergunta → identificação de entidades → seleção das fontes aplicáveis → busca semântica → resposta fundamentada e fontes.

As entidades só devem restringir a busca quando sua identificação e os metadados dos documentos forem confiáveis. Ambiguidades de curso ou unidade podem exigir esclarecimento ao usuário.

## Organização

```text
projeto-pln-chatbotFAQ-ibmec/
├── README.md
├── data/
│   ├── README.md
│   ├── raw/          # Materiais originais; ignorados pelo Git
│   ├── processed/    # Textos e trechos preparados; ignorados pelo Git
│   └── evaluation/   # Perguntas e anotações revisadas para avaliação
├── notebooks/       # Experimentos de preparação, Transformer e NER
├── src/             # Implementação futura do chatbot
└── reports/
    ├── proposta.md
    └── plano-de-trabalho.md
```

## Dados

Consulte [as fontes candidatas e as orientações de coleta](data/README.md). Antes de incluir um documento, registrar título, URL, unidade, data, versão e condições de uso. Materiais públicos não serão tratados automaticamente como conteúdo livre para redistribuição.

## Avaliação prevista

- Busca: Recall@3, usando perguntas com trechos relevantes previamente identificados.
- NER: precisão, revocação e F1 por tipo de entidade, considerando os limites e rótulos corretos.
- Respostas: revisão da correção, apoio nas fontes e indicação adequada da ausência de informação.
- Comparação: busca semântica versus uma abordagem lexical simples, quando viável.

Perguntas de avaliação serão mantidas separadas dos exemplos utilizados para ajustar regras e parâmetros. Resultados serão registrados somente após a execução dos experimentos.

## Execução

Ainda não há aplicação executável. As dependências e instruções serão adicionadas quando os primeiros experimentos forem implementados e verificados.

## Próximos passos

1. Definir a unidade e os assuntos iniciais.
2. Revisar a proposta e alinhar as entregas com o professor.
3. Selecionar documentos e registrar suas condições de uso.
4. Extrair os textos e preparar perguntas de avaliação.
5. Implementar e avaliar a busca com Transformer e o NER.
6. Integrar o RAG e a interface.

## Transparência

A documentação inicial foi elaborada com apoio de IA. O grupo deve revisar o material, registrar as ferramentas utilizadas durante o desenvolvimento e ser capaz de explicar o código e as decisões técnicas.
