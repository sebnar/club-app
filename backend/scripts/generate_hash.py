"""
Script simple para generar password hash
Uso: python backend/scripts/generate_hash.py
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = input("Ingrese la contraseña para hashear: ").strip() or "admin123"
hash_result = pwd_context.hash(password)

print("\n" + "="*60)
print("PASSWORD HASH GENERADO:")
print("="*60)
print(hash_result)
print("="*60)
print(f"\nContraseña original: {password}")
print(f"Hash (copiar este valor): {hash_result}")
