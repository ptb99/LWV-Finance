import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Calculation

    Download the .zip file of all 2026 transactions on the top-level Home page at https://netfile.com/public/SCC/campaign and unzip it to extract an efile_SCC_2026.xlsx file.
    """)
    return


@app.cell(hide_code=True)
def _():
    ## Standard Boilerplate

    #import re
    import io
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib

    #pd.show_versions()
    print('Pandas = ', pd.__version__)
    print('Numpy = ', np.__version__)
    print('Matplotlib = ', matplotlib.__version__)
    return io, mo, pd


@app.cell
def _(mo):
    file_select = mo.ui.file(kind='button', multiple=False, filetypes=['.xlsx', '.xls'])
    mo.vstack([file_select])
    return (file_select,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Divider
    """)
    return


@app.cell
def _(file_select, io, pd):
    # currently, SCC Netfile page doesn't support automated retreival, so export manually
    source = None
    if file_select.value:
        source = io.BytesIO(file_select.contents())

    # Use a cached copy to speed up testing:
    #source = 'efile_SCC_2026.xlsx'
    #source = 'efile_newest_SCC_2026.xlsx'

    ## Need to ensure all Filer_ID and Cmte_ID fields are converted to int!!
    force_types = {
        "Filer_ID": "string",
        "Cmte_ID": "string",

    }

    # skip all but the tabs we care about:
    tabs =  ["A-Contributions", "497"]

    # read all tabs:
    #tabs=None

    if source:
        df_sheets = pd.read_excel(source, sheet_name=tabs, dtype=force_types)
        for i in df_sheets.keys():
            print(i)
    else:
        print('No file loaded')
    return (df_sheets,)


@app.cell
def _(df_sheets, mo):
    #df_sheets['497']['Elect_Date'].unique()
    _elections = df_sheets['497'].groupby('Elect_Date', dropna=False)['Elect_Date'].size()
    mo.plain(_elections)
    # can use:
    #mo.plain(df_sheets['497']['Elect_Date'].value_counts(dropna=False))
    return


@app.cell
def _(df_sheets):
    _df = df_sheets['497']
    _subset = _df[_df['Elect_Date'] == '2026-11-03']
    #_subset = _df[ _df['Elect_Date'].isna() ]
    #subset.info()
    _subset
    return


@app.cell
def _(df_sheets, pd):
    _df = df_sheets['497']
    _subset = _df[ (_df['Committee_Type'] == 'BMC') & (_df['Rpt_Date'] > pd.Timestamp('2026/6/30')) ]
    #_subset

    # Prob don't need to dedup, but this gets the columns to line up
    late_contribs = _subset.groupby(['Filer_ID', 'Tran_ID'], as_index=False).first()
    late_contribs.rename(columns={'Enty_NamL':'Tran_NamL',
                                  'Enty_NamF': 'Tran_NamF',
                                  'Enty_NamT': 'Tran_NamT',
                                  'Enty_NamS': 'Tran_NamS',
                                  'Enty_Adr1': 'Tran_Adr1',
                                  'Enty_Adr2': 'Tran_Adr2',
                                  'Enty_City': 'Tran_City',
                                  'Enty_ST': 'Tran_State',
                                  'Enty_Zip4': 'Tran_Zip4',
                                  'Ctrib_Date': 'Tran_Date',
                                  'Ctrib_Emp': 'Tran_Emp',
                                  'Ctrib_Occ': 'Tran_Occ',
                                  'Ctrib_Self': 'Tran_Self',
                                  'Amount': 'Tran_Amt1',
                                 }, inplace=True)
    print(f"DEDUP took {_subset['Entity_Cd'].count():d} entries -> {late_contribs['Entity_Cd'].count():d} entries")
    #late_contribs
    return (late_contribs,)


@app.cell
def _(df_sheets):
    # First, we need to dedup by Tran_ID
    # (the spreadsheet seems to be reverse-chron, so take the first of each dupl)
    _df = df_sheets['A-Contributions']
    quarterly_contribs = _df.groupby(['Filer_ID', 'Tran_ID'], as_index=False).first()
    print(f"DEDUP took {_df['Entity_Cd'].count():d} entries -> {quarterly_contribs['Entity_Cd'].count():d} entries")

    #_df.info()
    quarterly_contribs.info()
    return (quarterly_contribs,)


@app.cell
def _(late_contribs, pd, quarterly_contribs):
    # combine late-contrib F497 data with dedup-ed F460 A-contribs
    contribs = pd.concat([quarterly_contribs, late_contribs])
    contribs.info()
    #contribs
    return (contribs,)


@app.cell
def _(contribs, mo):
    _temp = contribs.groupby('Committee_Type')['Committee_Type'].count()
    mo.plain(_temp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Divider
    """)
    return


@app.cell
def _(contribs):
    props = contribs[ contribs['Committee_Type'] == 'BMC' ]
    #props.head()
    _df = props.groupby(['Filer_ID', 'Filer_NamL'])['Filer_NamL'].count()
    _df.nlargest(10)
    return


@app.cell
def _(contribs):
    pro_id = '1483907'
    #pro_id = '1415769'
    con_id = '1492758'

    pro_df = contribs[ contribs['Filer_ID'] == pro_id ]
    con_df = contribs[ contribs['Filer_ID'] == con_id ]

    #pro_df.info()
    pro_df
    #pro_df['Tran_Amt1'].nlargest(10)
    #con_df.tail()
    return con_df, pro_df


@app.cell
def _(mo, pro_df):
    #_field = 'Rec_Type'
    _field = 'Entity_Cd'
    #_temp = contribs.groupby(_field)[_field].count()
    _temp = pro_df.groupby(_field)[_field].count()
    mo.plain(_temp)
    return


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
    _donors = pro_df.groupby(['Entity_Cd', 'Cmte_ID', 'Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt1'].sum()
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
    _donors = con_df.groupby(['Entity_Cd', 'Cmte_ID', 'Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt1'].sum()
    #donors = pro_df.groupby(['Entity_Cd', 'Cmte_ID', 'Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt2'].max()

    _donors.nlargest(10)
    #mo.plain(donors.nlargest(10))
    return


@app.cell
def _(con_df, pd, pro_df):
    _p = pro_df.groupby(['Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt1'].sum()
    _c = con_df.groupby(['Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt1'].sum()
    #_c = cons.groupby(['Recipient ID', 'Contributor Name'])['Amount'].sum()

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
def _(pro_df):
    # Check for unitemized entries:
    _mask = (pro_df['Tran_NamL'] == 'Unitemized Contributions') | (pro_df['Tran_NamF'] == 'Unitemized')
    pro_df[_mask]
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
    p = pro_df.groupby(['Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt1'].sum()
    c = con_df.groupby(['Tran_NamL', 'Tran_NamF'], dropna=False)['Tran_Amt1'].sum()

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
        total = df['Tran_Amt1'].sum()
        stats = pd.DataFrame(
            df.groupby(df['Tran_State'].apply(_in_state))['Tran_Amt1'].sum() )
        stats[f'{tag} Percentage'] = stats['Tran_Amt1'] / total * 100
        stats['Tran_Amt1'] /= 1e6
        return stats.rename(columns={'Tran_Amt1': f'{tag} Amount ($M)'})

    _header_css = {'selector': 'th',
                  'props': 'padding: 10px;'}
    _table_css = {'selector': 'td',
                 'props': 'border: 1px solid black; '
                          'padding: 2px 10px; text-align: right; font-size: 1em;'}

    _table = _make_stats(pro_df, 'PRO').join(_make_stats(con_df, 'CON'), how='outer').fillna(0)
    _table.style.format(precision=6).set_table_styles([_header_css, _table_css])
    return


if __name__ == "__main__":
    app.run()
