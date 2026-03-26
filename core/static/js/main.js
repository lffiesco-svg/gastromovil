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
function sendIA() {
    const input = document.getElementById('iaInput');
    const messages = document.getElementById('iaMessages');
    const text = input.value.trim();

    if (!text) return;

    // Mostrar mensaje del usuario
    const userMsg = document.createElement('div');
    userMsg.className = 'bg-[#FF8C00] text-white p-3 rounded-2xl rounded-br-sm text-sm self-end max-w-xs ml-auto';
    userMsg.textContent = text;
    messages.appendChild(userMsg);

    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    // Indicador de escritura (loader)
    const typingMsg = document.createElement('div');
    typingMsg.className = 'bg-white p-3 rounded-2xl rounded-bl-sm text-sm text-gray-400 shadow-sm max-w-xs italic';
    typingMsg.textContent = 'Escribiendo...';
    typingMsg.id = 'typing-indicator';
    messages.appendChild(typingMsg);
    messages.scrollTop = messages.scrollHeight;

    // Agregar mensaje al historial antes de enviarlo
    chatHistorial.push({ role: 'user', content: text });

    // Enviar al backend como JSON
    fetch("/api/chatbot/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRF(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mensaje: text,
            historial: chatHistorial.slice(-6) // Enviar últimos 6 mensajes de contexto
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
        botMsg.innerHTML = data.respuesta; // ← tu cambio
        messages.appendChild(botMsg);
        messages.scrollTop = messages.scrollHeight;

        chatHistorial.push({ role: 'assistant', content: data.respuesta });
    })
    .catch(err => {
        // Remover indicador de escritura
        document.getElementById('typing-indicator')?.remove();

        const errorMsg = document.createElement('div');
        errorMsg.className = 'bg-red-100 text-red-700 p-3 rounded-2xl text-sm max-w-xs';
        errorMsg.textContent = "Error conectando con la IA. Intenta de nuevo.";
        messages.appendChild(errorMsg);
        messages.scrollTop = messages.scrollHeight;

        // Remover el último mensaje del historial si hubo error
        chatHistorial.pop();

        console.error("[Chatbot error]:", err);
    });
}

// Enviar mensaje con ENTER
document.addEventListener("DOMContentLoaded", function () {
    const iaInput = document.getElementById("iaInput");
    if (iaInput) {
        iaInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                sendIA();
            }
        });
    }
});
