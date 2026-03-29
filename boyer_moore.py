from __future__ import annotations

from search_strategy import SearchStrategy, append_log


class BoyerMooreSearch(SearchStrategy):
	name = "Boyer-Moore"
	theoretical_best = "O(n / m)"
	theoretical_average = "O(n)"
	theoretical_worst = "O(n * m)"

	def _build_bad_char_table(self, pattern: str) -> dict[str, int]:
		table: dict[str, int] = {}
		for i, ch in enumerate(pattern):
			table[ch] = i
		return table

	def search(self, text: str, pattern: str, step_by_step: bool = False) -> tuple[list[int], int, list[str]]:
		n = len(text)
		m = len(pattern)
		bad_char = self._build_bad_char_table(pattern)

		matches: list[int] = []
		logs: list[str] = []
		comparisons = 0
		shift = 0

		while shift <= n - m:
			j = m - 1

			while j >= 0:
				comparisons += 1
				if step_by_step:
					append_log(
						logs,
						f"shift={shift}, j={j}, text[{shift + j}]='{text[shift + j]}' vs pattern[{j}]='{pattern[j]}'",
					)

				if pattern[j] != text[shift + j]:
					break
				j -= 1

			if j < 0:
				matches.append(shift)
				if step_by_step:
					append_log(logs, f"match encontrado em {shift}")

				if shift + m < n:
					shift += m - bad_char.get(text[shift + m], -1)
				else:
					shift += 1
			else:
				skip = max(1, j - bad_char.get(text[shift + j], -1))
				if step_by_step:
					append_log(logs, f"mismatch em j={j}, deslocamento={skip}")
				shift += skip

		return matches, comparisons, logs

	def expected_average_scale(self, n: int, m: int) -> int:
		return max(1, n)
