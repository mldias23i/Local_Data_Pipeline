import pytest
import pandas as pd
from kaggle import cleaning_world_data, cleaning_global_terrorism, cleaning_merged_data

@pytest.fixture
def sample_world_data():
    """Creates a small dataframe to test transformations of world_data"""
    data = {
        'Country': ['USA', 'Germany'],
        'Agricultural Land( %)': ['40%', '50%'],
        'Land Area(Km2)': ['9,147,593', '357,022'],
        'Capital/Major City': [None, 'Berlin'],
        'Gasoline Price': [None, '1.45'],
        'GDP': ['21,000,000,000,000', '4,200,000,000,000']
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_global_terrorism():
    """Creates a small dataframe to test transformations of global_terrorism"""
    data = {
        'eventid': [1, 2],
        'iyear': [2020, 2019],
        'imonth': [5, 0],
        'iday': [14, 0],
        'country': [100, 200],
        'country_txt': ['East Germany (GDR)', 'Germany'],
        'region': [1, 2],
        'region_txt': ['North America', 'Europe'],
        'city': ['New York', 'Berlin'],
        'latitude': [40.7128, 52.5200],
        'longitude': [-74.0060, 13.4050],
        'success': [1, 0],
        'attacktype1': [3, 2],
        'attacktype1_txt': ['Bombing/Explosion', 'Armed Assault'],
        'target1': ['Building', 'Military Base'],
        'nkill': [10, None],
        'nwound': [5, None],
        'property': [None, None],
        'weaptype1': [5, 6],
        'weaptype1_txt': ['Explosives', 'Firearms']
    }
    return pd.DataFrame(data)

def test_cleaning_world_data(sample_world_data):
    cleaned = cleaning_world_data(sample_world_data)

    # Check if percentage column was converted correctly
    assert cleaned['Agricultural Land( %)'].dtype == float
    assert cleaned['Agricultural Land( %)'].iloc[0] == 0.40
    assert cleaned['Agricultural Land( %)'].iloc[1] == 0.50

    # Check if values with ',' were converted correctly
    assert cleaned['Land Area(Km2)'].dtype == float
    assert cleaned['Land Area(Km2)'].iloc[0] == 9147593
    assert cleaned['Land Area(Km2)'].iloc[1] == 357022


    assert cleaned['Capital/Major City'].iloc[0] == 'Unknown'

def test_cleaning_global_terrorism(sample_global_terrorism):
    cleaned = cleaning_global_terrorism(sample_global_terrorism)

    # Check if columns with more than 90% of NaN were removed
    assert 'property' not in cleaned.columns  

    # Check substitution of names of countries
    assert (cleaned['country_txt'] == 'Germany').sum() == 2 

def test_cleaning_merged_data(sample_global_terrorism, sample_world_data):
    merged = pd.merge(sample_global_terrorism, sample_world_data, left_on='country_txt', right_on='Country', how='left')
    cleaned = cleaning_merged_data(merged)

    # Check if column date was created correctly
    assert 'Date' in cleaned.columns
    assert cleaned['Date'].iloc[0] == '14-05-2020'  

    # Check if columns were renamed correctly
    expected_columns = ['Event_Id', 'Country_Id', 'Country', 'Region_Id', 'Region', 'City', 'lat', 'lon']
    assert all(col in cleaned.columns for col in expected_columns)

    # Check if negative values were converted to positive
    assert not pd.isna(cleaned['Damaged_Properties'].iloc[0]) and cleaned['Damaged_Properties'].iloc[0] >= 0

