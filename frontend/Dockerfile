# frontend/Dockerfile

# Imagen oficial de Nginx, versión "alpine" = mucho más liviana
FROM nginx:alpine

# Eliminamos la página de bienvenida por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiamos tus archivos (index.html, style.css, script.js) a la carpeta
# que Nginx sirve por defecto
COPY . /usr/share/nginx/html

# Puerto en el que Nginx escucha dentro del contenedor
EXPOSE 80