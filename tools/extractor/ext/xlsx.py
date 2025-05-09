# ====== Standard Library Imports ======
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ====== Third Party Imports ======
import pandas as pd

# ====== Internal Project Imports ======
from extractor.abstract_extractor import AbstractExtractor
from loggerplusplus import Logger


class XLSXExtractor(AbstractExtractor):
    """
    Extractor for XLSX files.
    """

    def __init__(self, logger: Logger = None):
        super().__init__(logger=logger)

    def extract(self, file_path: str) -> str:
        self.logger.info(f"Extracting text from XLSX: {file_path}")
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            self.logger.error(f"Error extracting XLSX: {file_path}")
            raise e
