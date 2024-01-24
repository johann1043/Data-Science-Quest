
def data_frame_overview(data_frame):
    print(f'Column names: \n {data_frame.columns}\n')
    print(f'Dimensions: {data_frame.shape}\n')
    print(data_frame.info())
    return data_frame.head(10)


def format_column_names(data_frame, column_name_mapping = {}):
    '''
    Formats column names in a DataFrame based on a provided mapping.

    Parameters:
    data_frame: The DataFrame to format.
    column_mapping (dict): A dictionary containing old column names as keys and new names as values.

    Returns:
    None (modifies the DataFrame in place).
    '''
    # Perform additional formatting (lowercase, strip and replace spaces with underscores)
    data_frame.columns = [name.strip().replace(" ", "_").lower() for name in data_frame.columns]

    # Iterate through the provided column_name_mapping dictionary
    for old_name, new_name in column_name_mapping.items():
        # Check if the old column name exists in the DataFrame
        if old_name in data_frame.columns:
            # Rename the column with the new name
            data_frame.rename(columns={old_name: new_name}, inplace=True)
    print(f'New column names: \n {data_frame.columns}')


def null_check(data_frame):
    print(f'Total null values per row: \n{data_frame.isnull().sum(axis=1)}\n')
    print(f'Total null values per column: \n{data_frame.isnull().sum()}\n')


def dropna_rows_cols(data_frame, row_thresh, col_thresh):
    '''
    removes rows and columns with null values

    parameters:
    data_frame: data_frame from which to remove rows and columns
    row_thresh: minimum threshold for the number of non-null values that a row must have in order to be kept
    col_thresh: minimum threshold for the number of non-null values that a column must have in order to be kept

    returns:
    data frame in which the rows and columns containing null values have been removed
    '''
    rows_before = len(data_frame)
    cols_before = len(data_frame.columns)
    data_frame.dropna(thresh = row_thresh, inplace = True)
    data_frame.dropna(axis=1, thresh = col_thresh, inplace = True)
    rows_after = len(data_frame)
    cols_after = len(data_frame.columns)
    rows_deleted = rows_before - rows_after
    cols_deleted = cols_before - cols_after
    print(f'Deleted {rows_deleted} rows')
    print(f'Deleted {cols_deleted} columns')

    return data_frame


def dup_check(data_frame):
    print(f'Duplicates found: {data_frame.duplicated().any()}\n')
    print(f'Number of duplicates: {data_frame.duplicated().sum()}\n')

def drop_dup_reset(data_frame):
    rows_before = len(data_frame)
    data_frame.drop_duplicates(inplace=True)
    data_frame.reset_index(drop=True, inplace=True)
    rows_after = len(data_frame)
    num_dups_deleted = rows_before - rows_after
    print(f'Deleted {num_dups_deleted} duplicates')

    return data_frame

def clean_sex_column(data_frame):
    # Store the original 'sex' column for comparison
    original_sex_column = data_frame['sex'].copy()

    # Clean the 'sex' column
    data_frame['sex'] = data_frame['sex'].str.strip().str.lower()
    data_frame['sex'].replace({'male': 'm', 'female': 'f', 'femal': 'f'}, inplace=True)

    # Define a set of valid values
    valid_values = {'m', 'f'}

    # Replace invalid entries with NaN
    data_frame['sex'] = data_frame['sex'].apply(lambda x: x if x in valid_values else pd.NA)

    # Calculate the number of changed values
    changes = (original_sex_column.str.strip().str.lower() != data_frame['sex']).sum()
    print(f"Number of values changed in the 'sex' column: {changes}")
    print(data_frame['sex'].unique())

    return data_frame

def clean_countries_column(data_frame):
    original_country_column = data_frame['country'].copy()
    data_frame["country"] = data_frame["country"].str.upper().str.strip()
    data_frame["country"].unique()


    # Calculate the number of changed values
    changes = (original_country_column.str.strip().str.lower() != data_frame['country']).sum()
    print(f"Number of values changed in the 'country' column: {changes}")
    print(data_frame['country'].unique())

    return data_frame


def clean_fatality_column(data_frame):
    import numpy as np
    values_to_replace = ['M', 'F', 'n', 'Nq', 'UNKNOWN', 2017, 'Y x 2', ' N', 'N ', 'y']
    data_frame['fatal'] = data_frame['fatal'].replace(values_to_replace, np.nan)
    return data_frame

def clean_type_column(data_frame):
    import numpy as np
    values_to_replace = ["Questionable", "Unconfirmed", "Invalid", "nan", "?","Unverified", "Under investigation", "Watercraft", "Sea Disaster", "Boat"]
    data_frame['type'] = data_frame['type'].replace(values_to_replace, np.nan)

    return data_frame


def replace_strings_from_dict(df, column_name, replace_dict):
    """
    Replace entire strings in a DataFrame column based on multiple keywords, and print the number of changes for each.

    Parameters:
    df (pandas.DataFrame): The DataFrame to operate on.
    column_name (str): The name of the column to clean.
    replace_dict (dict): A dictionary where keys are keywords to search for, and values are the new values to replace the entire string with.

    Returns:
    pandas.DataFrame: The DataFrame with the modified column.
    """

    # Check if column exists in DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")

    for keyword, new_value in replace_dict.items():
        # Use str.contains() to find rows where the column contains the keyword
        mask = df[column_name].str.contains(keyword, case=False, na=False)

        # Count the number of values that will be changed
        num_changes = mask.sum()
        if num_changes > 0:
            print(f"Number of values changed for '{keyword}': {num_changes}")

            # Replace the entire string in these rows with the new value
            df.loc[mask, column_name] = new_value

    return df

def replace_values_with_nan(df, words_to_replace):
    for word in words_to_replace:
        df['species'] = df['species'].replace(to_replace=rf'.*{word}.*', value=np.nan, regex=True)

    return df

def replace_species(shark_attack_new):
    replacements = {
        'angel': 'Angel',
        'banjo': 'Banjo',
        'barracuda': 'Barracuda (not shark)',
        'basking': 'Basking',
        'black finned': 'Blackfin',
        'black-tipped': 'Black-tipped',
        'blackfin': 'Blackfin',
        'blacktip': 'Blacktip',
        'blind': 'Blind',
        'blined': 'Blind',
        'blue': 'Blue',
        'bonita': 'Bonita',
        'broadnose': 'Broadnose',
        'bronze whaler': 'Bronze whaler',
        'brown': 'Brown',
        'bu.ll': 'Bull',
        'bull': 'Bull',
        'captive': 'Captive',
        'carpet':'Carpet',
        'catshark': 'Scyliorhinus canicula',
        'cocktail': 'Cocktail',
        'cookiecutter': 'Cookiecutter',
        'copper': 'Copper',
        'cow': 'Cow',
        'dog shark': 'Dog shark',
        'dogfish': 'Scyliorhinus canicula',
        'dusky': 'Dusky',
        'epaulette': 'Epaulette',
        'gaffed': 'Gaffed',
        'galapagos': 'Galapagos',
        'gill': 'Gill',
        'goblin': 'Goblin',
        'gray nurse': 'Grey nurse',
        'gray shark': 'Grey colored',
        'grey colored': 'Grey colored',
        'grey-colored': 'Grey colored',
        'ground': 'Ground',
        'gummy': 'Gummy',
        'hammerhead': 'Hammerhead',
        'horn': 'Horn',
        'juvenile': 'Juvenile',
        'lemon': 'Lemon',
        'leopard': 'Leopard',
        'mako': 'Mako',
        'nurse': 'Nurse',
        'porbeagle': 'Porbeagle',
        'port jackson': 'Port jackson',
        'raggedtooth': 'Raggedtooth',
        'red': 'Red',
        'reef': 'Reef',
        'salmon': 'Salmon',
        'sand': 'Sand',
        'sandbar': 'Sandbar',
        'sevengill': 'Sevengill',
        'shovelnose': 'Shovelnose',
        'silky': 'Silky',
        'silvertip': 'Silvertip',
        'smooth hound': 'Smooth-hound',
        'smoothhound': 'Smooth-hound',
        'smooth-hound': 'Smooth-hound',
        'spear-eye': 'Spear-eye',
        'spinner': 'Spinner',
        'spotted dogfish': 'Spotted dogfish',
        'spurdog': 'Spurdog',
        'stingray': 'Stingray (not shark)',
        'tawney nurse': 'Tawney nurse',
        'thresher': 'Thresher',
        'tiger': 'Tiger',
        'tope': 'Tope',
        'wfite': 'White',
        'whaler': 'Whaler',
        'while shark': 'Whaler',
        'whiptail': 'Whiptail',
        'white': 'White',
        'wobbegong': 'Wobbegong',
        'zambesi': 'Zambezi',
        'zambezi': 'Zambezi',

    }

    shark_attack_new['species'] = shark_attack_new['species'].str.lower()

    for search_term, replacement in replacements.items():
        shark_attack_new.loc[shark_attack_new['species'].str.contains(search_term, case=False, na=False), 'species'] = replacement

    return shark_attack_new

#Define functions for the cleaned data
def fatality(data_frame):
    """Fatality"""
    fatal = data_frame['fatal'].value_counts().get('Y')
    no_fatal = data_frame['fatal'].value_counts().get('N')

    return (f"Count of 'fatal': {fatal}, Count of survivals: {no_fatal}")


def gender_risk(data_frame):
    females = data_frame['sex'].value_counts().get('f')
    males= data_frame['sex'].value_counts().get('m')
    print (f"Count of females attacked: {females}, Count of males atacked: {males}")
    return data_frame

