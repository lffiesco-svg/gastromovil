// ABRIR / CERRAR CHAT IA
function toggleChat() {
    const chat = document.getElementById('iaChat');
    if (chat.classList.contains('hidden')) {
        chat.classList.remove('hidden');
        chat.classList.add('flex');
    } else {
        chat.classList.add('hidden');
        chat.classList.remove('flex');
    }
}

// ABRIR / CERRAR MENU MOVIL
function toggleMenu() {
    const menu = document.getElementById('menuMovil');
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        menu.classList.add('flex');
    } else {
        menu.classList.add('hidden');
        menu.classList.remove('flex');
    }
}

function toggleUserMenu() {
    const menu = document.getElementById('userMenu');
    menu.classList.toggle('hidden');
}

document.addEventListener('click', function(e) {
    const menu = document.getElementById('userMenu');
    if (menu && !menu.contains(e.target) && !e.target.closest('button[onclick="toggleUserMenu()"]')) {
        menu.classList.add('hidden');
    }
});


// Obtener CSRF desde cookies
function getCSRF() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

// Historial de conversación (se mantiene en memoria durante la sesión)
const chatHistorial = [];

// ENVIAR MENSAJE A LA IA REAL
let esperandoRespuesta = false;

function sendIA() {
    if (esperandoRespuesta) return; // 🔒 Bloquea si está esperando respuesta

    const input = document.getElementById('iaInput');
    const messages = document.getElementById('iaMessages');
    const btn = document.querySelector('#iaChat button[onclick="sendIA()"]');
    const text = input.value.trim();

    if (!text) return;

    // 🔒 Bloquear input y botón
    esperandoRespuesta = true;
    input.setAttribute('readonly', true);        // ← bloquea escritura
    input.disabled = true;
    input.value = '';
    input.placeholder = 'Esperando respuesta...';
    if (btn) {
        btn.disabled = true;
        btn.classList.add('opacity-50', 'cursor-not-allowed');
        btn.classList.remove('hover:scale-110');
    }

    // Mostrar mensaje del usuario
    const userMsg = document.createElement('div');
    userMsg.className = 'bg-[#FF8C00] text-white p-3 rounded-2xl rounded-br-sm text-sm self-end max-w-xs ml-auto';
    userMsg.textContent = text;
    messages.appendChild(userMsg);

    messages.scrollTop = messages.scrollHeight;

    // Indicador de escritura
    const typingMsg = document.createElement('div');
    typingMsg.className = 'bg-white p-3 rounded-2xl rounded-bl-sm text-sm text-gray-400 shadow-sm max-w-xs italic';
    typingMsg.textContent = 'Escribiendo...';
    typingMsg.id = 'typing-indicator';
    messages.appendChild(typingMsg);
    messages.scrollTop = messages.scrollHeight;

    chatHistorial.push({ role: 'user', content: text });

    fetch("/api/chatbot/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRF(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mensaje: text,
            historial: chatHistorial.slice(-6)
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw new Error(JSON.stringify(err)); });
        }
        return res.json();
    })
    .then(data => {
        document.getElementById('typing-indicator')?.remove();

        const botMsg = document.createElement('div');
        botMsg.className = 'bg-white p-3 rounded-2xl rounded-bl-sm text-sm text-gray-700 shadow-sm max-w-[85%]';
        botMsg.innerHTML = data.respuesta;
        messages.appendChild(botMsg);
        messages.scrollTop = messages.scrollHeight;

        chatHistorial.push({ role: 'assistant', content: data.respuesta });
    })
    .catch(err => {
        document.getElementById('typing-indicator')?.remove();

        const errorMsg = document.createElement('div');
        errorMsg.className = 'bg-red-100 text-red-700 p-3 rounded-2xl text-sm max-w-xs';
        errorMsg.textContent = "Error conectando con la IA. Intenta de nuevo.";
        messages.appendChild(errorMsg);
        messages.scrollTop = messages.scrollHeight;

        chatHistorial.pop();
        console.error("[Chatbot error]:", err);
    })
    .finally(() => {
        // 🔓 Desbloquear siempre al terminar (éxito o error)
        esperandoRespuesta = false;
        input.removeAttribute('readonly');           // ← reactiva escritura
        input.disabled = false;
        input.placeholder = 'Escribe tu pregunta...';
        if (btn) {
            btn.disabled = false;
            btn.classList.remove('opacity-50', 'cursor-not-allowed');
            btn.classList.add('hover:scale-110');
        }
        input.focus();
    });
}

// Enviar mensaje con ENTER
document.addEventListener("DOMContentLoaded", function () {
    const iaInput = document.getElementById("iaInput");
    if (iaInput) {
        iaInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                if (!esperandoRespuesta) sendIA(); // ✅ Verifica el bloqueo antes de enviar
            }
        });
    }
});

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