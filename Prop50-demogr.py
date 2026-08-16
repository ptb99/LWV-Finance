import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    # '%matplotlib inline' command supported automatically in marimo
    #matplotlib.style.use('classic')

    #pd.show_versions()
    print('Pandas = ', pd.__version__)
    print('Numpy = ', np.__version__)
    print('Matplotlib = ', matplotlib.__version__)
    return pd, plt


@app.cell
def _(pd):
    f = 'Prop50-demographics.csv'
    csv = pd.read_csv(f, header=2, index_col='District')
    csv.head()
    return (csv,)


@app.cell
def _(csv):
    current = csv[['Latino Pct', 'Black Pct', 'Asian Pct']]
    current.head()
    return (current,)


@app.cell
def _(csv):
    proposed = csv[['Latino Pct.1', 'Black Pct.1', 'Asian Pct.1']]
    proposed.head()
    return (proposed,)


@app.cell
def _(current, pd, proposed):
    groups = ['Latino', 'Black', 'Asian']
    data = {}
    for _l in groups:
        data[_l] = pd.DataFrame()
        data[_l]['Current'] = current[f'{_l} Pct'].str.rstrip('%').astype('float')
        data[_l]['Proposed'] = proposed[f'{_l} Pct.1'].str.rstrip('%').astype('float')
        data[_l]['Difference'] = data[_l]['Proposed'] - data[_l]['Current']
    data['Latino'].head()
    return data, groups


@app.cell
def _(data, groups, plt):
    _fig, _axes = plt.subplots(3, 2, figsize=(10, 12), sharex=False, sharey=True)
    labels = ['Current', 'Proposed']
    for _i, g in enumerate(groups):
        for j, _l in enumerate(labels):
            if g == 'Latino':
                _rv = data[g][_l].plot.hist(ax=_axes[_i][j], bins=32, range=(0, 80), histtype='stepfilled', xlabel=f'{g} %', title=_l)
            if g == 'Black':
                _rv = data[g][_l].plot.hist(ax=_axes[_i][j], bins=20, range=(0, 50), histtype='stepfilled', xlabel=f'{g} %')
            if g == 'Asian':
                _rv = data[g][_l].plot.hist(ax=_axes[_i][j], bins=24, range=(0, 60), histtype='stepfilled', xlabel=f'{g} %')
    return


@app.cell
def _(data, groups, plt):
    _fig, _axes = plt.subplots(1, 3, figsize=(12, 4), sharex=True, sharey=True)
    for _i, _l in enumerate(groups):
        _rv = data[_l]['Difference'].plot.hist(ax=_axes[_i], bins=40, range=(-20, 20), histtype='stepfilled', xlabel='Change in district %', title=_l)
    return


if __name__ == "__main__":
    app.run()
