# Dockerfile para frontend


# Se trae la imagen de nginx, que es el web que va a servir nuestro front
FROM nginx:alpine   

# removemos la configuracion que tiene por defecto
RUN rm -rf /usr/share/nginx/html/*

# Copiamos el directorio raiz actual, dentro de la carpeta que sirve el front en nginx
COPY . /usr/share/nginx/html

# El mapeo actual seria 3000:80, nginx usa 80 por defecto.
EXPOSE 80

# CMD especifica el comando que se ejecuta cuando el cont arranca
#y en este caso es para que se mantenga en segundo plano
CMD ["nginx", "-g", "daemon off;"]