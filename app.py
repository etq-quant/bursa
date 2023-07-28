import streamlit as st
import pandas as pd
from plot import get_table, get_table_raw, style_table, style_raw_table

#def bursa_malaysia():
DAILY_DATA_PATH = "data/daily_data.csv"
META_DATA_PATH = "data/meta_data.csv"

st.set_page_config(
    page_title="Bursa Malaysia", layout="wide",
)
st.title("Bursa Malaysia | Market Capitalization")
st.sidebar.title("Bursa Malaysia")

#@st.cache(allow_output_mutation=True)
def load_data():
    df1 = pd.read_csv(DAILY_DATA_PATH)
    df2 = pd.read_csv(META_DATA_PATH)
    df = df1.merge(df2, on=['id'])
    return df

df = load_data()
df['date'] = pd.to_datetime(df['date']).dt.date

glevel = st.multiselect(
    "Group level", ['sector','name', 'bics_level_1_sector_name',
       'bics_level_2_industry_group_name', 'bics_level_3_industry_name',
       'bics_level_4_sub_industry_name', 'gics_sector_name',
       'gics_industry_group_name', 'gics_industry_name',
       'gics_sub_industry_name'], default="sector"
)

col1, col2 = st.columns(2)
udates = sorted(df['date'].unique())
start_date = col1.date_input('Start date', udates[-5], min_value=udates[0], max_value=udates[-2])
end_date = col2.date_input('End date', udates[-1], min_value=udates[1], max_value=udates[-1])


tdf = get_table(df, glevel, start_date, end_date)
stdf = style_table(tdf)
tdfr = get_table_raw(df, glevel, start_date, end_date)
stdfr = style_raw_table(tdfr, start_date, end_date)
tab1, tab2, = st.tabs(["summary", "raw"])
with tab1:
    st.table(stdf)
    st.download_button(
"Press to Download",
tdf.to_csv(),
"bursa_market_cap_{}_{}.csv".format(start_date, end_date),
"text/csv",
key='download-csv'
)
with tab2:
    st.dataframe(stdfr)
    st.download_button(
"Press to Download",
tdfr.to_csv(),
"bursa_market_cap_raw_{}_{}.csv".format(start_date, end_date),
"text/csv",
key='download-raw-csv'
)