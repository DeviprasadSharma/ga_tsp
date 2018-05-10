import matplotlib as mpl
import matplotlib.pyplot as plt


def plot_population(cities, population, name='diagram.png', ax=None):
    """Отрисовка всей входящей популяции в файл"""
    mpl.rcParams['agg.path.chunksize'] = 10000

    fig = plt.figure(figsize=(5, 5), frameon=False)
    axis = fig.add_axes([0, 0, 1, 1])

    axis.set_aspect('equal', adjustable='datalim')
    plt.axis('off')

    axis.scatter(cities['x'], cities['y'], color='red', s=4)
    axis.plot(population[:, 0], population[:, 1], 'r.', ls='-', color='#0063ba', markersize=2)

    plt.savefig(name, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.close()


def plot_route(cities, route, name='diagram.png', ax=None):
    """Отрисовка маршрута"""
    mpl.rcParams['agg.path.chunksize'] = 10000

    fig = plt.figure(figsize=(5, 5), frameon=False)
    axis = fig.add_axes([0, 0, 1, 1])

    axis.set_aspect('equal', adjustable='datalim')
    plt.axis('off')

    axis.scatter(cities['x'], cities['y'], color='red', s=4)
    route = cities.reindex(route)
    route.loc[route.shape[0]] = route.iloc[0]
    axis.plot(route['x'], route['y'], color='purple', linewidth=1)

    plt.savefig(name, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.close()
