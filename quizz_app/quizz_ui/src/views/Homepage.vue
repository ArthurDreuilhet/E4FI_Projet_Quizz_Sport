<script setup>
import { ref, onMounted } from 'vue'
import quizApiService from '@/services/QuizApiService'

const registeredScores = ref([])

onMounted(async () => {
  console.log('Home page mounted')
  const response = await quizApiService.getInfos()
  if (response && response.status === 200) {
    registeredScores.value = response.data
  } else {
    console.warn('Échec du chargement des scores enregistrés')
  }
})
</script>

<template>
  <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
</template>
