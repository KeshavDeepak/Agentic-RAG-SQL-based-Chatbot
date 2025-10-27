import sqlite3
from pathlib import Path
import csv
import chardet
import re

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
    "Person": "|",
    "Address": "|",
    "AddressType": "|",
    "BusinessEntity": "|",
    "BusinessEntityAddress": "|",
    "BusinessEntityContact": "|",
    "ContactType": "|",
    "CountryRegion": "|",
    "Document": "|",
    "EmailAddress": "|",
    "Illustration": "|",
    "JobCandidate": "|",
    "Password": "|",
    "PersonPhone": "|",
    "PhoneNumberType": "|",
    "StateProvince": "|",
    "Store": "|",
}

# -------------------------------
# Connect to SQLite
# -------------------------------
conn = sqlite3.connect(sqlite_path)
cursor = conn.cursor()

# -------------------------------
# Drop unwanted tables
# -------------------------------
tables_to_drop = ["dbo.DatabaseLog", "dbo.ErrorLog"]

for table in tables_to_drop:
    cursor.execute(f'DROP TABLE IF EXISTS "{table}"')
    print(f"🗑️ Dropped table: {table}")

# -------------------------------
# Helpers
# -------------------------------
def open_csv_safely(path):
    raw = open(path, "rb").read(4096)
    enc = chardet.detect(raw)["encoding"] or "utf-8"
    return open(path, encoding=enc, newline="", errors="replace")

def infer_type(value):
    if value is None or value == "":
        return None
    value = value.strip()
    if re.fullmatch(r"-?\d+", value):
        return "INTEGER"
    if re.fullmatch(r"-?\d+\.\d+", value):
        return "REAL"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return "DATE"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", value):
        return "DATETIME"
    return "TEXT"

def merge_types(type_list):
    # Prioritize TEXT > REAL > INTEGER > DATE > DATETIME
    if "TEXT" in type_list:
        return "TEXT"
    if "REAL" in type_list:
        return "REAL"
    if "INTEGER" in type_list:
        return "INTEGER"
    if "DATETIME" in type_list:
        return "DATETIME"
    if "DATE" in type_list:
        return "DATE"
    return "TEXT"

# -------------------------------
# Import CSVs
# -------------------------------
for csv_file in csv_folder.glob("*.csv"):
    csv_name = csv_file.stem
    table_name = csv_to_table.get(csv_name)

    if not table_name:
        print(f"⚠️ Skipping {csv_file.name}: No mapping found.")
        continue

    print(f"\n📦 Processing {csv_file.name} → {table_name}")

    # Get existing columns (from schema)
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    cols = [r[1] for r in cursor.fetchall()]
    if not cols:
        print(f"⚠️ Skipping {table_name}: no columns found in schema.")
        continue

    delimiter = delim_map.get(csv_name, "\t")

    # Collect samples for type inference
    type_samples = [[] for _ in cols]
    sample_limit = 500

    with open_csv_safely(csv_file) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if not row:
                continue
            row = (row + [None]*len(cols))[:len(cols)]
            for j, val in enumerate(row):
                t = infer_type(val)
                if t:
                    type_samples[j].append(t)
            if i > sample_limit:
                break

    inferred_types = [merge_types(tlist) if tlist else "TEXT" for tlist in type_samples]

    # Recreate table
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    col_defs = ", ".join([f'"{c}" {t}' for c, t in zip(cols, inferred_types)])
    cursor.execute(f'CREATE TABLE "{table_name}" ({col_defs})')
    print(f"🧩 Created table {table_name} with inferred schema ({len(cols)} columns).")

    # Insert data
    placeholders = ",".join(["?"] * len(cols))
    quoted_cols = ",".join([f'"{c}"' for c in cols])
    sql = f'INSERT INTO "{table_name}" ({quoted_cols}) VALUES ({placeholders})'

    batch, batch_size = [], 1000
    with open_csv_safely(csv_file) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            row = (row + [None]*len(cols))[:len(cols)]
            batch.append(tuple(row))
            if len(batch) >= batch_size:
                cursor.executemany(sql, batch)
                batch.clear()
        if batch:
            cursor.executemany(sql, batch)

    print(f"✅ Inserted rows into {table_name}")

# -------------------------------
# Commit and close
# -------------------------------
conn.commit()
conn.close()
print("\n🎯 All CSVs imported successfully with inferred types and cleaned DB!")
