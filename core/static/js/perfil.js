// PERFIL
function toggleEditar() {
    const campos = ['nombre', 'apellido', 'email', 'telefono'];
    const editarBtn = document.getElementById('editarBtn');
    const guardarBtn = document.getElementById('guardarBtn');
    
    campos.forEach(id => {
        const input = document.getElementById(id);
        input.disabled = !input.disabled;
        if (!input.disabled) {
            input.classList.add('border-[#FF8C00]', 'bg-white');
            input.classList.remove('bg-gray-100');
        }
    });

    editarBtn.classList.add('hidden');
    guardarBtn.classList.remove('hidden');
}

function guardarCambios() {
    const campos = ['nombre', 'apellido', 'email', 'telefono'];
    const editarBtn = document.getElementById('editarBtn');
    const guardarBtn = document.getElementById('guardarBtn');

    campos.forEach(id => {
        const input = document.getElementById(id);
        input.disabled = true;
        input.classList.remove('border-[#FF8C00]', 'bg-white');
        input.classList.add('bg-gray-100');
    });

    editarBtn.classList.remove('hidden');
    guardarBtn.classList.add('hidden');
}

// MODAL ELIMINAR CUENTA
function abrirModalEliminar() {
    document.getElementById('modal-eliminar').classList.remove('hidden');
}

function cerrarModalEliminar() {
    document.getElementById('modal-eliminar').classList.add('hidden');
}