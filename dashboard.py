from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DEFAULT_DATA_FILE = (
    Path(__file__).resolve().parent / "telemetry_data" / "search_runs.jsonl"
)


@st.cache_data(show_spinner=False)
def load_runs(data_file: str) -> pd.DataFrame:
    path = Path(data_file)
    if not path.exists():
        return pd.DataFrame()

    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as input_file:
        for line in input_file:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    if not records:
        return pd.DataFrame()

    dataframe = pd.DataFrame(records)
    dataframe["start_time"] = pd.to_datetime(dataframe["start_time"])
    dataframe["end_time"] = pd.to_datetime(dataframe["end_time"])
    dataframe["search.elapsed_ms"] = pd.to_numeric(
        dataframe["search.elapsed_ms"], errors="coerce"
    )
    dataframe["search.comparisons"] = pd.to_numeric(
        dataframe["search.comparisons"], errors="coerce"
    )
    dataframe["search.matches_count"] = pd.to_numeric(
        dataframe["search.matches_count"], errors="coerce"
    )
    return dataframe.sort_values("start_time", ascending=False)


def render_empty_state(data_file: Path) -> None:
    st.info(
        "Nenhuma execução instrumentada encontrada ainda. Rode o programa principal para gerar spans em "
        f"{data_file}."
    )
    st.code('python main.py text.txt -p "the" -a all', language="bash")


def main() -> None:
    st.set_page_config(
        page_title="OpenTelemetry Dashboard", page_icon="OT", layout="wide"
    )
    st.title("Dashboard de Busca com OpenTelemetry")
    st.caption(
        "Comparação histórica das execuções instrumentadas dos algoritmos de busca."
    )

    data_file = Path(
        st.sidebar.text_input("Arquivo de telemetria", value=str(DEFAULT_DATA_FILE))
    ).expanduser()
    dataframe = load_runs(str(data_file))

    if dataframe.empty:
        render_empty_state(data_file)
        return

    algorithms = sorted(dataframe["search.algorithm"].dropna().unique().tolist())
    selected_algorithms = st.sidebar.multiselect(
        "Algoritmos",
        options=algorithms,
        default=algorithms,
    )

    files = sorted(dataframe["search.file_path"].dropna().unique().tolist())
    selected_files = st.sidebar.multiselect("Arquivos", options=files, default=files)

    filtered = dataframe[
        dataframe["search.algorithm"].isin(selected_algorithms)
        & dataframe["search.file_path"].isin(selected_files)
    ].copy()

    if filtered.empty:
        st.warning("Os filtros atuais não retornaram execuções.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Execuções", int(len(filtered)))
    col2.metric("Tempo médio", f"{filtered['search.elapsed_ms'].mean():.3f} ms")
    col3.metric("Comparações médias", f"{filtered['search.comparisons'].mean():.0f}")

    grouped = (
        filtered.groupby("search.algorithm", as_index=False)
        .agg(
            execucoes=("search.algorithm", "count"),
            tempo_medio_ms=("search.elapsed_ms", "mean"),
            tempo_total_ms=("search.elapsed_ms", "sum"),
            comparacoes_medias=("search.comparisons", "mean"),
            matches_medios=("search.matches_count", "mean"),
        )
        .sort_values("tempo_medio_ms")
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Tempo de execução por algoritmo")
        fig_time = px.bar(
            grouped,
            x="search.algorithm",
            y="tempo_medio_ms",
            color="search.algorithm",
            labels={
                "search.algorithm": "Algoritmo",
                "tempo_medio_ms": "Tempo médio (ms)",
            },
        )
        fig_time.update_layout(showlegend=False)
        st.plotly_chart(fig_time, use_container_width=True)

    with right:
        st.subheader("Número de execuções")
        fig_runs = px.bar(
            grouped,
            x="search.algorithm",
            y="execucoes",
            color="search.algorithm",
            labels={"search.algorithm": "Algoritmo", "execucoes": "Execuções"},
        )
        fig_runs.update_layout(showlegend=False)
        st.plotly_chart(fig_runs, use_container_width=True)

    st.subheader("Comparações entre algoritmos")

    fig_compare = px.scatter(
        filtered,
        x="search.comparisons",
        y="search.elapsed_ms",
        color="search.algorithm",
        size="search.matches_count",
        hover_data=["search.file_path", "search.text_length", "search.pattern_length"],
        labels={
            "search.comparisons": "Comparações",
            "search.elapsed_ms": "Tempo (ms)",
            "search.algorithm": "Algoritmo",
            "search.matches_count": "Ocorrências",
        },
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    st.subheader("Resumo agregado")
    st.dataframe(
        grouped.rename(
            columns={
                "search.algorithm": "Algoritmo",
                "execucoes": "Execuções",
                "tempo_medio_ms": "Tempo médio (ms)",
                "tempo_total_ms": "Tempo total (ms)",
                "comparacoes_medias": "Comparações médias",
                "matches_medios": "Ocorrências médias",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()
