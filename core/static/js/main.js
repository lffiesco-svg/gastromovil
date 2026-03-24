// MENU MOVIL
function toggleMenu() {
    const menu = document.getElementById('menuMovil');
    const btn = document.getElementById('menuBtn');
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
    const icon = btn.querySelector('i');
    icon.classList.toggle('fa-bars');
    icon.classList.toggle('fa-xmark');
}

// CHAT IA
function toggleIA() {
    const chat = document.getElementById('iaChat');
    chat.classList.toggle('hidden');
    chat.classList.toggle('flex');
}

function sendIA() {
    const input = document.getElementById('iaInput');
    const messages = document.getElementById('iaMessages');
    const text = input.value.trim();
    if (!text) return;
    const userMsg = document.createElement('div');
    userMsg.className = 'bg-[#FF8C00] text-white p-3 rounded-2xl rounded-br-sm text-sm self-end max-w-xs ml-auto';
    userMsg.textContent = text;
    messages.appendChild(userMsg);
    input.value = '';
    messages.scrollTop = messages.scrollHeight;
    setTimeout(() => {
        const botMsg = document.createElement('div');
        botMsg.className = 'bg-white p-3 rounded-2xl rounded-bl-sm text-sm text-gray-700 shadow-sm max-w-xs';
        botMsg.textContent = '¡Gracias por tu mensaje! Pronto te ayudaremos. 🍔';
        messages.appendChild(botMsg);
        messages.scrollTop = messages.scrollHeight;
    }, 1000);
}

// OJO CONTRASEÑA
function togglePassword(inputId, eyeId) {
    const input = document.getElementById(inputId);
    const eye = document.getElementById(eyeId);
    if (input.type === 'password') {
        input.type = 'text';
        eye.classList.remove('fa-eye');
        eye.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        eye.classList.remove('fa-eye-slash');
        eye.classList.add('fa-eye');
    }
}