import keyboard

def verify_keypress():
    key_name = keyboard.read_event().name
    return key_name.lower()


if __name__ == "__main__":
    # Simple test to verify keypress detection
    print("Press 'A' to test keypress detection. Press 'Esc' to exit.")
    try:
        while True:
            key = verify_keypress()
            print(f"Key pressed: {key}")
    except KeyboardInterrupt:
        pass