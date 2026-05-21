<script setup lang="ts">
import { ref } from 'vue';

export type ComparisonScreenType = 'stepped' | 'not-stepped'

const screen = ref<ComparisonScreenType>('not-stepped');

const emit = defineEmits({
    'screen-change': (screenType: ComparisonScreenType) => {
        return screenType === 'stepped' || screenType === 'not-stepped';
    },
})

function setScreen(screenType: ComparisonScreenType) {
    screen.value = screenType;
    emit('screen-change', screenType);
}
</script>

<template>
    <div class="flex gap-4">
        <div class="" v-for="btn in ['not-stepped', 'stepped']">
            <button
                class="px-4 py-2 rounded-lg text-[#282a36] font-bold transition-colors duration-300"
                :class="{
                    'bg-[#ffb86c] text-[#282a36]': screen === btn,
                    'bg-[#44475a] text-[#f8f8f2]': screen !== btn,
                }"
                @click="setScreen(btn as ComparisonScreenType)"
            >
                {{ btn === 'not-stepped' ? 'Comparação normal' : '' }}
                {{ btn === 'stepped' ? 'Comparação stepped' : '' }}
            </button>
        </div>
    </div>
</template>
