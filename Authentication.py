import sqlite3
import hashlib

while True:
    password = input("Enter password: ").strip()

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT PasswordHash FROM Staff WHERE UserName = ?",
        ('smitchell',)
    )

    result = cursor.fetchone()
    conn.close()

    if result is None:
        print("User not found")
        continue

    input_hash = str(hashlib.sha256(password.encode()).hexdigest())

    print("DB hash:", result[0])
    print("Input hash:", input_hash)

    if str(result[0].strip()) == input_hash.strip():
        print("✅ Correct password")
    else:
        print("❌ Wrong, try again")