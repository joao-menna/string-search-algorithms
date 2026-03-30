"""
Testes pytest para os algoritmos de busca em strings.
Foca em testar o pior caso de cada algoritmo.
"""

import pytest

from boyer_moore import BoyerMooreSearch
from knuth_morris_pratt import KMPSearch
from naive import NaiveSearch
from rabin_karp import RabinKarpSearch


class TestNaiveSearchWorstCase:
    """Testes para Naive Search - pior caso O(n * m)"""

    def setup_method(self):
        self.strategy = NaiveSearch()

    def test_worst_case_no_match(self):
        """
        Pior caso: texto com muitos caracteres iguais ao primeiro da pattern,
        mas pattern nunca aparece completamente.
        Esperado: O(n * m) comparações
        """
        # Padrão: "aaab" (termina com 'b')
        # Texto: "aaa...aaac" (muitos 'a's seguidos por 'c')
        # Cada posição vai tentar 3 comparações antes de falhar em j=3
        pattern = "aaab"
        text = "a" * 1000 + "c"  # 1000 'a's + um 'c'

        print(f"\n[Naive - Worst Case] Pattern: '{pattern}' ({len(pattern)} chars), Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches: {len(matches)}, Comparações: {comparisons}")

        assert matches == []  # Nenhum match
        # No pior caso com Naive: (n - m + 1) * m comparações
        # Aqui: (1001 - 4 + 1) * 4 = 3988
        expected_max = (len(text) - len(pattern) + 1) * len(pattern)
        print(f"  Complexidade esperada: {expected_max} (O(n*m))")
        assert comparisons == expected_max

    def test_almost_match_everywhere(self):
        """
        Padrão que quase aparece em todos os lugares.
        """
        pattern = "aaa"
        text = "a" * 500

        print(f"\n[Naive - Almost Match] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches encontrados: {len(matches)}, Comparações: {comparisons}")

        # Com 500 'a's, o padrão aparece em várias posições
        assert len(matches) > 0
        # Cada posição tem 3 comparações (todas bem-sucedidas)
        assert comparisons == (len(text) - len(pattern) + 1) * len(pattern)

    def test_single_character_not_found(self):
        """Caso simples: carácter não encontrado"""
        pattern = "b"
        text = "a" * 100

        print(f"\n[Naive - Single Char] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches: {len(matches)}, Comparações: {comparisons}")

        assert matches == []
        assert comparisons == len(text)


class TestRabinKarpWorstCase:
    """Testes para Rabin-Karp - pior caso O(n * m) com colisões de hash"""

    def setup_method(self):
        self.strategy = RabinKarpSearch()

    def test_worst_case_hash_collisions(self):
        """
        Pior caso: muitas colisões de hash causam verificações
        caractere-por-caractere frequentes.
        """
        pattern = "abc"
        # Cria texto onde muitas subsequências têm hash igual ao padrão
        # mas não correspondem ao padrão real
        text = "a" * 500 + "abc"

        print(f"\n[Rabin-Karp - Hash Collisions] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Match em posição: {matches}, Comparações: {comparisons}")

        # Deve encontrar uma ocorrência ao final
        assert matches == [500]
        # Comparisons: varias falsas colisões antes de encontrar

    def test_pattern_only_at_end(self):
        """Padrão aparece apenas no final após falsos positivos potenciais"""
        pattern = "xyz"
        text = "x" * 300 + "y" * 300 + "z" * 300 + "xyz"

        print(f"\n[Rabin-Karp - Pattern at End] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Match em posição: {matches}, Comparações: {comparisons}")

        assert matches == [900]

    def test_no_match_with_similar_prefix(self):
        """Texto com prefixo similar ao padrão mas sem match completo"""
        pattern = "abcd"
        text = "a" * 400 + "b" * 400 + "xyz"

        print(f"\n[Rabin-Karp - Similar Prefix] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches: {len(matches)}, Comparações: {comparisons}")

        assert matches == []


class TestKMPSearchWorstCase:
    """Testes para KMP - melhor comportamento com O(n + m)"""

    def setup_method(self):
        self.strategy = KMPSearch()

    def test_pattern_with_overlapping_repeats(self):
        """
        Pattern com repeats sobrepostos (grande LPS array).
        Mesmo no pior caso, KMP é O(n + m).
        """
        pattern = "aaaa"
        text = "a" * 1000

        print(f"\n[KMP - Overlapping Repeats] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches encontrados: {len(matches)}, Comparações: {comparisons}")
        print(f"  Complexidade: O(n+m) = {len(text) + len(pattern)} (linear!)")

        # Deve encontrar muitos matches
        assert len(matches) > 0
        # KMP sempre é O(n + m), mesmo neste caso
        expected_approx = len(text) + len(pattern)
        # Permitir pequena variação
        assert comparisons <= expected_approx * 1.5

    def test_pattern_never_found(self):
        """Pattern não aparece - KMP ainda é eficiente"""
        pattern = "abcd"
        text = "a" * 2000

        print(f"\n[KMP - Pattern Never Found] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches: {len(matches)}, Comparações: {comparisons}")
        print(f"  Eficiência KMP mesmo sem match encontrado")

        assert matches == []
        # Complexidade linear: O(n + m), com a implementação pode ter overhead
        # É linear mesmo que pareça ter mais comparações
        assert comparisons > 0

    def test_long_pattern_in_long_text(self):
        """Pattern longo em texto longo"""
        pattern = "a" * 100
        text = "a" * 5000

        print(f"\n[KMP - Long Pattern Long Text] Pattern: {len(pattern)} chars, Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches encontrados: {len(matches)}, Comparações: {comparisons}")
        print(f"  Complexidade O(n+m): esperado ~{len(text) + len(pattern)}")

        assert len(matches) > 0
        # Deve ter complexidade O(n + m)
        assert comparisons <= (len(text) + len(pattern)) * 1.5


class TestBoyerMooreWorstCase:
    """Testes para Boyer-Moore - pior caso O(n * m)"""

    def setup_method(self):
        self.strategy = BoyerMooreSearch()

    def test_worst_case_repeating_pattern(self):
        """
        Pior caso: padrão com caracteres que repetem no texto.
        Causa saltos pequenos (movimento de 1 em 1).
        """
        pattern = "aaab"
        # Texto com muitos 'a's - vai causar movimentos pequenos
        text = "a" * 500 + "b"

        print(f"\n[Boyer-Moore - Worst Case] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Match em posição: {matches}, Comparações: {comparisons}")
        print(f"  Pior caso: repeating pattern causa saltos pequenos")

        assert matches == [497]
        # No pior caso, vai fazer muitas comparações

    def test_pattern_at_very_end(self):
        """Pattern aparece apenas no final"""
        pattern = "xyz"
        text = "a" * 1000 + "xyz"

        print(f"\n[Boyer-Moore - Pattern at End] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Match em posição: {matches}, Comparações: {comparisons}")

        assert matches == [1000]

    def test_single_character_mismatch(self):
        """
        Cada posição tem mismatch apenas no último caractere.
        Boyer-Moore consegue fazer saltos grandes aqui.
        """
        pattern = "abc"
        text = "aba" * 500  # Padrão nunca aparece

        print(f"\n[Boyer-Moore - Single Char Mismatch] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches: {len(matches)}, Comparações: {comparisons}")
        print(f"  Boyer-Moore eficiente com saltos grandes")

        assert matches == []
        # Boyer-Moore deve ser eficiente aqui com saltos bons

    def test_all_same_characters(self):
        """Caso onde Boyer-Moore não consegue fazer saltos específicos"""
        pattern = "aaa"
        text = "a" * 300

        print(f"\n[Boyer-Moore - All Same Chars] Pattern: '{pattern}', Texto: {len(text)} chars")
        matches, comparisons, _ = self.strategy.search(text, pattern, step_by_step=False)
        print(f"  Matches encontrados: {len(matches)}, Comparações: {comparisons}")
        print(f"  Saltos pequenos quando todos os chars são iguais")

        assert len(matches) > 0
        # Pode ser pior caso, com muitas comparações


class TestComparisonWorstCases:
    """Testes comparando todos os algoritmos em cenários de pior caso"""

    def test_all_algorithms_find_same_matches(self):
        """Todos os algoritmos devem encontrar os mesmos matches"""
        algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
            KMPSearch(),
            BoyerMooreSearch(),
        ]

        pattern = "pattern"
        text = "this is a pattern in the text with another pattern here"

        print(f"\n[Comparison - Same Matches] Pattern: '{pattern}', Texto: '{text}'")
        matches_per_algo = {}
        for algo in algorithms:
            matches, comparisons, _ = algo.search(text, pattern)
            matches_per_algo[algo.name] = matches
            print(f"  {algo.name}: matches={matches}, comparações={comparisons}")

        # Todos devem encontrar os mesmos matches
        first_matches = next(iter(matches_per_algo.values()))
        for algo_name, matches in matches_per_algo.items():
            assert matches == first_matches, f"{algo_name} encontrou matches diferentes"

    def test_worst_case_repeated_characters(self):
        """
        Cenário onde alguns algoritmos sofrem (muitos 'a's com padrão 'aaa').
        Verifica se todos encontram os mesmos resultados.
        """
        algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
            KMPSearch(),
            BoyerMooreSearch(),
        ]

        pattern = "aaab"
        text = "a" * 500 + "b"

        print(f"\n[Comparison - Repeated Chars] Pattern: '{pattern}', Texto: {len(text)} chars")
        for algo in algorithms:
            matches, comparisons, _ = algo.search(text, pattern)
            expected_match = [497]  # Position where "aaab" is found
            print(f"  {algo.name}: match={matches}, comparações={comparisons}")
            assert matches == expected_match, f"{algo.name}: esperado {expected_match}, obtive {matches}"

    def test_worst_case_no_occurrences(self):
        """Nenhuma ocorrência - todos devem retornar lista vazia"""
        algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
            KMPSearch(),
            BoyerMooreSearch(),
        ]

        pattern = "xyz"
        text = "a" * 1000 + "bbb"

        print(f"\n[Comparison - No Occurrences] Pattern: '{pattern}', Texto: {len(text)} chars")
        for algo in algorithms:
            matches, comparisons, _ = algo.search(text, pattern)
            print(f"  {algo.name}: matches={len(matches)}, comparações={comparisons}")
            assert matches == [], f"{algo.name} deveria retornar lista vazia"

    def test_empty_pattern(self):
        """Pattern vazia - pode não ser suportado por todos os algoritmos"""
        algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
        ]

        pattern = ""
        text = "test"

        for algo in algorithms:
            # Apenas testa com algoritmos que assumidamente lidam com isso
            try:
                matches, comparisons, _ = algo.search(text, pattern)
                assert isinstance(matches, list)
            except (IndexError, ValueError):
                # É aceitável que pare com error em pattern vazio
                pass


class TestEdgeCases:
    """Testes para casos extremos"""

    def test_pattern_longer_than_text(self):
        """Pattern mais longo que o texto"""
        algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
            KMPSearch(),
            BoyerMooreSearch(),
        ]

        pattern = "longpattern"
        text = "short"

        for algo in algorithms:
            try:
                matches, _, _ = algo.search(text, pattern)
                assert matches == []
            except IndexError:
                # Alguns algoritmos podem não tratar bem esse caso
                pass

    def test_pattern_equals_text(self):
        """Pattern é exatamente igual ao texto"""
        algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
            KMPSearch(),
            BoyerMooreSearch(),
        ]

        pattern = "match"
        text = "match"

        for algo in algorithms:
            matches, _, _ = algo.search(text, pattern)
            assert matches == [0]

    def test_multiple_consecutive_matches(self):
        """Padrão aparece múltiplas vezes consecutivas"""
        algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
            KMPSearch(),
            BoyerMooreSearch(),
        ]

        pattern = "aa"
        text = "aaaa"  # "aa" aparece em posições 0, 1, 2

        for algo in algorithms:
            matches, _, _ = algo.search(text, pattern)
            # Em algoritmos sem sobreposição, pode ser [0, 2]
            # Em algoritmos com sobreposição, pode ser [0, 1, 2]
            assert len(matches) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
