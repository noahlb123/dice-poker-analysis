import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#strat(3) is optimal
def strat(reroll_max):
    first_3d6 = [random.randint(1, 6) for i in range(3)]
    return np.sum([random.randint(1, 6) if roll <= reroll_max else roll for roll in first_3d6])

#plot stradegies
x = [i for i in range(1, 7)]
y = [np.mean([strat(n) for i in range(100000)]) for n in x]
plt.plot(x, y)
plt.xlabel('Max Dice Value Rerolled')
plt.ylabel('Mean Final Sum')
plt.show()
plt.close()

#plot sum CDF
data = [strat(0) for i in range(100000)]
hist, bins = np.histogram(data, bins=[i for i in range(2, 20)])
adj_hist = hist / len(data)
cdf = [np.sum(adj_hist[:i]) for i in range(len(adj_hist))]
plt.bar(bins[:-1], cdf)
plt.xticks(bins[:-1])
plt.xlabel('Roll Sum')
plt.ylabel('Probability (roll<=sum)')
plt.show()

#calcuate probs for n opps
df = pd.DataFrame(columns=[i for i in range(1, 11)], index=[i for i in range(3, 18)])
for n in df.columns:
    for i in range(len(cdf)):
        p = cdf[i]
        roll = bins[i + 1] - 1
        if roll == 2:
            continue
        opp_p = (1 - p) ** (1 / n)
        df.loc[roll, n] = round(opp_p, 2)

print(df)
