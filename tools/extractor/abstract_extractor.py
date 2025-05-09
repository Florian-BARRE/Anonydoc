# ====== Standard Library Imports ======
from abc import ABC, abstractmethod

# ====== Internal Project Imports ======
from loggerplusplus import Logger


class AbstractExtractor(ABC):
    """
    Abstract base class for text extractor.
    """

    def __init__(self, logger: Logger | None = None):
        # Automatically use the child class name as the identifier if no logger is provided.
        if logger is None:
            logger = Logger(identifier=self.__class__.__name__, follow_logger_manager_rules=True)
        self.logger = logger

    @abstractmethod
    def extract(self, file_path: str) -> str:
        """
        Extract text from the given file.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("The extract method must be implemented by subclasses.")
