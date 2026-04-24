function toggleEditar() {
    const campos = ['nombre', 'apellido', 'telefono'];
    const editarBtn = document.getElementById('editarBtn');
    const guardarBtn = document.getElementById('guardarBtn');
    
    campos.forEach(id => {
        const input = document.getElementById(id);
        input.disabled = false;
        input.style.borderColor = '#DC2626';
    });

    editarBtn.classList.add('hidden');
    guardarBtn.classList.remove('hidden');
}

function guardarCambios() {
    const campos = ['nombre', 'apellido', 'telefono'];
    const editarBtn = document.getElementById('editarBtn');
    const guardarBtn = document.getElementById('guardarBtn');

    campos.forEach(id => {
        const input = document.getElementById(id);
        input.disabled = true;
        input.style.borderColor = '#3a1515';
    });

    editarBtn.classList.remove('hidden');
    guardarBtn.classList.add('hidden');
}