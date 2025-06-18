import os
import pandas as pd
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(filepath):
    try:
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith(('.xlsx', '.xls')):
            return pd.read_excel(filepath)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        print(f"Error processing file: {e}")
        return pd.DataFrame()

def clean_data(df):
    cleaned_df = df.drop_duplicates()
    
    for column in cleaned_df.select_dtypes(include=['number']).columns:
        cleaned_df[column].fillna(cleaned_df[column].median(), inplace=True)
    
    return cleaned_df

def generate_stats(df):
    if df.empty:
        return {"error": "Dataframe is empty"}
    
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        return {"error": "No numeric columns found"}
    
    stats = {
        "mean": numeric_df.mean().to_dict(),
        "median": numeric_df.median().to_dict(),
        "correlation": numeric_df.corr().fillna(0).to_dict()
    }
    return stats

def generate_plot(df, column, plot_folder):
    if df.empty:
        raise ValueError("Dataframe is empty")
    
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in dataframe")
    
    plt.figure(figsize=(10, 6))
    
    if pd.api.types.is_numeric_dtype(df[column]):
        df[column].hist()
        plt.title(f'Histogram of {column}')
    else:
        df[column].value_counts().plot(kind='bar')
        plt.title(f'Bar chart of {column}')
    
    plt.xlabel(column)
    plt.ylabel('Frequency')
    
    plot_filename = f"plot_{secure_filename(column)}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.png"
    plot_path = os.path.join(plot_folder, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path