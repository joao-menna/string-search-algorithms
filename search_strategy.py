from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from time import perf_counter

from telemetry import get_tracer


@dataclass
class SearchResult:
    algorithm: str
    file_path: str
    pattern: str
    text_length: int
    pattern_length: int
    comparisons: int
    matches: list[int]
    elapsed_seconds: float
    theoretical_best: str
    theoretical_average: str
    theoretical_worst: str
    expected_scale_average: int
    step_logs: list[str] = field(default_factory=list)


class SearchStrategy(ABC):
    name: str = ""
    theoretical_best: str = ""
    theoretical_average: str = ""
    theoretical_worst: str = ""

    def run(
        self, text: str, pattern: str, file_path: str, step_by_step: bool = False
    ) -> SearchResult:
        tracer = get_tracer()
        with tracer.start_as_current_span("string_search.run") as span:
            span.set_attribute("search.algorithm", self.name)
            span.set_attribute("search.file_path", file_path)
            span.set_attribute("search.pattern", pattern)
            span.set_attribute("search.pattern_length", len(pattern))
            span.set_attribute("search.text_length", len(text))
            span.set_attribute("search.step_by_step", step_by_step)

            start = perf_counter()
            matches, comparisons, logs = self.search(text, pattern, step_by_step)
            elapsed = perf_counter() - start

            span.set_attribute("search.comparisons", comparisons)
            span.set_attribute("search.matches_count", len(matches))
            span.set_attribute("search.elapsed_ms", elapsed * 1000)

            return SearchResult(
                algorithm=self.name,
                file_path=file_path,
                pattern=pattern,
                text_length=len(text),
                pattern_length=len(pattern),
                comparisons=comparisons,
                matches=matches,
                elapsed_seconds=elapsed,
                theoretical_best=self.theoretical_best,
                theoretical_average=self.theoretical_average,
                theoretical_worst=self.theoretical_worst,
                expected_scale_average=self.expected_average_scale(
                    len(text), len(pattern)
                ),
                step_logs=logs,
            )

    @abstractmethod
    def search(
        self, text: str, pattern: str, step_by_step: bool = False
    ) -> tuple[list[int], int, list[str]]:
        raise NotImplementedError

    @abstractmethod
    def expected_average_scale(self, n: int, m: int) -> int:
        raise NotImplementedError


def append_log(logs: list[str], message: str, limit: int = 200) -> None:
    if len(logs) < limit:
        logs.append(message)
