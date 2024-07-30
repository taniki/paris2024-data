import pandas as pd
import world_bank_data as wb

gdp_pp_kd = wb.get_series('NY.GDP.PCAP.PP.KD', mrv=1)

# https://pypi.org/project/world-bank-data/

codes = wb.get_series('NY.GDP.PCAP.PP.KD', mrv=1, id_or_value='id')

codes

gdp_pp_kd.to_frame()

# +
df = (
    gdp_pp_kd
    .to_frame()
    .reset_index()
    .rename(
        {
            'NY.GDP.PCAP.PP.KD': 'gdp_capita',
            'Country': 'country'
            
        },
        axis = 1
    )
    [['country', 'gdp_capita']]
    .assign(
            gdp_capita_quantile = lambda df: pd.qcut(df.gdp_capita,6).cat.codes
    )
)

df
# -

gdp_pp_kd.to_csv('../extras/gdp_countries.csv')

df.gdp_capita_quantile.value_counts()

(
    df
    .query('~gdp_capita.isna()')
    .to_csv('../extras/gdp_countries.quantiles.csv')
)


