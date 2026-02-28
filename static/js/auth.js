/**
 * LearnSphere — Authentication JavaScript
 * Handles login, registration, and social auth
 */

// ─── Login ───
async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById('loginBtn');
    const errorEl = document.getElementById('loginError');
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    errorEl.classList.remove('show');
    btn.textContent = '⏳ Signing in...';
    btn.disabled = true;

    try {
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = '/dashboard';
        } else {
            errorEl.textContent = data.error || 'Login failed';
            errorEl.classList.add('show');
        }
    } catch (err) {
        errorEl.textContent = 'Connection error. Please try again.';
        errorEl.classList.add('show');
    }

    btn.textContent = '🚀 Sign In';
    btn.disabled = false;
    return false;
}

// ─── Register ───
async function handleRegister(e) {
    if (e) e.preventDefault();
    const btn = document.getElementById('registerBtn');
    const errorEl = document.getElementById('registerError');
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value.trim();
    const display_name = username; // Use username as display name

    if (errorEl) errorEl.classList.remove('show');

    if (!username || !password || !email) {
        if (errorEl) {
            errorEl.textContent = 'Username, password, and email are required';
            errorEl.classList.add('show');
        }
        return false;
    }

    if (btn) {
        btn.textContent = '⏳ Creating account...';
        btn.disabled = true;
    }

    try {
        const res = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, email, display_name })
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = '/dashboard';
        } else {
            if (errorEl) {
                errorEl.textContent = data.error || 'Registration failed';
                errorEl.classList.add('show');
            }
            if (btn) {
                btn.textContent = 'Create Account';
                btn.disabled = false;
            }
        }
    } catch (err) {
        if (errorEl) {
            errorEl.textContent = 'Connection error. Please try again.';
            errorEl.classList.add('show');
        }
        if (btn) {
            btn.textContent = 'Create Account';
            btn.disabled = false;
        }
    }

    return false;
}

// ─── 3D Tilt Effect on Auth Card ───
document.addEventListener('DOMContentLoaded', () => {
    const card = document.getElementById('authCard');
    if (!card) return;

    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 30;
        const rotateY = (centerX - x) / 30;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
    });
});
