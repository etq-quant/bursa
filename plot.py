cols = ['id','gics_sector_name', 'gics_industry_group_name', 'gics_industry_name', 'gics_sub_industry_name', 'company_common_name']

def get_table(df, glevel, sdate, edate):
    fdf = df.sort_values(['date','id']).reset_index(drop=True)
    sdf = fdf[(fdf['date']==sdate)|(fdf['date']==edate)]
    pdf = sdf.pivot_table(index=cols, columns=['date'], values=['company_market_cap']).reset_index().dropna()
    pdf.columns = [b if b else a for a,b in pdf.columns]
    adf = pdf.groupby(glevel)[[sdate, edate]].sum()
    adf['change'] = adf[edate] - adf[sdate]
    adf['change_pct'] = adf['change']/adf[sdate]*100

    return adf[['change_pct']].style.format("{:,.0f}").format("{:,.2f}%", subset=['change_pct'])\
            .bar(subset=(adf['change_pct']<0, 'change_pct'), color='#FF6347', align="zero")\
            .bar(subset=(adf['change_pct']>0, 'change_pct'), color="#54C571", align="zero")