# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "4e081237-3e52-41ae-8a03-1c9e0f13f7c6",
# META       "default_lakehouse_name": "LH_LF",
# META       "default_lakehouse_workspace_id": "6443336d-2e57-4f8f-acbf-3c1fe1869bb4"
# META     }
# META   }
# META }

# CELL ********************

# Import necessary libraries
import os
from bs4 import BeautifulSoup
import pandas as pd
import re
import glob

# Define the base directory containing your HTML files
base_directory_path = '/lakehouse/default/Files/exchange_rates/'

# Get a list of all HTML files in the base directory and its subdirectories
html_files = glob.glob(os.path.join(base_directory_path, '**', '*.html'), recursive=True)

# Print the list of HTML files for debugging
print("HTML files found:")
print(html_files)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Function to process each HTML file
def process_html_file(file_path):
    # Extract the date from the file name using regex
    date_match = re.search(r'exchange_rates_(\d{4})(\d{2})(\d{2})\.html', file_path)
    if date_match:
        year, month, day = date_match.groups()
        date_str = f'{year}-{month}-{day}'
        date_formatted = pd.to_datetime(date_str).strftime('%m-%d-%Y')
    else:
        raise ValueError("Date not found in file name")

    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the required data (example)
    data = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        data.append([col.text.strip() for col in cols])

    # Find the maximum number of columns
    max_cols = max(len(row) for row in data)

    # Pad rows with fewer columns with empty strings
    data = [row + [''] * (max_cols - len(row)) for row in data]

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Filter out rows where all elements are empty strings
    df = df[~df.apply(lambda row: all(cell == '' for cell in row), axis=1)]

    # Insert the date column at the beginning
    df.insert(0, 'Date', date_formatted)

    # Print DataFrame content for debugging
    print(f"DataFrame for {file_path}:")

    # Define the output path for the Parquet file
    output_path = f'/lakehouse/default/Files/exchange_rates/{year}/{month}/{day}/exchange_rates_{date_str}_parsed.parquet'

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Print output path for debugging

    # Save the DataFrame to a Parquet file
    df.to_parquet(output_path, index=False)

    # Verify file creation
    if os.path.exists(output_path):
        print(f"Parquet file successfully saved: {output_path}")
    else:
        print(f"Failed to save Parquet file: {output_path}")

# Process each HTML file in the directory
for html_file in html_files:
    process_html_file(html_file)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
