import pandas as pd
import world_bank_data as wb

gdp_pp_kd = wb.get_series('NY.GDP.PCAP.PP.KD', mrv=1)

gdp_pp_kd.to_frame()

gdp_pp_kd.to_csv('../extras/gdp_countries.csv')


