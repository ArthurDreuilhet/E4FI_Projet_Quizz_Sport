<script setup>
import { ref } from 'vue'

const playerName = ('') => {}
</script>

<template>
  <div class="quizz">
    <h1>This is the quizz page</h1>
    <p>saisissez votre nom</p>
    <input type="text" v-model="playerName" placeholder="Votre nom" />
    <button @click="launchNewQuiz"></button>
    <router-link to="/new-quiz">Démarrer le quiz !</router-link>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
