/**
 * LearnSphere — Main Application JavaScript
 * SPA-like navigation, API calls, quiz handling, chat, and 3D effects
 */

// ═══════════════════════════════════════════════════════
//                    STATE
// ═══════════════════════════════════════════════════════

const state = {
    level: window.APP_DATA?.level || null,
    roadmap: window.APP_DATA?.roadmap || null,
    topicsCompleted: window.APP_DATA?.topicsCompleted || [],
    xp: window.APP_DATA?.xp || 0,
    badges: window.APP_DATA?.badges || [],
    currentTopic: null,
    currentTopicTitle: null,
    learningStyle: null,
    content: null,
    quizData: null,
    userAnswers: {},
    feedback: null,
    chatMessages: [],
    chatMode: 'text',
    chatOpen: false
};

// ═══════════════════════════════════════════════════════
//                  NAVIGATION
// ═══════════════════════════════════════════════════════

function goToSection(name) {
    document.querySelectorAll('.learn-section').forEach(s => s.classList.remove('active'));
    const section = document.getElementById(`section-${name}`);
    if (section) {
        section.classList.add('active');
        section.style.animation = 'none';
        section.offsetHeight; // Trigger reflow
        section.style.animation = 'section-enter 0.5s ease-out';
    }
    updateProgressBar(name);
    updatePageHeader(name);

    // Fix: Wait for render, then scroll slightly below top to make buttons more obvious, or entirely to top
    setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
}

function updateProgressBar(currentSection) {
    const steps = [
        { key: 'level', num: '1', label: 'Level' },
        { key: 'roadmap', num: '2', label: 'Roadmap' },
        { key: 'style', num: '3', label: 'Style' },
        { key: 'content', num: '4', label: 'Learn' },
        { key: 'quiz', num: '5', label: 'Quiz' },
        { key: 'feedback', num: '6', label: 'Review' }
    ];

    const currentIdx = steps.findIndex(s => s.key === currentSection);
    const container = document.getElementById('progressBar');
    if (!container) return;

    let html = '';
    steps.forEach((step, i) => {
        let cls = 'pending';
        let content = step.num;
        if (i < currentIdx) { cls = 'completed'; content = '✓'; }
        else if (i === currentIdx) { cls = 'active'; }

        html += `<div class="progress-step">
            <div class="progress-dot ${cls}">${content}</div>
            <div class="progress-label">${step.label}</div>
        </div>`;
        if (i < steps.length - 1) {
            html += `<div class="progress-line ${i < currentIdx ? 'completed' : 'pending'}"></div>`;
        }
    });
    container.innerHTML = html;
}

function updatePageHeader(section) {
    const title = document.getElementById('pageTitle');
    const subtitle = document.getElementById('pageSubtitle');

    const headers = {
        level: ['Choose Your Level', 'Select your ML experience to get started'],
        roadmap: ['Your Learning Roadmap', `${state.level || ''} Track`],
        style: ['Choose Learning Style', `Topic: ${state.currentTopicTitle || ''}`],
        content: [state.currentTopicTitle || 'Learning', `${state.learningStyle || ''} Mode · ${state.level || ''} Level`],
        quiz: [`Quiz: ${state.currentTopicTitle || ''}`, '3 questions · Scenario, Code Analysis, and MCQ'],
        feedback: ['Quiz Results', 'See how you did'],
        revision: [`Revision: ${state.currentTopicTitle || ''}`, 'Targeted material for your weak areas'],
        flashcards: [`Flashcards: ${state.currentTopicTitle || ''}`, 'Click each card to flip']
    };

    const h = headers[section] || ['LearnSphere', ''];
    if (title) title.textContent = h[0];
    if (subtitle) subtitle.textContent = h[1];
}

// ═══════════════════════════════════════════════════════
//                  LEVEL SELECT
// ═══════════════════════════════════════════════════════

async function selectLevel(level) {
    // Highlight selected card
    document.querySelectorAll('.level-card').forEach(c => c.classList.remove('selected'));
    document.getElementById(`level-${level}`)?.classList.add('selected');

    state.level = level;
    state.roadmap = null;

    goToSection('roadmap');
    showLoader('topicList', 'Generating your personalized ML roadmap...');

    try {
        const res = await fetch('/api/roadmap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level })
        });
        const data = await res.json();
        state.roadmap = data.roadmap;
        renderRoadmap();
        updateSidebarRoadmap();
    } catch (err) {
        document.getElementById('topicList').innerHTML =
            '<div class="glass-card" style="text-align:center;color:#ff5252;">❌ Failed to generate roadmap. Please try again.</div>';
    }
}

function renderRoadmap() {
    const container = document.getElementById('topicList');
    const badge = document.getElementById('roadmapBadge');

    if (badge) badge.textContent = `📍 ${(state.level || 'BEGINNER').toUpperCase()} TRACK`;

    // Show completed
    const completedEl = document.getElementById('completedTopics');
    if (state.topicsCompleted.length > 0) {
        completedEl.innerHTML = `<div class="glass-card" style="background:rgba(105,240,174,0.05);border-color:rgba(105,240,174,0.2);padding:14px 18px;margin-bottom:16px;">
            ✅ <strong>Completed:</strong> ${state.topicsCompleted.join(', ')}
        </div>`;
    } else {
        completedEl.innerHTML = '';
    }

    if (!state.roadmap || !state.roadmap.length) {
        container.innerHTML = '<div class="glass-card" style="text-align:center;">No topics found.</div>';
        return;
    }

    container.innerHTML = state.roadmap.map(topic => {
        const isDone = state.topicsCompleted.includes(topic.title);
        return `<div class="topic-card ${isDone ? 'completed' : ''}" onclick="selectTopic(${topic.id}, '${escapeHtml(topic.title)}')">
            <div class="topic-num">${topic.id}</div>
            <div class="topic-info">
                <div class="topic-title">${isDone ? '✅' : topic.icon} ${topic.title}</div>
                <div class="topic-desc">${topic.description || ''}</div>
            </div>
            <div class="topic-action">
                <button class="btn btn-sm ${isDone ? 'btn-secondary' : 'btn-primary'}">${isDone ? 'Review' : 'Start'}</button>
            </div>
        </div>`;
    }).join('');
}

function selectTopic(id, title) {
    state.currentTopic = id;
    state.currentTopicTitle = title;
    state.content = null;

    document.getElementById('styleBadge').textContent = `📚 ${title}`;
    goToSection('style');
}

// ═══════════════════════════════════════════════════════
//                  STYLE SELECT
// ═══════════════════════════════════════════════════════

async function selectStyle(style) {
    state.learningStyle = style;
    state.content = null;

    const icons = { Reading: '📖', Auditory: '🎧', Kinesthetic: '💻', Visual: '🎨' };
    document.getElementById('contentIcon').textContent = icons[style] || '📘';
    document.getElementById('contentTitle').textContent = state.currentTopicTitle;
    document.getElementById('contentSubtitle').textContent = `${style} Mode · ${state.level} Level`;

    goToSection('content');
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = '';
    document.getElementById('audioPlayerContainer').style.display = 'none';
    document.getElementById('videoContainer').style.display = 'none';
    showLoader('contentArea', `Generating your ${style.toLowerCase()} content...`);

    try {
        const res = await fetch('/api/content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: state.currentTopicTitle, level: state.level, style })
        });
        const data = await res.json();
        hideLoader('contentArea');

        if (data.type === 'audio') {
            contentArea.innerHTML = renderMarkdown(data.content);
            const audioContainer = document.getElementById('audioPlayerContainer');
            const audioPlayer = document.getElementById('audioPlayer');
            if (data.audio_path) {
                audioPlayer.src = data.audio_path;
                audioContainer.style.display = 'block';
            }
        } else if (data.type === 'visual') {
            contentArea.innerHTML = renderMarkdown(data.content);
            if (data.videos && data.videos.length) {
                const vc = document.getElementById('videoContainer');
                vc.style.display = 'block';
                vc.innerHTML = '<h3 style="margin-bottom:12px;">🎬 Video Tutorials</h3><div class="video-grid">' +
                    data.videos.map(v => {
                        if (v.is_search_link) {
                            return `<div class="video-card"><div class="video-title"><a href="${v.url}" target="_blank" style="color:var(--accent-blue);">🔗 ${v.title}</a></div></div>`;
                        }
                        return `<div class="video-card"><iframe src="https://www.youtube.com/embed/${v.video_id}" allowfullscreen></iframe><div class="video-title">${v.title}</div></div>`;
                    }).join('') + '</div>';
            }
        } else {
            contentArea.innerHTML = renderMarkdown(data.content);
        }
    } catch (err) {
        hideLoader('contentArea');
        contentArea.innerHTML = '<div style="text-align:center;color:#ff5252;">❌ Failed to generate content. Please try again.</div>';
    }
}

// ═══════════════════════════════════════════════════════
//                  QUIZ
// ═══════════════════════════════════════════════════════

async function startQuiz() {
    state.quizData = null;
    state.userAnswers = {};

    document.getElementById('quizTitle').textContent = `Quiz: ${state.currentTopicTitle}`;
    goToSection('quiz');

    const container = document.getElementById('quizContainer');
    container.innerHTML = '';
    showLoader('quizContainer', 'Preparing your quiz...');

    try {
        const res = await fetch('/api/quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: state.currentTopicTitle, level: state.level })
        });
        const data = await res.json();
        state.quizData = data.quiz;
        hideLoader('quizContainer');
        renderQuiz();
    } catch (err) {
        hideLoader('quizContainer');
        container.innerHTML = '<div style="text-align:center;color:#ff5252;">❌ Failed to generate quiz. Please try again.</div>';
    }
}

function renderQuiz() {
    const container = document.getElementById('quizContainer');
    if (!state.quizData || !state.quizData.length) {
        container.innerHTML = '<div class="glass-card" style="text-align:center;">No quiz questions available.</div>';
        return;
    }

    const typeBadges = {
        scenario: ['🌍 Real-Life Scenario', 'scenario'],
        code_analysis: ['💻 Code Analysis', 'code'],
        mcq: ['✅ Multiple Choice', 'mcq']
    };

    container.innerHTML = state.quizData.map((q, i) => {
        const [badgeText, badgeClass] = typeBadges[q.type] || ['❓ Question', 'mcq'];
        let answersHtml = '';

        if (q.options && (q.type === 'mcq' || q.type === 'code_analysis')) {
            answersHtml = `<div class="quiz-options">
                ${q.options.map((opt, j) => `
                    <div class="quiz-option" onclick="selectQuizOption(${i}, ${j}, this)" data-q="${i}" data-o="${j}">
                        <div class="radio"></div>
                        <span>${opt}</span>
                    </div>
                `).join('')}
            </div>`;
        } else {
            answersHtml = `<textarea class="quiz-textarea" placeholder="Write your answer..." oninput="state.userAnswers[${i}] = this.value"></textarea>`;
        }

        return `<div class="quiz-question">
            <span class="quiz-type ${badgeClass}">${badgeText}</span>
            <div class="quiz-text"><strong>Question ${i + 1}:</strong> ${escapeHtml(q.question)}</div>
            ${answersHtml}
        </div>`;
    }).join('');

    document.getElementById('quizActions').style.display = 'flex';
}

function selectQuizOption(qIdx, optIdx, el) {
    // Deselect siblings
    el.parentElement.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    state.userAnswers[qIdx] = state.quizData[qIdx].options[optIdx];
}

async function submitQuiz() {
    const answers = [];
    for (let i = 0; i < state.quizData.length; i++) {
        const ans = state.userAnswers[i] || '';
        if (!ans) {
            showToast('⚠️ Please answer all questions before submitting.');
            return;
        }
        answers.push(ans);
    }

    goToSection('feedback');
    const container = document.getElementById('feedbackContent');
    container.innerHTML = '';
    showLoader('feedbackContent', 'Evaluating your answers...');

    try {
        const res = await fetch('/api/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: state.currentTopicTitle,
                level: state.level,
                quiz_data: state.quizData,
                answers
            })
        });
        const data = await res.json();
        state.feedback = data;
        hideLoader('feedbackContent');
        // Update local state and re-render roadmap so it reflects immediately
        if (!state.topicsCompleted.includes(state.currentTopicTitle)) {
            state.topicsCompleted.push(state.currentTopicTitle);
        }
        updateSidebarStats();

        // Re-render roadmap elements to show checkmarks
        if (state.roadmap && state.roadmap.length) {
            renderRoadmap();
            updateSidebarRoadmap();
        }

        if (data.percentage >= 70) {
            showConfetti();
        }
    } catch (err) {
        hideLoader('feedbackContent');
        container.innerHTML = '<div style="text-align:center;color:#ff5252;">❌ Failed to evaluate. Please try again.</div>';
    }
}

function renderFeedback(fb) {
    const container = document.getElementById('feedbackContent');
    const pct = fb.percentage || 0;

    let scoreClass = 'score-low';
    let emoji = '📚';
    if (pct >= 70) { scoreClass = 'score-high'; emoji = '🎉'; }
    else if (pct >= 40) { scoreClass = 'score-mid'; emoji = '💪'; }

    let html = `
        <div class="score-section">
            <div class="score-circle ${scoreClass}">${fb.score}/${fb.total}</div>
            <h2 style="font-size:1.5rem;">${emoji} ${pct}%</h2>
        </div>
        <div class="glass-card" style="margin-bottom: 16px;">
            <h3 style="margin-bottom:8px;">📋 Feedback</h3>
            <p style="color:var(--text-secondary);line-height:1.7;">${fb.overall_feedback || ''}</p>
        </div>`;

    // Per-question feedback
    if (fb.per_question) {
        fb.per_question.forEach(pq => {
            const cls = pq.is_correct ? 'feedback-correct' : 'feedback-wrong';
            const icon = pq.is_correct ? '✅' : '❌';
            html += `<div class="feedback-item ${cls}"><strong>Question ${pq.question_num}:</strong> ${icon} ${pq.feedback}</div>`;
        });
    }

    // Strong & weak areas
    html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px;">';
    if (fb.strong_areas && fb.strong_areas.length) {
        html += '<div class="glass-card"><h3 style="margin-bottom:8px;">💪 Strong Areas</h3>';
        fb.strong_areas.forEach(a => { html += `<div style="padding:4px 0;font-size:0.9rem;">✅ ${a}</div>`; });
        html += '</div>';
    }
    if (fb.weak_areas && fb.weak_areas.length) {
        html += '<div class="glass-card"><h3 style="margin-bottom:8px;">📌 Areas to Improve</h3>';
        fb.weak_areas.forEach(a => { html += `<div style="padding:4px 0;font-size:0.9rem;">🔸 ${a}</div>`; });
        html += '</div>';
    }
    html += '</div>';

    container.innerHTML = html;
}

// ═══════════════════════════════════════════════════════
//                  REVISION
// ═══════════════════════════════════════════════════════

async function startRevision() {
    document.getElementById('revisionTitle').textContent = `Revision: ${state.currentTopicTitle}`;
    goToSection('revision');

    const area = document.getElementById('revisionArea');
    area.innerHTML = '';
    showLoader('revisionArea', 'Generating targeted revision material...');

    try {
        const res = await fetch('/api/revision', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: state.currentTopicTitle,
                level: state.level,
                weak_areas: state.feedback?.weak_areas || []
            })
        });
        const data = await res.json();
        hideLoader('revisionArea');
        area.innerHTML = renderMarkdown(data.content);
    } catch (err) {
        hideLoader('revisionArea');
        area.innerHTML = '<div style="text-align:center;color:#ff5252;">❌ Failed to generate revision. Try again.</div>';
    }
}

function retakeQuiz() {
    state.quizData = null;
    state.userAnswers = {};
    state.feedback = null;
    startQuiz();
}

function goToNextTopic() {
    if (!state.roadmap || !state.roadmap.length) {
        goToSection('roadmap');
        return;
    }

    const currentIndex = state.roadmap.findIndex(t => t.title === state.currentTopicTitle);
    if (currentIndex >= 0 && currentIndex < state.roadmap.length - 1) {
        const nextTopic = state.roadmap[currentIndex + 1];
        selectTopic(nextTopic.id, nextTopic.title);
    } else {
        // Fallback to roadmap if no next topic or already at end
        goToSection('roadmap');
    }
}

// ═══════════════════════════════════════════════════════
//                  FLASHCARDS
// ═══════════════════════════════════════════════════════

async function startFlashcards() {
    document.getElementById('flashcardsTitle').textContent = `Flashcards: ${state.currentTopicTitle}`;
    goToSection('flashcards');

    const grid = document.getElementById('flashcardGrid');
    grid.innerHTML = '';
    showLoader('flashcardGrid', 'Creating flashcards...');

    try {
        const res = await fetch('/api/flashcards', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: state.currentTopicTitle, level: state.level })
        });
        const data = await res.json();
        hideLoader('flashcardGrid');
        renderFlashcards(data.cards);
        updateSidebarStats();
    } catch (err) {
        hideLoader('flashcardGrid');
        grid.innerHTML = '<div style="text-align:center;color:#ff5252;">❌ Failed to generate flashcards.</div>';
    }
}

function renderFlashcards(cards) {
    const grid = document.getElementById('flashcardGrid');
    grid.innerHTML = cards.map((card, i) => `
        <div class="flashcard" onclick="this.classList.toggle('flipped')" id="flashcard-${i}">
            <div class="flashcard-inner">
                <div class="flashcard-front">
                    <div style="font-size:2rem;margin-bottom:12px;">${card.emoji || '📘'}</div>
                    ${card.front}
                </div>
                <div class="flashcard-back">
                    ${card.back}
                </div>
            </div>
        </div>
    `).join('');
}

// ═══════════════════════════════════════════════════════
//                  GYANGURU CHAT
// ═══════════════════════════════════════════════════════

function toggleChat() {
    state.chatOpen = !state.chatOpen;
    const panel = document.getElementById('chatPanel');
    const fab = document.getElementById('chatFab');

    if (state.chatOpen) {
        panel.style.display = 'block';
        fab.textContent = '✕';
        if (state.chatMessages.length === 0) {
            addChatMessage('bot', '👋 **Namaste! I\'m GyanGuru!**\n\nAsk me anything — academics, science, math, coding, ML, general knowledge & more!');
        }
    } else {
        panel.style.display = 'none';
        fab.textContent = '🧠';
    }
}

function setChatMode(mode) {
    state.chatMode = mode;
    document.querySelectorAll('#chatModes button').forEach(btn => {
        btn.className = `btn btn-sm ${btn.dataset.mode === mode ? 'btn-primary' : 'btn-secondary'}`;
    });
}

async function sendChat() {
    const input = document.getElementById('chatInput');
    const question = input.value.trim();
    if (!question) return;

    input.value = '';
    addChatMessage('user', question);

    // Show thinking indicator
    const thinkingId = addChatMessage('bot', '🧠 *Thinking...*');

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question,
                level: state.level,
                context_topic: state.currentTopicTitle,
                chat_history: state.chatMessages.slice(-6),
                mode: state.chatMode
            })
        });
        const data = await res.json();

        // Remove thinking indicator
        removeChatMessage(thinkingId);
        addChatMessage('bot', data.text);

        // Handle media
        if (data.media) {
            if (data.media.type === 'image' && data.media.path) {
                addChatMessage('bot', `![Diagram](${data.media.path})\n\n*${data.media.desc || ''}*`);
            } else if (data.media.type === 'audio' && data.media.path) {
                addChatMessage('bot', `🎧 Audio generated. <audio controls src="${data.media.path}" style="width:100%;margin-top:8px;"></audio>`);
            } else if (data.media.type === 'video' && data.media.videos) {
                const vids = data.media.videos.slice(0, 2).map(v =>
                    v.video_id ? `🎥 [${v.title}](https://www.youtube.com/watch?v=${v.video_id})` : `🔗 [${v.title}](${v.url})`
                ).join('\n');
                addChatMessage('bot', vids);
            }
        }

        // Suggestions
        if (data.suggestions && data.suggestions.length) {
            const sugHtml = data.suggestions.map(s => `<button class="btn btn-sm btn-secondary" style="margin:2px;" onclick="document.getElementById('chatInput').value='${escapeHtml(s)}';sendChat();">${s.length > 35 ? s.slice(0, 35) + '…' : s}</button>`).join('');
            addChatMessageHtml('bot', `<div style="margin-top:8px;">${sugHtml}</div>`);
        }
    } catch (err) {
        removeChatMessage(thinkingId);
        addChatMessage('bot', '❌ Sorry, I encountered an error. Please try again.');
    }
}

let chatMsgCounter = 0;
function addChatMessage(role, text) {
    const id = `chat-msg-${chatMsgCounter++}`;
    state.chatMessages.push({ role: role === 'bot' ? 'assistant' : 'user', content: text });
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.id = id;
    div.className = `chat-msg ${role}`;
    div.innerHTML = role === 'user' ? `<strong>👤 You:</strong> ${escapeHtml(text)}` : renderMarkdown(text);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return id;
}

function addChatMessageHtml(role, html) {
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = `chat-msg ${role}`;
    div.innerHTML = html;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function removeChatMessage(id) {
    document.getElementById(id)?.remove();
}

// ═══════════════════════════════════════════════════════
//                  SIDEBAR
// ═══════════════════════════════════════════════════════

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('sidebarOverlay').classList.toggle('show');
}

function updateSidebarRoadmap() {
    const container = document.getElementById('sidebarRoadmap');
    if (!container || !state.roadmap) return;

    let html = '<div class="nav-section-title">Course Roadmap</div>';
    state.roadmap.forEach(topic => {
        const isDone = state.topicsCompleted.includes(topic.title);
        html += `<div class="nav-item ${isDone ? 'completed' : ''}" onclick="selectTopic(${topic.id}, '${escapeHtml(topic.title)}')">
            <span class="nav-icon">${topic.icon}</span>
            <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${topic.title}</span>
            ${isDone ? '<span class="nav-badge" style="background:var(--accent-green);color:#0a0a1a;">✓</span>' : ''}
        </div>`;
    });
    container.innerHTML = html;
}

function updateSidebarStats() {
    const xpEl = document.getElementById('sidebarXP');
    const barEl = document.getElementById('sidebarXPBar');
    const topicsEl = document.getElementById('sidebarTopics');

    if (xpEl) xpEl.textContent = state.xp;
    if (barEl) barEl.style.width = `${(state.xp % 150) / 1.5}%`;
    if (topicsEl) topicsEl.textContent = state.topicsCompleted.length;
}

// ═══════════════════════════════════════════════════════
//                  UTILITIES
// ═══════════════════════════════════════════════════════

function renderMarkdown(text) {
    if (!text) return '';
    try {
        if (typeof marked !== 'undefined') {
            marked.setOptions({ breaks: true, gfm: true });
            return marked.parse(text);
        }
    } catch (e) { }
    // Fallback: basic rendering
    return text
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
}

function escapeHtml(text) {
    if (!text) return '';
    return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function showLoader(containerId, text) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="spinner-container">
            <div class="spinner"></div>
            <div class="spinner-text">${text || 'Loading...'}</div>
        </div>`;
    }
}

function hideLoader(containerId) {
    // Loader gets replaced by actual content
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function showConfetti() {
    const colors = ['#4fc3f7', '#b388ff', '#69f0ae', '#f48fb1', '#ffab40', '#ff5252', '#40c4ff'];
    for (let i = 0; i < 30; i++) {
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';
        piece.style.left = `${Math.random() * 100}%`;
        piece.style.background = colors[Math.floor(Math.random() * colors.length)];
        piece.style.width = `${6 + Math.random() * 8}px`;
        piece.style.height = piece.style.width;
        piece.style.animationDelay = `${Math.random() * 2}s`;
        piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
        document.body.appendChild(piece);
        setTimeout(() => piece.remove(), 4000);
    }
}

// ═══════════════════════════════════════════════════════
//                  3D TILT EFFECTS
// ═══════════════════════════════════════════════════════

function init3DEffects() {
    document.querySelectorAll('.card-3d').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 25;
            const rotateY = (centerX - x) / 25;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// ═══════════════════════════════════════════════════════
//                  INIT
// ═══════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    init3DEffects();
    updateProgressBar('level');

    // If user already has a level and roadmap, go to roadmap
    if (state.level && state.roadmap && state.roadmap.length) {
        renderRoadmap();
        updateSidebarRoadmap();
        goToSection('roadmap');
    }

    // Re-init 3D effects when new content loads (via MutationObserver)
    const observer = new MutationObserver(() => {
        init3DEffects();
    });
    observer.observe(document.querySelector('.main-content'), { childList: true, subtree: true });
});
