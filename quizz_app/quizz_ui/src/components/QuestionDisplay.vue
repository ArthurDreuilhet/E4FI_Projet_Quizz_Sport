<script setup>
import { onMounted, ref, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import Checkbox from 'primevue/checkbox';
import ParticipationStorageService from '@/services/Participation_storage_service';

const props = defineProps({
    question: {
        type: Object,
        required: true
    }
});



onMounted(() => {
    console.log('QuestionDisplay component mounted with question:', props.question);
    // You can add any additional logic here if needed
});

</script>

<template>
    <h2 class="">Question {{ props.question.position }} : {{ props.question.title }}</h2>
    <img class="max_image" :src="props.question.image" alt="Question Image" />
    <p class="">{{ props.question.text }}</p>
    <ul class="">
        <li v-for="(option, index) in props.question.possibleAnswers" :key="index">
            <Checkbox v-model="checked" binary /> {{ option.text }}
        </li>
    </ul>
</template>

<style scoped>
.hundred {
    height: 100%;
    width: 100%;
}

.max_image {
    max-height: 100%;
    max-width: 100%;
}
</style>