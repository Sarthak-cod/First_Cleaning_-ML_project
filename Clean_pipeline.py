import sqlite3
import pandas as pd

def process_and_clean_data(csv_path: str, db_path: str, output_path: str) -> None:

    df = pd.read_csv(csv_path, on_bad_lines='skip')                       # Load raw data  and skip broken lines containing  extra comma delimiters

    conn = sqlite3.connect(db_path)                                         # Create a connection to the SQLite database

    df.to_sql('books_table', conn, if_exists='replace', index=False)              # Write the DataFrame to the SQLite database

    # Define an Sql query statement to filter and sort target records from the database
    
    query = """SELECT bookID,title, authors, average_rating, publication_date, language_code
               FROM books_table
               WHERE language_code IN ('eng', 'en-US', 'en-GB')
                AND average_rating >= 0 
               ORDER BY average_rating DESC;
               """

    extracted_df = pd.read_sql_query(query, conn)                         # Execute the SQL query and store the result in a new DataFrame
    conn.close()                                                                 # Close the database connection

    extracted_df['publication_date'] = pd.to_datetime(extracted_df['publication_date'], errors='coerce')    # Convert publication_date to datetime format, coercing errors to NaT
    extracted_df['title'] = extracted_df['title'].str.strip()                                 # Strip leading and trailing whites
    extracted_df['primary_author'] = extracted_df['authors'].str.split('/').str[0]              # Extract the primary author from the authors column by splitting on '/' and taking the first element

    extracted_df.to_csv(output_path, index=False)                                         # Write the cleaned DataFrame to a CSV file without the index column
    print("pipeline completed successfully.")

if __name__ == "__main__":                                                                 # Run the data processing and cleaning pipeline when the script is executed directly
    process_and_clean_data(                                            
        csv_path="books.csv",
        db_path="books.db",
        output_path="cleaned_books.csv")