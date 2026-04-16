
# A text encryption, decryption and verification program.

# WHY WE NEED encrypted_index.txt:
#   The encryption rules are not uniquely reversible - two different letters
#   Non-Bijective Cipher can encrypt to the same output letter (called a "collision").
#   For example with shift1=2, shift2=3:
#       'c' (first half)  -> 'i'
#       'n' (second half) -> 'i'
#   Both produce 'i', so when decrypting 'i' we cannot tell which it was
#   without storing extra information.


def encrypt_character(char, shift1, shift2):
    """
    Encrypts a single character and records which half it came from.
    """

    # LOWERCASE LETTERS (a-z)

    if char.islower():
        position = ord(char) - ord('a')   # Convert letter to 0-25

        if position <= 12:                # First half: a-m
            new_position = (position + shift1 * shift2) % 26  # Shift forward
            return chr(new_position + ord('a')), '0'           # Flag = first half

        else:                             # Second half: n-z
            new_position = (position - (shift1 + shift2)) % 26  # Shift backward
            return chr(new_position + ord('a')), '1'             # Flag = second half

    # UPPERCASE LETTERS (A-Z)
    elif char.isupper():
        position = ord(char) - ord('A')   # Convert letter to 0-25

        if position <= 12:                # First half: A-M
            new_position = (position - shift1) % 26          # Shift backward
            return chr(new_position + ord('A')), '0'          # Flag = first half

        else:                             # Second half: N-Z
            new_position = (position + shift2 ** 2) % 26     # Shift forward
            return chr(new_position + ord('A')), '1'          # Flag = second half


    # EVERYTHING ELSE (spaces, numbers, punctuation, newlines)

    else:
        return char, 'x'                  # Unchanged, flag = not a letter


def decrypt_character(char, half_flag, shift1, shift2):
    """
    Decrypts a single character using the stored half_flag to choose
    the exact reverse of the rule that was used during encryption.
    """


    # LOWERCASE LETTERS

    if char.islower():
        position = ord(char) - ord('a')

        if half_flag == '0':
            # Came from first half - encryption shifted FORWARD, so reverse = BACKWARD
            new_position = (position - shift1 * shift2) % 26
        else:
            # Came from second half - encryption shifted BACKWARD, so reverse = FORWARD
            new_position = (position + (shift1 + shift2)) % 26

        return chr(new_position + ord('a'))


    # UPPERCASE LETTERS

    elif char.isupper():
        position = ord(char) - ord('A')

        if half_flag == '0':
            # Came from first half - encryption shifted BACKWARD, so reverse = FORWARD
            new_position = (position + shift1) % 26
        else:
            # Came from second half - encryption shifted FORWARD, so reverse = BACKWARD
            new_position = (position - shift2 ** 2) % 26

        return chr(new_position + ord('A'))


    # EVERYTHING ELSE - unchanged

    else:
        return char


def encrypt_file(shift1, shift2):
    """
    Reads raw_text.txt, encrypts every character, and writes:
        - encrypted_text.txt  : the encrypted content
        - encrypted_index.txt : the half-flags for every character
                                (needed to correctly decrypt later)
    """

    # Read the original file
    input_file = open("raw_text.txt", "r", encoding="utf-8")
    original_text = input_file.read()
    input_file.close()

    # Encrypt every character and collect flags
    encrypted_text = ""
    index_flags    = ""

    for char in original_text:
        encrypted_char, flag = encrypt_character(char, shift1, shift2)
        encrypted_text += encrypted_char   # Build encrypted string
        index_flags    += flag             # Build flag string (same length)

    # Write the encrypted text
    output_file = open("encrypted_text.txt", "w", encoding="utf-8")
    output_file.write(encrypted_text)
    output_file.close()

    # Write the index flags (same length as encrypted_text, one char per position)
    index_file = open("encrypted_index.txt", "w", encoding="utf-8")
    index_file.write(index_flags)
    index_file.close()

    print("Encryption complete!")
    print("  -> encrypted_text.txt")
    print("  -> encrypted_index.txt")


def decrypt_file(shift1, shift2):
    """
    Reads encrypted_text.txt and encrypted_index.txt, decrypts every
    character using the stored flags, and writes decrypted_text.txt.

    shift1 : first shift value (must be same as used in encryption)
    shift2 : second shift value (must be same as used in encryption)
    """

    # Read the encrypted text
    enc_file = open("encrypted_text.txt", "r", encoding="utf-8")
    encrypted_text = enc_file.read()
    enc_file.close()

    # Read the index flags
    idx_file = open("encrypted_index.txt", "r", encoding="utf-8")
    index_flags = idx_file.read()
    idx_file.close()

    # Decrypt every character using its matching flag
    decrypted_text = ""

    for char, flag in zip(encrypted_text, index_flags):
        decrypted_text += decrypt_character(char, flag, shift1, shift2)

    # Write the decrypted text
    output_file = open("decrypted_text.txt", "w", encoding="utf-8")
    output_file.write(decrypted_text)
    output_file.close()

    print("Decryption complete!")
    print("  -> decrypted_text.txt")


def verify():
    """
    Compares raw_text.txt with decrypted_text.txt.
    Prints success if they match, or shows differing lines if not.
    """

    # Read original
    original_file = open("raw_text.txt", "r", encoding="utf-8")
    original_text = original_file.read()
    original_file.close()

    # Read decrypted
    decrypted_file = open("decrypted_text.txt", "r", encoding="utf-8")
    decrypted_text = decrypted_file.read()
    decrypted_file.close()

    # Compare
    if original_text == decrypted_text:
        print("Verification SUCCESSFUL! Decrypted text matches the original perfectly.")

    else:
        print("Verification FAILED! Decrypted text does not match the original.")
        print()

        original_lines  = original_text.splitlines()
        decrypted_lines = decrypted_text.splitlines()
        total_lines     = max(len(original_lines), len(decrypted_lines))

        for line_number in range(total_lines):
            original_line  = original_lines[line_number]  if line_number < len(original_lines)  else "LINE MISSING"
            decrypted_line = decrypted_lines[line_number] if line_number < len(decrypted_lines) else "LINE MISSING"

            if original_line != decrypted_line:
                print(f"  Line {line_number + 1} differs:")
                print(f"    Original  : {original_line}")
                print(f"    Decrypted : {decrypted_line}")


def main():
    """
    Runs the full program:
    1. Get shift values from user
    2. Encrypt raw_text.txt
    3. Decrypt the encrypted file
    4. Verify the result
    """

    print("=" * 50)
    print("       Simple Text Encryption Program")
    print("=" * 50)
    print()

    # Get shift1
    while True:
        try:
            shift1 = int(input("Enter shift1 (a whole number): "))
            break
        except ValueError:
            print("  That's not a valid number. Please try again.")

    # Get shift2
    while True:
        try:
            shift2 = int(input("Enter shift2 (a whole number): "))
            break
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


# Entry point

if __name__ == "__main__":
    main()