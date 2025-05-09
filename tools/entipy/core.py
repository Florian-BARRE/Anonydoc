# ====== Code Summary ======
# This module defines the `TextEntityProcessor` class, which performs text anonymization
# and pseudonymization using the GLiNER NLP model. It detects entities in text, replaces them
# either with fixed tags (anonymization) or reversible pseudonyms (pseudonymization),
# and constructs detailed processing results including entity metadata and context snippets.

# ====== Standard Library Imports ======
import re

# ====== Third-Party Library Imports ======
from loggerplusplus import Logger
from gliner import GLiNER

# ====== Internal Library Imports ======
from entipy.models import CharPosition, WordPosition, Entity, ContextSnippet, ProcessingResult
from entipy.pseudonymizer import Pseudonymizer


class TextEntityProcessor:
    """
    Processor for anonymization and pseudonymization of text using GLiNER.
    Allows for replacement of detected entities with either fixed tags or reversible pseudonyms.

    Attributes:
        logger (Logger): Logger instance for debug information.
        context_window (int): Number of words to include before and after entities for context snippets.
        threshold (float): Confidence threshold for accepting detected entities.
        model (GLiNER): Pretrained GLiNER model for entity extraction.
        pseudonymizer (Pseudonymizer): Handles pseudonym generation and reversal.
    """

    def __init__(
            self,
            model_name: str = "gliner-community/gliner_medium-v2.5",
            context_window: int = 20,
            threshold: float = 0.5,
            logger: Logger | None = None
    ):
        """
        Initialize the TextEntityProcessor.

        Args:
            model_name (str): GLiNER model to load.
            context_window (int): Number of words for context snippets.
            threshold (float): Confidence threshold for detected entities.
            logger (Logger | None): Optional custom logger.
        """
        self.logger = logger or Logger(
            identifier=self.__class__.__name__,
            follow_logger_manager_rules=True
        )
        self.logger.info("Initializing TextEntityProcessor...")
        self.context_window = context_window
        self.threshold = threshold
        self.logger.debug(f"Loading GLiNER model: {model_name}")
        self.model = GLiNER.from_pretrained(model_name, load_tokenizer=True)
        self.pseudonymizer = Pseudonymizer()
        self.logger.info("TextEntityProcessor initialized successfully.")

    def _compute_word_spans(self, text: str) -> list[tuple[int, int]]:
        """
        Compute character spans for each word in the text.

        Args:
            text (str): Input text.

        Returns:
            list[tuple[int, int]]: List of (start_char, end_char) for each word.
        """
        self.logger.debug("Computing word spans for the input text.")
        spans = [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
        self.logger.debug(f"Computed {len(spans)} word spans.")
        return spans

    def _char_to_word_index(self, char_idx: int, word_spans: list[tuple[int, int]]) -> int:
        """
        Map character index to corresponding word index.

        Args:
            char_idx (int): Character index.
            word_spans (list[tuple[int, int]]): List of word spans.

        Returns:
            int: Word index.
        """
        self.logger.debug(f"Mapping character index {char_idx} to word index.")
        for idx, (ws, we) in enumerate(word_spans):
            if ws <= char_idx < we:
                self.logger.debug(f"Character index {char_idx} maps to word index {idx}.")
                return idx
        for idx, (ws, _) in enumerate(word_spans):
            if char_idx < ws:
                fallback_idx = max(0, idx - 1)
                self.logger.debug(f"Fallback: character index {char_idx} maps to word index {fallback_idx}.")
                return fallback_idx
        fallback_idx = len(word_spans) - 1
        self.logger.debug(f"Fallback to last word index {fallback_idx}.")
        return fallback_idx

    def _extract_entities(self, text: str, labels: list[str]) -> list[dict]:
        """
        Extract entities from text using GLiNER and filter by confidence threshold.

        Args:
            text (str): Input text.
            labels (list[str]): Labels to extract.

        Returns:
            list[dict]: Filtered entity predictions.
        """
        self.logger.info(f"Extracting entities for labels: {labels}")
        raw_preds = self.model.predict_entities(text=text, labels=labels)
        filtered = [e for e in raw_preds if e.get('score', 0.0) >= self.threshold]
        self.logger.debug(f"Extracted {len(filtered)} entities after applying threshold {self.threshold}.")
        return filtered

    def _build_processing(self, text: str, raw_entities: list[dict], replacement_func) -> ProcessingResult:
        """
        Build ProcessingResult by replacing entities and collecting metadata.

        Args:
            text (str): Original text.
            raw_entities (list[dict]): Extracted raw entities.
            replacement_func (Callable): Function to determine replacement text.

        Returns:
            ProcessingResult: Processed text and associated metadata.
        """
        self.logger.info("Starting to build ProcessingResult.")
        word_spans = self._compute_word_spans(text)
        sorted_entities = sorted(raw_entities, key=lambda e: e['start'], reverse=True)
        entities: list[Entity] = []
        redacted = text

        for raw in sorted_entities:
            start, end = raw['start'], raw['end']
            label, span = raw['label'], raw['text']
            replacement = replacement_func(label, span)

            w_start = self._char_to_word_index(start, word_spans)
            w_end = self._char_to_word_index(end - 1, word_spans) + 1

            ent = Entity(
                label=label,
                text=span,
                replacement_text=replacement,
                detection_confidence=raw.get('score', 0.0),
                char_position=CharPosition(start=start, end=end),
                word_position=WordPosition(start=w_start, end=w_end)
            )
            entities.append(ent)
            redacted = redacted[:start] + replacement + redacted[end:]
            self.logger.debug(f"Replaced '{span}' with '{replacement}' at positions [{start}:{end}].")

        self.logger.info("Building context snippets.")
        contexts: list[ContextSnippet] = []
        total_words = len(word_spans)
        for ent in entities:
            ws, we = ent.word_position.start, ent.word_position.end
            cw_start = max(0, ws - self.context_window)
            cw_end = min(total_words, we + self.context_window)
            cs = word_spans[cw_start][0]
            ce = word_spans[cw_end - 1][1]
            left = text[cs:ent.char_position.start]
            right = text[ent.char_position.end:ce]

            contexts.append(
                ContextSnippet(
                    entity=ent,
                    left=left,
                    right=right,
                    window=self.context_window
                )
            )
        self.logger.debug(f"Generated {len(contexts)} context snippets.")

        pseudonym_map = {
            ent.text: ent.replacement_text
            for ent in entities
            if ent.replacement_text
        }

        self.logger.info("ProcessingResult built successfully.")
        return ProcessingResult(
            original_text=text,
            processed_text=redacted,
            entities=entities,
            contexts=contexts,
            pseudonym_table=pseudonym_map
        )

    def anonymize(self, text: str, label_to_tag_mapping: dict[str, str]) -> ProcessingResult:
        """
        Anonymize entities in text by replacing them with fixed tags.

        Args:
            text (str): Input text.
            label_to_tag_mapping (dict[str, str]): Mapping of labels to anonymization tags.

        Returns:
            ProcessingResult: Anonymized text and metadata.
        """
        self.logger.info("Starting anonymization process.")
        raw_entities = self._extract_entities(text, list(label_to_tag_mapping.keys()))
        result = self._build_processing(
            text,
            raw_entities,
            lambda label, span: label_to_tag_mapping.get(label, span)
        )
        self.logger.info("Anonymization completed.")
        return result

    def pseudonymize(self, text: str, labels: list[str]) -> ProcessingResult:
        """
        Pseudonymize entities in text using reversible pseudonyms.

        Args:
            text (str): Input text.
            labels (list[str]): Labels to extract and pseudonymize.

        Returns:
            ProcessingResult: Pseudonymized text and metadata.
        """
        self.logger.info("Starting pseudonymization process.")
        raw_entities = self._extract_entities(text, labels)
        result = self._build_processing(
            text,
            raw_entities,
            lambda label, span: self.pseudonymizer.generate(label, span)
        )
        self.logger.info("Pseudonymization completed.")
        return result

    def reverse_pseudonymization(self, text: str) -> str:
        """
        Reverse pseudonymization, restoring original mentions.

        Args:
           text (str): Text with pseudonyms.

        Returns:
           str: Text with original mentions restored.
        """
        self.logger.info("Reversing pseudonymization.")
        result = self.pseudonymizer.reverse(text)
        self.logger.info("Pseudonymization reversal completed.")
        return result
