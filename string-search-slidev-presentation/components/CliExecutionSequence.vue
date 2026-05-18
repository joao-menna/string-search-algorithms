<script lang="ts" setup>
import CliExecutionStep from './CliExecutionStep.vue';

const steps = [
    {
        iconColor: '#ff79c6',
        icon: 'fa-solid fa-terminal',
        title: 'Entrada da CLI',
    },
    {
        iconColor: '#50fa7b',
        icon: 'fa-solid fa-gears',
        title: 'Leitura dos Arquivos',
    },
    {
        iconColor: '#8be9fd',
        icon: 'fa-solid fa-chart-line',
        title: 'Execução dos Algoritmos',
    },
    {
        iconColor: '#ffb86c',
        icon: 'fa-solid fa-satellite-dish',
        title: 'Telemetria (Spans)',
    },
    {
        iconColor: '#bd93f9',
        icon: 'fa-solid fa-square-poll-vertical',
        title: 'Resultados',
    },
];
</script>

<template>
    <div class="flex gap-4 h-24">
        <CliExecutionStep
            v-for="(step, index) in steps"
            :key="index"
            :isLast="index === steps.length - 1"
            :icon="step.icon"
            :iconColor="step.iconColor"
            :title="step.title"
        />
    </div>
</template>
