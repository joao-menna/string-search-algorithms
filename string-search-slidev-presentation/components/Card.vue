<script setup lang="ts">
defineProps({
    title: {
        type: String,
    },
    icon: {
        type: String,
    },
    description: {
        type: String,
    }
})
</script>

<template>
    <div class="border rounded-lg p-4 bg-cyan/10 text-left flex flex-col items-center gap-2 shadow">
        <font-awesome-icon v-if="!!icon" :icon="icon" size="xl" class="text-[#8be9fd]" />
        <h4 v-if="!!title">{{ title }}</h4>
        <span v-if="!!description">{{ description }}</span>
    </div>
</template>
