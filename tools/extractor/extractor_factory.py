# ====== Standard Library Imports ======
import os

# ====== Internal Project Imports ======
from extractor.ext import (
    PDFExtractor,
    DOCXExtractor,
    XLSXExtractor,
    TXTExtractor
)
from extractor.unsupported import UnsupportedExtractor


class ExtractorFactory:
    """
    Factory to obtain the appropriate extractor based on file extension.
    """

    @staticmethod
    def get_extractor(file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return PDFExtractor()
        elif ext == '.docx':
            return DOCXExtractor()
        elif ext == '.xlsx':
            return XLSXExtractor()
        elif ext == '.txt':
            return TXTExtractor()
        else:
            return UnsupportedExtractor()

    @staticmethod
    def auto_extract(file_path: str):
        """
        Automatically extracts the content of a file based on its extension.
        """
        extractor = ExtractorFactory.get_extractor(file_path)
        return extractor.extract(file_path)
