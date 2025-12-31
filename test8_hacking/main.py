def decode_key(encoded_text: str) -> str:
    # First decode the hex string to bytes
    byte_data = bytes.fromhex(encoded_text)
    # Get the first 5 bytes
    first_five_bytes = byte_data[:5]
    # Convert each byte to its corresponding ASCII character
    decoded_chars = [chr(byte) for byte in first_five_bytes]
    supposed_decoded_string = "THM{}"
    decoded_key = ""
    for i, char in enumerate(decoded_chars):
        decoded_key += chr(ord(char) ^ ord(supposed_decoded_string[i]))
    
    return decoded_key

def decode_text(encoded_text: str, key: str) -> str:
    byte_data = bytes.fromhex(encoded_text)
    decoded_chars = []
    key_length = len(key)
    
    for i, byte in enumerate(byte_data):
        decoded_char = chr(byte ^ ord(key[i % key_length]))
        decoded_chars.append(decoded_char)
    
    return ''.join(decoded_chars)



if __name__ == "__main__":
    encoded_text = "060078034263295916461730413946267c5613511326474b533e044c1067203c4c484720307a0a4f"
    decoded_key = decode_key(encoded_text)
    print(f"Decoded Key: {decoded_key}")
        
    
    