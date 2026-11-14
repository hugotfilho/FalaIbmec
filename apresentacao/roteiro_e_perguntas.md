# FalaIbmec: roteiro da apresentação e perguntas prováveis

Tempo: 10 min de apresentação e 5 min de perguntas. O roteiro soma cerca de 9min30, então há 30 s de folga.

## Como usar o arquivo

- Abra `apresentacao/index.html` no Chrome ou no Safari. Funciona sem internet; sem internet, só a fonte muda para a padrão do sistema.
- **→ / espaço / clique**: avançar · **←**: voltar · **F**: tela cheia · **N**: notas do apresentador · **T**: cronômetro (fica âmbar aos 9 min e vermelho aos 10) · **R**: zera o cronômetro.
- O cronômetro começa quando você sai da capa.
- O vídeo toca sozinho no slide 7.
- Reserva: `FalaIbmec_apresentacao.pdf`. No PDF, o vídeo vira uma captura de tela.

## Versões citadas nos slides

- **v1, protótipo inicial:** primeira interface. As interações com os casos de trancamento e AAC e o piloto de 8 perguntas rodaram nessa versão.
- **v2, versão final:** a interface nova (painel de fontes com aviso de recusa e mascote). A demonstração, a comparação amplo × focado e o novo teste dos dois casos rodaram nessa versão.
- Base, busca, contexto focado e modelo são os mesmos nas duas. Se perguntarem o que mudou, a resposta é a interface.

## Roteiro

Se apresentarem em dupla, uma divisão natural é: slides 1 a 5 (problema, fundamentação e dados) com uma pessoa, e slides 6 a 11 (arquitetura, demonstração, métricas e conclusão) com a outra.

| # | Slide | Tempo | O que falar | Números para não esquecer |
|---|---|---|---|---|
| 1 | Capa | 0:15 | Quem somos e o que é o FalaIbmec, em uma frase. | — |
| 2 | Problema | 0:50 | A informação está espalhada, se repete e às vezes diverge. O aluno usa outras palavras. Daí os três requisitos: responder, mostrar a fonte e saber recusar. | 110 páginas · 14 páginas web · 7 pares sobrepostos · 2 versões da regra da AS |
| 3 | Por que RAG | 0:50 | A LLM sozinha não conhece o Ibmec e não cita a fonte. O fine-tuning é caro e desatualiza. O RAG consulta a base na hora. | Lewis et al., 2020 |
| 4 | Curadoria | 0:55 | A maior parte do trabalho foi decidir o que não entra. Todas as exclusões foram documentadas. | 130 → 89 registros · 9 fontes · 41 exclusões · 280 trechos de 120 tokens |
| 5 | NER | 0:40 | As regras confundem verbo com substantivo; um filtro gramatical melhorou a precisão. São só 8 frases sintéticas, e o NER não entra no RAG. | Precisão 81,8% → 90,0% · F1 90,0% → 94,7% |
| 6 | Arquitetura | 1:15 | Os 6 passos, por que usamos o Serafim e o contexto focado no exemplo da nota final. | 768 dimensões · top 3 · fórmula 0,74 × CR 0,63 |
| 7 | Demonstração | 1:00 | Narre o vídeo: regra, procedimento e recusa com o aviso amarelo. As fontes vêm dos metadados. | Gravado na v2, Colab, T4 |
| 8 | Métricas | 1:10 | Uma métrica para cada etapa. Resultado do piloto e tempos. **Diga a ressalva em voz alta.** | 4/4 em todas · respostas ~7,1 s · recusas ~1,3 s · 8 perguntas |
| 9 | Comparações | 1:15 | Amplo × focado: só o amplo teve recusa indevida, e o focado envia menos da metade dos trechos. Similaridade: perguntas pessoais têm valores parecidos com as respondíveis, então quem recusa é o modelo. | 1/4 × 0/4 · 9,3 s × 6,7 s · 3,0 × 1,36 trechos · senha 0,70 × carteirinha 0,72 |
| 10 | Erros | 0:50 | Trancar × excluir é um problema de vocabulário. Horas AAC: faltou recusar. Os dois erros se repetiram nas duas versões. | v1 e v2 |
| 11 | Conclusão | 0:30 | Três aprendizados e os próximos passos. "Obrigado, perguntas?" | — |

### Frases que não podem faltar

- No slide 8: "São 8 perguntas que conhecíamos durante os ajustes, com revisão assistida por IA. Isso descreve o piloto, não a precisão geral."
- No slide 9: "A comparação é de uma execução por pergunta. A recusa foi detectada pelo texto; não revisamos a correção das outras respostas."
- No slide 5: "O NER é um experimento separado; ele não filtra a busca."

## Perguntas prováveis e respostas

### Sobre as métricas

**1. "100% quer dizer que o sistema acerta sempre?"**
Não. São 8 perguntas de desenvolvimento, 4 com resposta e 4 sem, e várias foram usadas nos ajustes. A revisão das respostas teve assistência de IA. O próprio slide de erros mostra duas perguntas que falham. O 4/4 descreve o piloto, não a precisão geral.

**2. "Qual a diferença entre Recall@3 e cobertura do contexto?"**
O Recall@3 olha os 3 candidatos da busca. A cobertura olha só o que chegou ao gerador, depois do contexto focado. Se o focado descartasse o trecho certo, o Recall@3 seria 1 e a cobertura cairia. No piloto, as duas ficaram em 4/4.

**3. "Quem avaliou se as respostas estavam corretas?"**
A revisão de correção e sustentação do piloto foi assistida por IA, com critérios escritos antes da execução para cada pergunta. Não houve revisão humana independente, e isso está nos próximos passos. Na comparação da v2, só a recusa foi medida, de forma automática.

**4. "Por que não usaram mais perguntas?"**
Cada pergunta precisa de referências anotadas na base (quais trechos respondem) e de critérios de revisão. Preferimos poucas perguntas bem anotadas e deixar explícito o limite. Uma rodada com 12 perguntas novas foi preparada, mas não executada.

**5. "Por que a recusa é tão mais rápida?"**
O tempo é dominado pela geração. A recusa é uma frase fixa de 7 palavras; uma resposta de procedimento tem várias linhas. Nas medições, as recusas levaram ~1,3 s e as respostas ~7 s.

**6. "O focado é mais rápido mesmo?"**
Nas 4 perguntas com resposta, a média foi 9,3 s × 6,7 s. Mas a primeira chamada do amplo demorou 15,2 s; sem ela, a diferença cai para cerca de 0,9 s. Com uma execução por pergunta, o resultado mais sólido é a recusa indevida (1 × 0) e a quantidade de trechos enviados (3,0 × 1,36).

**7. "Como mediram o NER?"**
Correspondência exata de posição e rótulo, em 8 frases sintéticas, com precisão, revocação e F1 micro. Foram 9 verdadeiros positivos nas duas versões; os falsos positivos caíram de 2 para 1. As frases foram escritas conhecendo as regras, então a avaliação não é independente.

### Sobre as escolhas técnicas

**8. "Por que RAG e não fine-tuning?"**
O fine-tuning grava o conhecimento nos pesos: não mostra a fonte, precisa de novo treino a cada mudança de regra e exige dados e GPU. Com RAG, o modelo lê o trecho na hora e mostramos qual foi. Para atualizar, basta trocar a base.

**9. "Por que o Serafim?"**
É um encoder de sentenças para português, treinado para recuperação de informação, e roda via Sentence Transformers. Gera vetores de 768 dimensões, que normalizamos para usar o produto escalar como similaridade de cosseno.

**10. "A quantização em 4 bits não piora o modelo?"**
Pode haver alguma perda, e não medimos a mesma configuração em 16 bits. Foi a forma de rodar um modelo de 7B na T4 do Colab: em FP16 ele ocuparia cerca de 15 GB; em NF4, cerca de 5 GB (estimativa pelo número de parâmetros). Entre os modelos que testamos, o 1.5B, que caberia sem quantizar, inventou um link.

**11. "Por que top 3 e trechos de 120 tokens?"**
O limite do Serafim é 128 tokens com os tokens especiais, então usamos janelas de 120 com sobreposição de 20 para não cortar frases sem contexto. Escolhemos 3 candidatos para manter o prompt curto; não comparamos outros valores de k. Essa é uma comparação possível.

**12. "Por que o contexto focado? E se a resposta precisar de duas páginas?"**
O caso da nota final mostrou que trechos parecidos, mas de outro assunto (CR), levaram o modelo a recusar. O focado resolve isso. O risco é real: uma pergunta que precise de duas páginas perde parte da evidência. Por isso ele aparece nas limitações.

**13. "Por que a similaridade não é usada para recusar?"**
Os dados mostram que não separaria os casos: "qual é a minha senha do SIA" teve 0,70, e a carteirinha, 0,72. O que separa é o conteúdo, e por isso a recusa fica com o modelo, pelo prompt.

**14. "Por que o NER não está no pipeline?"**
Só foi testado em 8 frases sintéticas, e ainda erra formas verbais. Usá-lo para filtrar a busca poderia descartar trechos certos. A regra que adotamos é integrar só quando o reconhecimento e os metadados forem confiáveis.

### Sobre confiabilidade e limites

**15. "Como garantem que o modelo não inventa?"**
Não garantimos. Reduzimos o risco com o prompt (usar só os documentos, não escrever URLs e recusar com uma frase padrão), com a geração sem amostragem e com fontes que vêm dos metadados, e não do modelo. O painel mostra o que o modelo leu, mas não confere cada afirmação; isso está nos próximos passos.

**16. "E se o documento estiver desatualizado ou houver duas regras diferentes?"**
Na curadoria, excluímos as páginas com divergência (por exemplo, a regra da AS) e registramos abrangência e período de cada fonte. Essas informações vão no prompt e no painel. A curadoria não confirma a vigência de todas as regras, e isso aparece como limitação.

**17. "Como resolveriam o caso do trancamento?"**
O conteúdo existe como "exclusão de disciplina". Os caminhos são expandir a pergunta com sinônimos, fazer busca híbrida (semântica + palavras-chave, como BM25) ou reformular a pergunta com a própria LLM antes da busca. Nada disso foi testado ainda.

**18. "O chatbot lembra da conversa?"**
Não. Cada pergunta é processada sozinha, mesmo com o histórico visível. A interface pede uma pergunta completa por mensagem.

**19. "Ele acessa notas ou dados do aluno?"**
Não. O escopo exclui notas, pagamentos e dados pessoais, e o sistema recusa essas perguntas, como mostram a demonstração e as 4 perguntas sem resposta.

**20. "Quanto custa rodar? Escala?"**
Hoje roda numa GPU T4 gratuita do Colab, com uma pergunta por vez. Para uso real, seria preciso um servidor com GPU ou um modelo servido por API, além de fila de requisições. Não medimos carga.

**21. "Os documentos podem ser usados assim?"**
São documentos públicos do Ibmec, mas acesso público não implica autorização para redistribuir. Por isso os textos e a base ficam locais e fora do GitHub. O protótipo é acadêmico e diz na tela que não é canal oficial.

### Se perguntarem algo que vocês não sabem

Responda com o que existe: "Isso não medimos. O que temos é [dado mais próximo]. Seria um próximo passo." É melhor do que estimar um número.
