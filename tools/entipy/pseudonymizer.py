# ====== Code Summary ======
# This module implements a reversible pseudonymization mechanism for entity texts.
# It generates unique pseudonyms based on entity labels, tracks mappings between
# original texts and their pseudonyms, and provides functionality to reverse the
# pseudonymization in processed text. Native Python typing is used throughout.

# ====== Standard Library Imports ======
from collections import defaultdict


class Pseudonymizer:
    """
    Generates and tracks pseudonyms for entities to allow reversible pseudonymization.

    Attributes:
        counter (defaultdict[str, int]): Counts pseudonym occurrences per label.
        pseudonym_table (dict[str, str]): Maps original text to its pseudonym.
        reverse_table (dict[str, str]): Maps pseudonym back to original text.
    """

    def __init__(self):
        self.counter: defaultdict[str, int] = defaultdict(int)
        self.pseudonym_table: dict[str, str] = {}
        self.reverse_table: dict[str, str] = {}

    def generate(self, label: str, original_text: str) -> str:
        """
        Generates a unique pseudonym for the given label and original text.
        If a pseudonym for the original text already exists, it returns it.

        Args:
            label (str): Entity label (e.g., "PERSON", "LOCATION").
            original_text (str): The original entity text.

        Returns:
            str: The generated or existing pseudonym.
        """
        if original_text in self.pseudonym_table:
            return self.pseudonym_table[original_text]

        self.counter[label] += 1
        pseudonym = f"{label}_{self.counter[label]}"
        self.pseudonym_table[original_text] = pseudonym
        self.reverse_table[pseudonym] = original_text
        return pseudonym

    def get_table(self) -> dict[str, str]:
        """
        Retrieves the current pseudonym table mapping original texts to pseudonyms.

        Returns:
            dict[str, str]: Mapping from original text to pseudonym.
        """
        return self.pseudonym_table

    def reverse(self, text: str) -> str:
        """
        Reverses pseudonyms found in the provided text back to their original values.

        Args:
            text (str): Text containing pseudonyms.

        Returns:
            str: Text with pseudonyms replaced by their original values.
        """
        for pseudo, original in self.reverse_table.items():
            text = text.replace(pseudo, original)
        return text
