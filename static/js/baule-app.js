/* ========================================
   BAOULÉ LEARNING - Fonctionnalités Interactives
   ======================================== */

'use strict';

// ========== GESTION DU SON/AUDIO ==========

class AudioManager {
    constructor() {
        this.audioContext = null;
        this.currentAudio = null;
    }

    // Initialiser le contexte audio
    initAudioContext() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        return this.audioContext;
    }

    // Jouer un fichier audio
    playAudio(filePath) {
        if (this.currentAudio) {
            this.currentAudio.pause();
        }

        const audio = new Audio(filePath);
        this.currentAudio = audio;
        audio.play().catch(error => {
            console.error('Erreur lecture audio:', error);
        });
    }

    // Text-to-speech avec Web Speech API
    speak(text, language = 'fr-FR') {
        if (!('speechSynthesis' in window)) {
            alert('Synthèse vocale non supportée par ce navigateur');
            return;
        }

        // Arrêter la parole précédente
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = language;
        utterance.rate = 0.9;
        utterance.pitch = 1;

        window.speechSynthesis.speak(utterance);
    }

    // Arrêter l'audio
    stopAudio() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
        }
        window.speechSynthesis.cancel();
    }
}

// Instance globale du gestionnaire audio
const audioManager = new AudioManager();

// ========== QUIZ ET EXERCICES ==========

class QuizManager {
    constructor() {
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.totalQuestions = 0;
        this.selectedAnswers = [];
    }

    // Initialiser un quiz
    initQuiz(quizData) {
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.selectedAnswers = [];
        this.totalQuestions = quizData.length;
        return quizData;
    }

    // Afficher la question suivante
    showNextQuestion(quizData) {
        if (this.currentQuestionIndex < quizData.length) {
            const question = quizData[this.currentQuestionIndex];
            return question;
        }
        return null;
    }

    // Enregistrer la réponse
    recordAnswer(answerId, isCorrect) {
        this.selectedAnswers.push({
            questionIndex: this.currentQuestionIndex,
            answerId: answerId,
            isCorrect: isCorrect
        });

        if (isCorrect) {
            this.score++;
        }

        this.currentQuestionIndex++;
    }

    // Obtenir le score final
    getFinalScore() {
        return {
            correct: this.score,
            total: this.totalQuestions,
            percentage: Math.round((this.score / this.totalQuestions) * 100)
        };
    }
}

const quizManager = new QuizManager();

// ========== MINIGAMES ==========

class MemoryGame {
    constructor(containerId, cards) {
        this.container = document.getElementById(containerId);
        this.cards = cards;
        this.flipped = [];
        this.matched = [];
        this.moves = 0;
        this.score = 0;
    }

    // Initialiser le jeu
    init() {
        this.shuffleCards();
        this.renderCards();
        this.addEventListeners();
    }

    // Mélanger les cartes
    shuffleCards() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }

    // Afficher les cartes
    renderCards() {
        this.container.innerHTML = '';
        this.cards.forEach((card, index) => {
            const cardEl = document.createElement('div');
            cardEl.className = 'memory-card';
            cardEl.dataset.index = index;
            cardEl.innerHTML = '<div class="card-inner"><div class="card-front">?</div><div class="card-back"></div></div>';
            this.container.appendChild(cardEl);
        });
    }

    // Ajouter les écouteurs d'événement
    addEventListeners() {
        this.container.addEventListener('click', (e) => {
            const card = e.target.closest('.memory-card');
            if (card) {
                this.flipCard(card);
            }
        });
    }

    // Retourner une carte
    flipCard(cardEl) {
        const index = cardEl.dataset.index;

        if (this.flipped.length < 2 && !this.flipped.includes(index) && !this.matched.includes(index)) {
            this.flipped.push(index);
            cardEl.classList.add('flipped');
            cardEl.querySelector('.card-back').textContent = this.cards[index].french;

            if (this.flipped.length === 2) {
                this.moves++;
                this.checkMatch();
            }
        }
    }

    // Vérifier si les cartes correspondent
    checkMatch() {
        const [index1, index2] = this.flipped;
        const match = this.cards[index1].baule === this.cards[index2].baule;

        setTimeout(() => {
            if (match) {
                this.matched.push(index1, index2);
                this.score += 10;
                console.log('Paire trouvée! Score:', this.score);
            } else {
                document.querySelectorAll('.memory-card').forEach(card => {
                    if (this.flipped.includes(parseInt(card.dataset.index))) {
                        card.classList.remove('flipped');
                        card.querySelector('.card-back').textContent = '';
                    }
                });
            }

            this.flipped = [];

            if (this.matched.length === this.cards.length) {
                this.endGame();
            }
        }, 800);
    }

    // Terminer le jeu
    endGame() {
        console.log('Jeu terminé! Score final:', this.score, 'Mouvements:', this.moves);
        alert(`Jeu terminé! Score: ${this.score} | Mouvements: ${this.moves}`);
    }
}

// ========== GESTION DE LA PROGRESSION ==========

class ProgressTracker {
    constructor() {
        this.lessons = [];
        this.totalPoints = 0;
        this.currentLevel = 1;
    }

    // Ajouter des points
    addPoints(points) {
        this.totalPoints += points;
        this.updateLevel();
        this.saveProgress();
    }

    // Mettre à jour le niveau
    updateLevel() {
        this.currentLevel = Math.floor(this.totalPoints / 100) + 1;
    }

    // Marquer une leçon comme complétée
    completeLesson(lessonId, score) {
        this.lessons.push({
            id: lessonId,
            completedAt: new Date(),
            score: score
        });
        this.addPoints(score * 5);
    }

    // Sauvegarder la progression
    saveProgress() {
        const progressData = {
            totalPoints: this.totalPoints,
            currentLevel: this.currentLevel,
            lessons: this.lessons,
            lastUpdated: new Date()
        };
        localStorage.setItem('bauleProgress', JSON.stringify(progressData));
    }

    // Charger la progression
    loadProgress() {
        const saved = localStorage.getItem('bauleProgress');
        if (saved) {
            const data = JSON.parse(saved);
            this.totalPoints = data.totalPoints;
            this.currentLevel = data.currentLevel;
            this.lessons = data.lessons;
        }
    }
}

const progressTracker = new ProgressTracker();
progressTracker.loadProgress();

// ========== UTILITAIRES ==========

// Afficher un toast de notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Formater le temps en MM:SS
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// Obtenir un gradient de couleur basé sur le score
function getScoreGradient(percentage) {
    if (percentage >= 80) return '#009E60'; // Vert
    if (percentage >= 60) return '#FF8C00'; // Orange
    return '#dc3545'; // Rouge
}

// ========== ÉVÉNEMENTS DOM ==========

document.addEventListener('DOMContentLoaded', () => {
    // Initialiser les tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Initialiser les popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Gestion des boutons audio
    document.querySelectorAll('[data-audio-speak]').forEach(btn => {
        btn.addEventListener('click', () => {
            const text = btn.getAttribute('data-audio-speak');
            audioManager.speak(text);
        });
    });

    // Gestion des icônes d'audio play
    document.querySelectorAll('[data-audio-play]').forEach(btn => {
        btn.addEventListener('click', () => {
            const filePath = btn.getAttribute('data-audio-play');
            audioManager.playAudio(filePath);
        });
    });

    // Gestion des réponses de quiz
    document.querySelectorAll('.quiz-option').forEach(option => {
        option.addEventListener('click', () => {
            const isCorrect = option.getAttribute('data-correct') === 'true';
            const answerId = option.getAttribute('data-answer-id');
            quizManager.recordAnswer(answerId, isCorrect);

            option.classList.add(isCorrect ? 'correct' : 'incorrect');

            // Désactiver les autres options
            option.parentElement.querySelectorAll('.quiz-option').forEach(o => {
                o.style.pointerEvents = 'none';
            });

            showToast(isCorrect ? '✅ Correct!' : '❌ Incorrect', isCorrect ? 'success' : 'error');
        });
    });

    // Gestion des boutons suivant
    document.querySelectorAll('[data-quiz-next]').forEach(btn => {
        btn.addEventListener('click', () => {
            // Logique pour aller à la question suivante
            showToast('Passez à la question suivante');
        });
    });
});

// Arrêter l'audio quand on quitte la page
window.addEventListener('beforeunload', () => {
    audioManager.stopAudio();
});

// ========== EXPORTATIONS ==========

// Pour utilisation dans d'autres scripts
window.BauleApp = {
    audioManager,
    quizManager,
    MemoryGame,
    ProgressTracker: progressTracker,
    showToast,
    formatTime,
    getScoreGradient
};
