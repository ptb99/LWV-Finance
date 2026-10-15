import marimo

__generated_with = "0.24.0"
app = marimo.App(auto_download=["html"])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Calculation
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
      AND contributions_search.AlliedCommittee = 'N'
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Retreive Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    PROPS_LIST = [1, 2, 3, 4, 5, 37, 38, 39, 40, 41, 42 , 43, 44, 45]
    dropdown = mo.ui.dropdown(
        options=PROPS_LIST, value=39, label="##Choose Prop: "
    )
    dropdown
    return (dropdown,)


@app.cell
def _(dropdown, election, headers, make_url, pd):
    ## Data Retrieval
    USE_CACHE = False
    #prop_num = 39
    prop_num = dropdown.value

    ## Ensure that IDs are read/formatted as strings
    force_types = {
        "Recipient Committee ID": "str",
        "Contributor ID": "str",
    }

    if USE_CACHE:
        # Use a cached copy to speed up testing:
        url = 'powersearch-prop39-2026-08-09.csv'
        rawdata = pd.read_csv(url, skipfooter=9, engine='python', dtype=force_types)
    else:
        url = make_url(prop_num, election)
        rawdata = pd.read_csv(url, storage_options=headers, dtype=force_types)

    #rawdata = pd.read_csv(url, header=0)
    #rawdata = pd.read_csv(url, index_col=0)

    # drop any raw that is missing Cycle == 2025
    rawdata = rawdata.dropna(subset=['Cycle'])

    # shorten column name:
    rawdata.rename(columns={'Recipient Committee ID': 'Recipient ID'}, inplace=True)

    #rawdata.head() 
    rawdata.info()
    #rawdata.to_csv('powersearch-test-Oct30.csv')
    return prop_num, rawdata


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Basic Stats
    """)
    return


@app.cell
def _(mo, rawdata):
    print('Num Entries by Committee')
    _x = rawdata.groupby(['Ballot Measure(s)','Recipient ID','Recipient Committee'])['Election'].count()
    mo.plain(_x.rename('Count'))
    return


@app.cell
def _(prop_num, rawdata, re):
    # separate support/oppose, group by contributor, sum amount
    pro_regex = re.compile(rf'SUPPORTED:\s?PROPOSITION {prop_num:03d}', re.IGNORECASE)
    con_regex = re.compile(rf'OPPOSED:\s?PROPOSITION {prop_num:03d}', re.IGNORECASE)

    fields = ['Amount', 'Recipient Committee', 'Recipient ID',
              'Contributor Name', 'Contributor ID',
              'Contributor City', 'Contributor State', 'Contributor Zip Code']

    s = rawdata['Ballot Measure(s)']
    pros = rawdata[s.map(lambda x: pro_regex.search(x) is not None)][fields]
    cons = rawdata[s.map(lambda x: con_regex.search(x) is not None)][fields]

    cons.info()
    return cons, pros


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Results
    """)
    return


@app.cell
def _(cons, pd, pros):
    import jinja2

    _p = pros.groupby(['Recipient ID', 'Contributor Name'])['Amount'].sum()
    _c = cons.groupby(['Recipient ID', 'Contributor Name'])['Amount'].sum()

    rows = ['Total ($M)', 'Num Donors', 'Avg Donation ($)', 'Median Donation ($)']
    funs = [pd.Series.sum, pd.Series.count, pd.Series.mean, pd.Series.median]
    totals = pd.DataFrame({ 'PRO': [x(_p) for x in funs],
                            'CON': [x(_c) for x in funs]}, index=rows)

    totals.loc['Total ($M)'] /= 1000000.0

    header_css = {'selector': 'th',
                  'props': 'padding: 10px;'}
    table_css = {'selector': 'td',
                 'props': 'border: 1px solid black; '
                          'padding: 5px 20px; text-align: right; font-size: 1.5em;'}

    totals.style.format(
        precision=0, thousands=','
    ).format(
        lambda x: f'{int(x):,}',
        subset=('Num Donors', totals.columns)
    ).format(
        precision=6,
        subset=('Total ($M)', totals.columns)
    ).set_table_styles([header_css, table_css])

    ## Alternate idea:
    #mo.ui.dataframe(totals,
    #    format_mapping={
    #        "age": "{:d} years".format,
    #        "height_cm": format_height,
    #    },
    #)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Top PRO contributors
    """)
    return


@app.cell
def _(pros):
    print('Top PRO contributors')
    _df = pros.groupby(['Contributor Name', 'Recipient ID'])['Amount'].sum().nlargest(15)/1e6
    _df.head(10)
    #mo.plain(_df.head(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Top CON contributors
    """)
    return


@app.cell
def _(cons):
    print('Top CON contributors')
    _df = cons.groupby(['Contributor Name', 'Recipient ID'])['Amount'].sum().nlargest(10)/1e6
    _df.head(10)
    #mo.plain(_df.head(10))
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

    def _make_stats(df, tag):
        total = df['Amount'].sum()
        stats = pd.DataFrame(
            df.groupby(df['Contributor State'].apply(_in_state))['Amount'].sum() )
        stats[f'{tag} Percentage'] = stats['Amount'] / total * 100
        stats['Amount'] /= 1e6
        return stats.rename(columns={'Amount': f'{tag} Amount ($M)'})

    _header_css = {'selector': 'th',
                  'props': 'padding: 10px;'}
    _table_css = {'selector': 'td',
                 'props': 'border: 1px solid black; '
                          'padding: 2px 10px; text-align: right; font-size: 1em;'}

    _table = _make_stats(pros, 'PRO').join(_make_stats(cons, 'CON'), how='outer')
    _table.style.format(precision=6).set_table_styles([_header_css, _table_css])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ____

    ### [S = $0-500, M = $500-50k, L = $50k+]
    (Note: contributions < $100 do not need to be itemized and can be reported through a single entry labeled "Unitemized Contributions".  Hence, the number of "S" donors will not be accurate here, even though the "S" total dollars is accurate and includes those Unitemized Contributions.)
    """)
    return


@app.cell
def _(cons, mo, pd, pros):
    # Have to remove 'Unitemized' since they're usually small donors
    p = pros[pros['Contributor Name'] != 'Unitemized Contributions'].groupby(['Contributor Name', 'Recipient ID'])['Amount'].sum()
    c = cons[cons['Contributor Name'] != 'Unitemized Contributions'].groupby(['Contributor Name', 'Recipient ID'])['Amount'].sum()

    # S = 0-100, M = 101-999, L = 1000+
    #bins = [0, 100, 999.99, 1000000000000.0]

    # S = 0-500, M = 500-50k, L = 50k+
    bins = [0, 500, 50000, 1000000000000.0]

    names = ['S', 'M', 'L']
    p_labels = pd.cut(p, bins, labels=names)
    c_labels = pd.cut(c, bins, labels=names)
    _totals = pd.DataFrame(
        {'PRO Donors': p.groupby(p_labels, observed=False).count(),
         'PRO Total ($M)': p.groupby(p_labels, observed=False).sum()/1e6, 
         'CON Donors': c.groupby(c_labels, observed=False).count(),
         'CON Total ($M)': c.groupby(c_labels, observed=False).sum()/1e6})

    # add back in the Unitemized (<$100) totals:
    _p_unitemized = pros[pros['Contributor Name'] == 'Unitemized Contributions']['Amount'].sum()
    _c_unitemized = cons[cons['Contributor Name'] == 'Unitemized Contributions']['Amount'].sum()
    _totals.at['S', 'PRO Total ($M)'] += _p_unitemized / 1e6
    _totals.at['S', 'CON Total ($M)'] += _c_unitemized / 1e6

    mo.plain(_totals.sort_index(ascending=False).fillna(0))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Diagnostics
    """)
    return


@app.cell
def _():
    # All unitemized contribs PRO (i.e. < $100)
    #pros[pros['Contributor Name'] == 'Unitemized Contributions'].nlargest(20, 'Amount')
    return


@app.cell
def _():
    # All unitemized contribs CON (i.e. < $100)
    #cons[cons['Contributor Name'] == 'Unitemized Contributions'].nlargest(10, 'Amount')
    return


@app.cell
def _():
    # All recipient committees PRO
    #pros.groupby('Recipient ID')['Amount'].nunique().sort_values(ascending=False)
    return


@app.cell
def _():
    # All recipient committees CON
    #cons.groupby('Recipient ID')['Amount'].nunique().sort_values(ascending=False)
    return


@app.cell
def _():
    ## Find cases of committees giving to other committees
    #_temp = pros[(pros['Recipient ID'] > 0) & (pros['Contributor ID'] > 0)]
    #print(f"PRO donations from another committee: {_temp['Amount'].count()} for ${_temp['Amount'].sum() / 1000000.0:.2f}M")
    #_temp.nlargest(20, 'Amount')
    return


@app.cell
def _():
    #_comms = pros.groupby('Contributor ID')['Amount'].sum()
    #_comms
    return


@app.cell
def _():
    #_id = 1486767
    #_id = '1353866'
    #_id = 761010
    #_id = 1488414
    #pros[pros['Recipient ID'] == _id].sort_values('Amount', ascending=False)
    return


@app.cell
def _():
    #_id = 1488414
    #rawdata[ rawdata['Contributor ID'] == _id ]
    #rawdata[ rawdata['Recipient ID'] == _id ]
    return


@app.cell
def _(pd):
    def get_donors(df, id):
        return df[ df['Recipient ID'] == id ]

    def merge_donors(df):
        _comms = df.groupby('Contributor ID')['Amount'].sum()
        result = pd.concat( [get_donors(df, id) for id in _comms.index] )
        return result

    #merge_donors(pros)
    return


@app.cell
def _():
    ## Find cases of committees giving to other committees
    #_temp = cons[(cons['Recipient ID'] > 0) & (cons['Contributor ID'] > 0)]
    #print(f"CON donations from another committee: {_temp['Amount'].count()} for ${_temp['Amount'].sum() / 1000000.0:.2f}M")
    #_temp.nlargest(20, 'Amount')
    return


@app.cell
def _():
    #rawdata[ (rawdata['Recipient ID'] == '1484470') & (rawdata['Contributor Name'] == 'Unitemized Contributions') ].nlargest(20, 'Amount')
    return


@app.cell
def _():
    #rawdata[ (rawdata['Recipient ID'] == '1489007') & (rawdata['Contributor Name'] == 'Unitemized Contributions') ].nlargest(20, 'Amount')
    return


if __name__ == "__main__":
    app.run()
