<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'


const count = ref(0)

const inc = () => {
  count.value += 1
}
</script>

<template>
  <div class="px-8 app-container">
    <header class="app-header">
      <div class="wrapper">
        <nav class="main-nav">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
          <RouterLink to="/admin" class="nav-link">Admin</RouterLink>
        </nav>
      </div>
    </header>
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  height: 100vh;
  width: 100vw;
  background: var(--gradient-background);
  overflow: hidden;
  position: fixed; /* Force le container à rester dans la fenêtre */
  top: 0;
  left: 0;
}

.app-header {
  width: 100%;
  height: 10vh;
  background: var(--gradient-dark);
  box-shadow: 0 2px 10px rgba(0, 53, 97, 0.3);
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.main-nav {
  display: flex;
  justify-content: center;
  gap: 40px;
  align-items: center;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 1.1em;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 25px;
  transition: all 0.3s ease;
  position: relative;
  background: rgba(255, 255, 255, 0.1);
}

.nav-link:hover {
  background: var(--gradient-secondary);
  color: var(--text-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(241, 171, 201, 0.3);
}

.nav-link.router-link-exact-active {
  background: var(--gradient-secondary);
  color: var(--text-primary);
  box-shadow: 0 4px 15px rgba(217, 196, 122, 0.4);
}

.main-content {
  height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden; /* Empêche le scroll dans le contenu principal */
  padding: 20px 0;
  box-sizing: border-box;
}

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

@media (max-width: 768px) {
  .main-nav {
    gap: 20px;
  }
  
  .nav-link {
    font-size: 1em;
    padding: 8px 16px;
  }
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
