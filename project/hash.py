import bcrypt

def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    return password_hash.decode()

def check_password(password_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())

# # Пример использования
# if __name__ == "__main__":
#     password = "solka2k20"
    
#     # Генерация хэша
#     password_hash = generate_password_hash(password)
#     print(f"Хэш пароля: {password_hash}")
    
#     # Проверка пароля
#     is_correct = check_password(password_hash, password)
#     print(f"Пароль верный: {is_correct}")  # Должно быть True

#     is_correct = check_password(password_hash, "wrong_password")
#     print(f"Пароль верный: {is_correct}")  # Должно быть False