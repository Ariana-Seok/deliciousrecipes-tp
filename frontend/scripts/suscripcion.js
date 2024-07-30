document.addEventListener("DOMContentLoaded", function() {
    const subscriptionBtn = document.querySelector("#suscripcionBtn");
    const form = document.querySelector("#subscriptionForm");
    const telefonoInput = document.querySelector("#suscripcionTelefono");
    const codigoAreaInput = document.querySelector("#suscripcionCodigoArea");

    telefonoInput.addEventListener("input", function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
    });

    codigoAreaInput.addEventListener("input", function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 5);
    });

    subscriptionBtn.addEventListener("click", function(event) {
        event.preventDefault();
        if (form.checkValidity()) {
            alert("Formulario enviado correctamente ;)");
        } else {
            form.reportValidity();
            alert("Por favor, completa todos los campos correctamente.");
        }
    });
});
