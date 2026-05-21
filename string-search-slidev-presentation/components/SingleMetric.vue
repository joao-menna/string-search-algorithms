<script setup lang="ts">
defineProps({
    getBiggestTime: {
        type: Function,
        required: true,
    },
    name: {
        type: String,
        required: true,
    },
    time: {
        type: String,
        required: true,
    },
    comparisons: {
        type: Number,
        required: true,
    },
})
</script>

<template>
    <div class="flex flex-col gap-2">
        <div class="flex gap-8 justify-between items-end">
            <span class="bg-[#44475a] text-[#f8f8f2] px-2 rounded-lg">{{ name }}</span>
            <div class="flex gap-2 bg-[#ffb86c] text-[#282a36] px-2 rounded-lg items-center">
                <span class="font-bold">{{ comparisons }}</span>
                <span>comparações</span>
            </div>
        </div>
        <div class="w-full h-8 bg-gray-600 rounded-lg overflow-hidden">
            <div
                class="h-full bg-[#50fa7b] text-[#282a36] rounded-lg flex justify-start items-center"
                :style="{
                    width: `${(parseFloat(time) / getBiggestTime()) * 100}%`,
                }"
            >
                <span class="ml-2">{{ time }}ms</span>
            </div>
        </div>
    </div>
</template>