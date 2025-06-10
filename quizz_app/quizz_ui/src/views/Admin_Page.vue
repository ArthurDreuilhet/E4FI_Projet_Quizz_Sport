<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '@/services/QuizApiService';
import ParticipationStorageService from '@/services/Participation_storage_service';

const router = useRouter();

onMounted(async () => {
    
    const response = await QuizApiService.get_login("");

    if (response && response.status === 'success') {
        console.log('Login successful');
        ParticipationStorageService.save_Tokken(response.token);
    } else {
        router.push('/admin/login');
    }
});
</script>

<template>

</template>