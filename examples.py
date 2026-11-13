"""Run this script if you want to make a player's plot locally."""
from tennis_career import get_career_matches, plot_career_matches
import matplotlib.pyplot as plt

name = "Serena Williams"
career = get_career_matches(name)
print(career.head())
plot_career_matches(career)
plt.show()
