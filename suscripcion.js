document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("#subscriptionForm");
    const telefonoInput = document.querySelector("#suscripcionTelefono");
    const codigoAreaInput = document.querySelector("#suscripcionCodigoArea");
    const registerButton = document.querySelector("#registerSubscription");

    telefonoInput.addEventListener("input", function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
    });

    codigoAreaInput.addEventListener("input", function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 5);
    });

    // Función para suscripción de usuario
    async function suscripcion_usuario() {
        const email = document.getElementById('suscripcionEmail').value;
        const password = document.getElementById('suscripcionPassword').value;

        if (!email || !password) {
            alert("Por favor, complete todos los campos.");
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/suscripcion_usuario', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ correo: email, contrasenia: password })
            });

            const result = await response.json();
            if (response.ok) {
                alert("Suscripción realizada correctamente.");
                form.reset(); 
            } else {
                alert("Hubo un problema al realizar la suscripción: " + (result.error || "Error desconocido"));
            }
        } catch (error) {
            alert("Error en la conexión: " + error.message);
        } finally {
            registerButton.disabled = false;
        }
    };

    // Evento onclick del botón Registrar
    registerButton.addEventListener("click", function(event) {
        event.preventDefault(); 
        registerButton.disabled = true; 
        suscripcion_usuario();
    });
});
