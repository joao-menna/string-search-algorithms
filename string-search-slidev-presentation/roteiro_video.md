# Roteiro de Apresentação - Busca em Texto com Strategy e OpenTelemetry

## Slide 1 - Abertura

Olá! Eu sou João Miguel de Castro Menna e neste projeto eu exploro algoritmos clássicos de busca em texto: Naive, Rabin-Karp, KMP e Boyer-Moore.

O foco aqui não é só implementar os algoritmos, mas comparar como eles se comportam na prática, com métricas reais de execução. Ao longo da apresentação, eu vou mostrar arquitetura, fluxo de execução, base teórica e os resultados finais.

Antes de entrar na implementação, vale contextualizar o problema que estamos tentando resolver.

## Slide 2 - Problema e Objetivo

Buscar padrões em texto parece simples, mas fica caro quando o volume de dados cresce. Dependendo da estratégia, a diferença de desempenho pode ser muito grande.

Além disso, em muitos projetos, a gente conhece a complexidade teórica, mas não mede o comportamento real em execução.

Então o objetivo foi exatamente este: implementar diferentes estratégias de busca e medir o custo real delas com observabilidade moderna, para comparar teoria e prática com dados.

Com esse objetivo em mente, estas foram as principais entregas do projeto.

## Slide 3 - Entregas Principais

A primeira entrega foi uma execução flexível por linha de comando, permitindo processar tanto arquivos individuais quanto lotes de arquivos.

A segunda foi a coleta de métricas reais: tempo de CPU, número de comparações e memória, tudo instrumentado com OpenTelemetry.

E a terceira foi um dashboard em Streamlit, que facilita a análise histórica e comparativa dos benchmarks.

Se vocês quiserem explorar o projeto em detalhes, o código está público.

## Slide 4 - Código Fonte

Todo o código apresentado está disponível no GitHub, no repositório do projeto.

Lá vocês encontram a implementação dos algoritmos, a instrumentação de observabilidade, os scripts de benchmark e o dashboard.

Agora vou mostrar rapidamente como a apresentação está organizada.

## Slide 5 - Sumário

A sequência é: arquitetura com Strategy, fluxo da CLI, métricas, revisão dos algoritmos, camada de observabilidade e, por fim, resultados e conclusões.

Começando pela base de arquitetura do projeto.

## Slide 6 - Arquitetura Strategy

Eu usei o padrão Strategy para separar claramente cada algoritmo de busca.

Todos implementam uma interface comum, chamada SearchStrategy. Isso permite trocar o algoritmo em tempo de execução sem alterar a lógica cliente.

Na prática, a CLI atua como contexto e delega a execução para a estratégia escolhida. Esse desacoplamento facilita testes, manutenção e comparação objetiva entre algoritmos.

Com a arquitetura definida, vamos ao pipeline de execução.

## Slide 7 - Fluxo de Execução

Este fluxo mostra o caminho completo em cinco etapas visuais: Entrada da CLI, Leitura dos Arquivos, Execução dos Algoritmos, Telemetria com spans e Resultados.

A ideia foi deixar tudo automatizado, para que cada execução já produza dados prontos para análise no dashboard.

Para entender esse fluxo, vale olhar os parâmetros expostos na CLI.

## Slide 8 - Interface CLI: Parâmetros

Aqui estão os parâmetros principais da interface de linha de comando.

Concretamente, a tabela mostra as flags files, -p/--pattern, -a/--algorithm, --step-by-step e --telemetry-dir.

O parâmetro de algoritmo aceita naive, rabin-karp, boyer-moore, kmp ou all, então dá para rodar um único método ou comparar todos no mesmo comando.

Com isso, o mesmo pipeline atende cenários simples e também experimentos mais estruturados de benchmark.

Mas afinal, quais medidas nós capturamos em cada execução?

## Slide 9 - O que Medimos?

As métricas centrais são: tempo de execução em nanossegundos, número de comparações de caracteres e relação entre custo observado e custo esperado.

Nos cards, isso aparece como Nano para tempo, count++ para comparações, n/m para razão real vs esperado e O(f) para complexidade teórica.

Além disso, cada resultado é analisado junto da complexidade teórica do algoritmo.

Isso permite identificar não só quem foi mais rápido, mas também por que foi mais rápido em determinado cenário.

Com essas métricas em mente, vamos revisar a base teórica.

## Slide 10 - Base Teórica: Complexidade

Nesta tabela, n representa o tamanho do texto, m o tamanho do padrão e sigma o tamanho do alfabeto.

Ela traz melhor caso, pior caso e espaço adicional para cada algoritmo: por exemplo, KMP fica em O(n) no melhor e no pior caso, enquanto Boyer-Moore tem melhor caso O(n/m) e espaço O(m + sigma).

Ela resume os custos esperados de cada algoritmo e serve como referência para interpretar os resultados experimentais.

O ponto importante é: complexidade orienta, mas os dados reais é que validam comportamento em produção.

Agora, um resumo rápido de cada algoritmo começando pelo mais simples.

## Slide 11 - Naive

O Naive é a abordagem de força bruta: desliza o padrão posição por posição e compara caractere por caractere.

A vantagem é a simplicidade extrema de implementação.

A limitação é que ele repete muitas comparações desnecessárias, especialmente em textos longos com muitos prefixos parecidos.

Para reduzir comparações inúteis, uma alternativa é filtrar com hash.

## Slide 12 - Rabin-Karp

Rabin-Karp calcula assinaturas numéricas: uma do padrão e outra da janela atual do texto.

A comparação detalhada só acontece quando os hashes coincidem.

Com rolling hash, a atualização da janela é O(1), o que torna o algoritmo eficiente em vários cenários.

O cuidado é com colisões de hash, que podem degradar o desempenho em casos específicos.

Outra estratégia é evitar retrocessos no texto com pré-processamento do padrão.

## Slide 13 - KMP

O KMP usa a tabela LPS para reaproveitar informação de prefixos e sufixos já conhecidos.

Na prática, quando ocorre mismatch, ele não volta o ponteiro do texto, apenas ajusta o ponteiro do padrão.

Isso garante tempo linear em relação ao tamanho do texto e traz comportamento estável mesmo em entradas difíceis.

Por fim, temos um algoritmo famoso por dar saltos maiores na busca.

## Slide 14 - Boyer-Moore

No Boyer-Moore, a comparação acontece da direita para a esquerda.

Quando encontra um caractere inadequado, a regra do caractere ruim permite pular várias posições de uma vez.

Quanto maior o padrão, maior tende a ser o benefício desses saltos, por isso ele costuma se destacar em aplicações práticas.

Depois de implementar os algoritmos, a próxima etapa foi instrumentar o experimento.

## Slide 15 - Observabilidade do Experimento

Cada execução gera spans com metadados como algoritmo, tamanho do texto e padrão utilizado.

Esses dados são exportados em JSONL local para manter baixo overhead.

Em seguida, o dashboard em Streamlit processa o histórico e apresenta gráficos comparativos, como dispersão e boxplot.

Com a infraestrutura pronta, vamos ao cenário principal de teste.

## Slide 16 - Resultados: Especificações do Teste

Neste recorte, o padrão buscado foi 'Celebrity marriage', em um texto de cerca de 89 mil caracteres, combinando roteiros de Bee Movie e Shrek.

Um detalhe importante: o padrão está próximo do final do texto, o que força os algoritmos a percorrerem quase todo o conteúdo e evidencia diferenças de eficiência.

Aqui estão os números consolidados dessa comparação.

## Slide 17 - Resultados: Análise de Desempenho

Nesta visualização, comparamos tempo em milissegundos e total de comparações entre os algoritmos.

No modo Comparação normal, os tempos exibidos são: Naive 11.17ms, Rabin-Karp 13.47ms, KMP 6.52ms e Boyer-Moore 1.46ms.

No modo Comparação stepped, os tempos sobem por causa da visualização detalhada: Naive 43.00ms, Rabin-Karp 33.86ms, KMP 25.20ms e Boyer-Moore 5.65ms.

As comparações mostradas no componente são: Naive 87965, Rabin-Karp 862, KMP 87973 e Boyer-Moore 7708.

O comportamento observado confirma tendências clássicas: algoritmos com melhor heurística de salto e/ou melhor reaproveitamento de informação tendem a reduzir comparações e tempo total.

Mais importante: os dados tornam a discussão objetiva, porque permitem medir variação, estabilidade e impacto do tamanho do padrão.

E esses resultados não ficaram restritos a um único teste.

## Slide 18 - Resultados: Complemento

Também foram executados cenários com padrões menores e maiores.

As tendências gerais se mantiveram: Naive tende a sofrer mais em casos desfavoráveis, KMP mantém consistência e Boyer-Moore ganha força com padrões maiores.

O dashboard facilita justamente essa comparação entre diferentes contextos.

Para quem quiser reproduzir a análise, o processo é simples.

## Slide 19 - Análise do Dashboard

Com o ambiente Python configurado e dependências instaladas, basta executar o comando streamlit run dashboard.py.

Depois disso, o dashboard fica disponível no navegador para explorar filtros, distribuições e comparações históricas.

Fechando, estes são os principais aprendizados do projeto.

## Slide 20 - Conclusão

Boyer-Moore se destacou no cenário principal, especialmente com padrões maiores.

KMP apresentou desempenho consistente e previsível, superando o Naive em situações com muitos matches parciais.

E, talvez o principal ponto do trabalho: a observabilidade permitiu validar a teoria com evidências reais, mostrando nuances que só aparecem com medição.

Para encerrar, deixo os créditos das tecnologias utilizadas.

## Slide 21 - Créditos

Este trabalho foi construído com Slidev para a apresentação, OpenTelemetry para instrumentação e Streamlit para visualização.

As bases textuais utilizadas vieram dos roteiros de Bee Movie e Shrek.

Obrigado pela atenção!
