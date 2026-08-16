import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Calculation
    """)
    return


@app.cell
def _():
    ## Standard Boilerplate

    import re
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    # '%matplotlib inline' command supported automatically in marimo
    #matplotlib.style.use('classic')

    #pd.show_versions()
    print('Pandas = ', pd.__version__)
    print('Numpy = ', np.__version__)
    print('Matplotlib = ', matplotlib.__version__)
    return pd, re


@app.cell
def _(pd):
    ## Data Retrieval
    _url = 'powersearch-test-Oct7.csv'
    #url = 'https://powersearch.sos.ca.gov/download_csv.php?w=WHERE+contributions_search.BallotMeasureContribution+%3D+%27Y%27+AND+%28contributions_search.ElectionCycle+%3D+%3F%29&d=a%3A1%3A%7Bi%3A0%3Bs%3A4%3A%222025%22%3B%7D&c=a%3A6%3A%7Bs%3A16%3A%2200Contributor%28s%29%22%3Bs%3A3%3A%22All%22%3Bs%3A19%3A%2201Contributor_State%22%3Bs%3A3%3A%22All%22%3Bs%3A14%3A%2202Recipient%28s%29%%3B22s%3A19%3A%22All+ballot+measures%22%3Bs%3A31%3A%2207Contribution_Dates_and_Cycles%22%3Bs%3A0%3A%22%22%3Bs%3A27%3A%2206Exclude_Allied_Committees%22%3Bs%3A2%3A%22No%22%3Bs%3A21%3A%2209Contribution_Cycles%22%3Bs%3A4%3A%222025%22%3B%7D'
    #url = 'https://powersearch.sos.ca.gov/download_csv.php?w=WHERE+contributions_search.AlliedCommittee+%3D+%27N%27+AND+contributions_search.BallotMeasureContribution+%3D+%27Y%27+AND+%28contributions_search.ElectionCycle+%3D+%3F%29&d=a%3A1%3A%7Bi%3A0%3Bs%3A4%3A%222025%22%3B%7D&c=a%3A6%3A%7Bs%3A16%3A%2200Contributor%28s%29%22%3Bs%3A3%3A%22All%22%3Bs%3A19%3A%2201Contributor_State%22%3Bs%3A3%3A%22All%22%3Bs%3A14%3A%2202Recipient%28s%29%22%3Bs%3A19%3A%22All+ballot+measures%22%3Bs%3A31%3A%2207Contribution_Dates_and_Cycles%22%3Bs%3A0%3A%22%22%3Bs%3A27%3A%2206Exclude_Allied_Committees%22%3Bs%3A3%3A%22Yes%22%3Bs%3A21%3A%2209Contribution_Cycles%22%3Bs%3A4%3A%222025%22%3B%7D'
    rawdata = pd.read_csv(_url, index_col=0)
    # Use a cached copy to speed up testing:
    rawdata = rawdata.dropna(subset=['Cycle'])
    rawdata[['Recipient Committee ID', 'Contributor ID']] = rawdata[['Recipient Committee ID', 'Contributor ID']].astype(pd.Int64Dtype())
    # This may be brittle:
    #rawdata = pd.read_csv(url, skipfooter=6)
    # perhaps better:
    # Adjust to make IDs have integer values:
    rawdata.tail()  # drop any raw that is missing Cycle == 2025
    return (rawdata,)


@app.cell
def _():
    #url = 'https://powersearch.sos.ca.gov/download_csv.php?w=WHERE+contributions_search.BallotMeasureContribution+%3D+%27Y%27+AND+%28contributions_search.ElectionCycle+%3D+%3F%29&d=a%3A1%3A%7Bi%3A0%3Bs%3A4%3A%222025%22%3B%7D&c=a%3A6%3A%7Bs%3A16%3A%2200Contributor%28s%29%22%3Bs%3A3%3A%22All%22%3Bs%3A19%3A%2201Contributor_State%22%3Bs%3A3%3A%22All%22%3Bs%3A14%3A%2202Recipient%28s%29%%3B22s%3A19%3A%22All+ballot+measures%22%3Bs%3A31%3A%2207Contribution_Dates_and_Cycles%22%3Bs%3A0%3A%22%22%3Bs%3A27%3A%2206Exclude_Allied_Committees%22%3Bs%3A2%3A%22No%22%3Bs%3A21%3A%2209Contribution_Cycles%22%3Bs%3A4%3A%222025%22%3B%7D'
    _url = 'https://powersearch.sos.ca.gov/download_csv.php?w=WHERE+contributions_search.AlliedCommittee+%3D+%27N%27+AND+contributions_search.BallotMeasureContribution+%3D+%27Y%27+AND+%28contributions_search.ElectionCycle+%3D+%3F%29&d=a%3A1%3A%7Bi%3A0%3Bs%3A4%3A%222025%22%3B%7D&c=a%3A6%3A%7Bs%3A16%3A%2200Contributor%28s%29%22%3Bs%3A3%3A%22All%22%3Bs%3A19%3A%2201Contributor_State%22%3Bs%3A3%3A%22All%22%3Bs%3A14%3A%2202Recipient%28s%29%22%3Bs%3A19%3A%22All+ballot+measures%22%3Bs%3A31%3A%2207Contribution_Dates_and_Cycles%22%3Bs%3A0%3A%22%22%3Bs%3A27%3A%2206Exclude_Allied_Committees%22%3Bs%3A3%3A%22Yes%22%3Bs%3A21%3A%2209Contribution_Cycles%22%3Bs%3A4%3A%222025%22%3B%7D'
    import urllib
    _p = urllib.parse.urlparse(_url)
    ## It's not very clear how to make sense of these query params.  I guess it makes sense to the PowerSearch back-end.
    ## Potentially, one could tweak one of the params and call urllib.parse.quote_plus().
    ## Note that the scheme is 's:3:"All";' means a string of len 3 with value "All" and 'a:6:{...}' is an array of 6 elements.
    urllib.parse.parse_qs(_p.query)
    return


@app.cell
def _(rawdata):
    rawdata.info()
    rawdata.to_csv('powersearch-test-Oct30.csv')
    return


@app.cell
def _(rawdata):
    #rawdata['Ballot Measure(s)'].head()
    rawdata.groupby('Ballot Measure(s)')['Cycle'].count()
    return


@app.cell
def _(rawdata, re):
    # separate support/oppose, group by contributor, sum amount
    pro_regex = re.compile('^SUPPORT', re.IGNORECASE)
    con_regex = re.compile('^OPPOSE', re.IGNORECASE)
    fields = ['Amount', 'Recipient Committee', 'Recipient Committee ID', 'Contributor Name', 'Contributor ID', 'Contributor City', 'Contributor State', 'Contributor Zip Code']
    s = rawdata['Ballot Measure(s)']
    pros = rawdata[s.map(lambda x: pro_regex.match(_x) is not None)][fields]
    cons = rawdata[s.map(lambda x: con_regex.match(_x) is not None)][fields]
    cons.info()
    return cons, pros


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Results
    """)
    return


@app.cell
def _(cons, pd, pros):
    rows = ['Total ($M)', 'Num Donations', 'Avg Donation', 'Median Donation']
    funs = [pd.Series.sum, pd.Series.count, pd.Series.mean, pd.Series.median]
    _totals = pd.DataFrame({'PRO': [_x(pros['Amount']) for _x in funs], 'CON': [_x(cons['Amount']) for _x in funs]}, index=rows)
    #totals.iloc(0)
    _totals.loc['Total ($M)'] /= 1000000.0
    #totals.loc['Num Donations']
    _totals.style.format(precision=2, thousands=',').format(lambda x: f'{int(_x):,}', subset=('Num Donations', _totals.columns))
    return


@app.cell
def _(cons):
    cons.groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum().nlargest(10)/1e6
    return


@app.cell
def _(pros):
    pros.groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum().nlargest(10)/1e6
    return


@app.cell
def _(cons, pd, pros):
    from functools import partial

    def _in_state(df, label):
        val = df['Contributor State'][label]
        if val == 'CA':
            return 'In-State'
        elif pd.isna(val):
            return '?'
        else:
            return 'Out-State'
    print('PRO:')
    print((pros.groupby(partial(_in_state, pros))['Amount'].sum() / 1000000.0).to_string())
    print()
    print('CON:')
    print((cons.groupby(partial(_in_state, cons))['Amount'].sum() / 1000000.0).to_string())
    return


@app.cell
def _(cons, pd, pros):
    def _in_state(val):
        if val == 'CA':  #val = df['Contributor State'][label]
            return 'In-State'
        elif pd.isna(val):
            return '?'
        else:
            return 'Out-State'
    _x = cons.head(20).copy()
    _x.groupby(_x['Contributor State'].apply(_in_state))['Amount'].sum() / 1000000.0
    print('PRO:')
    print((pros.groupby(pros['Contributor State'].apply(_in_state))['Amount'].sum() / 1000000.0).to_string())
    print()
    print('CON:')
    print((cons.groupby(cons['Contributor State'].apply(_in_state))['Amount'].sum() / 1000000.0).to_string())
    return


@app.cell
def _(cons, pd, pros):
    # Have to remove 'Unitemized' since they're usually small donors
    _p = pros[pros['Contributor Name'] != 'Unitemized Contributions'].groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum()
    c = cons[cons['Contributor Name'] != 'Unitemized Contributions'].groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum()
    bins = [0, 100, 999.99, 1000000000000.0]
    # S = 0-100, M = 101-999, L = 1000+
    names = ['S', 'M', 'L']
    _totals = pd.DataFrame({'PRO Num Donors': pd.cut(_p, bins, labels=names).value_counts(), 'CON Num Donors': pd.cut(c, bins, labels=names).value_counts()}, dtype=pd.Int64Dtype())
    _totals.sort_index(ascending=False).fillna(0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Diagnostics
    """)
    return


@app.cell
def _(pros):
    pros[pros['Contributor Name'] == 'Unitemized Contributions'].nlargest(20, 'Amount')
    return


@app.cell
def _(cons):
    cons[cons['Contributor Name'] == 'Unitemized Contributions'].nlargest(10, 'Amount')
    return


@app.cell
def _(pros):
    pros.groupby('Recipient Committee ID')['Amount'].nunique().sort_values(ascending=False)
    return


@app.cell
def _(pros):
    _x = pros[pros['Recipient Committee ID'] == 1483877]
    print('Total = ', _x['Amount'].sum() / 1000000.0)
    _x
    return


@app.cell
def _(pros):
    _id = 1483877
    _x = pros[pros['Contributor ID'] == _id]
    print('Total = ', _x['Amount'].sum() / 1000000.0)
    _x.nlargest(10, 'Amount')
    return


@app.cell
def _(pros):
    ## What's the status of these other committees?
    #id = 1071446
    #id = 1483402
    #id = 1483630
    _id = 1465256
    #id = 1483677
    #id = 1483675
    #id = 1483721
    pros[pros['Recipient Committee ID'] == _id].sort_values('Amount', ascending=False)
    return


@app.cell
def _(pros):
    _id = 1465256
    pros[pros['Contributor ID'] == _id].sort_values('Amount', ascending=False)
    return


@app.cell
def _(pros):
    _id = 1483431
    _x = pros[pros['Contributor ID'] == _id]
    print('Total = ', _x['Amount'].sum() / 1000000.0)
    _x.sort_values('Amount', ascending=False)
    return


@app.cell
def _(pros):
    ## Find cases of committees giving to other committees
    _temp = pros[(pros['Recipient Committee ID'] > 0) & (pros['Contributor ID'] > 0)]
    print(f"PRO donations from another committee: {_temp['Amount'].count()} for ${_temp['Amount'].sum() / 1000000.0:.2f}M")
    _temp.nlargest(10, 'Amount')
    return


@app.cell
def _(cons):
    ## Find cases of committees giving to other committees
    _temp = cons[(cons['Recipient Committee ID'] > 0) & (cons['Contributor ID'] > 0)]
    print(f"CON donations from another committee: {_temp['Amount'].count()} for ${_temp['Amount'].sum() / 1000000.0:.2f}M")
    _temp.nlargest(10, 'Amount')
    return


@app.cell
def _(cons):
    _id = 1483647
    cons[cons['Recipient Committee ID'] == _id].sort_values('Amount', ascending=False)
    return


@app.cell
def _(cons):
    ## example of a pass-thru contrib that we should exclude from our totals
    _id = 1483647
    cons[cons['Contributor ID'] == _id].sort_values('Amount', ascending=False)
    return


@app.cell
def _(cons):
    ## all of these are empty (no contributions filed)
    #id = 1277366
    #id = 1293318
    #id = 1402911
    #id = 1311575
    _id = 1381029
    #cons[cons['Recipient Committee ID'] == id]['Amount'].sum()  ## 32.799M
    cons[cons['Recipient Committee ID'] == _id].sort_values('Amount', ascending=False)
    return


@app.cell
def _(cons):
    _id = 1483178
    _temp = cons[cons['Recipient Committee ID'] == _id].nlargest(10, 'Amount')
    #cons[cons['Recipient Committee ID'] == id]['Amount'].sum()  ## 8.040M
    _temp[['Amount', 'Contributor Name', 'Recipient Committee']]
    return


@app.cell
def _(rawdata):
    rawdata[ (rawdata['Recipient Committee ID'] == 1380675) & (rawdata['Contributor Name'] == 'Unitemized Contributions') ].nlargest(20, 'Amount')
    return


if __name__ == "__main__":
    app.run()
