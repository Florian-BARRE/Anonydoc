"""
entipy.models - Base data models for entity processing.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class CharPosition:
    """
    Represents character-based position in text.
    """
    start: int
    end: int


@dataclass(frozen=True)
class WordPosition:
    """
    Represents token-based position in text.
    """
    start: int
    end: int


@dataclass
class Entity:
    """
    Represents a detected entity in the text.
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
    Textual context around an entity.
    """
    entity: Entity
    left: str
    right: str
    window: int


from typing import List, Optional, Dict
from dataclasses import dataclass

@dataclass
class ProcessingResult:
    original_text: str
    processed_text: str
    entities: List[Entity]
    contexts: List[ContextSnippet]
    pseudonym_table: Dict[str, str]

    def get_stats(self, labels: Optional[List[str]] = None) -> dict:
        """
        Returns basic statistics about the processed text.
        Allows filtering by specific entity labels.

        Args:
            labels: Optional list of labels to filter stats by

        Returns:
            Dictionary with entity_count, label_distribution, and density
        """
        filtered_entities = (
            self.entities if labels is None else [e for e in self.entities if e.label in labels]
        )
        total_length = len(self.original_text)
        label_dist = self.label_distribution(labels=labels)
        count = len(filtered_entities)
        density = round(count / total_length, 3) if total_length > 0 else 0.0

        return {
            "entity_count": count,
            "label_distribution": label_dist,
            "density": density
        }

    def label_distribution(self, labels: Optional[List[str]] = None) -> dict:
        """
        Computes distribution of entity labels.

        Args:
            labels: Optional list of labels to filter by

        Returns:
            Dict[label, count]
        """
        dist = {}
        for e in self.entities:
            if labels is None or e.label in labels:
                dist[e.label] = dist.get(e.label, 0) + 1
        return dist

    def replacement_map(self) -> dict:
        """
        Returns a mapping of original text to replacement for all entities.
        """
        return {e.text: e.replacement_text for e in self.entities if e.replacement_text}
