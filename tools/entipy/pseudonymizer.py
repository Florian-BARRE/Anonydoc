"""
entipy.pseudonymizer - Unique pseudonym generator for reversible pseudonymisation.
"""

from collections import defaultdict
from typing import Dict


class Pseudonymizer:
    """
    Generates and tracks pseudonyms for reversibility.
    """

    def __init__(self):
        self.counter = defaultdict(int)
        self.pseudonym_table: Dict[str, str] = {}
        self.reverse_table: Dict[str, str] = {}

    def generate(self, label: str, original_text: str) -> str:
        """
        Returns a unique pseudonym for the entity based on label.
        """
        if original_text in self.pseudonym_table:
            return self.pseudonym_table[original_text]

        self.counter[label] += 1
        pseudonym = f"{label}_{self.counter[label]}"
        self.pseudonym_table[original_text] = pseudonym
        self.reverse_table[pseudonym] = original_text
        return pseudonym

    def get_table(self) -> Dict[str, str]:
        return self.pseudonym_table

    def reverse(self, text: str) -> str:
        """
        Reverses pseudonyms in processed text.
        """
        for pseudo, original in self.reverse_table.items():
            text = text.replace(pseudo, original)
        return text
