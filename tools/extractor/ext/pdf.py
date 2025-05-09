# ====== Third Party Imports ======
from pdfminer.high_level import extract_text

# ====== Internal Project Imports ======
from extractor.abstract_extractor import AbstractExtractor
from loggerplusplus import Logger


class PDFExtractor(AbstractExtractor):
    """
    Extracteur pour les fichiers PDF utilisant pdfminer.six.
    """

    def __init__(self, logger: Logger = None):
        super().__init__(logger=logger)

    def extract(self, file_path: str) -> str:
        self.logger.info(f"Extraction du texte depuis le PDF : {file_path}")
        try:
            text = extract_text(file_path)
            return text
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction du PDF : {file_path}")
            raise e
