<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'


const count = ref(0)

const inc = () => {
  count.value += 1
}
</script>

<template>
  <div class="px-8" style="height: 100%; width: 100vw;">
    <header  style="width: 100%; height: 10vh; padding-right: 0px; background-color: var(--color-bg);">
      <div class="wrapper">
        <nav class="flex items-center justify-between">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/start">Start</RouterLink>
          <RouterLink to="/admin">Admin</RouterLink>
        </nav>
      </div>
    </header>
    <div style="height: 90vh; width: 100%; padding: 0px; background-color: var(--color-bg); display: flex; flex-direction: column; align-items: center; ">
      <RouterView />
    </div>
    
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.hundred{
  height: 100%;
  width: 100%;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-border);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-text);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
