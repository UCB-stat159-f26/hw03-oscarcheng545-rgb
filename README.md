# Tennis Career Matches (HW3)

## About

This is a Python package based on my HW2 Serena Williams visualization. It gets career match data from [Tennis Abstract](https://www.tennisabstract.com/) and makes a scatterplot comparing a player's age to the age difference between them and their opponents.

Wins are shown in blue and losses in purple, similar to my HW2 graph.

## Installation

Install the package from GitHub:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-oscarcheng545-rgb.git
```

Or install it locally:

```bash
pip install -e .
```

## Example

```python
from tennis_career import get_career_matches, plot_career_matches
import matplotlib.pyplot as plt

serena = get_career_matches("Serena Williams")
print(serena.head())
plot_career_matches(serena)
plt.show()

rafa = get_career_matches("Rafael Nadal")
plot_career_matches(rafa)
plt.show()
```

The `get_career_matches()` function returns a pandas DataFrame with the match date, opponent, player age, opponent age, age difference, and match result.

The `plot_career_matches()` function creates a scatterplot using that data.

If an invalid player name is entered, the package raises an error.

## Testing

To run the tests:

```bash
pip install -e ".[test]"
python -m pytest -v
```

I wrote tests using sample JavaScript data instead of making requests to the actual website. The tests check player names, missing data, and the different formats used for men's and women's matches.

All 13 tests passed. I also checked the package using Serena Williams and Rafael Nadal's actual match data.

## Reflection

The main challenge in HW3 was changing my HW2 code so it could work for different players. In HW2, I only needed Serena Williams's data, but this time I had to get the information automatically based on the player's name.

I also learned that the men's and women's match files store opponent ages differently, so I had to handle both formats. Another issue I ran into was finding the player's birthday in the JavaScript files. Testing the package with actual players helped me figure out what was wrong.

Overall, this assignment helped me understand how Python packages work and why it's useful to split code into smaller functions and test them separately.