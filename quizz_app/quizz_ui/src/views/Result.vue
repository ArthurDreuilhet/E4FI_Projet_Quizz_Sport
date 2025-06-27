<template>
    <div class="result-container">
        <h1>Résultats du Quiz</h1>
        
        <div class="current-player-section" v-if="currentPlayer">
            <h2>Votre Score</h2>
            <div class="current-player-card">
                <span class="player-name">{{ currentPlayer.playerName }}</span>
                <span class="player-score">{{ currentPlayer.score }} points ⭐</span>
            </div>
        </div>
        <div class="ranking-section">
            <h2>Classement Général</h2>
            <div v-if="displayedParticipants.length > 0" class="participants-list">
                <div 
                    v-for="(participant, index) in displayedParticipants" 
                    :key="index"
                    :class="['participant-item', { 'current-player-highlight': isCurrentPlayer(participant) }]"
                >
                    <span class="rank">{{ index + 1 }}.</span>
                    <span class="name">{{ participant.playerName }}</span>
                    <span class="score">{{ participant.score }} points</span>
                </div>
                <div v-if="allParticipants.length > maxVisibleParticipants" class="more-participants">
                    ... et {{ allParticipants.length - maxVisibleParticipants }} autres participants
                </div>
            </div>
            <div v-else class="no-participants">
                Aucun participant pour le moment.
            </div>
        </div>
        
        <div class="actions">
            <button @click="goHome" class="home-btn">Accueil</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '@/services/QuizApiService';
import ParticipationStorageService from '@/services/Participation_storage_service';

const router = useRouter();
const allParticipants = ref([]);
const currentPlayer = ref(null);
const maxVisibleParticipants = ref(5);

const isCurrentPlayer = (participant) => {
    return currentPlayer.value && participant.playerName === currentPlayer.value.playerName;
};

const calculateMaxVisibleParticipants = () => {
    const windowHeight = window.innerHeight;
    const headerHeight = 150;
    const currentPlayerHeight = 120;
    const actionsHeight = 80;
    const sectionPadding = 100;
    const participantItemHeight = 65;
    
    const availableHeight = windowHeight - headerHeight - currentPlayerHeight - actionsHeight - sectionPadding;
    const maxItems = Math.floor(availableHeight / participantItemHeight);
    
    maxVisibleParticipants.value = Math.max(3, Math.min(maxItems, 10));
};

const displayedParticipants = computed(() => {
    return allParticipants.value.slice(0, maxVisibleParticipants.value);
});

const loadParticipants = async () => {
    try {
        const participants = await QuizApiService.get_all_participations();
        if (participants) {
            allParticipants.value = participants;
            
            const currentPlayerName = ParticipationStorageService.getPlayerName();
            const currentPlayerScore = ParticipationStorageService.getParticipationScore();
            
            if (currentPlayerName) {
                currentPlayer.value = {
                    playerName: currentPlayerName,
                    score: currentPlayerScore || 0
                };
            }
        }
    } catch (error) {
        console.error('Error loading participants:', error);
    }
};

const goHome = () => {
    router.push('/');
};

onMounted(() => {
    calculateMaxVisibleParticipants();
    loadParticipants();
    
    window.addEventListener('resize', calculateMaxVisibleParticipants);
});
</script>

<style scoped>
.result-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: transparent;
}

h1 {
    text-align: center;
    color: #003561;
    margin-bottom: 30px;
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5em;
}

h2 {
    color: #003561;
    margin-bottom: 15px;
    font-weight: 600;
}

.current-player-section {
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 30px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 32px rgba(35, 147, 205, 0.3);
    border: 1px solid rgba(116, 86, 219, 0.3);
}

.current-player-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    margin-top: 10px;
}

.current-player-card .player-name {
    font-size: 1.2em;
    font-weight: bold;
}

.current-player-card .player-score {
    font-size: 1.1em;
    font-weight: bold;
}

/* Classement général */
.ranking-section {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0, 53, 97, 0.1);
    border: 1px solid rgba(35, 147, 205, 0.2);
}

.participants-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.participant-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(174, 162, 208, 0.1) 100%);
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0, 53, 97, 0.1);
    transition: transform 0.2s;
    border: 1px solid rgba(35, 147, 205, 0.1);
}

.participant-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(35, 147, 205, 0.2);
}

.current-player-highlight {
    background: linear-gradient(135deg, #d9c47a 0%, #f1abc9 100%) !important;
    border: 2px solid #003561 !important;
    font-weight: bold;
    box-shadow: 0 4px 15px rgba(217, 196, 122, 0.4) !important;
    color: #003561 !important;
}

.rank {
    font-weight: bold;
    color: #2393cd;
    min-width: 30px;
}

.name {
    flex: 1;
    margin-left: 15px;
    font-size: 1.1em;
    color: #003561;
}

.score {
    font-weight: bold;
    color: #003561;
}

.no-participants {
    text-align: center;
    color: #003561;
    font-style: italic;
    padding: 20px;
}

.more-participants {
    text-align: center;
    color: #003561;
    font-style: italic;
    padding: 15px;
    background: rgba(174, 162, 208, 0.2);
    border-radius: 8px;
    margin-top: 10px;
    border: 1px solid rgba(116, 86, 219, 0.2);
}

.actions {
    display: flex;
    justify-content: center;
    gap: 20px;
}

.play-again-btn, .home-btn {
    padding: 12px 24px;
    border: none;
    border-radius: 25px;
    font-size: 1em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.play-again-btn {
    background: linear-gradient(135deg, #f1abc9 0%, #d9c47a 100%);
    color: #003561;
    border: 2px solid rgba(0, 53, 97, 0.1);
}

.play-again-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(241, 171, 201, 0.4);
    background: linear-gradient(135deg, #d9c47a 0%, #AEA2D0 100%);
}

.home-btn {
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    color: white;
    border: 2px solid rgba(35, 147, 205, 0.1);
}

.home-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(35, 147, 205, 0.4);
    background: linear-gradient(135deg, #7456db 0%, #AEA2D0 100%);
}

@media (max-width: 600px) {
    .current-player-card {
        flex-direction: column;
        gap: 10px;
    }
    
    .participant-item {
        flex-direction: column;
        text-align: center;
        gap: 5px;
    }
    
    .actions {
        flex-direction: column;
        align-items: center;
    }
}
</style>