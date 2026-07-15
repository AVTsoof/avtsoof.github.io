"""Optional plot builder for this post. Run:  python build.py

Writes assets/plot.html and prints a stable snippet-include line to paste into
index.md once. Load real data via avtsoof.common_utils.data_dir("<name>").
"""

from pathlib import Path

import plotly.express as px

from avtsoof.common_utils import save_fig

HERE = Path(__file__).parent


def main() -> None:
    df = px.data.iris()  # replace with your experiment (e.g. read from data_dir(...))
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    print(save_fig(fig, HERE / "assets" / "plot.html"))


if __name__ == "__main__":
    main()
