#!/bin/bash

PRIVATE_KEY="private_key.pem"
PUBLIC_KEY="public_key.pem"

# Remove old keys if they exist
rm -f "$PRIVATE_KEY" "$PUBLIC_KEY"
echo "Old RSA Key Pair Removed"

# Generate private key
openssl genpkey -algorithm RSA -out "$PRIVATE_KEY" -pkeyopt rsa_keygen_bits:2048

# Extract public key
openssl rsa -pubout -in "$PRIVATE_KEY" -out "$PUBLIC_KEY"

echo "New RSA Key Pair Generated"