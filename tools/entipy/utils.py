def replace_spans(text: str, spans: list[tuple[int, int, str]]) -> str:
    spans = sorted(spans, key=lambda s: s[0], reverse=True)
    for start, end, replacement in spans:
        text = text[:start] + replacement + text[end:]
    return text


def is_overlapping(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    return any(max(start, s) < min(end, e) for s, e in spans)
