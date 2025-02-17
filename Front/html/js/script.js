let raw_url = window.location.host
let isLoading = false;
let disconnection = false;

// Fonction pour charger le contenu via AJAX et mettre à jour l'URL dans l'historique du navigateur
function loadContent(url) {
	toggleButtonsVisibility();
	const token = getJwtTokenFromCookie(); // Fonction à implémenter pour récupérer le token JWT depuis les cookies

	// Définir les en-têtes avec le token JWT
	const headers = {};
	if (token) {
		headers['Authorization'] = `token ${token}`;
	}

	// Effectuer la requête fetch avec les en-têtes
	fetch(url, {
		method: 'GET',
		headers: headers,
		// credentials: 'same-origin' // Inclure les cookies dans les requêtes CORS
		credentials: 'include', // Inclure les cookies
		mode: 'cors' // Activer CORS
	})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.text(); // Ou response.json() si vous récupérez du JSON
		})
		.then(data => {
			const content = document.getElementById('content'); // Assurez-vous que cet élément existe
			content.innerHTML = data;
			if (url.includes(`https://${raw_url}/front/history/`)) {
				let startindex = url.lastIndexOf('/') + 1
				let Uniqid = url.substring(startindex)
				if (Uniqid) {
					fetch(`https://${raw_url}/front/history/get/${Uniqid}`)
						.then((reponse) => {
							if (reponse.ok)
								reponse.json().then((datas) => {
									leaderboard.setId(0);
									if (datas["all_matchs"].length !== 0)
										for (const data of datas["all_matchs"])
										{
											const score = data["player1_score"] + " - " + data["player2_score"];
											const eth_link = "https://sepolia.etherscan.io/tx/" + data["tx_hash"];
											const date = new Date(data["timestamp"] * 1000);
											leaderboard.addMatch(data["player1_pseudo"], data["player2_pseudo"], data["player1_img"], data["player2_img"], data["player1_id"], data["player2_id"], score, data["win"], data["from_blockchain"], eth_link, date.toLocaleDateString());
										}
									else
										leaderboard.NoMatchFound();
									document.getElementById('loader_history').style.display = "none";
									leaderboard.createProfil(datas);
									// Sauvegarder le contenu final du HTML généré
									const finalHTML = content.innerHTML;
									const newState = { content: finalHTML };
									history.pushState(newState, "", "");
								});
							else {
								document.getElementById('loader_history').style.display = "none";
								leaderboard.setId(0);
								leaderboard.NoMatchFound();
							}
						})
						.catch(() => {
							//console.log("wrong API call");
						})
						.finally(() => {
							isLoading = false;
						})
				} else {
					//console.log("Uniqid not found in cookies");
				}
				return;
			}
			// Mettre à jour l'URL dans l'historique du navigateur
			// if(url != `https://${raw_url}/front/game/local/` && url != `https://${raw_url}/front/game/on`)
			// {
				const newState = { content: data };
				loadTranslations(getCookie("langue"));
				history.pushState(newState, "", "");
			//}
			if (url != `https://${raw_url}/front/signup/` &&
				url != `https://${raw_url}/front/login/` &&
				url != `https://${raw_url}/front/game/on`) {
				social.Show();
			}
			else {
				social.Close();
				social.Hide();
			}

			if (url == `https://${raw_url}/front/pong/`) {
				CancelFakeGame();
				PlayFakeGame();
				matchmaking.getActualState();
			}
			else
				CancelFakeGame();
			if (url == `https://${raw_url}/front/game/on`)
			{
				initGame();
				document.getElementById("canvas_game").style.display = "none";
				document.getElementById("cli-input").style.display = "none";
			}
			if (url == `https://${raw_url}/front/game/local/`)
			{
				initGamelocal();
			}
			if (url == `https://${raw_url}/front/signup/`)
			{
				let identifiant = new FormInputTitle("identifiant");
				let username = new FormInputTitle("username");
				let email = new FormInputTitle("email");
				let password = new FormInputTitle("password");
				let confirm_password = new FormInputTitle("confirm_password");
			}
			if (url == `https://${raw_url}/auth/profil/`) {
				let username = new FormInputTitle("username");
				let email = new FormInputTitle("email");
				let password = new FormInputTitle("password");
			}
			if (url == `https://${raw_url}/front/login/`) {
				let identifiant = new FormInputTitle("identifiant");
				let password = new FormInputTitle("password");
				if (disconnection == true)
				{
					disconnection = false;
				}
			}
			if (url == `https://${raw_url}/front/2fa/`) {
				let identifiant = new FormInputTitle("identifiant");
				let otp_code = new FormInputTitle("otp_code");
			}
		})
		.catch(error => {
			console.error('There was a problem with the fetch operation:', error);
		});
}

// Gestionnaire d'événements popstate
window.addEventListener("popstate", (event) => {
	// Vérifiez si event.state est défini et contient le contenu
	if (event.state && event.state.content) {
		const content = document.getElementById('content');
		content.innerHTML = event.state.content; // Mettre à jour le contenu avec celui stocké dans l'état
	}
});

// Vérifier si le cookie 'token' est présent
function isTokenPresent() {
	const cookies = document.cookie.split(';').map(cookie => cookie.trim());
	const tokenCookie = cookies.find(cookie => cookie.startsWith('token='));
	return tokenCookie ? true : false;
}

// Écouteur d'événement pour le chargement initial de la page
window.addEventListener('DOMContentLoaded', () => {
	if (isTokenPresent()) {
		updatePlayerId();
		loadContent(`https://${raw_url}/front/pong/`);
	} else {
		loadContent(`https://${raw_url}/front/login/`);
	}

	//partie pour le select personnalisé
	const selectElement = document.getElementById('language-selector');
	const customSelect = document.querySelector('.custom-select');
	const selectedOption = customSelect.querySelector('.selected-option');
	const optionsContainer = customSelect.querySelector('.options-container');
	const options = optionsContainer.querySelectorAll('.option');

	selectedOption.addEventListener('click', () => {
		customSelect.classList.toggle('active');
	});

	options.forEach(option => {
		option.addEventListener('click', () => {
			const value = option.getAttribute('data-value');
			selectElement.value = value; // Mise à jour de la valeur du sélecteur natif
			customSelect.classList.remove('active');
			// Déclenchement de l'événement change pour mettre à jour les traductions
			var event = new Event('change');
			selectElement.dispatchEvent(event);
		});
	});

	document.addEventListener('click', (event) => {
		if (!customSelect.contains(event.target)) {
			customSelect.classList.remove('active');
		}
	});

	// Initialisation des traductions avec la langue par défaut

	if (getCookie("langue") != "") {
		loadTranslations(getCookie("langue"));
		return;
	}
	else {
		const defaultLanguage = selectElement.value;
		setCookie("langue", defaultLanguage, 365);
		loadTranslations(getCookie("langue"));
	}
});

// Écouteurs d'événements pour les boutons de navigation
document.getElementById('Game').addEventListener('click', () => {
	loadContent(`https://${raw_url}/front/pong/`);
});
document.getElementById('signinButton').addEventListener('click', () => {
	loadContent(`https://${raw_url}/front/signup/`);
});
document.getElementById('loginButton').addEventListener('click', () => {
	loadContent(`https://${raw_url}/front/login/`);
});

document.getElementById('Settings').addEventListener('click', () => {
	loadContent(`https://${raw_url}/auth/profil/`);
});

document.getElementById('History').addEventListener('click', () => {
		let uniqueID = getUniqidFromCookie();
		loadHistory(`https://${raw_url}/front/history/` + uniqueID);
});

function loadHistory(url)
{
	if(isLoading)
		return;
	isLoading = true;
	loadContent(url);
}

function localgame(){
	loadContent(`https://${raw_url}/front/game/local/`);
};

function botted(){
	loadContent(`https://${raw_url}/front/game/on`);
	joinBot();
};

function getJwtTokenFromCookie() {
	// Récupérer tous les cookies
	const cookies = document.cookie.split(';').map(cookie => cookie.trim());

	// Chercher le cookie contenant le token JWT
	const tokenCookie = cookies.find(cookie => cookie.startsWith('token='));

	// Si le cookie contenant le token JWT est trouvé
	if (tokenCookie) {
		// Extraire le token JWT de la chaîne du cookie
		const token = tokenCookie.split('=')[1];
		return token;
	} else {
		// Si le cookie contenant le token JWT n'est pas trouvé, retourner null
		return null;
	}
}

function getUniqidFromCookie() {
	// Récupérer tous les cookies
	const cookies = document.cookie.split(';').map(cookie => cookie.trim());

	// Chercher le cookie contenant Uniqid
	const uniqidCookie = cookies.find(cookie => cookie.startsWith('uniqid='));

	// Si le cookie contenant Uniqid est trouvé
	if (uniqidCookie) {
		// Extraire Uniqid de la chaîne du cookie
		const uniqid = uniqidCookie.split('=')[1];
		return uniqid;
	} else {
		// Si le cookie contenant Uniqid n'est pas trouvé, retourner null
		return null;
	}
}


function saveUniqidToCookie(uniqid) {
	const expirationDays = 7;
	setCookie("uniqid", uniqid, expirationDays);
	updatePlayerId();
}

function escapeHtml(unsafe) {
	return unsafe
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;")
		.replace(/"/g, "&quot;")
		.replace(/'/g, "&#039;");
}

// Récupérer le bouton de déconnexion
const logoutButton = document.getElementById('logoutButton');

// Ajouter un gestionnaire d'événements au clic sur le bouton de déconnexion
logoutButton.addEventListener('click', function () {
	matchmaking.sendDisconnect();
	notificationWS.sendDisconnect();
	game.sendDisconnect();
	social.clear();
	

	setCookie("notif_id", Uniqid.generate(), 365);
	eraseCookie("token");
	eraseCookie("uniqid");

	// Rediriger l'utilisateur vers la page de connexion ou effectuer d'autres actions de déconnexion
	loadContent(`https://${raw_url}/front/login/`); // Redirection vers la page de connexion
	//disconnection = true;
	location.reload();
});

function sendFormData(form) {
	const formData = new FormData(form);
	const token = getJwtTokenFromCookie(); // Fonction à implémenter pour récupérer le token JWT depuis les cookies
	const headers = {
		'Authorization': `Token ${token}`
	};
	// Récupérer l'URL de destination à partir de l'attribut action du formulaire
	const fetchUrl = form.action;
	// Envoyer la requête POST
	fetch(fetchUrl, {
		method: 'POST',
		headers: headers,
		body: formData
	})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(data => {
			// Traiter la réponse du serveur si nécessaire

			// Vérifier si data contient une propriété token
			if (data.hasOwnProperty('token')) {
				// Récupérer le token à partir de l'objet data
				const token = data.token;
				// Stocker le token et rediriger l'utilisateur
				handleToken(token);
			} else {
				//console.log('No token property found in data');
			}
			if (isTokenPresent())
				loadContent(`https://${raw_url}/front/pong/`);
			else
				loadContent(`https://${raw_url}/front/login/`);
		})
		.catch(error => {
			console.error('There was a problem with the fetch operation:', error);
		});
}

// Ajouter un écouteur d'événements pour le soumission du formulaire
document.addEventListener('submit', function (event) {
	// Empêcher le comportement par défaut du formulaire (rechargement de la page)
	event.preventDefault();

	// Identifier le formulaire soumis
	const form = event.target;

	if (form.id === 'profilForm') {
		sendFormData(form);
	}
	else {
		// Récupérer les données du formulaire
		const formData = new FormData(form);

		// Construire l'objet JSON à partir des données du formulaire
		const jsonData = {};
		formData.forEach((value, key) => {
			jsonData[key] = escapeHtml(value); // Échapper les données avant de les insérer dans l'objet JSON
		});

		// Récupérer l'URL de destination à partir de l'attribut action du formulaire
		const fetchUrl = form.action;
		const token = getJwtTokenFromCookie(); // Fonction à implémenter pour récupérer le token JWT depuis les cookies
		const headers = {
			'Content-Type': 'application/json'
		};
		if (token) {
			headers['Authorization'] = `token ${token}`;
		}
		// Envoyer la requête POST
		fetch(fetchUrl, {
			method: 'POST',
			headers: headers,
			body: JSON.stringify(jsonData)
		})
			.then(response => {
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			})
			.then(data => {
				// Traiter la réponse du serveur si nécessaire

				// Vérifier si data contient une propriété token

				if (data.hasOwnProperty('token')) {

					// Récupérer le token à partir de l'objet data
					const token = data.token;
					// Vérifier si 2FA est requis
					if (data.hasOwnProperty('2fa_required') && data['2fa_required']) {
						// Afficher le formulaire OTP
						showOTPForm();
					} else {
						// Stocker le token et rediriger l'utilisateur
						handleToken(token);
					}
					const uniqid = data.user.uniqid; // Récupération du uniqid depuis les données de réponse
					saveUniqidToCookie(uniqid);
				} else {
					//console.log('No token property found in data');
				}
				if (isTokenPresent())
					loadContent(`https://${raw_url}/front/pong/`);
				else
					loadContent(`https://${raw_url}/front/login/`);
			})
			.catch(error => {
				console.error('There was a problem with the fetch operation:', error);
			});
	}
});


// Fonction pour afficher ou masquer les boutons en fonction de la présence du token
function toggleButtonsVisibility() {
	const Game = document.getElementById('Game');
	const Profil = document.getElementById('Profil');
	const loginButton = document.getElementById('loginButton');
	const signinButton = document.getElementById('signinButton');
	if (isTokenPresent()) {
		Game.style.display = 'block';
		Profil.style.display = 'block';
		loginButton.style.display = 'none';
		signinButton.style.display = 'none';
	} else {
		Game.style.display = 'none';
		Profil.style.display = 'none';
		loginButton.style.display = 'block';
		signinButton.style.display = 'block';
	}
}


document.getElementById('SaveProfil').addEventListener('click', function (event) {
	event.preventDefault();

	const form = document.getElementById('profilForm');
	const formData = new FormData(form);

	const token = getJwtTokenFromCookie(); // Fonction à implémenter pour récupérer le token JWT depuis les cookies

	// Définir les en-têtes avec le token JWT

	fetch('/auth/profil/', {  // Assurez-vous que l'URL correspond à celle de votre vue Django
		method: 'POST',
		body: formData,
		headers: {
			'Authorization': `token ${token}`,
			'X-CSRFToken': getCookie('csrftoken'), // Assurez-vous d'inclure le jeton CSRF dans les en-têtes
		},
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				alert('Profile updated successfully');
				// Mettre à jour l'affichage ou rediriger l'utilisateur si nécessaire
			} else {
				alert('Failed to update profile');
				// Afficher les erreurs de validation du formulaire
			}
		})
		.catch(error => {
			console.error('Error updating profile:', error);
		});
});

function showOTPForm() {
	loadContent(`https://${raw_url}/front/2fa/`);
}

function handleToken(token) {
	if (token) {
		// Définir la durée de validité du cookie (en jours)
		const expirationDays = 2;

		// Calculer la date d'expiration du cookie
		const expirationDate = new Date();
		expirationDate.setDate(expirationDate.getDate() + expirationDays);

		// Construire la chaîne de cookie avec le nom "token" et la valeur du token
		const cookieString = `token=${token};expires=${expirationDate.toUTCString()};path=/;SameSite=Lax`;
		// Définir le cookie dans le navigateur
		document.cookie = cookieString;

	} else {
		//console.log('Token is empty');
	}

}


function verifyOTP(otp_code) {
	const fetchUrl = `https://${raw_url}/auth/verify_otp/`;
	const headers = {
		'Content-Type': 'application/json',
		'Authorization': `Token ${getToken()}`
	};
	const jsonData = {
		otp_code: otp_code
	};

	fetch(fetchUrl, {
		method: 'POST',
		headers: headers,
		body: JSON.stringify(jsonData)
	})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(data => {
			// Traiter la réponse du serveur si nécessaire
			// Stocker le token et rediriger l'utilisateur
			handleToken(data.token);
		})
		.catch(error => {
			console.error('There was a problem with the fetch operation:', error);
		});
}
