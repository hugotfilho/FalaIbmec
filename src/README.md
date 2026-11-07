# Componentes do RAG

`rag.py` contém as funções exportadas da sessão do notebook 06:

- `responder_rag`: recuperação por similaridade e geração com os trechos encontrados.
- `responder_rag_focado`: seleciona, entre os três primeiros candidatos, os trechos do mesmo registro de origem do primeiro colocado e chama a geração.

As funções recebem explicitamente os trechos, embeddings, modelo de busca, LLM e tokenizador. Importar o módulo não carrega os modelos. O carregamento e a interface Gradio estão no notebook 06; este módulo sozinho não inicia uma aplicação.

`fontes.py` contém `formatar_fontes`, que monta a apresentação de documentos, páginas, links e trechos consultados a partir dos metadados. A lista não é produzida pela LLM e não comprova automaticamente que cada trecho sustenta a resposta.

O NER ainda é um experimento separado e não participa deste fluxo. A seleção por registro pode perder informações que exigem combinar fontes diferentes; o histórico visual da conversa não é usado na interpretação da pergunta seguinte.
