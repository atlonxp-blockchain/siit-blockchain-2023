from Crypto.PublicKey import RSA

# Generate key pairs for CA
CA_key_pair = RSA.generate(2048)
AA_key_pair = RSA.generate(2048)

# Store CA and AA private key
with open(f"./contract_interface/CA_private_key.pem", "wb") as file:
    file.write(CA_key_pair.export_key("PEM"))

with open(f"./contract_interface/AA_private_key.pem", "wb") as file:
    file.write(AA_key_pair.export_key("PEM"))

# Store CA and AA public key
with open(f"./contract_interface/CA_public_key.pem", "wb") as file:
    file.write(CA_key_pair.public_key().export_key("PEM"))

with open(f"./contract_interface/AA_public_key.pem", "wb") as file:
    file.write(AA_key_pair.public_key().export_key("PEM"))
