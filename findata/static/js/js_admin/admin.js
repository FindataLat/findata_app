// Toggle Sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

// Abrir modal de edición
function openEditModal(userName, userLastname, userMail, userPhone, userContry, userAge, userOcupation, userRol, userId) {
    fetch(`/update-user/${userId}`)
        .then(res => res.json())
        .then(data => {
            console.log("📌 DATOS DEL BACKEND:", data);

            document.getElementById('editUserId').value = data.id ?? userId;
            document.getElementById('editUserName').value = data.name ?? userName;
            document.getElementById('editUserLastname').value = data.lastname ?? userLastname;
            document.getElementById('editUserEmail').value = data.mail ?? userMail;
            document.getElementById('editUserPhone').value = data.phone ?? userPhone;
            document.getElementById('editUserCountry').value = data.contry ?? userContry;
            document.getElementById('editUserAge').value = data.age ?? userAge;
            document.getElementById('editUserOcupation').value = data.ocupation ?? userOcupation;
            document.getElementById('editUserPlan').value = data.rol ?? userRol;

            if (data.status) {
                document.getElementById('editUserStatus').value = data.status;
            }
        })
        .catch(err => console.error("❌ ERROR FETCH:", err));

    document.getElementById('editModal').classList.add('active');
}

// Cerrar modal de edición
function closeEditModal() {
    document.getElementById('editModal').classList.remove('active');
}

// Guardar cambios del usuario
function saveUserChanges(event) {
    event.preventDefault();
    
    const userId = document.getElementById('editUserId').value;
    const formData = new FormData(event.target);

    fetch(`/update-user/${userId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Cerrar modal de edición
        closeEditModal();
        
        // Mostrar modal de éxito/error
        showMessageModal(data.success, data.message);
        
        // Recargar después de 2 segundos
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessageModal(false, 'Error al actualizar el usuario');
    });
}

// Mostrar modal de mensajes dinámicamente
function showMessageModal(isSuccess, message) {
    // Crear modal si no existe
    let modal = document.getElementById('messageModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'messageModal';
        modal.className = 'modal-overlay';
        document.body.appendChild(modal);
    }
    
    const theme = isSuccess ? 'modal-success-theme' : 'modal-error-theme';
    const icon = isSuccess ? 'bi-check-circle' : 'bi-x-circle';
    const title = isSuccess ? '¡Actualización exitosa!' : 'Error en la actualización';
    
    modal.innerHTML = `
        <div class="modal-content ${theme}">
            <div class="modal-icon">
                <i class="bi ${icon}"></i>
            </div>
            <div class="modal-body">
                <h3>${title}</h3>
                <p>${message}</p>
            </div>
            <button class="modal-btn" onclick="closeModal()">
                ${isSuccess ? 'Continuar' : 'Intentar nuevamente'}
            </button>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// Cerrar modal de mensajes
function closeModal() {
    const messageModal = document.getElementById('messageModal');
    if (messageModal) {
        messageModal.style.display = 'none';
    }
}

// Mostrar modal de mensajes al cargar (si viene de URL)
window.onload = function() {
    const messageModal = document.getElementById('messageModal');
    if (messageModal) {
        messageModal.style.display = 'flex';
    }
}

// Cerrar modales con ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
        closeEditModal();
    }
});

// Cerrar modal de mensajes al hacer clic fuera
document.addEventListener('DOMContentLoaded', function() {
    const messageModal = document.getElementById('messageModal');
    if (messageModal) {
        messageModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    }

    const editModal = document.getElementById('editModal');
    if (editModal) {
        editModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeEditModal();
            }
        });
    }
});