import os
import subprocess
from datetime import datetime

BACKUP_DIR = '/app/backups'
LOG_PATH = os.path.join(BACKUP_DIR, 'backup.log')

def generate_backup(manual=False):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{'manual' if manual else 'auto'}_backup_{now}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)
    
    cmd = [
        'pg_dump',
        '-h', 'db',
        '-U', 'equipo',
        '-d', 'isw',
        '-f', filepath
    ]

    try:
        subprocess.run(cmd, check=True)
        log_message(f"Backup generado correctamente: {filename}")
        return filepath
    except subprocess.CalledProcessError as e:
        log_message(f"Error al generar backup: {e}")
        return None

def restore_backup(filename):
    filepath = os.path.join(BACKUP_DIR, filename)
    cmd = [
        'psql',
        '-h', 'db',
        '-U', 'equipo',
        '-d', 'isw',
        '-f', filepath
    ]
    try:
        subprocess.run(cmd, check=True)
        log_message(f"🔄 Restauración exitosa desde: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Error al restaurar backup: {e}")
        return False

def log_message(message):
    with open(LOG_PATH, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")
