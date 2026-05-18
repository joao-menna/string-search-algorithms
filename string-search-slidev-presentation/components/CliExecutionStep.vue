<script lang="ts" setup>
defineProps({
    isLast: {
        type: Boolean,
        required: true,
    },
    icon: {
        type: String,
        required: true,
    },
    iconColor: {
        type: String,
        required: true,
    },
    title: {
        type: String,
        required: true,
    },
})
</script>

<template>
    <div class="p-2 w-32 h-12 flex flex-col items-center justify-between gap-2">
        <font-awesome-icon :icon="icon" size="xl" :style="{ color: iconColor }" />
        <span class="text-[#f8f8f2] text-sm text-center">{{ title }}</span>
    </div>
    <div v-if="!isLast" class="self-center">
        <font-awesome-icon icon="fa-solid fa-arrow-right" size="xs" class="text-gray/20" />
    </div>
</template>