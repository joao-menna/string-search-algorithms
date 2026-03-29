from __future__ import annotations

from search_strategy import SearchStrategy, append_log


class KMPSearch(SearchStrategy):
	name = "Knuth-Morris-Pratt"
	theoretical_best = "O(n + m)"
	theoretical_average = "O(n + m)"
	theoretical_worst = "O(n + m)"

	def _build_lps(self, pattern: str, step_by_step: bool, logs: list[str]) -> tuple[list[int], int]:
		m = len(pattern)
		lps = [0] * m
		length = 0
		i = 1
		comparisons = 0

		while i < m:
			comparisons += 1
			if step_by_step:
				append_log(logs, f"LPS: pattern[{i}]='{pattern[i]}' vs pattern[{length}]='{pattern[length]}'")

			if pattern[i] == pattern[length]:
				length += 1
				lps[i] = length
				i += 1
			elif length != 0:
				length = lps[length - 1]
			else:
				lps[i] = 0
				i += 1

		return lps, comparisons

	def search(self, text: str, pattern: str, step_by_step: bool = False) -> tuple[list[int], int, list[str]]:
		n = len(text)
		m = len(pattern)
		logs: list[str] = []
		matches: list[int] = []

		lps, lps_comparisons = self._build_lps(pattern, step_by_step, logs)
		i = 0
		j = 0
		comparisons = lps_comparisons

		while i < n:
			comparisons += 1
			if step_by_step:
				append_log(logs, f"Busca: text[{i}]='{text[i]}' vs pattern[{j}]='{pattern[j]}'")

			if text[i] == pattern[j]:
				i += 1
				j += 1

				if j == m:
					matches.append(i - j)
					if step_by_step:
						append_log(logs, f"match encontrado em {i - j}")
					j = lps[j - 1]
			elif j != 0:
				j = lps[j - 1]
			else:
				i += 1

		return matches, comparisons, logs

	def expected_average_scale(self, n: int, m: int) -> int:
		return max(1, n + m)
