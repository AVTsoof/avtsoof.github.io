"""Build the interactive figure for this post. Run:  python build.py

Self-contained (no external dataset) so the committed plot reproduces exactly.
"""

from pathlib import Path

import plotly.graph_objects as go

from avtsoof.common_utils import save_fig

HERE = Path(__file__).parent


def main() -> None:
    posts = list(range(1, 11))
    written_once = [40] * len(posts)              # the shared toolkit, written once
    rewritten_each = [40 * n for n in posts]      # plumbing re-invented per post

    fig = go.Figure()
    fig.add_scatter(
        x=posts, y=rewritten_each, mode="lines+markers",
        name="plumbing rewritten per post",
    )
    fig.add_scatter(
        x=posts, y=written_once, mode="lines+markers",
        name="shared toolkit (written once)",
    )
    fig.update_layout(
        title="Cumulative plumbing code as the blog grows",
        xaxis_title="number of posts",
        yaxis_title="cumulative plumbing LOC",
        legend_title="approach",
    )
    print(save_fig(fig, HERE / "assets" / "plot.html"))


if __name__ == "__main__":
    main()
