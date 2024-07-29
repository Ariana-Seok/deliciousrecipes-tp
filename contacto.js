document.addEventListener("DOMContentLoaded", function() {
    const searchBtn = document.querySelector(".search-btn");
    const searchForm = document.querySelector(".search-form");
    const searchInput = document.querySelector(".search-form input[type='search']");
    const subscriptionBtn = document.querySelector("#suscripcionBtn");
    const loginBtn = document.querySelector("#loginBtn");
    const sendContactFormBtn = document.querySelector("#sendContactForm");
    const deleteContactBtn = document.querySelector("#deleteContact");
    const editContactBtn = document.querySelector("#editContact");
    const enviarComentarioBtn = document.getElementById('enviarComentarioBtn');

    


    // Mostrar u ocultar el formulario de búsqueda
    searchBtn.addEventListener("click", function() {
        searchForm.classList.toggle("open");
        if (searchForm.classList.contains("open")) {
            searchInput.focus();
        } else {
            searchInput.value = "";
        }
    });

    // Mostrar el modal de inicio de sesión
    loginBtn.addEventListener("click", function() {
        $('#loginModal').modal('show');
    });

    // Abrir la página de suscripción en una nueva ventana
    subscriptionBtn.addEventListener("click", function() {
        window.open("suscripcion.html", "_blank");
    });

    // Cerrar el formulario de búsqueda si se hace clic fuera de él
    document.addEventListener("click", function(event) {
        if (!event.target.closest(".search-form") && !event.target.closest(".search-btn")) {
            searchForm.classList.remove("open");
            searchInput.value = "";
        }
    });

    // Validar el campo de nombre para permitir solo letras y espacios
    const nameInput = document.getElementById('name');
    nameInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^A-Za-záéíóúñÁÉÍÓÚÑ\s]/g, '');
    });

    // Inicializar el carrusel del modal de inicio de sesión
    $('#loginModal').on('shown.bs.modal', function() {
        $('#loginCarousel').carousel({
            interval: 3000
        });
    });

    window.iniciar_sesion = async function() {
        const email = document.getElementById('emailModal').value;
        const password = document.getElementById('passwordModal').value;
        const messageElement = document.getElementById('loginMessage');
    
        if (!email || !password) {
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Por favor, ingrese ambos campos.</div>';
            return;
        }
    
        try {

            const url = `http://127.0.0.1:5000/iniciar_sesion?correo=${encodeURIComponent(email)}&contrasenia=${encodeURIComponent(password)}`;
    

            const response = await fetch(url, {
                method: 'GET'
            });
    
            const result = await response.json();
    
            // Mostrar mensaje basado en la respuesta del servidor
            if (response.ok) {
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">Sesión iniciada con éxito.</div>';
                document.getElementById('loginButtonModal').textContent = 'Sesión OK';
    
                deleteContactBtn.disabled = false;
                editContactBtn.disabled = false;
    
                // Ocultar el modal de inicio de sesión después de 2 segundos
                setTimeout(() => {
                    $('#loginModal').modal('hide');
                }, 2000);
            } else {
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + result.error + '</div>';
            }
        } catch (error) {
            console.error('Error en el inicio de sesión:', error);
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Error en el servidor. Intente nuevamente más tarde.</div>';
        }
    };

    // Función para eliminar usuario
    async function eliminar_usuario() {
        const email = document.getElementById('emailModal').value;
        const password = document.getElementById('passwordModal').value;
        const messageElement = document.getElementById('loginMessage');
    
        if (!email || !password) {
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Por favor, ingrese ambos campos para eliminar el usuario.</div>';
            return;
        }
    
        try {
           
            const url = `http://127.0.0.1:5000/eliminar_usuario?correo=${encodeURIComponent(email)}&contrasenia=${encodeURIComponent(password)}`;
            
            
            const response = await fetch(url, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
    
            if (response.ok) {
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">Usuario eliminado con éxito.</div>';
                setTimeout(() => {
                    $('#loginModal').modal('hide');
                }, 2000);
            } else {
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + result.error + '</div>';
            }
        } catch (error) {
            console.error('Error al eliminar el usuario:', error);
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Error en el servidor. Intente nuevamente más tarde.</div>';
        }
    }
    


    // Función para editar usuario
    async function editar_usuario() {
        
        const email = document.getElementById('emailModal').value;
        const password = document.getElementById('passwordModal').value;
        const messageElement = document.getElementById('loginMessage');
        const contrasenia_nueva = document.getElementById('passwordModal2').value;

        
        if (!email || !password) {
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Por favor, ingrese ambos campos.</div>';
            return;
        }

        try {

            const url = `http://127.0.0.1:5000/editar_usuario?correo=${encodeURIComponent(email)}&contrasenia=${encodeURIComponent(password)}&contrasenia_nueva={${encodeURIComponent(contrasenia_nueva)}`;

            const response = await fetch(url, {
                method: 'PATCH'
            });

            const result = await response.json();

            
            if (response.ok) {
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">Usuario editado con éxito.</div>';
                setTimeout(() => {
                    $('#editar_modal').modal('hide');  // Ocultar el modal después de editar
                }, 7000);
            } else {
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + result.error + '</div>';
            }
        } catch (error) {
            console.error('Error al editar el usuario:', error);
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Error en el servidor. Intente nuevamente más tarde.</div>';
        }
    }

    document.addEventListener("DOMContentLoaded", function() {
        const enviarComentarioBtn = document.getElementById('enviarComentarioBtn');
    
        enviarComentarioBtn.addEventListener("click", function() {
            enviarComentario();
        });
    
        async function enviarComentario() {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            const messageElement = document.getElementById('loginMessage1');
    
            if (!name || !email || !message) {
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Por favor, complete todos los campos.</div>';
                return;
            }
    
            try {
                const url = `http://127.0.0.1:5000/comentarios2`;
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        nombre: name,
                        correo: email,
                        mensaje: message
                    }),
                });
    
                const result = await response.json();
    
                if (response.ok) {
                    messageElement.innerHTML = '<div class="alert alert-success" role="alert">Comentario enviado con éxito.</div>';
                    // Limpiar el formulario después de enviar el comentario
                    document.getElementById('contactForm').reset();
                } else {
                    messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + result.error + '</div>';
                }
            } catch (error) {
                console.error('Error al enviar el comentario:', error);
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Error en el servidor. Intente nuevamente más tarde.</div>';
            }
        }
    });
    
    

document.getElementById('editContact').addEventListener('click', mostrarModalEditarUsuario);


    deleteContactBtn.addEventListener("click", eliminar_usuario);
    editContactBtn.addEventListener("click", editar_usuario);
});
