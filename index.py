import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.patches import Patch
from matplotlib.colors import Normalize

n_sims = 100000
#strat(3) is optimal
def strat(reroll_max):
    first_3d6 = [random.randint(1, 6) for i in range(3)]
    return np.sum([random.randint(1, 6) if roll <= reroll_max else roll for roll in first_3d6])

#plot strats
x = [i for i in range(1, 7)]
y = [np.mean([strat(n) for i in range(n_sims)]) for n in x]
plt.plot(x, y)
plt.xlabel('Max Dice Value Rerolled')
plt.ylabel('Mean Final Sum')
plt.savefig('dice-poker-strats.png', dpi=200)
plt.close()

#plot sum CDF
data = [strat(0) for i in range(n_sims)]
hist, bins = np.histogram(data, bins=[i for i in range(3, 20)])
adj_hist = hist / len(data)
cdf = [np.sum(adj_hist[:i]) for i in range(len(adj_hist))]
plt.bar(bins[:-1], cdf)
plt.xticks(bins[:-1])
plt.xlabel('Roll Sum')
plt.ylabel('Probability (roll<=sum)')
plt.savefig('dice-poker-cdf.png', dpi=200)
plt.close()

#calcuate probs for n opps
df = pd.DataFrame(columns=[i for i in range(1, 11)], index=[i for i in range(3, 19)])
for n in df.columns:
    for i in range(len(cdf)):
        p = cdf[i]
        roll = bins[i + 1] - 1
        if roll == 2:
            continue
        opp_p = 1 - (p ** n)
        df.loc[roll, n] = round(opp_p, 2)

#get table colors
vals = np.vectorize(lambda a : round(a, 2))(df.to_numpy())
cmap = colormaps['PiYG_r']
c_norm = Normalize(vmin=0, vmax=1)
colors = cmap(c_norm(vals))
#plot
fig, ax = plt.subplots()
ax.table(df, loc='center', cellColours=colors)
plt.xlabel('Number of Opponents')
plt.ylabel('Your Step 2 Sum')
ax.set_axis_off()
ax.legend(loc='best', bbox_to_anchor=(0.1, 0.6, 0.5, 0.5), handles=[Patch(label='Raise', facecolor='#276419', edgecolor='#000000', linewidth=1), Patch(label='Hold', facecolor='#ffffff', edgecolor='#000000', linewidth=1), Patch(label='Fold', facecolor='#8e0152', edgecolor='#000000', linewidth=1)])
plt.savefig('dice-poker-table.png', dpi=200)
plt.close()