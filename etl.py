import pandas as pd

# Rimuovo le colonne inutili
accident_df = pd.read_csv('Accident_Information.csv', low_memory=False) \
    .drop(columns=['InScotland', 'Police_Force', 'LSOA_of_Accident_Location',
                   'Location_Easting_OSGR', 'Location_Northing_OSGR'])
vehicle_df = pd.read_csv('Vehicle_Information.csv', encoding="ISO-8859-1") \
    .drop(columns=['Vehicle_Location.Restricted_Lane', 'Vehicle_Reference'])

# Prendo una data ogni 100
# accident_df = pd.read_csv('accident_etl.csv')
# accident_df = pd.read_csv('accident_etl_100.csv', low_memory=False)
# vehicle_df = pd.read_csv('vehicle_etl.csv', encoding="ISO-8859-1")

accident_df['Date'] = pd.to_datetime(accident_df['Date'])
accident_df.sort_values(by='Date', inplace=True)
accident_df = accident_df.iloc[::10, :]

# Rimuovo gli incidenti di cui non si hanno informazioni sui veicoli
incidents_in_veichle_df = vehicle_df[['Accident_Index']].drop_duplicates(subset='Accident_Index')
accident_df = pd.merge(accident_df, incidents_in_veichle_df, on='Accident_Index', how='inner')
# accident_df = accident_df.drop_duplicates(subset='Accident_Index', keep=False)
accident_df.to_csv('accident_etl_10.csv', index=False)

# Rimuovo i veicoli non legati ad un incidente nel primo dataset
vehicle_df = pd.merge(accident_df[['Accident_Index']], vehicle_df, on='Accident_Index', how='inner')
vehicle_df.to_csv('vehicle_etl_10.csv', index=False)
