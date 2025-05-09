# ====== Internal Project Imports ======
from extractor.abstract_extractor import AbstractExtractor
from loggerplusplus import Logger


class TXTExtractor(AbstractExtractor):
    """
    Extracteur pour les fichiers texte (.txt) utilisant uniquement les fonctions I/O intégrées.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialise l'extracteur TXT.

        Args:
            logger (Logger, optional): Instance du logger. Par défaut, None.
        """
        super().__init__(logger=logger)

    def extract(self, file_path: str) -> str:
        """
        Extrait le texte brut d'un fichier .txt.

        Args:
            file_path (str): Chemin du fichier à lire.

        Returns:
            str: Contenu du fichier texte.

        Raises:
            FileNotFoundError: Si le fichier est introuvable.
            IOError: Si une erreur survient pendant la lecture du fichier.
        """
        self.logger.info(f"Lecture du fichier texte : {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError as e:
            self.logger.error(f"Fichier non trouvé : {file_path}")
            raise
        except IOError as e:
            self.logger.error(f"Erreur d'I/O pendant la lecture du fichier : {file_path}")
            raise
