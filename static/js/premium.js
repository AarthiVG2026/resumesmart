/**
 * ResumeSmart Premium - Career Assistant JavaScript
 * Handles: Interview Simulator, Copilot Chat, Heatmap rendering
 */

document.addEventListener('DOMContentLoaded', () => {
    initCopilot();
    initInterviewer();
});

// --- Career Copilot ---
function initCopilot() {
    const chatInput = document.getElementById('copilotInput');
    const chatBtn = document.getElementById('copilotSend');
    const chatHistory = document.getElementById('copilotHistory');

    if (!chatBtn) return;

    chatBtn.addEventListener('click', async () => {
        const msg = chatInput.value.trim();
        if (!msg) return;

        appendMessage('user', msg);
        chatInput.value = '';

        try {
            const res = await fetch('/copilot/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg })
            });
            const data = await res.json();
            appendMessage('bot', data.response);
        } catch (e) {
            appendMessage('bot', "Sorry, I'm having trouble connecting right now.");
        }
    });

    function appendMessage(role, text) {
        const div = document.createElement('div');
        div.className = `chat-msg ${role}-msg`;
        div.innerHTML = `<div class="msg-bubble">${text}</div>`;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

// --- Interview Simulator ---
let currentQuestions = [];
let currentQIndex = 0;

async function initInterviewer() {
    const startBtn = document.getElementById('startInterview');
    if (!startBtn) return;

    startBtn.addEventListener('click', async () => {
        startBtn.disabled = true;
        startBtn.innerHTML = '⏳ Loading Questions...';
        
        try {
            const res = await fetch('/interview/generate');
            currentQuestions = await res.json();
            showQuestion();
            document.getElementById('interviewIntro').style.display = 'none';
            document.getElementById('interviewActive').style.display = 'block';
        } catch (e) {
            alert('Failed to load interview simulator.');
            startBtn.disabled = false;
        }
    });
}

function showQuestion() {
    const q = currentQuestions[currentQIndex];
    document.getElementById('interviewQuestion').innerText = q.question;
    document.getElementById('interviewTopic').innerText = `${q.type} - ${q.topic}`;
    document.getElementById('interviewProgress').innerText = `Question ${currentQIndex + 1} of ${currentQuestions.length}`;
}

async function submitAnswer() {
    const answer = document.getElementById('interviewAnswer').value.trim();
    if (!answer) return alert('Please enter an answer.');

    const submitBtn = document.getElementById('submitAnswerBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Evaluating...';

    const res = await fetch('/interview/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            answer: answer, 
            question: currentQuestions[currentQIndex].question 
        })
    });
    const result = await res.json();
    
    showFeedback(result);
}

function showFeedback(result) {
    document.getElementById('interviewActive').style.display = 'none';
    document.getElementById('interviewFeedback').style.display = 'block';
    
    document.getElementById('confScore').innerText = `${Math.round(result.confidence)}%`;
    document.getElementById('clarScore').innerText = `${Math.round(result.clarity)}%`;
    document.getElementById('relScore').innerText = `${Math.round(result.relevance)}%`;
    document.getElementById('feedbackText').innerText = result.feedback;
}

function nextQuestion() {
    currentQIndex++;
    if (currentQIndex < currentQuestions.length) {
        document.getElementById('interviewFeedback').style.display = 'none';
        document.getElementById('interviewActive').style.display = 'block';
        document.getElementById('interviewAnswer').value = '';
        document.getElementById('submitAnswerBtn').disabled = false;
        showQuestion();
    } else {
        alert('Interview Simulation Complete! Check your overall score in the dashboard.');
        location.reload();
    }
}


// FLOATING CHATBOT TOGGLE LOGIC
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('chatbotToggleBtn');
    const chatWindow = document.getElementById('copilotChatWindow');
    const closeBtn = document.getElementById('closeCopilotBtn');
    if(toggleBtn && chatWindow) {
        toggleBtn.addEventListener('click', () => {
            chatWindow.classList.toggle('hidden');
        });
        if(closeBtn) {
            closeBtn.addEventListener('click', () => {
                chatWindow.classList.add('hidden');
            });
        }
    }
});
