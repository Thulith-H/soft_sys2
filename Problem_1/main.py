def encrypt_character(char, shift1, shift2):
    """
    Encrypts a single character using the shift rules.

    Parameters:
        char   : the single character to encrypt
        shift1 : first shift value provided by the user
        shift2 : second shift value provided by the user

    Returns:
        The encrypted character, or the original character if no rule applies.
    """

    # ----------------------------------------------------------------
    # LOWERCASE LETTERS (a-z)
    # ----------------------------------------------------------------
    if char.islower():

        # Convert the letter to a number between 0 and 25
        # ord() gives the ASCII number of a character
        # ord('a') = 97, so subtracting 97 gives us 0-25
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


    # STEP 1 - Read the original file
    # Open raw_text.txt in read mode ("r")
    # 'encoding="utf-8"' handles special characters safely
    input_file = open("raw_text.txt", "r", encoding="utf-8")

    # Read the entire contents as one big string
    original_text = input_file.read()

    # Always close the file after reading
    input_file.close()


    # STEP 2 - Encrypt every character

    # We'll build the encrypted text one character at a time
    encrypted_text = ""

    # Loop through every single character in the original text
    for char in original_text:

        # Encrypt this character and add it to our result string
        encrypted_text = encrypted_text + encrypt_character(char, shift1, shift2)


    # STEP 3 - Write the encrypted text to a new file

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


def verify():


    # Open and read the original raw text
    original_file = open("raw_text.txt", "r", encoding="utf-8")
    original_text = original_file.read()
    original_file.close()


    # Open and read the decrypted text
    decrypted_file = open("decrypted_text.txt", "r", encoding="utf-8")
    decrypted_text = decrypted_file.read()
    decrypted_file.close()

    # Simple check — are both strings exactly the same?
    if original_text == decrypted_text:
        print("Verification SUCCESSFUL! Decrypted text matches the original perfectly.")

    else:
        # They don't match — let's help the user see where it went wrong
        print("Verification FAILED! Decrypted text does not match the original.")
        print()

        # Split both texts into individual lines for easier comparison
        original_lines = original_text.splitlines()
        decrypted_lines = decrypted_text.splitlines()

        # Check each line one by one
        # We use the length of the longer file so we don't miss any extra lines
        total_lines = max(len(original_lines), len(decrypted_lines))

        for line_number in range(total_lines):

            # Get the line from each file
            # If a file has fewer lines, use "LINE MISSING" as a placeholder
            if line_number < len(original_lines):
                original_line = original_lines[line_number]
            else:
                original_line = "LINE MISSING"

            if line_number < len(decrypted_lines):
                decrypted_line = decrypted_lines[line_number]
            else:
                decrypted_line = "LINE MISSING"

            # Only print lines that are different
            if original_line != decrypted_line:
                print(f"  Line {line_number + 1} differs:")
                print(f"    Original  : {original_line}")
                print(f"    Decrypted : {decrypted_line}")

def main():


    print("=" * 50)
    print("       Simple Text Encryption Program")
    print("=" * 50)
    print()


    # Keep asking until the user gives a valid whole number for shift1
    while True:
        try:
            shift1 = int(input("Enter shift1 (a whole number): "))
            break   # If we got here, the input was valid, exit the loop
        except ValueError:
            # int() failed because the user typed something that isn't a number
            print("  That's not a valid number. Please try again.")

    # Keep asking until the user gives a valid whole number for shift2
    while True:
        try:
            shift2 = int(input("Enter shift2 (a whole number): "))
            break   # Valid input received, exit the loop
        except ValueError:
            print("  That's not a valid number. Please try again.")

    print()


    print("Encrypting...")
    encrypt_file(shift1, shift2)
    print()

    print("Decrypting...")
    decrypt_file(shift1, shift2)
    print()

    print("Verifying...")
    verify()
    print()

    print("=" * 50)
    print("           Program complete!")
    print("=" * 50)


# Entry point of the program

if __name__ == "__main__":
    main()