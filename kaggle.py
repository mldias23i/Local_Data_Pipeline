import pandas as pd

#Convert percentage columns to decimal values
def convert_percentage(value):
    if isinstance(value, str) and "%" in value:
        return float(value.strip("%")) / 100
    return value

#Convert numeric columns with commas to float values
def convert_numeric(value):
    if isinstance(value, str):
        value = value.replace(",", "").strip()
        if value.replace(".", "", 1).isdigit():
            return float(value)
    return value

#Drop columns with percentage of NaN values bigger than 90%
def drop_columns_with_high_nan(data, threshold=0.9):
    # Percentage of NaN on each column
    nan_percentage = data.isna().mean()
    
    # Columns with percentage higher than 0.9
    columns_to_drop = nan_percentage[nan_percentage > threshold].index
    
    # Drop those columns
    data = data.drop(columns=columns_to_drop)
    
    return data

# Fuction to do some transformations and cleaning to the dataset world-data-2023
def cleaning_world_data(world_data):
    world_data.drop_duplicates()   
    #Filling some NaN values with 'Unkown' or 0 
    world_data.fillna({'Capital/Major City': 'Unknown', 'Gasoline Price': 'Unknown'}, inplace=True)
    #Converting percentage values to decimal
    world_data = world_data.map(convert_percentage)
    world_data.fillna({'Agricultural Land( %)': 0, 'Land Area(Km2)': 0}, inplace=True)
    #Converting values with ',' to floats
    world_data = world_data.map(convert_numeric)
    # Drop columns with percentage of NaNs bigger than 90%
    world_data = drop_columns_with_high_nan(world_data)

    return world_data

# Fuction to do some transformations and cleaning to the dataset globalterrorism
def cleaning_global_terrorism(global_terrorism):
    global_terrorism = global_terrorism.drop_duplicates()
    # Drop columns with percentage of NaNs bigger than 90%
    global_terrorism = drop_columns_with_high_nan(global_terrorism)
    # Replacing different sides of germany, in the country context, by the name of the country but
    # maintaining the id of each side
    global_terrorism['country_txt'] = global_terrorism['country_txt'].replace('East Germany (GDR)', 'Germany')
    global_terrorism['country_txt'] = global_terrorism['country_txt'].replace('West Germany (FRG)', 'Germany')

    return global_terrorism

# Replacing three columns of day, month and year by one column containing the date
def create_date(row):
    if (row['imonth'] == 0 and row['iday'] == 0) or (row['imonth'] > 12 and row['iday'] > 31) or (row['imonth'] == 0 and row['iday'] != 0):
        return str(row['iyear'])
    elif row['imonth'] != 0 and row['iday'] == 0: 
        return f"{row['imonth']:02d}-{row['iyear']}"
    else:
        return f"{row['iday']:02d}-{row['imonth']:02d}-{row['iyear']}"
  

# Fuction to do some transformations and cleaning to the merged dataset
def cleaning_merged_data(global_terrorism_with_world_data):
    global_terrorism_with_world_data = global_terrorism_with_world_data.drop(columns='Country')
    #Adding new column date
    global_terrorism_with_world_data['Date'] = global_terrorism_with_world_data.apply(create_date, axis=1)
    global_terrorism_with_world_data = global_terrorism_with_world_data.drop(columns=['iyear', 'imonth', 'iday'])

    #Renaming columns
    global_terrorism_with_world_data = global_terrorism_with_world_data.rename(columns={
        'eventid': 'Event_Id',
        'country': 'Country_Id',
        'country_txt': 'Country',
        'region': 'Region_Id',
        'region_txt': 'Region',
        'city': 'City',
        'latitude': 'lat',
        'longitude': 'lon',
        'success': 'Success',
        'attacktype1': 'Attack_Id',
        'attacktype1_txt': 'Attack_Type',
        'target1': 'Target',
        'nkill': 'Number_of_Kills',
        'nwound': 'Number_of_Wounds',
        'property': 'Damaged_Properties',
        'weaptype1': 'Weaptype_Id',
        'weaptype1_txt': 'Weaptype',
        'Agricultural Land( %)': 'Agricultural_Land(Ratio)',
        'Land Area(Km2)': 'Land_Area(Km2)',
        'Armed Forces size': 'Number_Armed_Forces',
        'Capital/Major City': 'Capital_or_MajorCity',
        'Gasoline Price': 'Gasoline_Price',
        'GDP': 'Gross_Domestic_Product',
        'Life expectancy': 'Life_Expectancy'
    })

    #Changing the location of column Date in the dataframe
    date_column = global_terrorism_with_world_data.pop("Date")
    global_terrorism_with_world_data.insert(1, "Date", date_column)

    #Replacing negative values to postive ones to be more explicit in the context of the column
    global_terrorism_with_world_data["Damaged_Properties"] = global_terrorism_with_world_data["Damaged_Properties"].fillna(0).abs()

    global_terrorism_with_world_data[["Number_of_Kills", "Number_of_Wounds", "Target"]] = global_terrorism_with_world_data[["Number_of_Kills", "Number_of_Wounds", "Target"]].fillna("Unknown")

    return global_terrorism_with_world_data


#Try-catch exceptions to get data and if it is not possible throw an error
try:
    global_terrorism = pd.read_csv('globalterrorism.csv', encoding="ISO-8859-1", low_memory=False)
except Exception as e:
    print('Error loading data:', e)
try:
    world_data = pd.read_csv('world-data-2023.csv')
except Exception as e:
    print('Error loading data:', e)

# Specific column of world_data
world_data = world_data[[
    'Country', 'Agricultural Land( %)', 'Land Area(Km2)', 'Armed Forces size',
    'Capital/Major City', 'Gasoline Price', 'GDP', 'Life expectancy', 
    'Population'
]]

# Specific column of global_terrorism
global_terrorism = global_terrorism[[
    'eventid', 'iyear', 'imonth', 'iday', 'country', 'country_txt', 
    'region', 'region_txt', 'city', 'latitude', 'longitude', 'success', 'attacktype1', 
    'attacktype1_txt', 'target1', 'nkill', 'nwound', 'property', 
    'weaptype1', 'weaptype1_txt'
]]


world_data = cleaning_world_data(world_data)

global_terrorism = cleaning_global_terrorism(global_terrorism)

global_terrorism_with_world_data = pd.merge(global_terrorism, world_data, left_on='country_txt', right_on='Country', how='left')
global_terrorism_with_world_data = cleaning_merged_data(global_terrorism_with_world_data)
global_terrorism_with_world_data.to_csv('global_terrorism_world_data.csv', index=False)






