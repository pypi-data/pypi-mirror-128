from matplotlib.patches import Rectangle

for i, row in enumerate(K):
    for j, k in enumerate(row):
        ax.add_patch(Rectangle((i, j), 1, 1, color=np.ones(3) * k / K.max()))
