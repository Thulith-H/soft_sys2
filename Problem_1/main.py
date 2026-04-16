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