def encrypt_character(char, shift1, shift2):
    """
    Parameters:
            char   : the single character to encrypt
            shift1 : first shift value provided by the user
            shift2 : second shift value provided by the user
    Returns:
        The encrypted character, or the original character if no rule applies.
    """

    # LOWERCASE LETTERS (a-z)
    if char.islower():


        position = ord(char) - ord('a')

        # First half of alphabet: a-m have positions 0 to 12
        if position <= 12:
            # Shift FORWARD by shift1 * shift2
            new_position = (position + shift1 * shift2) % 26

        # Second half of alphabet: n-z have positions 13 to 25
        else:
            # Shift BACKWARD by shift1 + shift2
            new_position = (position - (shift1 + shift2)) % 26

        # Convert the number back to a letter
        # chr() is the opposite of ord()
        return chr(new_position + ord('a'))

    # UPPERCASE LETTERS (A-Z)

    elif char.isupper():

        # Same idea, but using 'A' as our base (ord('A') = 65)
        position = ord(char) - ord('A')

        # First half: A-M have positions 0 to 12
        if position <= 12:
            # Shift BACKWARD by shift1
            new_position = (position - shift1) % 26

        # Second half: N-Z have positions 13 to 25
        else:
            # Shift FORWARD by shift2 squared
            new_position = (position + shift2 ** 2) % 26

        # Convert back to an uppercase letter
        return chr(new_position + ord('A'))

    # EVERYTHING ELSE (spaces, numbers, punctuation, newlines, etc.)
    else:
        # Return the character completely unchanged
        return char



def encrypt_file(shift1, shift2):
    """
    Reads raw_text.txt, encrypts every character, and writes
    the result to encrypted_text.txt.

    Parameters:
        shift1 : first shift value provided by the user
        shift2 : second shift value provided by the user
    """


    # Open raw_text.txt in read mode ("r")
    # 'encoding="utf-8"' handles special characters safely
    input_file = open("raw_text.txt", "r", encoding="utf-8")

    # Read the entire contents as one big string
    original_text = input_file.read()

    # Always close the file after reading
    input_file.close()


    # Build the encrypted text one character at a time
    encrypted_text = ""

    # Loop through every single character in the original text
    for char in original_text:

        # Encrypt this character and add it to our result string
        encrypted_text = encrypted_text + encrypt_character(char, shift1, shift2)


    # Open encrypted_text.txt in write mode ("w")
    # This creates the file if it doesn't exist, or overwrites it if it does
    output_file = open("encrypted_text.txt", "w", encoding="utf-8")

    # Write our encrypted string to the file
    output_file.write(encrypted_text)

    # Always close the file after writing
    output_file.close()

    # Let the user know it worked
    print("Encryption complete! Saved to encrypted_text.txt")


def decrypt_character(char, shift1, shift2):
    if char.islower():
        position = ord(char) - ord('a')

        # Came from first half (0-12), was shifted forward
        candidate = (position - shift1 * shift2) % 26
        if 0 <= candidate <= 12:
            return chr(candidate + ord('a'))

        # Otherwise it came from second half (13-25), was shifted backward
        candidate = (position + (shift1 + shift2)) % 26
        return chr(candidate + ord('a'))

    elif char.isupper():
        position = ord(char) - ord('A')

        # Came from first half (0-12), was shifted backward
        candidate = (position + shift1) % 26
        if 0 <= candidate <= 12:
            return chr(candidate + ord('A'))

        # Otherwise it came from second half (13-25), was shifted forward
        candidate = (position - shift2 ** 2) % 26
        return chr(candidate + ord('A'))

    else:
        return char


def decrypt_file(shift1, shift2):
    # Read the encrypted file
    # Open encrypted_text.txt in read mode
    input_file = open("encrypted_text.txt", "r", encoding="utf-8")

    # Read the entire contents as one big string
    encrypted_text = input_file.read()

    # Always close the file after reading
    input_file.close()

    # Decrypt every character
    # Build the decrypted text one character at a time
    decrypted_text = ""

    # Loop through every single character in the encrypted text
    for char in encrypted_text:
        # Decrypt this character and add it to our result string
        decrypted_text = decrypted_text + decrypt_character(char, shift1, shift2)

    # Write the decrypted text to a new file
    # Open decrypted_text.txt in write mode
    # This creates the file if it doesn't exist, or overwrites it if it does
    output_file = open("decrypted_text.txt", "w", encoding="utf-8")

    # Write our decrypted string to the file
    output_file.write(decrypted_text)

    # Always close the file after writing
    output_file.close()

    # Let the user know it worked
    print("Decryption complete! Saved to decrypted_text.txt")