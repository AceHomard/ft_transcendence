let end_status_title;
		let title_tournament;
		let title_match;
		let translations;

		function translateElementsWithId(language, translations) {
			var elements = document.querySelectorAll('[id]');
			elements.forEach(function (elements) {
				var translationKey = elements.id;
				if (translationKey && translations[language][translationKey]) {
					elements.textContent = translations[language][translationKey];
				}
			});
		}

		function loadTranslations(language) {
			fetch('translations.json')
				.then(response => response.json())
				.then(data => {
					translations = data;
					notificationWS.sendLang(language);
					if (translations[language]) {
						end_status_title = translations[language]["winner_id"];
						title_tournament = translations[language]["title_tournament"];
						title_match = translations[language]["title_match"];
					} else {
						end_status_title = translations["en"]["winner_id"];
						title_tournament = translations["en"]["title_tournament"];
						title_match = translations["en"]["title_match"];
					}
					translateElementsWithId(language, translations);
				})
				.catch(error => console.error('Error loading translations:', error));
		}

		document.getElementById('language-selector').addEventListener('change', (event) => {
			var selectedLanguage = event.target.value;
			setCookie("langue", selectedLanguage, 365);
			loadTranslations(getCookie("langue"));
		});

		window.addEventListener('load', () => {

			if (getCookie("langue") != "") {
				loadTranslations(getCookie("langue"));
				return;
			}
			setCookie("langue", 'en', 365);
			loadTranslations(getCookie("langue"));
		});