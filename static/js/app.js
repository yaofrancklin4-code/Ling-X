// Fonction pour jouer l'audio
function playAudio(url) {
    const audio = new Audio(url);
    audio.play().catch(error => {
        console.error('Erreur lors de la lecture audio:', error);
    });
}

// Fonction pour afficher les notifications
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Fonction pour mettre à jour la progression
function updateProgress(lessonId, score) {
    fetch(`/api/lessons/${lessonId}/progress/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ score: score })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Progression mise à jour:', data);
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

// Fonction pour obtenir le cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Animation au scroll
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .stat-card').forEach(el => {
        observer.observe(el);
    });
});

// Fonction pour le compte à rebours
function startCountdown(duration, display) {
    let timer = duration, minutes, seconds;
    const interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(interval);
            display.textContent = "Temps écoulé!";
        }
    }, 1000);
    
    return interval;
}

// Fonction pour sauvegarder la progression locale (mode hors ligne)
function saveLocalProgress(lessonId, data) {
    if (typeof(Storage) !== "undefined") {
        const progress = JSON.parse(localStorage.getItem('lingx_progress') || '{}');
        progress[lessonId] = {
            ...data,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('lingx_progress', JSON.stringify(progress));
    }
}

// Fonction pour récupérer la progression locale
function getLocalProgress(lessonId) {
    if (typeof(Storage) !== "undefined") {
        const progress = JSON.parse(localStorage.getItem('lingx_progress') || '{}');
        return progress[lessonId] || null;
    }
    return null;
}

// Fonction pour synchroniser la progression locale avec le serveur
function syncLocalProgress() {
    if (typeof(Storage) !== "undefined") {
        const progress = JSON.parse(localStorage.getItem('lingx_progress') || '{}');
        Object.keys(progress).forEach(lessonId => {
            updateProgress(lessonId, progress[lessonId].score);
        });
        localStorage.removeItem('lingx_progress');
    }
}

// Vérifier la connexion et synchroniser au chargement
window.addEventListener('load', function() {
    if (navigator.onLine) {
        syncLocalProgress();
    }
});

// Écouter les changements de connexion
window.addEventListener('online', syncLocalProgress);
window.addEventListener('offline', function() {
    showNotification('Mode hors ligne activé', 'warning');
});

// Fonction pour le jeu de mémoire
class MemoryGame {
    constructor(containerId, words) {
        this.container = document.getElementById(containerId);
        this.words = words;
        this.flippedCards = [];
        this.matchedPairs = 0;
        this.score = 0;
    }

    init() {
        this.container.innerHTML = '';
        const cards = [...this.words, ...this.words].sort(() => Math.random() - 0.5);
        
        cards.forEach((word, index) => {
            const card = this.createCard(word, index);
            this.container.appendChild(card);
        });
    }

    createCard(word, index) {
        const card = document.createElement('div');
        card.className = 'memory-card';
        card.dataset.word = word;
        card.dataset.index = index;
        card.innerHTML = '?';
        card.addEventListener('click', () => this.flipCard(card));
        return card;
    }

    flipCard(card) {
        if (this.flippedCards.length >= 2 || card.classList.contains('flipped')) {
            return;
        }

        card.classList.add('flipped');
        card.innerHTML = card.dataset.word;
        this.flippedCards.push(card);

        if (this.flippedCards.length === 2) {
            setTimeout(() => this.checkMatch(), 500);
        }
    }

    checkMatch() {
        const [card1, card2] = this.flippedCards;
        
        if (card1.dataset.word === card2.dataset.word) {
            card1.classList.add('matched');
            card2.classList.add('matched');
            this.score += 10;
            this.matchedPairs++;
            
            if (this.matchedPairs === this.words.length) {
                setTimeout(() => this.gameComplete(), 500);
            }
        } else {
            card1.classList.remove('flipped');
            card2.classList.remove('flipped');
            card1.innerHTML = '?';
            card2.innerHTML = '?';
        }
        
        this.flippedCards = [];
        this.updateScore();
    }

    updateScore() {
        const scoreElement = document.getElementById('score');
        if (scoreElement) {
            scoreElement.textContent = this.score;
        }
    }

    gameComplete() {
        showNotification('🎉 Félicitations! Vous avez terminé le jeu!', 'success');
    }
}

// Fonction pour le quiz interactif
class InteractiveQuiz {
    constructor(quizData) {
        this.quizData = quizData;
        this.currentQuestion = 0;
        this.score = 0;
        this.answers = [];
    }

    start() {
        this.showQuestion();
    }

    showQuestion() {
        const question = this.quizData[this.currentQuestion];
        // Afficher la question
        console.log('Question:', question);
    }

    submitAnswer(answer) {
        this.answers.push(answer);
        this.currentQuestion++;
        
        if (this.currentQuestion < this.quizData.length) {
            this.showQuestion();
        } else {
            this.finish();
        }
    }

    finish() {
        // Calculer le score final
        console.log('Quiz terminé! Score:', this.score);
    }
}

// Exporter les fonctions pour utilisation globale
window.LingX = {
    playAudio,
    showNotification,
    updateProgress,
    saveLocalProgress,
    getLocalProgress,
    MemoryGame,
    InteractiveQuiz
};
