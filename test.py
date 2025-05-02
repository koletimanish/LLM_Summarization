import pandas as pd

# Read the CSV files
raw_acquisition_data = pd.read_csv('data/raw/acquisitions.csv')
raw_funding_data = pd.read_csv('data/raw/funding_rounds.csv')
raw_investments_data = pd.read_csv('data/raw/investments.csv')
raw_ipos_data = pd.read_csv('data/raw/ipos.csv')
raw_objects_data = pd.read_csv('data/raw/objects.csv')

# Create name lookup dictionaries from objects data
id_to_name = dict(zip(raw_objects_data['id'], raw_objects_data['name']))

# Select and rename columns from acquisitions data
acquisitions_selected_columns = raw_acquisition_data[['acquiring_object_id', 'acquired_object_id', 'price_amount', 'source_url']]
acquisitions_selected_columns = acquisitions_selected_columns.rename(columns={'source_url': 'acquisition_source_url'})

# Add names for acquiring and acquired objects
acquisitions_selected_columns['acquiring_object_name'] = acquisitions_selected_columns['acquiring_object_id'].map(id_to_name)
acquisitions_selected_columns['acquired_object_name'] = acquisitions_selected_columns['acquired_object_id'].map(id_to_name)

# Select and rename columns from funding rounds data
funding_selected_columns = raw_funding_data[['object_id', 'funding_round_type', 'funding_round_code', 'raised_amount', 'source_url']]
funding_selected_columns = funding_selected_columns.rename(columns={'source_url': 'funding_source_url'})

# Select columns from investments data
investments_selected_columns = raw_investments_data[['funded_object_id', 'investor_object_id']].copy()
investments_selected_columns['investment_source_url'] = "https://www.kaggle.com/datasets/justinas/startup-investments?resource=download&select=investments.csv"

objects_selected_columns = raw_objects_data[['id', 'name', 'permalink', 'category_code']]

# Start with acquisitions data and merge with funding data (using acquiring_object_id)
merged_data = pd.merge(
    acquisitions_selected_columns,
    funding_selected_columns,
    left_on='acquiring_object_id',
    right_on='object_id',
    how='left'
)

# Merge with investments data (using acquired_object_id)
merged_data = pd.merge(
    merged_data,
    investments_selected_columns,
    left_on='acquired_object_id',
    right_on='funded_object_id',
    how='left'
)

# Merge with objects data for acquiring company
merged_data = pd.merge(
    merged_data,
    objects_selected_columns,
    left_on='acquiring_object_id',
    right_on='id',
    how='left',
    suffixes=('', '_acquiring')
)

# Merge with objects data for acquired company
merged_data = pd.merge(
    merged_data,
    objects_selected_columns,
    left_on='acquired_object_id',
    right_on='id',
    how='left',
    suffixes=('', '_acquired')
)

# Remove duplicates based on all columns
merged_data = merged_data.drop_duplicates()

# Drop the redundant columns
merged_data = merged_data.drop(['id', 'id_acquired', 'object_id', 'funded_object_id'], axis=1, errors='ignore')

print("\nShape of final dataframe:", merged_data.shape)
print("Number of unique acquired_object_ids:", merged_data['acquired_object_id'].nunique())

# Keep only the first row for each acquired_object_id
print("\nRemoving duplicate acquired_object_ids...")
merged_data = merged_data.groupby('acquired_object_id').first().reset_index()
print("New shape of dataframe:", merged_data.shape)
print("Number of unique acquired_object_ids:", merged_data['acquired_object_id'].nunique())

merged_data.to_csv("data/processed/startup_data.csv", index=False)
