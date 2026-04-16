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