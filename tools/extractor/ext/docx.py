# ====== Third Party Imports ======
from docx import Document

# ====== Internal Project Imports ======
from extractor.abstract_extractor import AbstractExtractor
from loggerplusplus import Logger


class DOCXExtractor(AbstractExtractor):
    """
    Extractor for DOCX files.
    """

    def __init__(self, logger: Logger = None):
        super().__init__(logger=logger)

    def extract(self, file_path: str) -> str:
        self.logger.info(f"Extracting text from DOCX: {file_path}")
        try:
            doc = Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        except Exception as e:
            self.logger.error(f"Error extracting DOCX: {file_path}")
            raise e
