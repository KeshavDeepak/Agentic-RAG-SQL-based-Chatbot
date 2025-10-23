import sqlite3
from pathlib import Path

# -------------------------------
# Paths
# -------------------------------
sqlite_path = Path("backend/data/adventureworks.sqlite")
csv_folder = Path("backend/data/adventureworks_csv_files")

# -------------------------------
# CSV → Table mapping
# -------------------------------
csv_to_table = {
    "AWBuildVersion": "dbo.AWBuildVersion",
    "Department": "HumanResources.Department",
    "Employee": "HumanResources.Employee",
    "EmployeeDepartmentHistory": "HumanResources.EmployeeDepartmentHistory",
    "EmployeePayHistory": "HumanResources.EmployeePayHistory",
    "JobCandidate": "HumanResources.JobCandidate",
    "Shift": "HumanResources.Shift",
    "Address": "Person.Address",
    "AddressType": "Person.AddressType",
    "BusinessEntity": "Person.BusinessEntity",
    "BusinessEntityAddress": "Person.BusinessEntityAddress",
    "BusinessEntityContact": "Person.BusinessEntityContact",
    "ContactType": "Person.ContactType",
    "CountryRegion": "Person.CountryRegion",
    "EmailAddress": "Person.EmailAddress",
    "Password": "Person.Password",
    "Person": "Person.Person",
    "PersonPhone": "Person.PersonPhone",
    "PhoneNumberType": "Person.PhoneNumberType",
    "StateProvince": "Person.StateProvince",
    "BillOfMaterials": "Production.BillOfMaterials",
    "Culture": "Production.Culture",
    "Document": "Production.Document",
    "Illustration": "Production.Illustration",
    "Location": "Production.Location",
    "Product": "Production.Product",
    "ProductCategory": "Production.ProductCategory",
    "ProductCostHistory": "Production.ProductCostHistory",
    "ProductDescription": "Production.ProductDescription",
    "ProductDocument": "Production.ProductDocument",
    "ProductInventory": "Production.ProductInventory",
    "ProductListPriceHistory": "Production.ProductListPriceHistory",
    "ProductModel": "Production.ProductModel",
    "ProductModelIllustration": "Production.ProductModelIllustration",
    "ProductModelProductDescriptionCulture": "Production.ProductModelProductDescriptionCulture",
    "ProductPhoto": "Production.ProductPhoto",
    "ProductProductPhoto": "Production.ProductProductPhoto",
    "ProductReview": "Production.ProductReview",
    "ProductSubcategory": "Production.ProductSubcategory",
    "ScrapReason": "Production.ScrapReason",
    "TransactionHistory": "Production.TransactionHistory",
    "TransactionHistoryArchive": "Production.TransactionHistoryArchive",
    "UnitMeasure": "Production.UnitMeasure",
    "WorkOrder": "Production.WorkOrder",
    "WorkOrderRouting": "Production.WorkOrderRouting",
    "ProductVendor": "Purchasing.ProductVendor",
    "PurchaseOrderDetail": "Purchasing.PurchaseOrderDetail",
    "PurchaseOrderHeader": "Purchasing.PurchaseOrderHeader",
    "ShipMethod": "Purchasing.ShipMethod",
    "Vendor": "Purchasing.Vendor",
    "CountryRegionCurrency": "Sales.CountryRegionCurrency",
    "CreditCard": "Sales.CreditCard",
    "Currency": "Sales.Currency",
    "CurrencyRate": "Sales.CurrencyRate",
    "Customer": "Sales.Customer",
    "PersonCreditCard": "Sales.PersonCreditCard",
    "SalesOrderDetail": "Sales.SalesOrderDetail",
    "SalesOrderHeader": "Sales.SalesOrderHeader",
    "SalesOrderHeaderSalesReason": "Sales.SalesOrderHeaderSalesReason",
    "SalesPerson": "Sales.SalesPerson",
    "SalesPersonQuotaHistory": "Sales.SalesPersonQuotaHistory",
    "SalesReason": "Sales.SalesReason",
    "SalesTaxRate": "Sales.SalesTaxRate",
    "SalesTerritory": "Sales.SalesTerritory",
    "SalesTerritoryHistory": "Sales.SalesTerritoryHistory",
    "ShoppingCartItem": "Sales.ShoppingCartItem",
    "SpecialOffer": "Sales.SpecialOffer",
    "SpecialOfferProduct": "Sales.SpecialOfferProduct",
    "Store": "Sales.Store",
}

# -------------------------------
# Per-file delimiters
# -------------------------------
delim_map = {
    # Most AdventureWorks CSVs
    "Person": "|",
    "Address": "|",
    "AddressType": "|",
    "BusinessEntity": "|",
    "BusinessEntityAddress": "|",
    "BusinessEntityContact": "|",
    "ContactType": "|",
    "CountryRegion": "|",
    "Docuemnt": "|",
    "EmailAddress": "|",
    "Illustration": "|",
    "JobCandidate": "|",
    "Password": "|",
    "PersonPhone": "|",
    "PhoneNumberType": "|",
    "StateProvince": "|",
    "Store": "|",
    "ProductModel": "|",
    "ProductModelorg": "|",
    "ProductPhoto": "|",
    # Default to tab if not listed
}

# -------------------------------
# Connect to SQLite
# -------------------------------
conn = sqlite3.connect(sqlite_path)
cursor = conn.cursor()

# -------------------------------
# Helper: Open CSV safely with encoding detection
# -------------------------------
def open_csv_safe(csv_file):
    import chardet
    raw = open(csv_file, 'rb').read(4096)
    result = chardet.detect(raw)
    encoding = result['encoding'] or 'utf-8'
    return open(csv_file, newline='', encoding=encoding, errors='replace')

# -------------------------------
# Import CSVs
# -------------------------------
for csv_file in csv_folder.glob("*.csv"):
    csv_name = csv_file.stem
    table_name = csv_to_table.get(csv_name)
    
    if not table_name:
        print(f"Skipping {csv_file.name}: No mapping found")
        continue

    print(f"\nProcessing CSV: {csv_file.name} → Table: {table_name}")

    # Truncate table
    cursor.execute(f'DELETE FROM "{table_name}"')

    # Get columns from SQLite
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    columns = [row[1] for row in cursor.fetchall()]
    if not columns:
        print(f"Skipping {table_name}: No columns found")
        continue

    # Determine delimiter
    delimiter = delim_map.get(csv_name, '\t')

    batch_size = 1000
    rows_batch = []

    with open_csv_safe(csv_file) as f:
        for line in f:
            line = line.rstrip('\n\r')

            # Remove BOM and trailing +/ &
            line = line.lstrip('\ufeff').strip('+&')

            # Split manually using the correct delimiter
            row = [cell.strip().strip('+&') if cell else None for cell in line.split(delimiter)]

            # Pad or trim to match table columns
            row = (row + [None]*len(columns))[:len(columns)]
            rows_batch.append(tuple(row))

            # Batch insert
            if len(rows_batch) >= batch_size:
                placeholders = ",".join("?" * len(columns))
                quoted_columns = [f'"{c}"' for c in columns]
                sql = f'INSERT INTO "{table_name}" ({",".join(quoted_columns)}) VALUES ({placeholders})'
                cursor.executemany(sql, rows_batch)
                rows_batch.clear()

        # Insert remaining rows
        if rows_batch:
            placeholders = ",".join("?" * len(columns))
            quoted_columns = [f'"{c}"' for c in columns]
            sql = f'INSERT INTO "{table_name}" ({",".join(quoted_columns)}) VALUES ({placeholders})'
            cursor.executemany(sql, rows_batch)

    print(f"Inserted rows into {table_name}")

# -------------------------------
# Commit and close
# -------------------------------
conn.commit()
conn.close()
print("\nAll CSVs imported successfully!")
