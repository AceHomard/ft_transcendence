.PHONY: run stop clear logs

run:
	cp -r Secret/keyauthapi Auth/api/
	cp -r Secret/keydjangoWebSocketapi djangoWebSocket/
	cp -r Secret/keynotif notif/
	cp Secret/.envauthentification Auth/
	cp Secret/.envbot Botted/
	cp Secret/.envcrypto DjangoWeb3/
	cp Secret/.envfrontend ApiHTMLFront/
	cp Secret/.envmatchmaking djangoWebSocket/
	cp Secret/.envnotification notif/
	cp Secret/public_key_DjangoWeb3.pem DjangoWeb3/
	cp Secret/.env ./
	docker-compose up --build -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

clear:
	rm -rf Auth/api/keyauthapi
	rm -rf djangoWebSocket/keydjangoWebSocketapi
	rm -rf notif/keynotif
	rm Auth/.envauthentification
	rm Botted/.envbot
	rm DjangoWeb3/.envcrypto
	rm ApiHTMLFront/.envfrontend
	rm djangoWebSocket/.envmatchmaking
	rm notif/.envnotification
	rm DjangoWeb3/public_key_DjangoWeb3.pem
	rm ./.env
	docker system prune -af --volumes