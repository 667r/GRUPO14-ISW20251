import pandas as pd
import requests
import json
import logging
from abc import ABC, abstractmethod
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

class BaseSourceHandler(ABC):
    def __init__(self, fuente):
        self.fuente = fuente

    @abstractmethod
    def ingest(self):
        """Retorna los datos como diccionario o lista"""
        pass

class CSVSourceHandler(BaseSourceHandler):
    def ingest(self):
        try:
            df = pd.read_csv(self.fuente.archivo_csv.path)
            return df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Error leyendo CSV: {e}")
            raise

class APISourceHandler(BaseSourceHandler):
    def ingest(self):
        try:
            response = requests.get(self.fuente.url_api)
            response.raise_for_status()

            data = response.json()
            self.fuente.contenido = data
            self.fuente.save()
            return data
        except Exception as e:
            logger.error(f"Error llamando a API: {e}")
            raise