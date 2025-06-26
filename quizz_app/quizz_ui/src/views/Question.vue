<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import QuizApiService from '@/services/QuizApiService';
import ParticipationStorageService from '@/services/Participation_storage_service';

const router = useRouter();
const quiz_infos = ref({});
const playerName = ref('');
const question = ref([]);

const num_questions = ref(0);

const quizzAnswers = ref();

const score = ref([]);

const page_suivante = async () => {
    console.log('Proceeding to next question:', question.value[num_questions.value]);
    if (quizzAnswers.value === undefined) {
        alert('Please select an answer before proceeding to the next question.');
        return; // Prevent proceeding without an answer
    }
    score.value.push(quizzAnswers.value);
    console.log('Incorrect answer selected, score remains:', score.value);
    
    quizzAnswers.value = undefined; // Reset the answer selection for the next question
    if (num_questions.value < quiz_infos.value.size - 1) {
        num_questions.value++;
    } else {
        ParticipationStorageService.savePlayerName(playerName.value);
        console.log("Joueur : ", playerName.value, score.value)
        const result = await QuizApiService.post_participations(playerName.value, score.value);
        ParticipationStorageService.saveParticipationScore(result.score);
        console.log('Participation result:', result);
        console.log(`Quiz completed by ${playerName.value}!`);
        console.log('Final score:', result.score);
        router.push('/result');
    }
}

const get_Question = async () => {
    console.log('Fetching questions...');
    question.value = []; // Reset array
    
    if (!quiz_infos.value.size) {
        console.error('No quiz size found');
        return;
    }
    
    for (let index = 0; index < quiz_infos.value.size; index++) {
        console.log('Fetching question for index: ', index + 1);
        try {
            const quest = await QuizApiService.get_Question(index + 1);
            console.log('Question fetched: ', quest);
            if (quest) {
                question.value.push(quest);
            }
        } catch (error) {
            console.error('Error fetching question:', error);
        }
    }
    console.log('All questions loaded:', question.value);
}

const handlMessage = (event) => {
    const { type, data } = event.data;
    if (type === 'answerSelected') {

        console.log('Answer selected from upper:', data);
        quizzAnswers.value = data;
        
    }
}

onMounted(async () => {
    console.log('=== Question.vue onMounted started ===');
    window.addEventListener('message', handlMessage);
    playerName.value = ParticipationStorageService.getPlayerName() || '';
    console.log('Player name:', playerName.value);
    
    try {
        // Utilisation de l'API réelle pour récupérer les questions
        console.log('Fetching real quiz data from API...');
        quiz_infos.value = await QuizApiService.getInfos();
        console.log('Quiz infos fetched:', quiz_infos.value);
        
        if (quiz_infos.value && quiz_infos.value.size > 0) {
            await get_Question();
            console.log('Questions loaded, count:', question.value.length);
        }
    } catch (error) {
        console.error('Error in onMounted:', error);
    }
    
    console.log('=== Question.vue onMounted finished ===');
});

onUnmounted(() => {
    window.removeEventListener('message', handlMessage);
    console.log('Event listener removed');
});
</script>


<template>
    <div class="question-page-container">
        <div class="question-header">
            <h1 class="page-title">Quiz - Question {{ num_questions + 1 }}/{{ quiz_infos.size || '?' }}</h1>
            <div class="progress-bar" v-if="quiz_infos.size > 0">
                <div class="progress-fill" :style="{ width: ((num_questions + 1) / quiz_infos.size) * 100 + '%' }"></div>
            </div>
            <!-- Debug info (à supprimer en production) -->
            <div class="debug-info" v-if="false">
                <p style="font-size: 0.8em; color: #666;">
                    Debug: Questions loaded: {{ question.length }}, Quiz size: {{ quiz_infos.size }}, Current: {{ num_questions }}
                </p>
            </div>
        </div>
        <div class="question-content" v-if="question.length > 0 && question[num_questions]">
            <QuestionDisplay :question="question[num_questions]" />
        </div>
        
        <div class="question-loading" v-else-if="quiz_infos.size && quiz_infos.size > 0">
            <p>🔄 Chargement de la question...</p>
        </div>
        
        <div class="no-questions" v-else>
            <p>❌ Aucune question disponible</p>
        </div>
        
        <div class="question-navigation">
            <button @click="page_suivante" class="next-question-btn" :disabled="quizzAnswers === undefined">
                {{ num_questions === quiz_infos.size - 1 ? '🏁 Terminer le Quiz' : '➡️ Question Suivante' }}
            </button>
            <p v-if="quizzAnswers === undefined" class="selection-hint">
                ⚠️ Veuillez sélectionner une réponse avant de continuer
            </p>
        </div>
    </div>
</template>

<style scoped>
.question-page-container {
    max-width: 1000px;
    width: 100%;
    margin: 0 auto;
    padding: 20px;
    height: calc(90vh - 40px); /* Utilise la hauteur disponible moins les paddings */
    display: flex;
    flex-direction: column;
    gap: 20px; /* Réduit l'espacement pour optimiser l'espace */
    background: transparent;
    overflow: hidden; /* Empêche le scroll global du container */
    box-sizing: border-box;
}

.question-header {
    text-align: center;
    margin-bottom: 10px; /* Réduit la marge */
    flex-shrink: 0; /* Empêche la compression */
}

.page-title {
    color: #003561;
    font-size: 2em; /* Légèrement réduit pour économiser l'espace */
    font-weight: bold;
    margin-bottom: 15px; /* Réduit la marge */
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.progress-bar {
    width: 100%;
    height: 10px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    overflow: hidden;
    border: 2px solid rgba(35, 147, 205, 0.3);
}

.progress-fill {
    height: 100%;
    background: linear-gradient(135deg, #f1abc9 0%, #d9c47a 100%);
    transition: width 0.5s ease;
    border-radius: 8px;
}

.question-content {
    flex: 1; /* Prend tout l'espace disponible */
    display: flex;
    justify-content: center;
    align-items: stretch; /* Permet au contenu d'utiliser toute la hauteur */
    padding: 10px 0; /* Réduit le padding */
    overflow: hidden; /* Empêche le débordement */
    min-height: 0; /* Permet la réduction si nécessaire */
}

.question-loading,
.no-questions {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 20px;
    text-align: center;
}

.question-loading p,
.no-questions p {
    font-size: 1.5em;
    color: #003561;
    background: rgba(255, 255, 255, 0.9);
    padding: 30px 40px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 53, 97, 0.1);
    border: 1px solid rgba(35, 147, 205, 0.2);
}

.question-loading p {
    background: linear-gradient(135deg, rgba(241, 171, 201, 0.1) 0%, rgba(217, 196, 122, 0.1) 100%);
    border-color: #f1abc9;
}

.no-questions p {
    background: linear-gradient(135deg, rgba(66, 9, 51, 0.1) 0%, rgba(0, 53, 97, 0.1) 100%);
    border-color: #420933;
    color: #420933;
}

.question-navigation {
    text-align: center;
    padding: 15px; /* Réduit le padding */
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 53, 97, 0.1);
    border: 1px solid rgba(35, 147, 205, 0.2);
    flex-shrink: 0; /* Empêche la compression */
}

.next-question-btn {
    background: linear-gradient(135deg, #d9c47a 0%, #f1abc9 100%);
    color: #003561;
    border: none;
    padding: 15px 40px;
    font-size: 1.2em;
    font-weight: bold;
    border-radius: 30px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(217, 196, 122, 0.4);
    border: 2px solid rgba(0, 53, 97, 0.1);
}

.next-question-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #f1abc9 0%, #AEA2D0 100%);
    transform: translateY(-3px);
    box-shadow: 0 6px 25px rgba(241, 171, 201, 0.5);
}

.next-question-btn:disabled {
    background: linear-gradient(135deg, #AEA2D0 0%, rgba(174, 162, 208, 0.5) 100%);
    color: rgba(0, 53, 97, 0.5);
    cursor: not-allowed;
    transform: none;
    box-shadow: 0 2px 8px rgba(174, 162, 208, 0.3);
}

.selection-hint {
    color: #003561;
    font-size: 1em;
    margin-top: 15px;
    font-weight: 500;
    background: rgba(241, 171, 201, 0.2);
    padding: 10px 20px;
    border-radius: 10px;
    border: 1px solid rgba(241, 171, 201, 0.4);
    display: inline-block;
}

@media (max-width: 768px) {
    .question-page-container {
        padding: 15px;
        gap: 15px; /* Réduit l'espacement sur mobile */
        height: calc(90vh - 30px); /* Ajuste pour le padding réduit */
    }
    
    .page-title {
        font-size: 1.6em; /* Plus petit sur mobile */
        margin-bottom: 10px;
    }
    
    .next-question-btn {
        padding: 12px 30px;
        font-size: 1.1em;
    }
    
    .selection-hint {
        font-size: 0.9em;
        padding: 8px 15px;
    }
    
    .question-navigation {
        padding: 12px; /* Réduit sur mobile */
    }
}

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