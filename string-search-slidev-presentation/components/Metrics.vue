<script setup lang="ts">
import { ref } from 'vue';
import SingleMetric from './SingleMetric.vue';
import { ComparisonScreenType } from './MetricSelector.vue';
import { AnimatePresence, motion } from 'motion-v';

const screen = ref<ComparisonScreenType>('not-stepped')

const runsNormal = ref([
    {
        name: 'Naive',
        time: '11.17',
        comparisons: 87965,
    },
    {
        name: 'Rabin-Karp',
        time: '13.47',
        comparisons: 862,
    },
    {
        name: 'KMP',
        time: '6.52',
        comparisons: 87973,
    },
    {
        name: 'Boyer-Moore',
        time: '1.46',
        comparisons: 7708,
    },
])

const runsStepped = ref([
    {
        name: 'Naive',
        time: '43.00',
        comparisons: 87965,
    },
    {
        name: 'Rabin-Karp',
        time: '33.86',
        comparisons: 862,
    },
    {
        name: 'KMP',
        time: '25.20',
        comparisons: 87973,
    },
    {
        name: 'Boyer-Moore',
        time: '5.65',
        comparisons: 7708,
    },
])

function handleScreenChange(screenType: ComparisonScreenType) {
    screen.value = screenType;
}

function getBiggestTime(runs: { time: string }[]) {
    return Math.max(...runs.map(run => parseFloat(run.time)))
}
</script>

<template>
    <div class="flex flex-col items-center gap-4 h-full">
        <MetricSelector @screen-change="handleScreenChange" />

        <div class="size-full relative">
            <motion.div
            >
                <AnimatePresence>
                    <motion.div
                        class="flex flex-col gap-4 size-full absolute"
                        v-if="screen === 'not-stepped'"
                        layout
                        :initial="{ opacity: 0, x: -120 }"
                        :animate="{ opacity: 1, x: 0 }"
                        :exit="{ opacity: 0, x: -120 }"
                    >
                        <SingleMetric
                            v-for="row in runsNormal"
                            :key="row.name"
                            :name="row.name"
                            :time="row.time"
                            :comparisons="row.comparisons"
                            :getBiggestTime="() => getBiggestTime(runsNormal)"
                        />
                    </motion.div>
                    <motion.div
                        class="flex flex-col gap-4 size-full absolute"
                        v-if="screen === 'stepped'"
                        layout
                        :initial="{ opacity: 0, x: 120 }"
                        :animate="{ opacity: 1, x: 0 }"
                        :exit="{ opacity: 0, x: 120 }"
                    >
                    <SingleMetric
                        v-for="row in runsStepped"
                        :key="row.name"
                        :name="row.name"
                        :time="row.time"
                        :comparisons="row.comparisons"
                        :getBiggestTime="() => getBiggestTime(runsStepped)"
                    />
                    </motion.div>
                </AnimatePresence>
            </motion.div>
        </div>
    </div>
</template>