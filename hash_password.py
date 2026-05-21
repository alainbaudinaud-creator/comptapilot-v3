import bcrypt

mot_de_passe = "admin123"

hash_password = bcrypt.hashpw(
    mot_de_passe.encode('utf-8'),
    bcrypt.gensalt()
)

print(hash_password.decode('utf-8'))
