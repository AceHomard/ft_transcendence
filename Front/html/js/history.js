class Leaderboard {
	#id;

	constructor() {
		this.#id = 0;
	}

	setId(id_value) {
		this.#id = id_value;
	}

	#createElement(tag, attributes = {}, ...children) {
		const element = document.createElement(tag);

		for (const [key, value] of Object.entries(attributes))
			element.setAttribute(key, value);

		for (const child of children)
			if (typeof child === 'string')
				element.appendChild(document.createTextNode(child));
			else
				element.appendChild(child);

		return element;
	}

	#createTeamDiv(image_player, pseudo_player, unique_id,teamSide) {
		const teamImg = this.#createElement("img", {
			src: "." + image_player,
			alt: pseudo_player,
			class: "team-logo",
			onclick: "loadHistory('" + `https://${raw_url}/front/history/` + unique_id + "')"
		});

		const teamName = this.#createElement("div", {
			class: "team-name",
		}, pseudo_player);

		return this.#createElement("div", {
			class: "team " + teamSide
		}, teamImg, teamName);

	}

	#createMatchInfo(score, win, date) {
		const dateDiv = this.#createElement("div", {
			class: "date",
		}, date);

		const scoreDiv = this.#createElement("div", {
			class: "score",
		}, score);

		const timeDiv = this.#createElement("div", {
			class: win ? "win-match press-start-2p-regular" : "loose-match press-start-2p-regular",
			id: win ? "win_id" : "loose_id"
		}, win ? "WIN" : "LOOSE");

		return this.#createElement("div", {
			class: "match-info silkscreen-regular"
		}, dateDiv, scoreDiv, timeDiv);
	}

	#createMatchModule(image_playerA, pseudo_playerA, id_playerA, image_playerB, pseudo_playerB, id_playerB,score, win, date) {
		const teamLeftDiv = this.#createTeamDiv(image_playerA, pseudo_playerA, id_playerA,"team-left");
		const teamRightDiv = this.#createTeamDiv(image_playerB, pseudo_playerB, id_playerB,"team-right");
		const matchInfoDiv = this.#createMatchInfo(score, win, date);

		return this.#createElement("div", {
			class: "match-module",
			id: "ldb_matchbox_" + this.#id
		}, teamLeftDiv, matchInfoDiv, teamRightDiv);
	}

	#createLogoDiv(blockchain, ether_link, arrow_id) {
		// Modification du texte
		const stored = this.#createElement("span", {
			class: "logo-text"
		}, "Stored in");

		// Ajout du logo Ethereum
		const ethLogoImg = this.#createElement("img", {
			src: "img/Ethereum%20Icon.svg",
			alt: "Etherum logo",
			class: "eth-logo"
		});

		const DbLogoImg = this.#createElement("img", {
			src: "img/database2.svg",
			alt: "Db logo",
			class: "db-logo"
		});
		// Création du div logo vide
		const logoDiv = this.#createElement("div", {
			class: "logo"
		});

		// Création du lien avec les classes et href appropriés
		const logoBoxDiv = this.#createElement(blockchain ? "a" : "div", {
			class: "logo-box clickable-logo bck-hover",
			href: ether_link,
			target: "_blank"
		}, stored, blockchain ? ethLogoImg : DbLogoImg, logoDiv);

		// Ajout d'une flèche avec un identifiant dynamique
		const arrowImg = this.#createElement("img", {
			src: "img/arrow.svg",
			alt: "Arrow down",
			class: "arrow-logo animation-arrow unselectable",
			id: "ldb_arrow_" + this.#id
		});

		const arrowDiv = this.#createElement("div", {
			class: "arrow-main bck-hover unselectable"
		}, arrowImg);

		// Retour du div principal contenant tous les éléments
		const logoBoxMainDiv = this.#createElement("div", {
			class: "logo-box-main"
		}, logoBoxDiv, arrowDiv);

		return this.#createElement("div", {
			class: "logo-main animation-info",
			id: "ldb_info_" + this.#id,
			onclick: "leaderboard.toggleScoreStore('" + this.#id + "')"
		}, logoBoxMainDiv);
	}
	toggleScoreStore(id) {
		if (document.getElementById("ldb_info_" + id).style.marginTop == "90px") {
			document.getElementById("ldb_arrow_" + id).style.transform = "rotateZ(0deg)";
			document.getElementById("ldb_matchbox_" + id).style.background = "";
			document.getElementById("ldb_match_" + id).style.height = "108px";
			document.getElementById("ldb_info_" + id).style.marginTop = "55px";
		}
		else {
			document.getElementById("ldb_arrow_" + id).style.transform = "rotateZ(180deg)";
			document.getElementById("ldb_matchbox_" + id).style.background = "#222223";
			document.getElementById("ldb_match_" + id).style.height = "142px";
			document.getElementById("ldb_info_" + id).style.marginTop = "90px";
		}
	}

	addMatch(pseudo_playerA, pseudo_playerB, image_playerA, image_playerB, id_playerA, id_playerB, score, win, blockchain, ether_link, date) {
		const matchModuleDiv = this.#createMatchModule(image_playerA, pseudo_playerA, id_playerA ,image_playerB, pseudo_playerB, id_playerB ,score, win, date)
		const logoMainDiv = this.#createLogoDiv(blockchain, ether_link)
		const matchDiv = this.#createElement("div", {
			class: "match animation-info unselectable",
			id: "ldb_match_" + this.#id
		}, matchModuleDiv, logoMainDiv);

		document.getElementById("leaderboard_list").appendChild(matchDiv);
		this.#id += 1;
	}

	createProfil(datas) {
		document.getElementById("player-name").innerText = datas["player_name"];
		document.getElementById("win-number").innerText = datas["player_win"];
		document.getElementById("loose-number").innerText = datas["player_loose"];
		document.getElementById("ratio-number").innerText = datas["player_ratio"];
		document.getElementById("Profil-picture").src = datas["player_picture"];
		document.getElementById("profil").style.display = "flex";
	}

	NoMatchFound() {
		const ErrorDiv = this.#createElement("div", {
			class: "match-module no-match-found",
			id: "Mnotfound"
		}, "NO MATCH FOUND");

		document.getElementById("leaderboard_list").appendChild(ErrorDiv);
	}

}