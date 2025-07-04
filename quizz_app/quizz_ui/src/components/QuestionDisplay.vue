<script setup>
import { onMounted, ref, defineProps, watch } from 'vue';
import { useRouter } from 'vue-router';
import ParticipationStorageService from '@/services/Participation_storage_service';

const props = defineProps({
    question: {
        type: Object,
        required: true
    }
});

const selectedAnswer = ref(null);

watch(() => props.question, (newQuestion) => {
    console.log('Question updated:', newQuestion);
    selectedAnswer.value = null;
});

const selectAnswer = (index) => {
    selectedAnswer.value = index;
    console.log('Answer selected at index:', index);
    window.postMessage({type: 'answerSelected', data: index});
    
}

onMounted(() => {
    selectedAnswer.value = null;
    console.log('QuestionDisplay component mounted with question:', props.question);

});

</script>

<template>
    <div class="question-container card">
        <h2 class="question-title">Question {{ props.question.position }} : {{ props.question.title }}</h2>
        <div class="question-image-container" v-if="props.question.image">
            <img class="question-image" :src="props.question.image" alt="Question Image" />
        </div>
        <p class="question-text">{{ props.question.text }}</p>
        <ul class="answers-list">
            <li v-for="(option, index) in props.question.possibleAnswers" :key="index" class="answer-item">
                <div class="answer-option" :class="{ 'selected': selectedAnswer === index }" @click="selectAnswer(index)">
                    <input 
                        type="radio"
                        :id="`answer-${index}`"
                        :value="index" 
                        v-model="selectedAnswer"
                        @change="selectAnswer(index)"
                        class="radio-input"
                    /> 
                    <label :for="`answer-${index}`" class="answer-label">{{ option.text }}</label>
                </div>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.question-container {
    max-width: 800px;
    width: 100%;
    height: 100%;
    margin: 0 auto;
    font-family: 'Arial', sans-serif;
    display: flex;
    flex-direction: column;
    padding: 15px;
    box-sizing: border-box;
    overflow: hidden;
}

.question-title {
    color: var(--text-primary);
    font-size: 1.4em;
    font-weight: bold;
    margin-bottom: 12px;
    text-align: center;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    flex-shrink: 0;
}

.question-image-container {
    text-align: center;
    margin: 10px 0;
    flex-shrink: 0;
}

.question-image {
    max-height: 150px;
    max-width: 100%;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 53, 97, 0.1);
    border: 2px solid rgba(35, 147, 205, 0.2);
}

.question-text {
    font-size: 1em;
    color: var(--text-primary);
    line-height: 1.4;
    margin-bottom: 15px;
    text-align: center;
    font-weight: 500;
    flex-shrink: 0;
}

.answers-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
    overflow-y: auto;
    max-height: 100%;
    padding-right: 5px;
}

.answer-item {
    margin: 0;
    flex-shrink: 0;
}

.answer-option {
    display: flex;
    align-items: center;
    padding: 10px 14px;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(174, 162, 208, 0.1) 100%);
    border: 2px solid var(--border-primary);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 53, 97, 0.1);
}

.answer-option:hover {
    background: var(--gradient-accent);
    border-color: var(--border-secondary);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(241, 171, 201, 0.3);
}

.answer-option.selected {
    background: var(--gradient-secondary);
    border-color: var(--border-focus);
    border-width: 3px;
    color: var(--text-primary);
    font-weight: bold;
    box-shadow: 0 6px 20px rgba(217, 196, 122, 0.4);
}

.radio-input {
    margin-right: 15px;
    accent-color: var(--quiz-navy);
}

.answer-label {
    flex: 1;
    font-size: 1.1em;
    color: inherit;
    cursor: pointer;
    font-weight: inherit;
}

.selected .answer-label {
    color: #003561;
    font-weight: bold;
}

@media (max-width: 768px) {
    .question-container {
        padding: 15px;
        margin: 5px;
    }
    
    .question-title {
        font-size: 1.3em;
        margin-bottom: 10px;
    }
    
    .question-text {
        font-size: 0.95em;
        margin-bottom: 12px;
    }
    
    .answer-option {
        padding: 10px 12px;
    }
    
    .answer-label {
        font-size: 0.95em;
    }
    
    .question-image {
        max-height: 120px;
    }
}

.hundred {
    height: 100%;
    width: 100%;
}

.max_image {
    max-height: 100%;
    max-width: 100%;
}
</style>