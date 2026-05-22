from __future__ import annotations

import argparse
from pathlib import Path

from boyer_moore import BoyerMooreSearch
from knuth_morris_pratt import KMPSearch
from naive import NaiveSearch
from rabin_karp import RabinKarpSearch
from search_strategy import SearchResult, SearchStrategy
from telemetry import configure_telemetry, get_export_path, shutdown_telemetry


def format_result(result: SearchResult) -> str:
    expected = result.expected_scale_average
    ratio = result.comparisons / expected if expected else 0.0
    ms = result.elapsed_seconds * 1000
    us_per_comp = (
        (result.elapsed_seconds * 1_000_000 / result.comparisons)
        if result.comparisons
        else 0.0
    )

    lines = [
        f"Algoritmo: {result.algorithm}",
        f"Arquivo: {result.file_path}",
        f"Padrao pesquisado: {result.pattern}",
        f"Tamanho do texto (n): {result.text_length}",
        f"Tamanho do padrao (m): {result.pattern_length}",
        f"Ocorrencias encontradas: {len(result.matches)}",
        f"Posicoes: {result.matches if result.matches else 'nenhuma'}",
        f"Tempo de execucao: {ms:.6f} ms",
        f"Comparacoes relacionadas: {result.comparisons}",
        "Complexidade teorica:",
        f"  Melhor caso: {result.theoretical_best}",
        f"  Caso medio: {result.theoretical_average}",
        f"  Pior caso: {result.theoretical_worst}",
        "Comparacao real vs esperado:",
        f"  Escala esperada (aprox. caso medio): {expected}",
        f"  Razao comparacoes / escala esperada: {ratio:.4f}",
        f"  Tempo medio por comparacao: {us_per_comp:.4f} microssegundos",
    ]
    return "\n".join(lines)


def build_strategies(choice: str) -> list[SearchStrategy]:
    available: dict[str, SearchStrategy] = {
        "naive": NaiveSearch(),
        "rabin-karp": RabinKarpSearch(),
        "kmp": KMPSearch(),
        "boyer-moore": BoyerMooreSearch(),
    }

    if choice == "all":
        return [
            available["naive"],
            available["rabin-karp"],
            available["kmp"],
            available["boyer-moore"],
        ]
    return [available[choice]]


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def run_searches(
    files: list[Path], patterns: list[str], algorithm: str, step_by_step: bool
) -> list[SearchResult]:
    strategies = build_strategies(algorithm)
    results: list[SearchResult] = []

    for file_path in files:
        text = read_text_file(file_path)
        for pattern in patterns:
            for strategy in strategies:
                result = strategy.run(
                    text=text,
                    pattern=pattern,
                    file_path=str(file_path),
                    step_by_step=step_by_step,
                )
                results.append(result)

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Busca em texto usando Strategy Pattern: Naive, Rabin-Karp, KMP e Boyer-Moore."
    )
    parser.add_argument("files", nargs="+", help="Um ou mais arquivos .txt para busca")
    parser.add_argument(
        "-p",
        "--pattern",
        required=True,
        help=(
            "Padrao de busca. Pode ser string direta ou caminho de arquivo existente "
            "com um padrao por linha"
        ),
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        default="all",
        choices=["naive", "rabin-karp", "kmp", "boyer-moore", "all"],
        help="Algoritmo para executar ou 'all' para rodar todos",
    )
    parser.add_argument(
        "--step-by-step",
        action="store_true",
        help="Mostra log de execucao passo a passo (limitado para nao poluir saida)",
    )
    parser.add_argument(
        "--disable-telemetry",
        action="store_true",
        help="Desabilita a exportacao local de spans OpenTelemetry",
    )
    parser.add_argument(
        "--telemetry-dir",
        default="telemetry_data",
        help="Diretorio onde os spans OpenTelemetry serao exportados em JSONL",
    )
    return parser.parse_args()


def validate_input(files: list[str]) -> list[Path]:
    normalized_files = [Path(f).expanduser().resolve() for f in files]
    missing = [str(p) for p in normalized_files if not p.exists()]
    if missing:
        raise FileNotFoundError("Arquivos nao encontrados: " + ", ".join(missing))

    not_files = [str(p) for p in normalized_files if not p.is_file()]
    if not_files:
        raise ValueError(
            "Caminhos invalidos (nao sao arquivo): " + ", ".join(not_files)
        )

    return normalized_files


def resolve_patterns(pattern_input: str) -> tuple[list[str], Path | None]:
    if not pattern_input:
        raise ValueError("O padrao de busca nao pode ser vazio.")

    candidate = Path(pattern_input).expanduser()
    if candidate.exists():
        resolved = candidate.resolve()
        if not resolved.is_file():
            raise ValueError(
                "O caminho informado em -p/--pattern existe, mas nao e um arquivo: "
                + str(resolved)
            )

        patterns = [line for line in read_text_file(resolved).splitlines() if line]
        if not patterns:
            raise ValueError(
                "O arquivo de padroes esta vazio ou contem apenas linhas em branco."
            )
        return patterns, resolved

    return [pattern_input], None


def main() -> None:
    args = parse_args()
    telemetry_path: Path | None = None
    if not args.disable_telemetry:
        telemetry_path = configure_telemetry(export_dir=args.telemetry_dir)
    files = validate_input(args.files)
    patterns, pattern_file = resolve_patterns(args.pattern)
    try:
        results = run_searches(
            files=files,
            patterns=patterns,
            algorithm=args.algorithm,
            step_by_step=args.step_by_step,
        )
    finally:
        if not args.disable_telemetry:
            shutdown_telemetry()

    for idx, result in enumerate(results, start=1):
        if idx > 1:
            print("\n" + "=" * 72)
        print(format_result(result))

        if args.step_by_step:
            print("Passo a passo (amostra):")
            if result.step_logs:
                for line in result.step_logs:
                    print(f"  {line}")
            else:
                print("  sem eventos detalhados")

    if pattern_file is not None:
        print("\n" + "-" * 72)
        print(f"Padroes carregados de: {pattern_file} ({len(patterns)} linhas validas)")

    if telemetry_path is not None:
        print("\n" + "-" * 72)
        print(f"OpenTelemetry exportado em: {get_export_path()}")


if __name__ == "__main__":
    main()
