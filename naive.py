from __future__ import annotations

from search_strategy import SearchStrategy, append_log


class NaiveSearch(SearchStrategy):
	name = "Naive"
	theoretical_best = "O(n)"
	theoretical_average = "O(n * m)"
	theoretical_worst = "O(n * m)"

	def search(self, text: str, pattern: str, step_by_step: bool = False) -> tuple[list[int], int, list[str]]:
		n = len(text)
		m = len(pattern)
		comparisons = 0
		matches: list[int] = []
		logs: list[str] = []

		for shift in range(n - m + 1):
			matched = True
			for j in range(m):
				comparisons += 1
				if step_by_step:
					append_log(
						logs,
						f"shift={shift}, j={j}, text[{shift + j}]='{text[shift + j]}' vs pattern[{j}]='{pattern[j]}'",
					)
				if text[shift + j] != pattern[j]:
					matched = False
					break
			if matched:
				matches.append(shift)
				if step_by_step:
					append_log(logs, f"match encontrado em {shift}")

		return matches, comparisons, logs

	def expected_average_scale(self, n: int, m: int) -> int:
		return max(1, n * m)
