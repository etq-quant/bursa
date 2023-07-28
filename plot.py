cols = ['id', 'sector','name', 'bics_level_1_sector_name',
       'bics_level_2_industry_group_name', 'bics_level_3_industry_name',
       'bics_level_4_sub_industry_name', 'gics_sector_name',
       'gics_industry_group_name', 'gics_industry_name',
       'gics_sub_industry_name']

def highlight_rows(x):
    if x.change_pct>0:
        return 'background-color: pink'
    else:
        return 'background-color: blue'

green = [{'selector': 'th', 'props': 'background-color: #98FB98; color: black'}]
white = [{'selector': 'th', 'props': 'background-color: white; color: black'}]
red = [{'selector': 'th', 'props': 'background-color: #FFA07A; color: black'}]

def highlight_col(x):
    #copy df to new - original data are not changed
    df = x.copy()
    #set by condition
    maskp = df['change'] > 0
    mask0 = df['change'] == 0
    maskn = df['change'] < 0
    df.loc[maskp, :] = 'background-color: #98FB98; color: black'
    df.loc[mask0, :] = 'background-color: white; color: black'
    df.loc[maskn, :] = 'background-color: #FFA07A; color: black'
    return df 

def get_table(df, glevel, sdate, edate):
    fdf = df.sort_values(['date','id']).reset_index(drop=True)
    sdf = fdf[(fdf['date']==sdate)|(fdf['date']==edate)]
    pdf = sdf.pivot_table(index=cols, columns=['date'], values=['cur_mkt_cap']).reset_index().dropna()
    pdf.columns = [b if b else a for a,b in pdf.columns]
    adf = pdf.groupby(glevel)[[sdate, edate]].sum()
    adf['change'] = adf[edate] - adf[sdate]
    adf['change_pct'] = adf['change']/adf[sdate]*100
    adf = adf[['change_pct']]
    return adf 

def style_table(adf):
    a={}
    for k,i in zip(adf.index, adf['change_pct']):
        if i>0:
            a[k]=green
        elif i<0:
            a[k]=red
        else:
            a[k]=white
    return adf.style.format("{:,.2f}%", subset=['change_pct'])\
    .bar(subset=['change_pct'], color=['#FF6347','#54C571'], align="zero")\
    .set_table_styles(a, axis=1)\
    .set_table_styles([{'selector': 'tr:hover', 'props': 'background-color: #D5D8DC; font-color: black'},
                      {'selector': 'th:hover', 'props': 'background-color: #D5D8DC; font-color: black'}], overwrite=False)

def get_table_raw(df, glevel, sdate, edate):
    fdf = df.sort_values(['date','id']).reset_index(drop=True)
    sdf = fdf[(fdf['date']==sdate)|(fdf['date']==edate)]
    pdf = sdf.pivot_table(index=cols, columns=['date'], values=['cur_mkt_cap']).reset_index().dropna()
    pdf.columns = [b if b else a for a,b in pdf.columns]
    adf = pdf.groupby(glevel)[[sdate, edate]].sum()
    adf['change'] = adf[edate] - adf[sdate]
    adf['change_pct'] = adf['change']/adf[sdate]*100
    return adf

def style_raw_table(adf, sdate, edate):
    a={}
    for k,i in zip(adf.index, adf['change_pct']):
        if i>0:
            a[k]=green
        elif i<0:
            a[k]=red
        else:
            a[k]=white
    
    return adf.style.format("{:,.0f}", subset=[sdate, edate,'change']).format("{:,.2f}%", subset=['change_pct'])\
    .background_gradient(cmap='YlOrRd_r', axis=0)\
    .bar(subset=['change_pct'], color=['#FF6347','#54C571'], align="zero")\
    .apply(highlight_col, subset=[i for i in adf.columns if i!='change_pct'], axis=None)\
    .set_table_styles(a, axis=1)\
    .set_table_styles([{'selector': 'tr:hover', 'props': 'background-color: #D5D8DC; font-color: black'},
                      {'selector': 'th:hover', 'props': 'background-color: #D5D8DC; font-color: black'}], overwrite=False)
