<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import ParticipationStorageService from '@/services/Participation_storage_service';

const router = useRouter();
const playerName = ref('');

onMounted(() => {
    playerName.value = ParticipationStorageService.getPlayerName() || '';
    console.log('Participation storage service initialized: ', playerName.value);
});
</script>


<template>
    <div style="width: 100%; height: 100vh; display: flex; align-items: center; justify-content: center;">
        <p>caca prout {{ playerName }}</p>
    </div>
</template>