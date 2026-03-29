from __future__ import annotations

from search_strategy import SearchStrategy, append_log


class RabinKarpSearch(SearchStrategy):
	name = "Rabin-Karp"
	theoretical_best = "O(n + m)"
	theoretical_average = "O(n + m)"
	theoretical_worst = "O(n * m)"

	def __init__(self, prime: int = 101, alphabet_size: int = 256) -> None:
		self.prime = prime
		self.alphabet_size = alphabet_size

	def search(self, text: str, pattern: str, step_by_step: bool = False) -> tuple[list[int], int, list[str]]:
		n = len(text)
		m = len(pattern)
		matches: list[int] = []
		logs: list[str] = []
		comparisons = 0

		h = 1
		for _ in range(m - 1):
			h = (h * self.alphabet_size) % self.prime

		pattern_hash = 0
		window_hash = 0
		for i in range(m):
			pattern_hash = (self.alphabet_size * pattern_hash + ord(pattern[i])) % self.prime
			window_hash = (self.alphabet_size * window_hash + ord(text[i])) % self.prime

		for shift in range(n - m + 1):
			if step_by_step:
				append_log(logs, f"shift={shift}, hash_text={window_hash}, hash_pattern={pattern_hash}")

			if pattern_hash == window_hash:
				if step_by_step:
					append_log(logs, "hash igual: iniciando verificacao caractere a caractere")

				matched = True
				for j in range(m):
					comparisons += 1
					if step_by_step:
						append_log(
							logs,
							f"  text[{shift + j}]='{text[shift + j]}' vs pattern[{j}]='{pattern[j]}'",
						)
					if text[shift + j] != pattern[j]:
						matched = False
						break

				if matched:
					matches.append(shift)
					if step_by_step:
						append_log(logs, f"match encontrado em {shift}")

			if shift < n - m:
				window_hash = (
					self.alphabet_size * (window_hash - ord(text[shift]) * h) + ord(text[shift + m])
				) % self.prime

				if window_hash < 0:
					window_hash += self.prime

		return matches, comparisons, logs

	def expected_average_scale(self, n: int, m: int) -> int:
		return max(1, n + m)
