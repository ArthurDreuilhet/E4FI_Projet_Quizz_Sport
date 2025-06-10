<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { InputText, Button, Message, Password } from 'primevue';
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
    <div class="flex flex-col gap-3" style="width: 90vw; max-width: 300px;">
        <h2 class="text-3xl font-bold ">Admin Login</h2>
        <Password type="text" placeholder="Password" :feedback="false" toggleMask fluid v-model="password"
            @keyup.enter="submitPassword" />

        <Button type="submit" severity="secondary" label="Submit" @click="submitPassword" style="max-width: 150px;" />
    </div>
</template>