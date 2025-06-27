<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '@/services/QuizApiService';
import ParticipationStorageService from '@/services/Participation_storage_service';

const router = useRouter();
const token = ref('');
const questions = ref([]);
const participants = ref([]);
const currentView = ref('dashboard'); // dashboard, create, edit
const editingQuestion = ref(null);
const message = ref('');
const messageType = ref('');

// Formulaire pour nouvelle question
const newQuestion = ref({
    title: '',
    text: '',
    position: 1,
    image: '',
    possibleAnswers: [
        { text: '', isCorrect: false },
        { text: '', isCorrect: false }
    ]
});

const showMessage = (msg, type = 'info') => {
    message.value = msg;
    messageType.value = type;
    setTimeout(() => {
        message.value = '';
    }, 5000);
};

const loadQuestions = async () => {
    try {
        const response = await QuizApiService.getInfos();
        if (response) {
            // Charger questions
            questions.value = [];
            for (let i = 1; i <= response.size; i++) {
                const question = await QuizApiService.get_question_by_position(i);
                if (question && question.status === 'success') {
                    questions.value.push(question);
                }
            }
        }
    } catch (error) {
        showMessage('Erreur lors du chargement des questions', 'error');
    }
};

const loadParticipants = async () => {
    try {
        participants.value = await QuizApiService.get_all_participations() || [];
    } catch (error) {
        showMessage('Erreur lors du chargement des participants', 'error');
    }
};

const addAnswer = () => {
    newQuestion.value.possibleAnswers.push({ text: '', isCorrect: false });
};

const removeAnswer = (index) => {
    if (newQuestion.value.possibleAnswers.length > 2) {
        newQuestion.value.possibleAnswers.splice(index, 1);
    }
};

const setCorrectAnswer = (index) => {
    newQuestion.value.possibleAnswers.forEach((answer, i) => {
        answer.isCorrect = (i === index);
    });
};

const validateQuestion = () => {
    if (!newQuestion.value.title || !newQuestion.value.text) {
        showMessage('Titre et texte sont obligatoires', 'error');
        return false;
    }
    
    const validAnswers = newQuestion.value.possibleAnswers.filter(a => a.text.trim());
    if (validAnswers.length < 2) {
        showMessage('Au moins 2 réponses sont nécessaires', 'error');
        return false;
    }
    
    const correctAnswers = validAnswers.filter(a => a.isCorrect);
    if (correctAnswers.length !== 1) {
        showMessage('Une seule réponse doit être correcte', 'error');
        return false;
    }
    
    return true;
};

const createQuestion = async () => {
    if (!validateQuestion()) return;
    
    try {
        const questionData = {
            ...newQuestion.value,
            possibleAnswers: newQuestion.value.possibleAnswers.filter(a => a.text.trim())
        };
        
        const result = await QuizApiService.post_question(questionData, token.value);
        if (result) {
            showMessage('Question créée avec succès !', 'success');
            resetForm();
            currentView.value = 'dashboard';
            await loadQuestions();
        }
    } catch (error) {
        showMessage('Erreur lors de la création', 'error');
    }
};

const editQuestion = (question) => {
    editingQuestion.value = question;
    newQuestion.value = {
        title: question.title,
        text: question.text,
        position: question.position,
        image: question.image || '',
        possibleAnswers: [...question.possibleAnswers]
    };
    currentView.value = 'edit';
};

const updateQuestion = async () => {
    if (!validateQuestion()) return;
    
    try {
        const questionData = {
            ...newQuestion.value,
            possibleAnswers: newQuestion.value.possibleAnswers.filter(a => a.text.trim())
        };
        
        const result = await QuizApiService.update_question(editingQuestion.value.id, questionData, token.value);
        if (result) {
            showMessage('Question modifiée avec succès !', 'success');
            resetForm();
            currentView.value = 'dashboard';
            await loadQuestions();
        }
    } catch (error) {
        showMessage('Erreur lors de la modification', 'error');
    }
};

const deleteQuestion = async (questionId) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette question ?')) {
        try {
            const result = await QuizApiService.delete_question(questionId, token.value);
            if (result) {
                showMessage('Question supprimée avec succès !', 'success');
                await loadQuestions();
            }
        } catch (error) {
            showMessage('Erreur lors de la suppression', 'error');
        }
    }
};

const deleteAllQuestions = async () => {
    if (confirm('Êtes-vous sûr de vouloir supprimer TOUTES les questions ? Cette action est irréversible !')) {
        try {
            const result = await QuizApiService.delete_all_questions(token.value);
            if (result) {
                showMessage('Toutes les questions ont été supprimées !', 'success');
                questions.value = [];
            }
        } catch (error) {
            showMessage('Erreur lors de la suppression', 'error');
        }
    }
};

const deleteAllParticipants = async () => {
    if (confirm('Êtes-vous sûr de vouloir supprimer TOUS les participants ? Cette action est irréversible !')) {
        try {
            const result = await QuizApiService.delete_all_participants(token.value);
            if (result) {
                showMessage('Tous les participants ont été supprimés !', 'success');
                participants.value = [];
            }
        } catch (error) {
            showMessage('Erreur lors de la suppression', 'error');
        }
    }
};

const seedDatabase = async () => {
    if (confirm('Êtes-vous sûr de vouloir reconstruire la base de données et ajouter les questions JO ? Cela supprimera toutes les données existantes !')) {
        try {
            showMessage('Reconstruction de la base de données...', 'info');
            const rebuildResult = await QuizApiService.rebuild_database(token.value);
            if (!rebuildResult) {
                throw new Error('Échec de la reconstruction de la base de données');
            }
            
            const response = await fetch('/jo_questions.json');
            if (!response.ok) {
                throw new Error('Impossible de charger le fichier des questions');
            }
            const predefinedQuestions = await response.json();

            let successCount = 0;
            let currentPosition = 1;

            for (const questionData of predefinedQuestions) {
                try {
                    const questionWithPosition = {
                        ...questionData,
                        position: currentPosition
                    };

                    const result = await QuizApiService.post_question(questionWithPosition, token.value);
                    if (result) {
                        successCount++;
                        currentPosition++;
                    }
                } catch (error) {
                    console.error('Erreur lors de la création de la question:', error);
                }
            }

            showMessage(`Base de données reconstruite et ${successCount} questions ajoutées avec succès !`, 'success');
            await loadQuestions();
            await loadParticipants();
        } catch (error) {
            showMessage('Erreur lors de la reconstruction et de l\'ajout des questions: ' + error.message, 'error');
        }
    }
};

const resetForm = () => {
    newQuestion.value = {
        title: '',
        text: '',
        position: questions.value.length + 1,
        image: '',
        possibleAnswers: [
            { text: '', isCorrect: false },
            { text: '', isCorrect: false }
        ]
    };
    editingQuestion.value = null;
};

const logout = () => {
    ParticipationStorageService.clearToken();
    router.push('/admin/login');
};

onMounted(async () => {
    const response = await QuizApiService.get_login("");
    
    if (response && response.status === 'success') {
        token.value = response.token;
        ParticipationStorageService.save_Tokken(response.token);
        await loadQuestions();
        await loadParticipants();
    } else {
        router.push('/admin/login');
    }
});
</script>

<template>
    <div class="admin-container">
        <div class="admin-header">
            <h1>🔧 Administration Quiz</h1>
            <div class="header-actions">
                <button @click="logout" class="logout-btn">Déconnexion</button>
            </div>
        </div>

        <div v-if="message" :class="['message', messageType]">
            {{ message }}
        </div>

        <div class="admin-nav">
            <button 
                @click="currentView = 'dashboard'" 
                :class="['nav-btn', { active: currentView === 'dashboard' }]"
            >
                📊 Tableau de bord
            </button>
            <button 
                @click="currentView = 'create'; resetForm()" 
                :class="['nav-btn', { active: currentView === 'create' }]"
            >
                ➕ Créer une question
            </button>
        </div>

        <div v-if="currentView === 'dashboard'" class="dashboard">
            <div class="stats-section">
                <div class="stat-card">
                    <h3>📝 Questions</h3>
                    <span class="stat-number">{{ questions.length }}</span>
                </div>
                <div class="stat-card">
                    <h3>👥 Participants</h3>
                    <span class="stat-number">{{ participants.length }}</span>
                </div>
            </div>

            <div class="quick-actions">
                <h3>⚡ Actions rapides</h3>
                <div class="action-buttons">
                    <button @click="deleteAllQuestions" class="danger-btn">
                        🗑️ Supprimer toutes les questions
                    </button>
                    <button @click="deleteAllParticipants" class="danger-btn">
                        🗑️ Supprimer tous les participants
                    </button>
                    <button @click="seedDatabase" class="success-btn">
                        🎯 Ajouter les questions JO (15 questions)
                    </button>
                </div>
            </div>

            <div class="questions-section">
                <h3>📋 Gestion des questions</h3>
                <div v-if="questions.length === 0" class="no-questions">
                    Aucune question créée. Commencez par en créer une !
                </div>
                <div v-else class="questions-list">
                    <div 
                        v-for="question in questions" 
                        :key="question.id"
                        class="question-card"
                    >
                        <div class="question-info">
                            <div class="question-header">
                                <span class="position-badge">{{ question.position }}</span>
                                <h4>{{ question.title }}</h4>
                            </div>
                            <p class="question-text">{{ question.text }}</p>
                            <div class="answers-preview">
                                <span class="answers-count">{{ question.possibleAnswers.length }} réponses</span>
                            </div>
                        </div>
                        <div class="question-actions">
                            <button @click="editQuestion(question)" class="edit-btn">✏️ Modifier</button>
                            <button @click="deleteQuestion(question.id)" class="delete-btn">🗑️ Supprimer</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="currentView === 'create' || currentView === 'edit'" class="form-section">
            <h2>{{ currentView === 'create' ? '➕ Créer une question' : '✏️ Modifier la question' }}</h2>
            
            <form @submit.prevent="currentView === 'create' ? createQuestion() : updateQuestion()">
                <div class="form-group">
                    <label>Titre de la question *</label>
                    <input v-model="newQuestion.title" type="text" placeholder="Ex: Quel sport...?" required>
                </div>

                <div class="form-group">
                    <label>Texte de la question *</label>
                    <textarea v-model="newQuestion.text" placeholder="Description détaillée de la question" required></textarea>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>Position</label>
                        <input v-model.number="newQuestion.position" type="number" min="1" required>
                    </div>
                    <div class="form-group">
                        <label>Image (URL)</label>
                        <input v-model="newQuestion.image" type="url" placeholder="https://...">
                    </div>
                </div>

                <div class="answers-section">
                    <div class="answers-header">
                        <label>Réponses possibles *</label>
                        <button type="button" @click="addAnswer" class="add-answer-btn">➕ Ajouter une réponse</button>
                    </div>
                    
                    <div 
                        v-for="(answer, index) in newQuestion.possibleAnswers" 
                        :key="index"
                        class="answer-item"
                    >
                        <input 
                            v-model="answer.text" 
                            type="text" 
                            :placeholder="`Réponse ${index + 1}`"
                            class="answer-input"
                        >
                        <div class="answer-controls">
                            <label class="correct-label">
                                <input 
                                    type="radio" 
                                    :name="'correct-answer'"
                                    @change="setCorrectAnswer(index)"
                                    :checked="answer.isCorrect"
                                >
                                Correcte
                            </label>
                            <button 
                                v-if="newQuestion.possibleAnswers.length > 2"
                                type="button" 
                                @click="removeAnswer(index)"
                                class="remove-answer-btn"
                            >
                                ❌
                            </button>
                        </div>
                    </div>
                </div>

                <div class="form-actions">
                    <button type="button" @click="currentView = 'dashboard'" class="cancel-btn">Annuler</button>
                    <button type="submit" class="submit-btn">
                        {{ currentView === 'create' ? '✅ Créer' : '💾 Sauvegarder' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.admin-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #ffffff 0%, #AEA2D0 100%);
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, #003561 0%, #420933 100%);
    padding: 20px 30px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 53, 97, 0.3);
    flex-shrink: 0;
}

.admin-header h1 {
    margin: 0;
    color: white;
    font-size: 2em;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.logout-btn {
    background: linear-gradient(135deg, #f1abc9 0%, #d9c47a 100%);
    color: #003561;
    border: none;
    padding: 10px 20px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 2px 10px rgba(241, 171, 201, 0.3);
}

.logout-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(241, 171, 201, 0.5);
    background: linear-gradient(135deg, #d9c47a 0%, #AEA2D0 100%);
}

/* Messages */
.message {
    padding: 15px 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-weight: bold;
    text-align: center;
    flex-shrink: 0;
}

.message.success {
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(35, 147, 205, 0.3);
}

.message.error {
    background: linear-gradient(135deg, #420933 0%, #003561 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(66, 9, 51, 0.3);
}

.message.info {
    background: linear-gradient(135deg, #f1abc9 0%, #AEA2D0 100%);
    color: #003561;
    box-shadow: 0 2px 10px rgba(241, 171, 201, 0.3);
}

/* Navigation */
.admin-nav {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-shrink: 0;
}

.nav-btn {
    background: white;
    border: 2px solid #2393cd;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    color: #2393cd;
}

.nav-btn:hover {
    background: linear-gradient(135deg, #f1abc9 0%, #d9c47a 100%);
    color: #003561;
    transform: translateY(-2px);
}

.nav-btn.active {
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    color: white;
    border-color: #2393cd;
    box-shadow: 0 4px 15px rgba(35, 147, 205, 0.4);
}

/* Container scrollable */
.dashboard,
.form-section {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
}

/* Scrollbar personnalisée */
.dashboard::-webkit-scrollbar,
.form-section::-webkit-scrollbar {
    width: 8px;
}

.dashboard::-webkit-scrollbar-track,
.form-section::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.dashboard::-webkit-scrollbar-thumb,
.form-section::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    border-radius: 10px;
}

.dashboard::-webkit-scrollbar-thumb:hover,
.form-section::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #f1abc9 0%, #d9c47a 100%);
}

/* Dashboard */
.dashboard {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.stats-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.stat-card {
    background: linear-gradient(135deg, white 0%, #f8f9fa 100%);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(35, 147, 205, 0.1);
    border: 2px solid transparent;
    transition: all 0.3s;
}

.stat-card:hover {
    border-color: #f1abc9;
    transform: translateY(-5px);
}

.stat-card h3 {
    margin: 0 0 15px 0;
    color: #003561;
    font-size: 1.1em;
}

.stat-number {
    font-size: 3em;
    font-weight: bold;
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Actions rapides */
.quick-actions {
    background: linear-gradient(135deg, white 0%, #f8f9fa 100%);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(35, 147, 205, 0.1);
    border: 2px solid transparent;
    transition: all 0.3s;
}

.quick-actions:hover {
    border-color: #f1abc9;
}

.quick-actions h3 {
    margin-top: 0;
    color: #003561;
}

.action-buttons {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}

.danger-btn {
    background: linear-gradient(135deg, #420933 0%, #003561 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 3px 15px rgba(66, 9, 51, 0.3);
}

.danger-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(66, 9, 51, 0.5);
}

.success-btn {
    background: linear-gradient(135deg, #28a745 0%, #218838 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 3px 15px rgba(40, 167, 69, 0.3);
}

.success-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(40, 167, 69, 0.5);
}

/* Section questions */
.questions-section {
    background: linear-gradient(135deg, white 0%, #f8f9fa 100%);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(35, 147, 205, 0.1);
    border: 2px solid transparent;
    transition: all 0.3s;
}

.questions-section:hover {
    border-color: #f1abc9;
}

.questions-section h3 {
    margin-top: 0;
    color: #003561;
}

.no-questions {
    text-align: center;
    color: #003561;
    font-style: italic;
    padding: 40px;
}

.questions-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.question-card {
    background: linear-gradient(135deg, #f8f9fa 0%, white 100%);
    border-radius: 10px;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    transition: all 0.3s;
    border: 2px solid transparent;
}

.question-card:hover {
    border-color: #E4007C;
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(228, 0, 124, 0.2);
}

.question-info {
    flex: 1;
}

.question-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 10px;
}

.position-badge {
    background: linear-gradient(135deg, #f1abc9 0%, #d9c47a 100%);
    color: #003561;
    padding: 5px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9em;
    box-shadow: 0 2px 8px rgba(241, 171, 201, 0.3);
}

.question-header h4 {
    margin: 0;
    color: #003561;
}

.question-text {
    color: #2393cd;
    margin: 10px 0;
    line-height: 1.4;
}

.answers-count {
    color: #7456db;
    font-weight: bold;
    font-size: 0.9em;
}

.question-actions {
    display: flex;
    gap: 10px;
    flex-shrink: 0;
}

.edit-btn {
    background: linear-gradient(135deg, #2393cd 0%, #7456db 100%);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 2px 10px rgba(35, 147, 205, 0.3);
}

.edit-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(35, 147, 205, 0.5);
}

.delete-btn {
    background: linear-gradient(135deg, #420933 0%, #003561 100%);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 2px 10px rgba(66, 9, 51, 0.3);
}

.delete-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(66, 9, 51, 0.5);
}

/* Formulaire */
.form-section {
    background: linear-gradient(135deg, white 0%, #f8f9fa 100%);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(35, 147, 205, 0.1);
    border: 2px solid #f1abc9;
}

.form-section h2 {
    margin-top: 0;
    color: #003561;
    margin-bottom: 30px;
    font-size: 1.8em;
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #003561;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #2393cd;
    border-radius: 10px;
    font-size: 1em;
    transition: all 0.3s;
    box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #f1abc9;
    box-shadow: 0 0 15px rgba(241, 171, 201, 0.3);
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 20px;
}

/* Section réponses */
.answers-section {
    margin-bottom: 30px;
}

.answers-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.answers-header label {
    font-weight: bold;
    color: #8B5A96;
}

.add-answer-btn {
    background: linear-gradient(135deg, #2393cd 0%, #f1abc9 100%);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 2px 10px rgba(35, 147, 205, 0.3);
}

.add-answer-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(35, 147, 205, 0.5);
}

.answer-item {
    display: flex;
    gap: 15px;
    align-items: center;
    margin-bottom: 15px;
    padding: 15px;
    background: linear-gradient(135deg, #f8f9fa 0%, white 100%);
    border-radius: 10px;
    border: 2px solid #E4007C;
    transition: all 0.3s;
}

.answer-item:hover {
    border-color: #f1abc9;
    transform: translateY(-2px);
}

.answer-input {
    flex: 1;
    padding: 10px 15px;
    border: 2px solid #8B5A96;
    border-radius: 8px;
    font-size: 1em;
    transition: all 0.3s;
}

.answer-input:focus {
    outline: none;
    border-color: #f1abc9;
    box-shadow: 0 0 10px rgba(241, 171, 201, 0.3);
}

.answer-controls {
    display: flex;
    align-items: center;
    gap: 15px;
}

.correct-label {
    display: flex;
    align-items: center;
    gap: 5px;
    font-weight: bold;
    color: #2393cd;
    cursor: pointer;
    transition: all 0.3s;
}

.correct-label:hover {
    color: #f1abc9;
}

.remove-answer-btn {
    background: linear-gradient(135deg, #FF6900 0%, #E4007C 100%);
    color: white;
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    box-shadow: 0 2px 8px rgba(255, 105, 0, 0.3);
}

.remove-answer-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(255, 105, 0, 0.5);
}

/* Actions du formulaire */
.form-actions {
    display: flex;
    gap: 15px;
    justify-content: flex-end;
    padding-top: 20px;
    border-top: 2px solid #E4007C;
}

.cancel-btn {
    background: linear-gradient(135deg, #8B5A96 0%, #636e72 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 3px 10px rgba(139, 90, 150, 0.3);
}

.cancel-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(139, 90, 150, 0.5);
}

.submit-btn {
    background: linear-gradient(135deg, #2393cd 0%, #f1abc9 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 3px 15px rgba(35, 147, 205, 0.3);
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(35, 147, 205, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
    .admin-container {
        padding: 15px;
    }
    
    .admin-header {
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }
    
    .form-row {
        grid-template-columns: 1fr;
    }
    
    .question-card {
        flex-direction: column;
        gap: 15px;
    }
    
    .question-actions {
        align-self: stretch;
        justify-content: center;
    }
    
    .action-buttons {
        justify-content: center;
    }
    
    .form-actions {
        flex-direction: column;
    }
    
    .answers-header {
        flex-direction: column;
        gap: 10px;
        align-items: stretch;
    }
    
    .answer-item {
        flex-direction: column;
        gap: 10px;
    }
    
    .answer-controls {
        justify-content: center;
    }
}
</style>
