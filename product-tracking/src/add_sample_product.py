from contract_interface import PKI_contract_interface
from contract_interface import Product_contract_interface
import time

# -----------------------------------------------------------

Product = Product_contract_interface.add_new_product(
    "Laptop A", "China", "Company X", "Good Laptop"
)["product_ID"]
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "Company B", "Import from Company X"
)
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "Company C", "Import from Company B"
)
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "Company Y", "Import from Company C"
)

Product = Product_contract_interface.add_new_product(
    "Laptop B", "China", "MSI", "TITAN GT77"
)["product_ID"]
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "MSI_CH", "Import from manufacturer"
)
time.sleep(1)

detail = """
1.Up to latest Intel® Core™ i9-12900HX processor
2.Windows 11 Home / Windows 11 Pro
3.NVIDIA® GeForce RTX™ 3080 Ti Laptop GPU 16GB GDDR6 (12UHS)
4.NVIDIA® GeForce RTX™ 3070 Ti Laptop GPU 8GB GDDR6 (12UGS)
5.17.3"" UHD (3840x2160), 120 Hz Refresh Rate, 100% DCI-P3(Typical), IPS-Level panel (Optional)
6.Cherry Mechanical Per-Key RGB gaming keyboard by SteelSeries
"""
Product_contract_interface.add_new_product_track(Product, "MSI_TH", detail)

# -----------------------------------------------------------

Product = Product_contract_interface.add_new_product(
    "Laptop B", "China", "MSI", "TITAN GT77"
)["product_ID"]
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "MSI_CH", "Import from manufacturer"
)
time.sleep(1)

detail = """
1.Up to latest Intel® Core™ i9-12900HX processor
2.Windows 11 Home / Windows 11 Pro
3.NVIDIA® GeForce RTX™ 3080 Ti Laptop GPU 16GB GDDR6 (12UHS)
4.NVIDIA® GeForce RTX™ 3070 Ti Laptop GPU 8GB GDDR6 (12UGS)
5.17.3"" UHD (3840x2160), 120 Hz Refresh Rate, 100% DCI-P3(Typical), IPS-Level panel (Optional)
6.Cherry Mechanical Per-Key RGB gaming keyboard by SteelSeries
"""
Product_contract_interface.add_new_product_track(Product, "MSI_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(Product, "JIB_TH", detail)

# -----------------------------------------------------------

Product = Product_contract_interface.add_new_product(
    "Laptop C", "China", "MSI", "TITAN GT77"
)["product_ID"]
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "MSI_CH", "Import from manufacturer"
)
time.sleep(1)

detail = """
1.Up to latest Intel® Core™ i9-12900HX processor
2.Windows 11 Home / Windows 11 Pro
3.NVIDIA® GeForce RTX™ 3080 Ti Laptop GPU 16GB GDDR6 (12UHS)
4.NVIDIA® GeForce RTX™ 3070 Ti Laptop GPU 8GB GDDR6 (12UGS)
5.17.3"" UHD (3840x2160), 120 Hz Refresh Rate, 100% DCI-P3(Typical), IPS-Level panel (Optional)
6.Cherry Mechanical Per-Key RGB gaming keyboard by SteelSeries
"""
Product_contract_interface.add_new_product_track(Product, "MSI_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(Product, "JIB_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "Bluedegard", "Buy from JIB_TH"
)

# -----------------------------------------------------------

Product = Product_contract_interface.add_new_product(
    "Laptop D", "China", "MSI", "TITAN GT77"
)["product_ID"]
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "MSI_CH", "Import from manufacturer"
)
time.sleep(1)

detail = """
1.Up to latest Intel® Core™ i9-12900HX processor
2.Windows 11 Home / Windows 11 Pro
3.NVIDIA® GeForce RTX™ 3080 Ti Laptop GPU 16GB GDDR6 (12UHS)
4.NVIDIA® GeForce RTX™ 3070 Ti Laptop GPU 8GB GDDR6 (12UGS)
5.17.3"" UHD (3840x2160), 120 Hz Refresh Rate, 100% DCI-P3(Typical), IPS-Level panel (Optional)
6.Cherry Mechanical Per-Key RGB gaming keyboard by SteelSeries
"""
Product_contract_interface.add_new_product_track(Product, "MSI_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(Product, "JIB_TH", detail)

# -----------------------------------------------------------

Product = Product_contract_interface.add_new_product(
    "Laptop E", "China", "MSI", "TITAN GT77"
)["product_ID"]
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "MSI_CH", "Import from manufacturer"
)
time.sleep(1)

detail = """
1.Up to latest Intel® Core™ i9-12900HX processor
2.Windows 11 Home / Windows 11 Pro
3.NVIDIA® GeForce RTX™ 3080 Ti Laptop GPU 16GB GDDR6 (12UHS)
4.NVIDIA® GeForce RTX™ 3070 Ti Laptop GPU 8GB GDDR6 (12UGS)
5.17.3"" UHD (3840x2160), 120 Hz Refresh Rate, 100% DCI-P3(Typical), IPS-Level panel (Optional)
6.Cherry Mechanical Per-Key RGB gaming keyboard by SteelSeries
"""
Product_contract_interface.add_new_product_track(Product, "MSI_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(Product, "JIB_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "Bluedegard", "Buy from JIB_TH"
)
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "Aekanut", "Second Hand Laptop But good!"
)

# -----------------------------------------------------------

Product = Product_contract_interface.add_new_product(
    "Laptop F", "China", "MSI", "TITAN GT77"
)["product_ID"]
time.sleep(1)
Product_contract_interface.add_new_product_track(
    Product, "MSI_CH", "Import from manufacturer"
)
time.sleep(1)

detail = """
1.Up to latest Intel® Core™ i9-12900HX processor
2.Windows 11 Home / Windows 11 Pro
3.NVIDIA® GeForce RTX™ 3080 Ti Laptop GPU 16GB GDDR6 (12UHS)
4.NVIDIA® GeForce RTX™ 3070 Ti Laptop GPU 8GB GDDR6 (12UGS)
5.17.3"" UHD (3840x2160), 120 Hz Refresh Rate, 100% DCI-P3(Typical), IPS-Level panel (Optional)
6.Cherry Mechanical Per-Key RGB gaming keyboard by SteelSeries
"""
Product_contract_interface.add_new_product_track(Product, "MSI_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(Product, "JIB_TH", detail)
time.sleep(1)
Product_contract_interface.add_new_product_track(Product, "Aekanut", "Buy from JIB_TH")

# -----------------------------------------------------------

print("Add sample product successfully")
print("Please register Aekanut to see the sample item")
