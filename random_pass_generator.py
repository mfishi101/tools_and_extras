import random
import string

def generate_password(length=12, include_uppercase=True, include_lowercase=True, 
                     include_digits=True, include_symbols=True):
    """
    Generate a random password with specified criteria.
    
    Args:
        length (int): Length of the password (default: 12)
        include_uppercase (bool): Include uppercase letters
        include_lowercase (bool): Include lowercase letters
        include_digits (bool): Include digits
        include_symbols (bool): Include symbols
    
    Returns:
        str: Generated password
    """
    characters = ""
    
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        raise ValueError("At least one character type must be included")
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("Random Password Generator")
    print("-" * 25)
    
    try:
        length = int(input("Enter password length (default 12): ") or 12)
        
        print("\nCharacter types to include:")
        include_upper = input("Include uppercase letters? (Y/n): ").lower() != 'n'
        include_lower = input("Include lowercase letters? (Y/n): ").lower() != 'n'
        include_digits = input("Include digits? (Y/n): ").lower() != 'n'
        include_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
        
        password = generate_password(
            length=length,
            include_uppercase=include_upper,
            include_lowercase=include_lower,
            include_digits=include_digits,
            include_symbols=include_symbols
        )
        
        print(f"\nGenerated password: {password}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nPassword generation cancelled.")

if __name__ == "__main__":
    main()
