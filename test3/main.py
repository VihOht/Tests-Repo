def greet_user(username):
    greeting = f"Hello, {username}! \U0001F600"
    return greeting


if __name__ == "__main__":
    user_name = input("Enter your name: ")
    print(greet_user(user_name))