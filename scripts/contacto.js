document.addEventListener("DOMContentLoaded", function() {
    const searchBtn = document.querySelector(".search-btn");
    const searchForm = document.querySelector(".search-form");
    const searchInput = document.querySelector(".search-form input[type='search']");
    const loginDropdown = document.querySelector(".login-dropdown");
    const loginBtn = document.querySelector("#loginBtn");
    const dropdownMenu = document.querySelector(".login-dropdown .dropdown-menu");
    const subscriptionLink = document.querySelector("#subscriptionLink");

    searchBtn.addEventListener("click", function() {
        searchForm.classList.toggle("open");
        if (searchForm.classList.contains("open")) {
            searchInput.focus();
        } else {
            searchInput.value = ""; // Limpiar el valor cuando se cierra
        }
    });

    loginBtn.addEventListener("click", function() {
        dropdownMenu.classList.toggle("show");
    });

    document.addEventListener("click", function(event) {
        if (!event.target.closest(".search-form") && !event.target.closest(".search-btn")) {
            searchForm.classList.remove("open");
            searchInput.value = ""; // Limpiar el valor cuando se cierra
        }
        if (!event.target.closest(".login-dropdown")) {
            dropdownMenu.classList.remove("show");
        }
    });

    subscriptionLink.addEventListener("click", function() {
        $('#loginModal').modal('show');
    });

    const nameInput = document.getElementById('name');
    nameInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^A-Za-záéíóúñÁÉÍÓÚÑ\s]/g, '');
    });
});
