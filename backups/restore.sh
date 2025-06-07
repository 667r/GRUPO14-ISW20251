#!/bin/bash

# Restaurar base de datos
BACKUP_FILE=$1  # El archivo de backup se pasa como argumento
if [ -z "$BACKUP_FILE" ]; then
  echo "No se especificó el archivo de backup."
  exit 1
fi

echo "Restaurando base de datos desde $BACKUP_FILE"
psql -U equipo -h db -d isw -f "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Restauración exitosa."
else
  echo "Error al restaurar."
  exit 1
fi
