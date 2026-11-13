"""Plot age differences for career matches."""
import matplotlib.pyplot as plt


def plot_career_matches(data):
    """Show the player's age against player minus opponent age, colored by result."""
    needed = {"player_age", "age_difference", "result"}
    if not needed.issubset(data.columns) or data.empty:
        raise ValueError("Expected a nonempty career DataFrame from get_career_matches().")
    fig, ax = plt.subplots(figsize=(11, 7))
    for result, color in (("Win", "#39BCE1"), ("Loss", "#8E3C97")):
        rows = data[data["result"] == result]
        ax.scatter(rows["player_age"], rows["age_difference"],
                   s=15, alpha=0.8, c=color, label=result)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set(xlabel="Player's age (years)", ylabel="Player age minus opponent age (years)")
    ax.set_title(f"{data.attrs.get('player', 'Player')} career matches")
    ax.grid(alpha=0.2)
    ax.legend(title="Result")
    fig.tight_layout()
    return fig
