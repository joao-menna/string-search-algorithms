<script lang="ts" setup>
import { ref } from 'vue';

const rows = ref([
    {
        flag: "files",
        description: "Caminho(s) para arquivos ou diretórios",
        example: "./data/logs",
    },
    {
        flag: "-p, --pattern",
        description: "O termo de busca (string)",
        example: '"ERROR"',
    },
    {
        flag: "-a, --algorithm",
        description: "Seleção da estratégia",
        example: "(naive|rabin-karp|boyer-moore|kmp|all)",
    },
    {
        flag: "--step-by-step",
        description: "Ativa modo visualização detalhada",
        example: "--step-by-step",
    },
    {
        flag: "--telemetry-dir",
        description: "Diretório para salvar os logs JSONL",
        example: "./otel_data",
    },
])
</script>

<template>
    <table class="border-spacing-0 overflow-hidden rounded-lg">
        <thead class=" text-[#8be9fd]">
            <tr class="bg-slate-600/80">
                <th>Flag</th>
                <th>Descrição</th>
                <th>Exemplo</th>
            </tr>
        </thead>
        <tbody class="text-sm bg-slate-600/20">
            <tr v-for="row in rows" class="overflow-hidden">
                <td>
                    <pre>{{ row.flag }}</pre>
                </td>
                <td>{{ row.description }}</td>
                <td>
                    <pre>{{ row.example }}</pre>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style>
    tbody tr:last-child {
        border-bottom: 0 !important;
    }
</style>
