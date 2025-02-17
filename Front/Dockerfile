# Use the Nginx image as base
FROM nginx

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy all static files into the Nginx document root
COPY html/index.html /usr/share/nginx/html/
COPY html/css/ /usr/share/nginx/html/css/
COPY translations.json /usr/share/nginx/html/
COPY img/ /usr/share/nginx/html/img/
COPY html/js/ /usr/share/nginx/html/js/
COPY html/favicon.ico /usr/share/nginx/html/favicon.ico
RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/inception.key -out /etc/nginx/ssl/inception.crt -subj "/C=AT/ST=W/L=W/O=42/OU=42k/CN=trans/UID=trans"
