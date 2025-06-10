<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import QuizApiService from '@/services/QuizApiService';
import ParticipationStorageService from '@/services/Participation_storage_service';

const router = useRouter();
const quiz_infos = ref({});
const playerName = ref('');
const question = ref([]);

const num_questions = ref(0);

const page_precedente = () => {
    if (num_questions.value > 0) {
        num_questions.value--;
    }
}

const page_suivante = () => {
    if (num_questions.value < quiz_infos.value.size - 1) {
        num_questions.value++;
    } else {
        ParticipationStorageService.savePlayerName(playerName.value);
        console.log(`Quiz completed by ${playerName.value}!`);
        router.push('/result');
    }
}

const get_Question = async () => {
    console.log('Fetching questions...');
    for (let index = 0; index < quiz_infos.value.size; index++) {
        console.log('Fetching question for index: ', index + 1);
        const quest = await QuizApiService.get_Question(index + 1);
        console.log('Question fetched: ', quest);
        question.value.push(quest);
    }
}

onMounted(async () => {
    playerName.value = ParticipationStorageService.getPlayerName() || '';
    console.log('Participation storage service initialized: ', playerName.value);
    quiz_infos.value = await QuizApiService.getInfos();
    console.log('Question fetched: ', quiz_infos.value);
    await get_Question();
    console.log('Questions loaded: ', question.value);
});
</script>


<template>
    <div class="question hundred">
        <div class="hundred">
            <h1 class="text-3xl font-bold underline">This is the question page</h1>
        </div>
        <div class="hundred affichage_question" v-if="question[num_questions]">
            <QuestionDisplay :question="question[num_questions]" />
        </div>
        <div class="hundred flex flex-row items-center justify-between gap-20">
            <button @click="page_precedente">Question Precedente</button>
            <button @click="page_suivante">Question Suivante</button>
        </div>
    </div>
</template>

<style>

.hundred {
    height: 100%;
    width: 100%;
}

.affichage_question {
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: 10% 50% 20% 20%;
    align-items: center;
    justify-items: center;
    gap: 0px;
}

.question {
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: 10% 80% 10%;
    align-items: center;
    justify-items: center;
    gap: 0px;
}
</style>