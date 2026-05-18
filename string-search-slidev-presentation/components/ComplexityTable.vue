<script setup lang="ts">
import { ref } from 'vue';
import { renderToString } from 'katex';

const rows = ref([
    {
        algorithm: "Naive",
        bestCase: renderToString("O(n)"),
        worstCase: renderToString("O(n \\times m)"),
        additionalSpace: renderToString("O(1)")
    },
    {
        algorithm: "Rabin-Karp",
        bestCase: renderToString("O(n + m)"),
        worstCase: renderToString("O(n \\times m)"),
        additionalSpace: renderToString("O(1)")
    },
    {
        algorithm: "KMP",
        bestCase: renderToString("O(n)"),
        worstCase: renderToString("O(n)"),
        additionalSpace: renderToString("O(m)")
    },
    {
        algorithm: "Boyer-Moore",
        bestCase: renderToString("O(n / m)"),
        worstCase: renderToString("O(n \\times m)"),
        additionalSpace: renderToString("O(m + \\Sigma)")
    },
])
</script>

<template>
    <table class="border-spacing-0 overflow-hidden rounded-lg">
        <thead class=" text-[#8be9fd]">
            <tr class="bg-slate-600/80">
                <th>Algoritmo</th>
                <th>Melhor Caso</th>
                <th>Pior Caso</th>
                <th>Espaço Adicional</th>
            </tr>
        </thead>
        <tbody class="text-sm bg-slate-600/20">
            <tr v-for="row in rows" class="overflow-hidden">
                <td>
                    <pre>{{ row.algorithm }}</pre>
                </td>
                <td v-html="row.bestCase"></td>
                <td v-html="row.worstCase"></td>
                <td v-html="row.additionalSpace"></td>
            </tr>
        </tbody>
    </table>
</template>