#!/bin/bash

DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="backup_$DATE.sql"
DESTINATION="/app/backups"
LOG_FILE="/app/backups/backup.log"

# Realizar el backup
PGPASSWORD=equipo123 pg_dump -U equipo -h db isw > "$DESTINATION/$BACKUP_FILE"

# Verificar si el backup fue exitoso
if [ $? -eq 0 ]; then
    echo "[$DATE] Backup exitoso: $BACKUP_FILE" >> $LOG_FILE
    echo "Backup realizado exitosamente: $BACKUP_FILE"
else
    echo "[$DATE] Error al realizar el backup" >> $LOG_FILE
    echo "Error al realizar el backup."
fi
