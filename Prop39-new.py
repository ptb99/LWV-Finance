import marimo

__generated_with = "0.23.16"
app = marimo.App()


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
    import urllib
    import marimo as mo
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
    return mo, pd, re, urllib


@app.cell
def _(urllib):
    baseurl = 'https://powersearch.sos.ca.gov/download_csv.php'
    headers = {"referer": "https://powersearch.sos.ca.gov/advanced.php"}
    election = "2026-11-03"

    def php_serialize_strings(values):
        result = [f"a:{len(values)}:{{"]

        for i, value in enumerate(values):
            encoded = value.encode("utf-8")
            result.append(
                f'i:{i};s:{len(encoded)}:"{value}";'
            )

        result.append("}")
        return "".join(result)

    # SQL query based on powersearch website 8/11/2026
    def make_url(prop_num, election):
        query = """
    WHERE smry_propositions.Target LIKE ?
      AND smry_propositions.Election = ?
      AND contributions_search.BallotMeasureContribution = 'Y'
    """
        arg_list = [
            f'PROPOSITION {prop_num:03d}%',
            election
        ]
        params = {'w': query, 'd': php_serialize_strings(arg_list)}
        urlstr = f'{baseurl}?{urllib.parse.urlencode(params)}'
        return urlstr

    #_url = make_url(39, election)
    #print('URL =', _url)
    return election, headers, make_url


@app.cell(disabled=True, hide_code=True)
def _(urllib):
    _urlstr = 'https://powersearch.sos.ca.gov/download_csv.php?w=WHERE+contributions_search.BallotMeasureContribution+%3D+%27Y%27+AND+%28contributions_search.ElectionCycle+%3D+%3F%29&d=a%3A1%3A%7Bi%3A0%3Bs%3A4%3A%222025%22%3B%7D&c=a%3A6%3A%7Bs%3A16%3A%2200Contributor%28s%29%22%3Bs%3A3%3A%22All%22%3Bs%3A19%3A%2201Contributor_State%22%3Bs%3A3%3A%22All%22%3Bs%3A14%3A%2202Recipient%28s%29%%3B22s%3A19%3A%22All+ballot+measures%22%3Bs%3A31%3A%2207Contribution_Dates_and_Cycles%22%3Bs%3A0%3A%22%22%3Bs%3A27%3A%2206Exclude_Allied_Committees%22%3Bs%3A2%3A%22No%22%3Bs%3A21%3A%2209Contribution_Cycles%22%3Bs%3A4%3A%222025%22%3B%7D'
    #url = 'https://powersearch.sos.ca.gov/download_csv.php?w=WHERE+contributions_search.AlliedCommittee+%3D+%27N%27+AND+contributions_search.BallotMeasureContribution+%3D+%27Y%27+AND+%28contributions_search.ElectionCycle+%3D+%3F%29&d=a%3A1%3A%7Bi%3A0%3Bs%3A4%3A%222025%22%3B%7D&c=a%3A6%3A%7Bs%3A16%3A%2200Contributor%28s%29%22%3Bs%3A3%3A%22All%22%3Bs%3A19%3A%2201Contributor_State%22%3Bs%3A3%3A%22All%22%3Bs%3A14%3A%2202Recipient%28s%29%22%3Bs%3A19%3A%22All+ballot+measures%22%3Bs%3A31%3A%2207Contribution_Dates_and_Cycles%22%3Bs%3A0%3A%22%22%3Bs%3A27%3A%2206Exclude_Allied_Committees%22%3Bs%3A3%3A%22Yes%22%3Bs%3A21%3A%2209Contribution_Cycles%22%3Bs%3A4%3A%222025%22%3B%7D'
    #urlstr = 'https://powersearch.sos.ca.gov/download_csv.php?w=WHERE+smry_propositions.Target+%3D+%3F+AND+smry_propositions.Election+%3D+%3F+AND+contributions_search.BallotMeasureContribution+%3D+%27Y%27&d=a%3A2%3A%7Bi%3A0%3Bs%3A141%3A%22PROPOSITION+039+-+ESTABLISHES+ADDITIONAL+VOTER+IDENTIFICATION+AND+CITIZENSHIP+VERIFICATION+REQUIREMENTS.+INITIATIVE+CONSTITUTIONAL+AMENDMENT.%22%3Bi%3A1%3Bs%3A10%3A%222026-11-03%22%3B%7D&c=a%3A6%3A%7Bs%3A16%3A%2200Contributor%28s%29%22%3Bs%3A3%3A%22All%22%3Bs%3A19%3A%2201Contributor_State%22%3Bs%3A3%3A%22All%22%3Bs%3A14%3A%2202Recipient%28s%29%22%3Bs%3A157%3A%22Ballot+measure%3A+PROPOSITION+039+-+ESTABLISHES+ADDITIONAL+VOTER+IDENTIFICATION+AND+CITIZENSHIP+VERIFICATION+REQUIREMENTS.+INITIATIVE+CONSTITUTIONAL+AMENDMENT.%22%3Bs%3A31%3A%2207Contribution_Dates_and_Cycles%22%3Bs%3A3%3A%22All%22%3Bs%3A27%3A%2206Exclude_Allied_Committees%22%3Bs%3A2%3A%22No%22%3Bs%3A10%3A%2205Election%22%3Bs%3A10%3A%222026-11-03%22%3B%7D'
    _p = urllib.parse.urlparse(_urlstr)
    ## It's not very clear how to make sense of these query params.  I guess it makes sense to the PowerSearch back-end.
    ## Potentially, one could tweak one of the params and call urllib.parse.quote_plus().
    ## Note that the scheme is 's:3:"All";' means a string of len 3 with value "All" and 'a:6:{...}' is an array of 6 elements.
    urllib.parse.parse_qs(_p.query)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Retreive Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    PROPS_LIST = [1, 2, 3, 4, 5, 37, 38, 39, 40, 41, 42 , 43, 44, 45]
    dropdown = mo.ui.dropdown(
        options=PROPS_LIST, value=39, label="choose Prop"
    )
    dropdown
    return (dropdown,)


@app.cell
def _(dropdown, election, headers, make_url, pd):
    ## Data Retrieval
    USE_CACHE = False
    #prop_num = 39
    prop_num = dropdown.value

    if USE_CACHE:
        # Use a cached copy to speed up testing:
        url = 'powersearch-prop39-2026-08-09.csv'
        rawdata = pd.read_csv(url, skipfooter=9, engine='python')
    else:
        url = make_url(prop_num, election)
        rawdata = pd.read_csv(url, storage_options=headers)

    #rawdata = pd.read_csv(url, header=0)
    #rawdata = pd.read_csv(url, index_col=0)

    # drop any raw that is missing Cycle == 2025
    rawdata = rawdata.dropna(subset=['Cycle'])

    # Adjust to make IDs have integer values:
    rawdata[['Recipient Committee ID', 'Contributor ID']] = rawdata[['Recipient Committee ID', 'Contributor ID']].astype(pd.Int64Dtype())

    #rawdata.head() 
    rawdata.info()
    #rawdata.to_csv('powersearch-test-Oct30.csv')
    return (rawdata,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Basic Stats
    """)
    return


app._unparsable_cell(
    r"""
    print('Num Entries by Committee')
    _x = rawdata.groupby(['Ballot Measure(s)','Recipient Committee ID','Recipient Committee'])['Election'].count()
    _x.rename('Count'))

    """,
    name="_"
)


@app.cell
def _(rawdata, re):
    # separate support/oppose, group by contributor, sum amount
    pro_regex = re.compile(r'^SUPPORT', re.IGNORECASE)
    con_regex = re.compile(r'^OPPOSE', re.IGNORECASE)

    fields = ['Amount', 'Recipient Committee', 'Recipient Committee ID', 'Contributor Name', 'Contributor ID', 
              'Contributor City', 'Contributor State', 'Contributor Zip Code']

    s = rawdata['Ballot Measure(s)']
    pros = rawdata[s.map(lambda x: pro_regex.match(x) is not None)][fields]
    cons = rawdata[s.map(lambda x: con_regex.match(x) is not None)][fields]

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
    import jinja2

    rows = ['Total ($M)', 'Num Donations', 'Avg Donation ($)', 'Median Donation ($)']
    funs = [pd.Series.sum, pd.Series.count, pd.Series.mean, pd.Series.median]
    totals = pd.DataFrame({'PRO': [x(pros['Amount']) for x in funs], 
                            'CON': [x(cons['Amount']) for x in funs]}, index=rows)

    totals.loc['Total ($M)'] /= 1000000.0

    header_css = {'selector': 'th',
                  'props': 'padding: 10px;'}
    table_css = {'selector': 'td',
                 'props': 'border: 1px solid black; '
                          'padding: 5px 20px; text-align: right; font-size: 1.5em;'}

    totals.style.format(precision=2, thousands=',').format(lambda x: f'{int(x):,}',       subset=('Num Donations', totals.columns)).set_table_styles([header_css, table_css])

    return


@app.cell
def _(pros):
    print('Top PRO contributors')
    pros.groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum().nlargest(15)/1e6
    return


@app.cell
def _(cons):
    print('Top CON contributors')
    cons.groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum().nlargest(10)/1e6
    return


@app.cell
def _(cons, pd, pros):
    def _in_state(val):
        #val = df['Contributor State'][label]
        if val == 'CA':  
            return 'In-State'
        elif pd.isna(val):
            return '?'
        else:
            return 'Out-State'

    def _make_stats(df):
        total = df['Amount'].sum()
        stats = pd.DataFrame(
            df.groupby(df['Contributor State'].apply(_in_state))['Amount'].sum() )
        stats['Percentage'] = stats['Amount'] / total * 100
        stats['Amount'] /= 1e6
        return stats.rename(columns={'Amount': 'Amount ($M)'})

    _header_css = {'selector': 'th',
                  'props': 'padding: 10px;'}
    _table_css = {'selector': 'td',
                 'props': 'border: 1px solid black; '
                          'padding: 2px 20px; text-align: right; font-size: 1em;'}

    print('PRO:')
    #_make_stats(pros).style.format(precision=3).set_table_styles([_header_css, _table_css])
    print(_make_stats(pros).to_string(float_format=lambda x: f'{x:.3f}'))

    print()
    print('CON:')
    print(_make_stats(cons).to_string(float_format=lambda x: f'{x:.3f}'))
    return


@app.cell
def _(cons, pd, pros):
    # Have to remove 'Unitemized' since they're usually small donors
    p = pros[pros['Contributor Name'] != 'Unitemized Contributions'].groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum()
    c = cons[cons['Contributor Name'] != 'Unitemized Contributions'].groupby(['Contributor Name', 'Recipient Committee ID'])['Amount'].sum()

    # S = 0-100, M = 101-999, L = 1000+
    #bins = [0, 100, 999.99, 1000000000000.0]

    print('S = 0-500, M = 500-50k, L = 50k+')
    bins = [0, 500, 50000, 1000000000000.0]

    names = ['S', 'M', 'L']
    p_labels = pd.cut(p, bins, labels=names)
    c_labels = pd.cut(c, bins, labels=names)
    _totals = pd.DataFrame(
        {'PRO Num Donors': p.groupby(p_labels, observed=False).count(),
         'PRO Total ($M)': p.groupby(p_labels, observed=False).sum()/1e6, 
         'CON Num Donors': c.groupby(c_labels, observed=False).count(),
         'CON Total ($M)': c.groupby(c_labels, observed=False).sum()/1e6})

    # add back in the Unitemized (<$100) totals:
    _p_unitemized = pros[pros['Contributor Name'] == 'Unitemized Contributions']['Amount'].sum()
    _c_unitemized = cons[cons['Contributor Name'] == 'Unitemized Contributions']['Amount'].sum()
    _totals.at['S', 'PRO Total ($M)'] += _p_unitemized / 1e6
    _totals.at['S', 'CON Total ($M)'] += _c_unitemized / 1e6

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
    # All unitemized contribs PRO (i.e. < $100)
    pros[pros['Contributor Name'] == 'Unitemized Contributions'].nlargest(20, 'Amount')
    return


@app.cell
def _(cons):
    # All unitemized contribs CON (i.e. < $100)
    cons[cons['Contributor Name'] == 'Unitemized Contributions'].nlargest(10, 'Amount')
    return


@app.cell
def _(pros):
    # All recipient committees PRO
    pros.groupby('Recipient Committee ID')['Amount'].nunique().sort_values(ascending=False)
    return


@app.cell
def _(cons):
    # All recipient committees CON
    cons.groupby('Recipient Committee ID')['Amount'].nunique().sort_values(ascending=False)
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
    _id =  1485228
    cons[cons['Recipient Committee ID'] == _id].sort_values('Amount', ascending=False)
    return


@app.cell
def _(rawdata):
    rawdata[ (rawdata['Recipient Committee ID'] == 1484470) & (rawdata['Contributor Name'] == 'Unitemized Contributions') ].nlargest(20, 'Amount')
    return


@app.cell
def _(rawdata):
    rawdata[ (rawdata['Recipient Committee ID'] == 1489007) & (rawdata['Contributor Name'] == 'Unitemized Contributions') ].nlargest(20, 'Amount')
    return


if __name__ == "__main__":
    app.run()
