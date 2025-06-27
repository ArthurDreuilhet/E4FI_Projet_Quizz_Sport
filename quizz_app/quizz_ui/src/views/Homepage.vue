<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import quizApiService from '@/services/QuizApiService'

const router = useRouter()
const quizInfo = ref(null)
const participants = ref([])
const maxVisibleParticipants = ref(4)

const startQuiz = () => {
  router.push('/start')
}

const calculateMaxVisibleParticipants = () => {
  const windowHeight = window.innerHeight
  const headerHeight = 200
  const startSectionHeight = 120
  const leaderboardHeaderHeight = 80
  const padding = 100
  const participantCardHeight = 90
  
  const availableHeight = windowHeight - headerHeight - startSectionHeight - leaderboardHeaderHeight - padding
  const maxItems = Math.floor(availableHeight / participantCardHeight)
  
  maxVisibleParticipants.value = Math.max(2, Math.min(maxItems, 8))
}

const displayedParticipants = computed(() => {
  return participants.value.slice(0, maxVisibleParticipants.value)
})

onMounted(async () => {
  console.log('Home page mounted')
  calculateMaxVisibleParticipants()
  
  const response = await quizApiService.getInfos()
  if (response && response.size) {
    quizInfo.value = response
    participants.value = response.scores || []
  } else {
    console.warn('Échec du chargement des informations du quiz')
  }
  
  window.addEventListener('resize', calculateMaxVisibleParticipants)
})
</script>

<template>
  <div class="homepage-container">
    <div class="quiz-header">
      <h1>🏆 Quiz Sport</h1>
      <p class="quiz-description">Testez vos connaissances sportives !</p>
      <div v-if="quizInfo" class="quiz-stats">
        <span class="question-count">{{ quizInfo.size }} questions</span>
        <span class="participant-count">{{ participants.length }} participants</span>
      </div>
    </div>

    <div class="start-section">
      <button @click="startQuiz" class="start-btn">
        🚀 Commencer le Quiz
      </button>
    </div>

    <div class="leaderboard-section" v-if="participants.length > 0">
      <h2>🎯 Tableau des Scores</h2>
      <div class="participants-grid">
        <div 
          v-for="(participant, index) in displayedParticipants" 
          :key="index"
          class="participant-card"
        >
          <div class="rank-badge">
            <span v-if="index === 0">🥇</span>
            <span v-else-if="index === 1">🥈</span>
            <span v-else-if="index === 2">🥉</span>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div class="participant-info">
            <div class="participant-name">{{ participant.playerName }}</div>
            <div class="participant-score">{{ participant.score }} points</div>
          </div>
        </div>
      </div>
      <div v-if="participants.length > maxVisibleParticipants" class="more-participants">
        ... et {{ participants.length - maxVisibleParticipants }} autres participants
      </div>
    </div>

    <div v-else class="no-participants">
      <p>🎯 Soyez le premier à jouer !</p>
    </div>
  </div>
</template>

<style scoped>
.homepage-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.quiz-header {
  text-align: center;
  margin-bottom: 40px;
}

.quiz-header h1 {
  font-size: 3em;
  color: #003561;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 2px 2px 4px rgba(0, 53, 97, 0.1);
}

.quiz-description {
  font-size: 1.2em;
  color: #003561;
  margin-bottom: 20px;
  font-weight: 500;
}

.quiz-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 15px;
}

.quiz-stats span {
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  color: #003561;
  box-shadow: 0 2px 8px rgba(0, 53, 97, 0.1);
  border: 1px solid rgba(35, 147, 205, 0.2);
}

.question-count {
  background: linear-gradient(135deg, #2393cd 0%, #7456db 100%) !important;
  color: white !important;
  box-shadow: 0 4px 15px rgba(35, 147, 205, 0.3) !important;
}

.participant-count {
  background: linear-gradient(135deg, #f1abc9 0%, #d9c47a 100%) !important;
  color: #003561 !important;
  box-shadow: 0 4px 15px rgba(241, 171, 201, 0.3) !important;
}

.start-section {
  text-align: center;
  margin-bottom: 50px;
}

.start-btn {
  background: linear-gradient(135deg, #d9c47a 0%, #f1abc9 100%);
  color: #003561;
  border: none;
  padding: 20px 40px;
  font-size: 1.3em;
  font-weight: bold;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(217, 196, 122, 0.4);
  border: 2px solid rgba(0, 53, 97, 0.1);
}

.start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(217, 196, 122, 0.6);
  background: linear-gradient(135deg, #f1abc9 0%, #AEA2D0 100%);
}

.start-btn:active {
  transform: translateY(-1px);
}

.leaderboard-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 20px;
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(0, 53, 97, 0.1);
  border: 1px solid rgba(35, 147, 205, 0.2);
}

.leaderboard-section h2 {
  text-align: center;
  color: #003561;
  margin-bottom: 25px;
  font-size: 1.8em;
  flex-shrink: 0;
  background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.participants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
  flex: 1;
  overflow: hidden;
}

.more-participants {
  text-align: center;
  color: #003561;
  font-style: italic;
  padding: 10px;
  background: rgba(174, 162, 208, 0.3);
  border-radius: 8px;
  margin-top: 15px;
  flex-shrink: 0;
  border: 1px solid rgba(116, 86, 219, 0.2);
}

.participant-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(174, 162, 208, 0.1) 100%);
  border-radius: 15px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 3px 10px rgba(0, 53, 97, 0.1);
  transition: all 0.3s ease;
  border: 1px solid rgba(35, 147, 205, 0.2);
}

.participant-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(35, 147, 205, 0.2);
  background: linear-gradient(135deg, rgba(241, 171, 201, 0.1) 0%, rgba(217, 196, 122, 0.1) 100%);
}

.rank-badge {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d9c47a 0%, #f1abc9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2em;
  margin-right: 15px;
  color: #003561;
  box-shadow: 0 3px 10px rgba(217, 196, 122, 0.3);
  border: 2px solid rgba(0, 53, 97, 0.1);
}

.participant-info {
  flex: 1;
}

.participant-name {
  font-size: 1.1em;
  font-weight: bold;
  color: #003561;
  margin-bottom: 5px;
}

.participant-score {
  color: #2393cd;
  font-weight: 600;
}

.no-participants {
  text-align: center;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 40px;
  color: #003561;
  font-size: 1.2em;
  box-shadow: 0 4px 15px rgba(0, 53, 97, 0.1);
  border: 1px solid rgba(35, 147, 205, 0.2);
}

@media (max-width: 768px) {
  .quiz-header h1 {
    font-size: 2.5em;
  }
  
  .quiz-stats {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
  
  .start-btn {
    padding: 15px 30px;
    font-size: 1.1em;
  }
  
  .participants-grid {
    grid-template-columns: 1fr;
  }
  
  .participant-card {
    padding: 15px;
  }
}

@media (max-width: 480px) {
  .homepage-container {
    padding: 15px;
  }
  
  .quiz-header h1 {
    font-size: 2em;
  }
  
  .start-btn {
    padding: 12px 25px;
    font-size: 1em;
  }
}
</style>
