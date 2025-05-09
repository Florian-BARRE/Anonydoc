# ====== Third Party Imports ======
from loggerplusplus import Logger

# ====== Internal Project Imports ======
from extractor.abstract_extractor import AbstractExtractor


class UnsupportedExtractor(AbstractExtractor):
    """
    Extractor for unsupported file types.
    """

    def __init__(self, logger: Logger = None):
        super().__init__(logger=logger)

    def extract(self, file_path: str):
        self.logger.error(f"Unsupported file type: {file_path}")
        raise ValueError(f"Unsupported file type: {file_path}")
