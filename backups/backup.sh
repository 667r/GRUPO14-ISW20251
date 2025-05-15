#!/bin/bash


DATE=$(date +%Y-%m-%d_%H-%M-%S)


BACKUP_FILE="backup_$DATE.sql"

DESTINATION="/app/backups"

PGPASSWORD=equipo123 pg_dump -U equipo -h db isw > "$DESTINATION/$BACKUP_FILE"

