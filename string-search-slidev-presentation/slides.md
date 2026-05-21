---
theme: dracula
title: Introdução
class: text-center
transition: slide-up
comark: true
---

# Projeto de Busca em Texto com Strategy e OpenTelemetry

<div class="mt-4 mb-8 flex gap-8 justify-center text-yellow text-xl">
  <span>Naive</span>
  <span>Rabin-Karp</span>
  <span>KMP</span>
  <span>Boyer-Moore</span>
</div>

Por João Miguel de Castro Menna

---
title: Problema e Objetivo
layout: two-cols-header
transition: slide-up
---

# Qual problema estamos resolvendo?

::left::

### O Desafio da Eficiência

- Localizar padrões em grandes volumes de texto rapidamente.
- Complexidade: Algoritmos simples podem ser muito lentos $O(n \times m)$.
- Falta de visibilidade sobre o custo real de execução em ambiente produtivo.

### Nosso Objetivo

Implementar e medir o desempenho real vs. teórico de difertentes estratégias usando observabilidade moderna.

::right::

<div class="mt-12 flex flex-col gap-2 items-center justify-center">
  <span>Este é meu texto exemplo</span>
  <span>↓</span>
  <div class="flex flex-col items-center">
    <span>Padrão:</span>
    <span class="text-yellow">texto</span>
  </div>
  <span>↓</span>
  <div class="flex flex-col items-center">
    <span>Este é meu <span v-mark.circle.red="1">texto</span> exemplo</span>
    <span>Posição: <span class="text-yellow">11</span></span>
  </div>
</div>

<!--
Here is another comment.
-->

---
title: Entregas Principais
layout: center
transition: slide-up
---

<div class="flex flex-col gap-4">
  <h1 class="text-center">Entregas principais</h1>

  <div class="flex gap-4">
    <Card
      icon="fa-solid fa-file-code"
      title="Execução Flexível"
      description="Suporte a arquivos únicos ou processamento em lote de diretórios inteiros."
    />
    <Card
      icon="fa-solid fa-gauge-high"
      title="Métricas Reais"
      description="Coleta de tempo de CPU, número de comparações e uso de memória via OpenTelemetry."
    />
    <Card
      icon="fa-solid fa-chart-line"
      title="Dashboard"
      description="Interface em Streamlit para visualização histórica e comparação de benchmarks."
    />
  </div>
</div>

---
title: Código Fonte
layout: center
class: text-center
transition: slide-up
---

Todo código aqui mostrado está disponível em:

[https://github.com/joao-menna/string-search-algorithms](https://github.com/joao-menna/string-search-algorithms)

---
title: Sumário
transition: slide-up
---

<div class="flex flex-col">
  <h1>Sumário</h1>
  <div class="flex items-start">
    <Toc columns="2" minDepth="1" maxDepth="2" />
  </div>
</div>

---
layout: two-cols
transition: slide-up
---

::left::

# Arquitetura Strategy

O padrão **Strategy** permite trocar o algoritmo de busca em tempo de execução sem alterar o cliente. Cada algoritmo é encapsulado em uma classe que implementa uma interface comum, facilitando a comparação de desempenho.

- SearchStrategy: Interface Abstrata comum para todos os algoritmos.
- ConcreteStrategies: Implementações específicas (Naive, KMP, etc.).
- Context: CLI que delega a execução.

::right::

<div class="size-full flex items-center justify-center">
  <img src="/assets/strategy.png" alt="Strategy Pattern" class="flex items-center rounded">
</div>

---
title: Fluxo de Execução
layout: center
transition: slide-up
---

<div class="flex flex-col items-center">
  <h1 class="text-center pb-4">Fluxo de Execução da CLI</h1>

  <CliExecutionSequence />

  <span class="text-gray/40">
    Pipeline automatizado do parsing de argumentos à exportação de dados.
  </span>
</div>

---
layout: default
transition: slide-up
---

# Interface CLI: Parâmetros

<div class="flex items-center h-full pb-8">
  <ParameterTable />
</div>

---
transition: slide-up
---

# O que Medimos?

<div class="flex flex-col justify-center size-full gap-8 pb-8">
  <div class="flex gap-8">
    <MeasureCard title="Nano" description="TEMPO DE EXECUÇÃO" />
    <MeasureCard title="count++" description="COMPARAÇÕES DE CARACTERES" />
  </div>
  <div class="flex gap-8">
    <MeasureCard title="n / m" description="RAZÃO REAL VS ESPERADO" />
    <MeasureCard title="O(f)" description="COMPLEXIDADE TEÓRICA" />
  </div>
</div>

---
transition: slide-up
---

# Base Teórica: Complexidade

<div class="flex flex-col items-center gap-8 ">
  <ComplexityTable />
</div>

\* n = comprimento do texto, m = comprimento do padrão, $\Sigma$ = tamanho do alfabeto.

---
layout: two-cols-header
transition: slide-up
---

# Naive: Simples e Didático

<br />
<br />

::left::

### Abordagem Força Bruta

- Desliza o padrão sobre o texto, uma posição por vez.
- Compara todos os caracteres da janela atual.
- **Vantagem**: Implementação trivial, sem pré-processamento.
- **Limitação**: Muitos retrocessos desnecessários no texto.

::right::

<img src="/assets/naive.jpg" class="rounded-lg" />

---
layout: two-cols-header
transition: slide-up
---

# Rabin-Karp: Hash Dinâmico

<br />
<br />

::left::

<div class="pr-8">
  <img src="/assets/rabin-karp.png" class="rounded-lg" />
</div>

::right::

### Filtragem por Assinatura

- Calcula um valor de hash para o padrão e para a janela do texto.
- Só faz a comparação real se os hashes coincidirem.
- **Rolling Hash**: Atualiza o hash em $O(1)$ ao deslizar a janela.
- **Risco**: Colisões de hash podem degradar a performance.

---
layout: two-cols-header
transition: slide-up
---

# KMP: Sem Retrocessos

<br />
<br />

::left::

### Tabela LPS (Longest Prefix Suffix)

- Pré-processa o padrão para encontrar sub-padrões repetidos.
- Evita voltar o ponteiro do texto após um mismatch.
- Garante tempo linear $O(n)$ independente da entrada.
- Ideal para fluxos de dados (streaming).

::right::

<img src="/assets/kmp.png" class="rounded-lg" />

---
layout: two-cols-header
transition: slide-up
---

# Boyer-Moore: Saltos Inteligentes

<br />

::left::

<div class="mr-8 h-full rounded-lg relative flex justify-center">
  <img src="/assets/bm.png" class="p-2 rounded-lg bg-white/40 h-96 object-contain" />
</div>

::right::

<br />

### Regra do Caractere Ruim

- Compara da **direita para a esquerda**.
- Pula várias posições do texto ao encontrar caracteres que não existem no padrão.
- Torna-se mais rápido à medida que o padrão cresce.
- Padrão ouro em buscas práticas (grep, editores).

---
layout: two-cols-header
transition: slide-up
---

# Observabilidade do Experimento

::left::

<br />
<br />
<br />

Fluxo de Dados:

- **Spans**: Cada busca é rastraeada com metadados ricos (pattern, size, algorithm).
- **Exportação**: Arquivos JSONL locais para baixo overhead.
- **Dashboard**: Streamlit lê o histórico e gera gráficos de dispersão e boxplots.

::right::

<div class="size-full flex items-center justify-center">
  <img src="/assets/observability.png" class="flex items-center rounded">
</div>

---
transition: slide-up
---

# Resultados Finais - Especificações do Teste

- **Padrão**: "Celebrity marriage"
- **Texto**: Roteiro de Bee Movie + Roteiro de Shrek (~89.000 caracteres)
- **Observação**: O padrão se encontra no final do texto

---
title: Resultados Finais - Análise de Desempenho
transition: slide-up
---

<div class="size-full flex flex-col gap-4">
  <h1>Resultados Finais - Análise de Desempenho</h1>

  <div class="h-full">
    <Metrics />
  </div>
</div>

---
transition: slide-up
---

# Resultados Finais - Complemento

- Foram feitas mais execuções com padrões menores e maiores, confirmando as tendências observadas.
- O dashboard permite comparar facilmente o desempenho de cada algoritmo em diferentes cenários, revelando insights sobre suas eficiências relativas.

---
transition: slide-up
---

# Análise do Dashboard

Instruções para acessar o dashboard:

- Certifique-se de ter o ambiente Python configurado e as dependências instaladas.
- Execute o comando `streamlit run dashboard.py` no terminal.
- Abra o link abaixo para visualizar os resultados e interagir com os gráficos.

[Acessar Dashboard](http://localhost:8501)

---
transition: slide-up
---

# Conclusão

- Boyer-moore se destacou como eficiente, especialmente para padrões maiores.
- KMP mostrou desempenho consistente, superando o Naive em casos de muitos matches parciais.
- A observabilidade permitiu validar as complexidades teóricas com dados reais, revelando nuances de desempenho em diferentes cenários.

---
transition: slide-up
---

# Créditos

- Slidev para a plataforma de apresentação.
- OpenTelemetry para a coleta de métricas.
- Streamlit para o dashboard de visualização.
- Fontes de dados: Roteiros de Bee Movie e Shrek.
