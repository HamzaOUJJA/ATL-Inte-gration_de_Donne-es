import atoti as tt
import pandas as pd

# Créer une session Atoti
session = tt.Session.start()

# Chargement des données
print("Chargement des fichiers de données...")
dim_city = pd.read_csv("DimCity.csv")
dim_customer = pd.read_csv("DimCustomer.csv")
dim_date = pd.read_csv("DimDate.csv")
dim_stock_item = pd.read_csv("DimStockItem.csv")
fact_sale = pd.read_csv("FactSale.csv")
dim_employee = pd.read_excel("DimEmployee.xlsx")

# Création des tables Atoti
city_store = session.read_pandas(dim_city, keys=["CityID"], table_name="DimCity")
customer_store = session.read_pandas(dim_customer, keys=["CustomerID"], table_name="DimCustomer")
date_store = session.read_pandas(dim_date, keys=["DateID"], table_name="DimDate")
stock_item_store = session.read_pandas(dim_stock_item, keys=["StockItemID"], table_name="DimStockItem")
sales_store = session.read_pandas(fact_sale, keys=["SaleID"], table_name="FactSale")
employee_store = session.read_pandas(dim_employee, keys=["EmployeeID"], table_name="DimEmployee")

# Création du cube
cube = session.create_cube(sales_store, "Sales Cube")

# Définition des hiérarchies
dimensions = {
    "City": city_store["CityName"],
    "Customer": customer_store["CustomerName"],
    "Date": date_store["FullDate"],
    "Stock Item": stock_item_store["StockItemName"],
    "Employee": employee_store["EmployeeName"]
}

for dim_name, column in dimensions.items():
    cube.hierarchies[dim_name] = [column]

# Définition des mesures
cube.measures["Total Sales"] = tt.agg.sum(sales_store["TotalIncludingTax"])
cube.measures["Total Quantity"] = tt.agg.sum(sales_store["Quantity"])
cube.measures["Average Sales"] = tt.agg.mean(sales_store["TotalIncludingTax"])

# Affichage du lien pour l'interface Atoti
print(f"🔗 Open Atoti UI: {session.url}")
