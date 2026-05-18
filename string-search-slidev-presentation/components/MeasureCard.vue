<script setup lang="ts">
defineProps({
    title: {
        type: String,
        required: true,
    },
    description: {
        type: String,
        required: true,
    },
})
</script>

<template>
    <div class="p-8 w-full border-b-4 border-b-cyan rounded-xl bg-slate-700/50 flex flex-col items-center">
        <span class="text-cyan text-6xl">{{ title }}</span>
        <span class="text-gray/40">{{ description.toUpperCase() }}</span>
    </div>
</template>
