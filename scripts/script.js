document.addEventListener("DOMContentLoaded", function() {
    const subscriptionBtn = document.querySelector("#suscripcionBtn");
    const loginBtn = document.querySelector("#loginBtn");

    // Mostrar el modal de inicio de sesión
    loginBtn.addEventListener("click", function() {
        $('#loginModal').modal('show');
    });

    loginBtn.addEventListener("click", function() {
        $('#loginModal').modal('show');
    });
    // Validación del campo de nombre
    const nameInput = document.getElementById('name');
    nameInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^A-Za-záéíóúñÁÉÍÓÚÑ\s]/g, '');
    });
});