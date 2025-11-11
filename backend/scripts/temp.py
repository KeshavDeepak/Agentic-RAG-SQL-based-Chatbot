import sqlite3

conn = sqlite3.connect("backend/data/adventureworks.sqlite")
cursor = conn.cursor()

cursor.execute('''
    SELECT 
    c."CustomerID",
    p."FirstName" || ' ' || p."LastName" AS CustomerName,
    ea."EmailAddress",
    SUM(soh."TotalDue") AS TotalOrderAmount,
    sp."FirstName" || ' ' || sp."LastName" AS SalesPerson,
    st."Name" AS Territory
FROM "Sales.Customer" AS c
LEFT JOIN "Person.Person" AS p
    ON c."PersonID" = p."BusinessEntityID"
LEFT JOIN "Person.EmailAddress" AS ea
    ON p."BusinessEntityID" = ea."BusinessEntityID"
JOIN "Sales.SalesOrderHeader" AS soh
    ON c."CustomerID" = soh."CustomerID"
LEFT JOIN "Sales.SalesPerson" AS sps
    ON soh."SalesPersonID" = sps."BusinessEntityID"
LEFT JOIN "Person.Person" AS sp
    ON sps."BusinessEntityID" = sp."BusinessEntityID"
LEFT JOIN "Sales.SalesTerritory" AS st
    ON soh."TerritoryID" = st."TerritoryID"
GROUP BY 
    c."CustomerID", p."FirstName", p."LastName", ea."EmailAddress", sp."FirstName", sp."LastName", st."Name"
ORDER BY 
    TotalOrderAmount DESC;

''')
# print(cursor.fetchall())

cursor.execute('''
pragma foreign_key_list('Person.Person');
               ''')
print(cursor.fetchall())

# cursor.execute('''
#                PRAGMA table_info("Sales.SalesOrderHeader");
#                ''')
# print(cursor.fetchall())

# cursor.execute('''
#                PRAGMA table_info("Sales.SalesPerson");
#                ''')
# print(cursor.fetchall())

# cursor.execute('''
#                PRAGMA table_info("Person.Person");
#                ''') 
# print(cursor.fetchall())

conn.close()