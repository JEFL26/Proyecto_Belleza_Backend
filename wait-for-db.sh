#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

echo "Esperando a que la base de datos $host esté disponible..."

until nc -z "$host" 3306; do
  echo "Base de datos no disponible, esperando 2 segundos..."
  sleep 2
done

echo "Base de datos lista, ejecutando comando..."
exec $cmd