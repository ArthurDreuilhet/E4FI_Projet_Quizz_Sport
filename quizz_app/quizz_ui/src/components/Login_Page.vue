<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '@/services/QuizApiService';
import ParticipationStorageService from '@/services/Participation_storage_service';

const router = useRouter();

const password = ref('');

const submitPassword = async () => {
    const response = await QuizApiService.get_login(password.value);

    console.log('Response from login API:', response);

    if (response && response.status === 'success') {
        console.log('Login successful');
        ParticipationStorageService.save_Tokken(response.token);
        router.push('/admin');
    } else {
        console.warn('Login failed');
    }

};

onMounted(async () => {
});

</script>

<template>
    <div class="login-container">
        <div class="login-card card">
            <h2 class="login-title">🔐 Admin Login</h2>
            <div class="form-group">
                <input type="password" placeholder="Mot de passe admin" v-model="password" @keyup.enter="submitPassword" class="password-input input-field" />
            </div>
            <button type="submit" @click="submitPassword" class="submit-button btn btn-secondary">
                Se connecter
            </button>
        </div>
    </div>
</template>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
    padding: 20px;
}

.login-card {
    background: rgba(255, 255, 255, 0.95);
    text-align: center;
    width: 100%;
    max-width: 400px;
}

.login-title {
    color: var(--text-primary);
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 30px;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.form-group {
    margin-bottom: 25px;
}

.password-input {
    width: 100%;
}

.submit-button {
    width: 100%;
    font-size: 1.1em;
    padding: 15px;
}

@media (max-width: 480px) {
    .login-card {
        padding: 30px 20px;
    }
    
    .login-title {
        font-size: 1.8em;
    }
}
</style>