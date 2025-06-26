<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router';
import Participation_storage_service from '@/services/Participation_storage_service';

const router = useRouter();

const playerName = ref('')

const launchNewQuizz = () => {
  if (!playerName.value) {
    alert('Veuillez saisir votre nom avant de continuer !')
    return
  }
  Participation_storage_service.savePlayerName(playerName.value);
  console.log(`Bienvenue ${playerName.value} !`)
  router.push('/question');
}

onMounted(() => {
  playerName.value = Participation_storage_service.getPlayerName() || '';
  console.log('Participation storage service initialized : ', playerName.value);
});

</script>

<template>
  <div class="quiz-start-container">
    <div class="quiz-start-card">
      <h1 class="quiz-start-title">🏆 Commencer le Quiz</h1>
      <p class="quiz-start-description">Saisissez votre nom pour commencer l'aventure :</p>
      <div class="form-container">
        <input 
          type="text" 
          v-model="playerName" 
          placeholder="Votre nom" 
          class="player-input input-field"
          @keyup.enter="launchNewQuizz"
        />
        <button 
          type="submit" 
          @click="launchNewQuizz"
          class="start-button btn btn-secondary"
        >
          🚀 C'est parti !
        </button>
        <p v-if="playerName" class="welcome-message">Bienvenue {{ playerName }} ! 🎉</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz-start-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  padding: 20px;
}

.quiz-start-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 50px 40px;
  border-radius: 25px;
  box-shadow: 0 12px 40px rgba(0, 53, 97, 0.15);
  border: 2px solid rgba(35, 147, 205, 0.2);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.quiz-start-title {
  color: #003561;
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.quiz-start-description {
  color: #003561;
  font-size: 1.3em;
  margin-bottom: 40px;
  font-weight: 500;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.player-input {
  padding: 15px 20px;
  border: 3px solid #f1abc9;
  border-radius: 15px;
  font-size: 1.2em;
  text-align: center;
  color: #003561;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
}

.player-input:focus {
  border-color: #2393cd;
  box-shadow: 0 0 20px rgba(35, 147, 205, 0.3);
  outline: none;
}

.start-button {
  background: linear-gradient(135deg, #d9c47a 0%, #f1abc9 100%);
  color: #003561;
  border: 3px solid rgba(0, 53, 97, 0.1);
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.3em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(217, 196, 122, 0.4);
}

.start-button:hover {
  background: linear-gradient(135deg, #f1abc9 0%, #AEA2D0 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(241, 171, 201, 0.5);
}

.welcome-message {
  color: #003561;
  font-size: 1.2em;
  font-weight: 600;
  background: linear-gradient(135deg, rgba(174, 162, 208, 0.2) 0%, rgba(217, 196, 122, 0.2) 100%);
  padding: 15px 25px;
  border-radius: 15px;
  border: 2px solid rgba(116, 86, 219, 0.3);
}

@media (max-width: 600px) {
  .quiz-start-card {
    padding: 30px 25px;
    margin: 10px;
  }
  
  .quiz-start-title {
    font-size: 2em;
  }
  
  .quiz-start-description {
    font-size: 1.1em;
  }
  
  .player-input {
    font-size: 1.1em;
    padding: 12px 16px;
  }
  
  .start-button {
    font-size: 1.1em;
    padding: 12px 25px;
  }
}

.hundred {
  height: 100%;
  width: 100%;
}
</style>
