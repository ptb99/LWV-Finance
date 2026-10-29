import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Calculation

    Download the .zip file of all 2026 transactions on the top-level Home page at https://netfile.com/public/SCC/campaign and unzip it to extract an efile_SCC_2026.xlsx file.
    """)
    return


@app.cell
def _():
    ## Standard Boilerplate

    #import re
    #import io
    import requests
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib

    #pd.show_versions()
    print('Pandas = ', pd.__version__)
    print('Numpy = ', np.__version__)
    print('Matplotlib = ', matplotlib.__version__)
    return mo, pd, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Divider
    """)
    return


@app.cell
def _():
    ## Global settings (across multiple calls)
    baseurl = 'https://netfile.com/Connect2/api/public/campaign'
    headers = {"Accept": "application/json"}
    local_agency = 51   # 51 = Santa Clara County
    #election = "2026-11-03"

    # For now, skip 406D == 5
    contrib_types = (0, 1, 2, 4, 20)
    expense_types = (6, 7, 9, 11, 21)

    pro_cmte = 'SCC-114447'
    con_cmte = 'SCC-114539'

    # Need mo equivalent of this:
    #pd.set_option('display.float_format', '{:.1f}'.format)
    return (
        baseurl,
        con_cmte,
        contrib_types,
        expense_types,
        headers,
        local_agency,
        pro_cmte,
    )


@app.cell
def _(baseurl, headers, pd, requests):
    _url = baseurl+'/list/transaction/types'
    _r = requests.get(_url, headers=headers)
    _data = _r.json()
    types = pd.DataFrame(_data['items'])
    trans_mapping = dict(zip(types['id'], types['abbreviation']))
    types
    return (trans_mapping,)


@app.cell
def _(baseurl, headers, local_agency, pd, requests, trans_mapping):
    def get_transactions(keyword, agency, transType=None):
        url = baseurl + '/search/transaction/query'
        params = {'QueryString': keyword,
                  'Agency': str(agency),
                  'DateStart': '2025-1-1',
                  'ShowSuperceded': 'false',
                  'SortOrder': 'AmountDescending',
                  'PageSize': '100',
                  'CurrentPageIndex': '0'
                 }
        # if transType supplied, add it to the query filter
        if transType:
            params['TransactionType'] = str(transType)

        r = requests.get(url, params=params, headers=headers)
        data = r.json()
        max_page = data['totalMatchingPages']
        df = [ pd.DataFrame(data['results']) ]
        for i in range(max_page):
            if i > 0:
                params['CurrentPageIndex'] = str(i)
                r = requests.get(url, params=params, headers=headers)
                data = r.json()
                df.append( pd.DataFrame(data['results']) )

        return pd.concat(df)

    rawdata = get_transactions('transit', local_agency)
    rawdata['transactionForm'] = rawdata['transactionType'].map(trans_mapping)
    #rawdata.info()
    rawdata.head(20)
    return (rawdata,)


@app.cell
def _(rawdata):
    #_elections = df_sheets['497'].groupby('Elect_Date', dropna=False)['Elect_Date'].size()
    #_elections
    #mo.plain(_elections)#mo.plain(df_sheets['497']['Elect_Date'].value_counts(dropna=False))

    #rawdata['filerFppcId'].value_counts()
    rawdata['transactionForm'].value_counts()
    return


@app.cell
def _(contrib_types, expense_types, rawdata):
    contribs = rawdata[ rawdata['transactionType'].map(lambda x: x in contrib_types) ].drop_duplicates(subset='id')
    expenses = rawdata[ rawdata['transactionType'].map(lambda x: x in expense_types) ].drop_duplicates(subset='id')
    #contribs.info()
    expenses.info()
    return contribs, expenses


@app.cell
def _(contribs):
    #rawdata['transactionType'].value_counts()
    #rawdata[ rawdata['code']== '' ]['transactionForm'].value_counts()
    contribs['code'].value_counts(dropna=False)
    return


@app.cell
def _(expenses):
    expenses['code'].value_counts(dropna=False)
    return


@app.cell
def _():
    #contribs['filingId'].value_counts(dropna=False)
    #contribs['id'].value_counts(dropna=False)
    #expenses['id'].value_counts()
    return


@app.cell
def _(contribs):
    contribs[ contribs['id'] == 'd2cd3cc6-c1e6-40ef-84c1-b4f10181d0e8' ]
    return


@app.cell
def _(contribs):
    #contribs['filerFppcId'].value_counts(dropna=False)
    #contribs['filerName'].value_counts(dropna=False)
    contribs.groupby(['filerFppcId', 'filerLocalId', 'filerName'], dropna=False)['amount'].count()
    return


@app.cell
def _(con_cmte, contribs, pro_cmte):
    pro_df = contribs[ contribs['filerLocalId'] == pro_cmte ]
    con_df = contribs[ contribs['filerLocalId'] == con_cmte ]
    pro_df
    return con_df, pro_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Divider
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### PRO Contributors
    """)
    return


@app.cell
def _(pro_df):
    _donors = pro_df.groupby(['filerFppcId', 'name'], dropna=False)['amount'].sum()
    #donors = pro_df.groupby(['Entity_Cd', 'Cmte_ID', 'Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt2'].max()

    _donors.nlargest(20)
    #mo.plain(donors.nlargest(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### CON Contributors
    """)
    return


@app.cell
def _(con_df):
    _donors = con_df.groupby(['filerFppcId', 'name'], dropna=False)['amount'].sum()

    _donors.nlargest(10)
    #mo.plain(donors.nlargest(10))
    return


@app.cell
def _(con_df, pd, pro_df):
    _p = pro_df.groupby('name', dropna=False)['amount'].sum()
    _c = con_df.groupby('name', dropna=False)['amount'].sum()

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
    return


@app.cell
def _():
    # Check for unitemized entries:
    #_mask = (pro_df['name'] == 'Unitemized Contributions') | (pro_df['name'] == 'Unitemized')
    #pro_df[_mask]
    #_mask.sum()
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
def _(con_df, mo, pd, pro_df):
    p = pro_df.groupby('name', dropna=False)['amount'].sum()
    c = con_df.groupby('name', dropna=False)['amount'].sum()

    _pro_sum = p.sum()
    _con_sum = c.sum()

    # S = 0-500, M = 500-50k, L = 50k+
    bins = [0, 500, 50000, 1000000000000.0]

    names = ['S', 'M', 'L']
    p_labels = pd.cut(p, bins, labels=names)
    c_labels = pd.cut(c, bins, labels=names)
    _totals = pd.DataFrame(
        {'PRO Donors': p.groupby(p_labels, observed=False).count(),
         'PRO Total ($M)': p.groupby(p_labels, observed=False).sum()/1e6,
         'PRO Percentage (%)': p.groupby(p_labels, observed=False).sum()/_pro_sum*100, 
         'CON Donors': c.groupby(c_labels, observed=False).count(),
         'CON Total ($M)': c.groupby(c_labels, observed=False).sum()/1e6,
         'CON Percentage (%)': c.groupby(c_labels, observed=False).sum()/_con_sum*100})

    mo.plain(_totals.sort_index(ascending=False).fillna(0))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### In-State Analysis
    """)
    return


@app.cell
def _(con_df, pd, pro_df):
    def _in_state(val):
        #val = df['Contributor State'][label]
        if val == 'CA':  
            return 'In-State'
        elif pd.isna(val):
            return '?'
        else:
            return 'Out-State'

    def _make_stats(df, tag):
        total = df['amount'].sum()
        stats = pd.DataFrame(
            df.groupby(df['state'].apply(_in_state))['amount'].sum() )
        stats[f'{tag} Percentage'] = stats['amount'] / total * 100
        stats['amount'] /= 1e6
        return stats.rename(columns={'amount': f'{tag} Amount ($M)'})

    _header_css = {'selector': 'th',
                  'props': 'padding: 10px;'}
    _table_css = {'selector': 'td',
                 'props': 'border: 1px solid black; '
                          'padding: 2px 10px; text-align: right; font-size: 1em;'}

    _table = _make_stats(pro_df, 'PRO').join(_make_stats(con_df, 'CON'), how='outer').fillna(0)
    _table.style.format(precision=6).set_table_styles([_header_css, _table_css])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Expenses vs. Conrributions
    """)
    return


@app.cell
def _(con_cmte, con_df, expenses, pro_cmte, pro_df):
    pro_exp = expenses[ expenses['filerLocalId'] == pro_cmte ]
    con_exp = expenses[ expenses['filerLocalId'] == con_cmte ]

    print(f'PRO: contribs {pro_df["amount"].sum()/1e6:.3f}, expenses {pro_exp["amount"].sum()/1e6:.3f}')
    print(f'CON: contribs {con_df["amount"].sum()/1e6:.3f}, expenses {con_exp["amount"].sum()/1e6:.3f}')
    return con_exp, pro_exp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### PRO Top Expenses
    """)
    return


@app.cell
def _(pro_exp):
    _spending = pro_exp.groupby(['filerFppcId', 'name', 'code'], dropna=False)['amount'].sum()
    _spending.nlargest(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### CON Top Expenses
    """)
    return


@app.cell
def _(con_exp):
    _spending = con_exp.groupby(['filerFppcId', 'name', 'code'], dropna=False)['amount'].sum()
    _spending.nlargest(10)
    return


if __name__ == "__main__":
    app.run()
