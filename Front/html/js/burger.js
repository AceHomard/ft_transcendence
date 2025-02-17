document.getElementById('burgerMenu').addEventListener('click', function () {
	this.classList.toggle('open');
	document.querySelector('.nav-buttons').classList.toggle('open');
});

// Fonction pour gérer le clic sur le bouton dropdown en mode mobile
function toggleDropdown() {
    var dropdownContent = document.querySelector('.dropdown .dropdown-content');
    dropdownContent.classList.toggle('show');
}

// Ajoute un écouteur d'événements au bouton dropdown pour le clic
document.getElementById('Profil').addEventListener('click', function (e) {
    e.preventDefault(); // Empêche le comportement par défaut du bouton
    toggleDropdown();
});

// Ajoute un écouteur d'événements global pour fermer le dropdown si on clique en dehors
document.addEventListener('click', function (e) {
    var dropdown = document.querySelector('.dropdown');
    var dropdownContent = document.querySelector('.dropdown .dropdown-content');

    // Vérifie si le clic est en dehors du dropdown
    if (!dropdown.contains(e.target)) {
        dropdownContent.classList.remove('show');
    }
});
