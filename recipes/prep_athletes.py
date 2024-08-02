import pandas as pd
import json
import requests

source = "https://olympics.com/OG2024/data/MIS_Athletes~comp=OG2024~lang=ENG~functionCategory=A.json"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
}

data_json = requests.get(source, headers=headers)

# +
# data_json.json()['persons']

# +
base = (
    pd
    .DataFrame.from_records(data_json.json()['persons'])
    .assign(
        country_code = lambda df: df.organisation.apply(lambda x: x['code']),
        country_name = lambda df: df.organisation.apply(lambda x: x['description']),
        country_name_long = lambda df: df.organisation.apply(lambda x: x['longDescription']),
        gender = lambda df: df.personGender.apply(lambda x: x['code'])
    )
    [[
        'code',
        'name',
        'birthDate',
        'height',
        'gender',
        'country_code',
        'country_name',
        'country_name_long',
    ]]
    .set_index('code')
)

base
# -



base.to_csv('../datasets/athletes.csv')

# +
athletes_countries = (
    base
    .groupby('country_name_long')
    .agg(
        name =  ('name', 'count'),
        m    =  ('gender', lambda x: (x == "M").sum()),
        f    =  ('gender', lambda x: (x == "F").sum()),
    )
)

athletes_countries
# -

athletes_countries.to_csv('../datasets/athletes_countries.csv')

# +
athletes_disciplines = (
    pd
    .DataFrame.from_records(data_json.json()['persons'])
    .assign(
        disciplines = lambda x: x.disciplines.apply(lambda y: [ z['description'] for z in y] )
    )
    .set_index('code')
    [['disciplines']]
    #.reset_index()
    .explode('disciplines')
)

athletes_disciplines
# -

athletes_disciplines.disciplines.value_counts()

athletes_disciplines.to_csv('../datasets/athletes_disciplines.csv')

# +
athletes_events = (
    pd
    .DataFrame.from_records(data_json.json()['persons'])
    .assign(
        events = lambda x: x.registeredEvents.apply(lambda y: [ z['event']['description'] for z in y] )
    )
    .set_index('code')
    [['events']]
    #.reset_index()
    .explode('events')
)

athletes_events
# -

athletes_events.to_csv('../datasets/athletes_events.csv')
