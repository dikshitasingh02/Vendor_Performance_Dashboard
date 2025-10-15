import pandas as pd
import sqlite3
import logging

# ---------------------------------------
# Setup Logging
# ---------------------------------------
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


# ---------------------------------------
# Function to Ingest DataFrame into SQLite
# ---------------------------------------
def ingest_db(df, table_name, conn, chunksize=5000):
    '''Ingests the dataframe into a database table.'''
    try:
        df.to_sql(
            table_name,
            con=conn,
            if_exists='replace',
            index=False,
            chunksize=chunksize
        )
        logging.info(f" Successfully inserted '{table_name}' in chunks.")
    except Exception as e:
        logging.error(f" Error while inserting '{table_name}': {e}")
        print(f"Error while inserting '{table_name}': {e}")


# ---------------------------------------
# Function to Create Vendor Summary
# ---------------------------------------
def create_vendor_summary(conn):
    '''Merges multiple tables to create an overall vendor summary.'''
    query = """
    WITH FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(Freight) AS TotalFreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    
    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,  
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),
    
    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )
    
    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.TotalFreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """

    try:
        df = pd.read_sql_query(query, conn)
        logging.info(" Vendor summary created successfully.")
        return df
    except Exception as e:
        logging.error(f" Error creating vendor summary: {e}")
        raise


# ---------------------------------------
# Function to Clean Data
# ---------------------------------------
def clean_data(df):
    '''Cleans and adds calculated columns.'''
    try:
        df['Volume'] = df['Volume'].astype('float64', errors='ignore')
        df.fillna(0, inplace=True)
        df['VendorName'] = df['VendorName'].astype(str).str.strip()

        # Derived columns
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        df['ProfitMargin'] = (
            (df['GrossProfit'] / df['TotalSalesDollars']) * 100
        ).replace([float('inf'), -float('inf')], 0)
        df['StockTurnOver'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
        df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

        logging.info(" Data cleaned successfully.")
        return df

    except Exception as e:
        logging.error(f" Error cleaning data: {e}")
        raise


# ---------------------------------------
# Main Execution
# ---------------------------------------
if __name__ == '__main__':
    try:
        conn = sqlite3.connect('inventory.db')

        logging.info(' Creating Vendor Summary Table...')
        summary_df = create_vendor_summary(conn)
        logging.info(f"Sample Summary Data:\n{summary_df.head()}")

        logging.info(' Cleaning Data...')
        clean_df = clean_data(summary_df)
        logging.info(f"Sample Clean Data:\n{clean_df.head()}")

        logging.info(' Ingesting Clean Data into Database...')
        ingest_db(clean_df, 'vendor_sales_summary', conn)
        logging.info(' Completed Successfully!')

        conn.close()
    except Exception as e:
        logging.error(f" Script failed: {e}")
        print(f"Script failed: {e}")
