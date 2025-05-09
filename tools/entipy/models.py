# ====== Code Summary ======
# This code defines several data structures for handling text entity detection,
# their positions within the text, and processing results. It includes functionality
# for computing statistics on detected entities, such as label distribution and entity density.
# The code is fully typed using Python's native type annotations without relying on the `typing` module.

# ====== Standard Library Imports ======
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CharPosition:
    """
    Represents a character-based position in text.

    Attributes:
        start (int): Starting character index.
        end (int): Ending character index.
    """
    start: int
    end: int


@dataclass(frozen=True)
class WordPosition:
    """
    Represents a token-based position in text.

    Attributes:
        start (int): Starting token index.
        end (int): Ending token index.
    """
    start: int
    end: int


@dataclass
class Entity:
    """
    Represents a detected entity in the text.

    Attributes:
        label (str): Label assigned to the entity (e.g., PERSON, LOCATION).
        text (str): Original detected text.
        replacement_text (str): Replacement text for pseudonymization or anonymization.
        detection_confidence (float): Confidence score of the entity detection.
        char_position (CharPosition): Character position of the entity in text.
        word_position (WordPosition): Token position of the entity in text.
    """
    label: str
    text: str
    replacement_text: str
    detection_confidence: float
    char_position: CharPosition
    word_position: WordPosition


@dataclass
class ContextSnippet:
    """
    Represents the textual context surrounding an entity.

    Attributes:
        entity (Entity): The target entity.
        left (str): Text to the left of the entity.
        right (str): Text to the right of the entity.
        window (int): Size of the context window.
    """
    entity: Entity
    left: str
    right: str
    window: int


@dataclass
class ProcessingResult:
    """
    Holds results from processing text for entity detection and pseudonymization.

    Attributes:
        original_text (str): The original input text.
        processed_text (str): The processed text after replacements.
        entities (list[Entity]): List of detected entities.
        contexts (list[ContextSnippet]): List of context snippets for each entity.
        pseudonym_table (dict[str, str]): Mapping from original text to pseudonymized replacements.
    """
    original_text: str
    processed_text: str
    entities: list[Entity] = field(default_factory=list)
    contexts: list[ContextSnippet] = field(default_factory=list)
    pseudonym_table: dict[str, str] = field(default_factory=dict)

    def get_stats(self, labels: list[str] | None = None) -> dict[str, int | dict[str, int] | float]:
        """
        Returns basic statistics about the processed text.
        Allows filtering by specific entity labels.

        Args:
            labels (list[str] | None): Optional list of labels to filter stats by.

        Returns:
            dict: Contains 'entity_count', 'label_distribution', and 'density'.
        """
        filtered_entities = (
            self.entities if labels is None else [e for e in self.entities if e.label in labels]
        )
        total_length = len(self.original_text)
        label_dist = self.label_distribution(labels)
        count = len(filtered_entities)
        density = round(count / total_length, 3) if total_length > 0 else 0.0

        return {
            "entity_count": count,
            "label_distribution": label_dist,
            "density": density
        }

    def label_distribution(self, labels: list[str] | None = None) -> dict[str, int]:
        """
        Computes distribution of entity labels.

        Args:
            labels (list[str] | None): Optional list of labels to filter by.

        Returns:
            dict: A dictionary mapping labels to their counts.
        """
        dist: dict[str, int] = {}
        for e in self.entities:
            if labels is None or e.label in labels:
                dist[e.label] = dist.get(e.label, 0) + 1
        return dist

    def replacement_map(self) -> dict[str, str]:
        """
        Returns a mapping of original entity text to its replacement.

        Returns:
            dict: Mapping from original text to replacement text.
        """
        return {e.text: e.replacement_text for e in self.entities if e.replacement_text}
