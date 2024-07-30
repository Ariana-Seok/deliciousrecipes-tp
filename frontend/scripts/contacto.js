
/* PARTE QUE HACE QUE APARESCA LA VENTANAN
document.addEventListener("DOMContentLoaded", function() {
  const subscriptionBtn = document.querySelector("#suscripcionBtn");
  const loginBtn = document.querySelector("#loginBtn");
  
  subscriptionBtn.addEventListener("click", function() {
      window.open("suscripcion.html", "_blank");
  });

  loginBtn.addEventListener("click", function() {
      $('#loginModal').modal('show');
  });
});

*/
/*
PUEBA
*/


document.addEventListener("DOMContentLoaded", function() {
  const searchBtn = document.querySelector(".search-btn");
  const searchForm = document.querySelector(".search-form");
  const searchInput = document.querySelector(".search-form input[type='search']");
  const subscriptionBtn = document.querySelector("#suscripcionBtn");
  const loginBtn = document.querySelector("#loginBtn");

  /*
  const loginBtn = document.querySelector("#loginBtn");
  const subscriptionBtn = document.querySelector("#subscriptionBtn");*/

  // Funcionalidad del botón de búsqueda
  searchBtn.addEventListener("click", function() {
    searchForm.classList.toggle("open");
    if (searchForm.classList.contains("open")) {
      searchInput.focus();
    } else {
      searchInput.value = ""; // Limpiar el valor cuando se cierra
    }
  });

  // Mostrar el modal de inicio de sesión
  loginBtn.addEventListener("click", function() {
    $('#loginModal').modal('show');
  });

  // Redirigir a la página de suscripción
    subscriptionBtn.addEventListener("click", function() {
      window.open("suscripcion.html", "_blank");
  });

  loginBtn.addEventListener("click", function() {
      $('#loginModal').modal('show');
  });


  /*/
  subscriptionBtn.addEventListener("click", function() {
    window.location.href = "url_to_subscription_page.html";

  });
  */

  // Cerrar el formulario de búsqueda si se hace clic fuera de él
  document.addEventListener("click", function(event) {
    if (!event.target.closest(".search-form") && !event.target.closest(".search-btn")) {
      searchForm.classList.remove("open");
      searchInput.value = ""; // Limpiar el valor cuando se cierra
    }
  });

  // Validación del campo de nombre
  const nameInput = document.getElementById('name');
  nameInput.addEventListener('input', function() {
    this.value = this.value.replace(/[^A-Za-záéíóúñÁÉÍÓÚÑ\s]/g, '');
  });

  // Inicializar carrusel en el modal de inicio de sesión
  $('#loginModal').on('shown.bs.modal', function() {
    $('#loginCarousel').carousel({
      interval: 3000 // Cambia cada 3 segundos
    });
  });
});
