def clean_data(df):
    # Drop unnecessary columns
    df = df.drop(['Unnamed: 0'], axis=1, errors='ignore')

    # Fill nulls (example: fill rating with median)
    if 'overall' in df.columns:
        df['overall'] = df['overall'].fillna(df['overall'].median())

    # Normalize a numerical column (example: 'pace')
    if 'pace' in df.columns:
        max_pace = df['pace'].max()
        df['pace_normalized'] = df['pace'] / max_pace

    # One-hot encode position (example: 'position')
    if 'position' in df.columns:
        df = dd.get_dummies(df, columns=['position'])

    return df
