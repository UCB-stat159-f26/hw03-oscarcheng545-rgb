import matplotlib
matplotlib.use("Agg")
import pandas as pd
import pytest
from tennis_career import plot_career_matches


def test_scatterplot_has_two_result_groups():
    data = pd.DataFrame({"player_age": [18.1, 20.5],
                         "age_difference": [-2.0, 3.0], "result": ["Win", "Loss"]})
    data.attrs["player"] = "Test Player"
    fig = plot_career_matches(data)
    assert "Test Player" in fig.axes[0].get_title()
    assert len(fig.axes[0].collections) == 2
    fig.clf()


def test_plot_rejects_bad_dataframe():
    with pytest.raises(ValueError, match="Expected"):
        plot_career_matches(pd.DataFrame())
