# Projeto de Busca em Texto

Por João Miguel de Castro Menna em parceria com GitHub Copilot

Este projeto implementa 4 algoritmos clássicos de busca de padrão em texto com arquitetura orientada a objetos usando o padrão Strategy:

- Naive Search

- Rabin-Karp Search

- Knuth-Morris-Pratt (KMP)

- Boyer-Moore Search

A aplicação permite processar um ou mais arquivos .txt, escolher um algoritmo específico ou executar todos, e comparar desempenho real com complexidade teórica.

## Objetivo

Buscar uma string padrão dentro de textos e exibir, para cada algoritmo executado:

- Tempo de execução

- Número de comparações relacionadas

- Tamanho do texto (n)

- Tamanho do padrão (m)

- Quantidade de ocorrências e posições encontradas

- Complexidade teórica (melhor, médio e pior caso)

- Comparação entre comportamento real e esperado

## Arquitetura

A solução segue o padrão Strategy:

- Interface abstrata SearchStrategy define o contrato comum de busca

- Cada algoritmo é uma estratégia concreta com sua própria lógica

- A aplicação principal escolhe e executa estratégias em tempo de execução

Estrutura conceitual:

- SearchStrategy (abstrata)

- NaiveSearch

- RabinKarpSearch

- KMPSearch

- BoyerMooreSearch

## Como Executar

Pré-requisitos:

- Windows, Linux ou macOS

- Python 3.10+

Exemplos de execução:

1. Executar todos os algoritmos em um arquivo:

   python main.py text.txt -p "the" -a all

2. Executar apenas KMP:

   python main.py text.txt -p "the" -a kmp

3. Executar em múltiplos arquivos:

   python main.py texto1.txt texto2.txt texto3.txt -p "padrao" -a all

4. Modo passo a passo (log detalhado):

   python main.py text.txt -p "the" -a boyer-moore --step-by-step

## Parâmetros da CLI

- files: um ou mais arquivos .txt

- -p, --pattern: string/padrão a ser buscado (obrigatório)

- -a, --algorithm: naive | rabin-karp | kmp | boyer-moore | all

- --step-by-step: habilita log detalhado da execução

## Saída e Métricas

Para cada execução, a aplicação mostra:

- Algoritmo

- Arquivo processado

- Tamanho do texto e do padrão

- Total de ocorrências e lista de posições

- Tempo de execução em ms

- Total de comparações relacionadas

- Complexidade teórica:
  
  - Melhor caso
  
  - Caso médio
  
  - Pior caso

- Comparação real vs esperado:
  - Escala esperada aproximada para o caso médio
  - Razão comparações / escala esperada
  - Tempo médio por comparação

## Complexidades Teóricas

- Naive
  - Melhor: O(n)
  - Médio: O(n * m)
  - Pior: O(n * m)

- Rabin-Karp
  - Melhor: O(n + m)
  - Médio: O(n + m)
  - Pior: O(n * m)

- KMP
  - Melhor: O(n + m)
  - Médio: O(n + m)
  - Pior: O(n + m)

- Boyer-Moore (bad character)
  - Melhor: O(n / m)
  - Médio: O(n)
  - Pior: O(n * m)

## Explicação dos Algoritmos Implementados

### 1. Naive Search

O algoritmo ingênuo testa o padrão em todas as posições possíveis do texto.

- Ideia: alinhar o padrão ao texto e comparar caractere a caractere.

- Vantagem: implementação simples e fácil de entender.

- Limitação: pode repetir muitas comparações já feitas, principalmente em textos longos.

### 2. Rabin-Karp

Usa hash para comparar o padrão com cada janela do texto.

- Ideia: calcular hash do padrão e hash da janela atual; só compara caractere a caractere quando os hashes coincidem.

- Vantagem: costuma reduzir comparações diretas entre caracteres.

- Limitação: colisões de hash podem provocar verificações extras; no pior caso pode degradar.

### 3. Knuth-Morris-Pratt (KMP)

Evita retrocessos desnecessários no texto usando a tabela LPS (Longest Prefix Suffix).

- Ideia: quando há falha, usa informação de prefixo/sufixo já conhecida para continuar da melhor posição.

- Vantagem: garante complexidade linear O(n + m).

- Limitação: precisa de pré-processamento do padrão (tabela LPS).

### 4. Boyer-Moore (bad character)

Compara o padrão da direita para a esquerda e usa saltos maiores quando encontra mismatch.

- Ideia: usar heurística de caractere ruim para pular várias posições.

- Vantagem: excelente na prática para muitos textos reais, principalmente com padrão maior.

- Limitação: em cenários desfavoráveis pode se aproximar do pior caso O(n * m).

## Análise Comparativa de Desempenho

Exemplo real obtido com:

- Arquivo: text.txt

- Tamanho do texto: n = 49474

- Padrão: "the" (m = 3)

- Execução: todos os algoritmos

<div>
    <table>
        <thead>
            <tr>
                <th>Algoritmo</th>
                <th>Tempo (ms)</th>
                <th>Comparações</th>
                <th>Razão comp./escala esperada</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Naive</td>
                <td>6.4667</td>
                <td>53392</td>
                <td>0.3597</td>
            </tr>
            <tr>
                <td>Rabin-Karp</td>
                <td>8.0282</td>
                <td>1598</td>
                <td>0.0323</td>
            </tr>
            <tr>
                <td>KMP</td>
                <td>4.1449</td>
                <td>52310</td>
                <td>1.0573</td>
            </tr>
            <tr>
                <td>Boyer-Moore</td>
                <td>3.8446</td>
                <td>19940</td>
                <td>0.4030</td>
            </tr>
        </tbody>
    </table>
</div>

Leituras importantes desses dados:

- Boyer-Moore foi o mais rápido nesse cenário específico.

- KMP ficou próximo do melhor tempo e manteve comportamento linear estável.

- Rabin-Karp fez poucas comparações de caracteres, mas teve overhead de hash que impactou o tempo total nesse teste.

- Naive teve desempenho aceitável para padrão curto, mas tende a escalar pior em casos gerais.

Observação: tempo absoluto varia por hardware, versão do interpretador e conteúdo do texto. A comparação entre algoritmos é mais útil quando repetida em vários tamanhos de entrada e padrões diferentes.

## Discussão: Quando Cada Algoritmo É Mais Eficiente

### Use Naive quando

- você precisa de uma solução didática e rápida de implementar;

- os textos são pequenos;

- a simplicidade é mais importante que otimização.

### Use Rabin-Karp quando

- você quer buscar muitos padrões ou fazer filtragem por hash;

- há interesse em reduzir verificações caractere a caractere;

- colisões não são um problema crítico no seu conjunto de dados.

### Use KMP quando

- você precisa de desempenho previsível e robusto;

- quer evitar degradação para casos ruins;

- o padrão é reutilizado várias vezes (o custo da LPS compensa).

### Use Boyer-Moore quando

- o padrão não é muito curto;

- o alfabeto é razoavelmente grande;

- você busca alta performance prática em textos longos.

Resumo prático:

- Melhor equilíbrio teórico: KMP.

- Melhor desempenho observado neste experimento: Boyer-Moore.

- Melhor simplicidade: Naive.

- Melhor estratégia baseada em hash: Rabin-Karp.

## Observações

- Arquivos são lidos em UTF-8 com substituição de caracteres inválidos.

- O modo passo a passo possui limite de logs para evitar saída excessiva.

- Resultados de tempo podem variar conforme máquina, sistema operacional e carga do processador.
