<script setup>
import { onMounted, ref } from 'vue'
import { InputText, Button } from 'primevue';
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
  <div class="quizz">
    <h1 class="text-3xl font-bold underline">This is the quizz page</h1>
    <p class="text-lg">saisissez votre nom : </p>
    <div class="flex flex-col items-start justify-center gap-4">
      <InputText type="text" v-model="playerName" placeholder="Votre nom" />
      <Button label="GO" variant="outlined" type="submit" severity="secondary" @click="launchNewQuizz"></Button>
      <p class="text-lg">Bienvenue {{ playerName }} !</p>
      <router-link to="/new-quiz">Démarrer le quiz !</router-link>
    </div>
  </div>


</template>

<style>
@import "tailwindcss";


</style>
