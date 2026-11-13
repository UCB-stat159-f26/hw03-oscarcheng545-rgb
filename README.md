# Tennis Career Matches (HW3)

This is a Python package based on my HW2 Serena Williams visualization. It reads a player's career matches from [Tennis Abstract](https://www.tennisabstract.com/), calculates the age difference between the player and each opponent, and makes a scatterplot. Wins are cyan and losses are purple, like my HW2 graph. I left out the annotations for HW3.

## Install

Install from GitHub after pushing this repository:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-oscarcheng545-rgb.git
```

Or install locally from the repository folder:

```bash
pip install -e .
```

## Example

```python
from tennis_career import get_career_matches, plot_career_matches
import matplotlib.pyplot as plt

serena = get_career_matches("serena williams")
print(serena.head())
plot_career_matches(serena)
plt.show()

rafa = get_career_matches("Rafael Nadal")
plot_career_matches(rafa)
plt.show()

# Raises ValueError with an explanation if the player cannot be found
get_career_matches("GastonSanchez")
```

`get_career_matches` returns a pandas DataFrame with the match date, opponent, player age, opponent age, age difference, and win/loss result. The plot function returns a Matplotlib Figure, so it can also be saved using `fig.savefig("career.png")`.

## Testing

```bash
pip install -e '.[test]'
pytest -q
```

Tests use made-up career JavaScript samples rather than sending requests to Tennis Abstract. Both opponent birth dates (women's match data) and precomputed opponent ages (men's match data) are tested. I also checked the cleaning code against the Serena JS file from HW2: both produced 1,038 usable matches.

## Notes

- The match file is downloaded when you call `get_career_matches`. An internet connection is needed for this function.
- The player's birthday comes from the Tennis Abstract profile. If the birthday or career match data is unavailable, the function raises an error instead of making up ages.
- Tennis Abstract can change its page or JavaScript format; the package currently follows the fields shown in the HW3 assignment.
- Ages use days divided by 365.2425, the same method I used in HW2.

## Reflection

The biggest change from HW2 was making the code reusable. In HW2, the birthday and filenames were only for Serena Williams. For this assignment, I needed to pull the player's name from the function argument and also handle two different opponent-age formats. Splitting the downloading, data cleaning, and plotting into separate functions made it easier to test mistakes without rerunning the entire project. The tests also helped me catch a problem with names written in CamelCase.
