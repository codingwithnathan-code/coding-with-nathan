import random


def main():
    print("🎉 Welcome to the Number Guessing Game! 🎉")
    print("I have picked a secret number between 1 and 100.")
    print("Can you guess it? I'll tell you if your guess is too high or too low.\n")

    secret_number = random.randint(1, 100)
    guesses = 0
    is_running = True

    while is_running:
        try:
            guess = int(input("Enter your guess (1-100): "))
            guesses += 1
            if guess < 1 or guess > 100:
                print("⚠️ Please enter a number between 1 and 100.")
                continue
            if guess == secret_number:
                print(
                    f"🎉 Congratulations! You guessed the number {secret_number} correctly!"
                )
                print(f"It took you {guesses} guesses.")
                is_running = False

            elif guess < secret_number:
                print("📉 Too low! Try a higher number.")

            else:
                print("📈 Too high! Try a lower number.")

        except ValueError:
            print("❌ Invalid input! Please enter a whole number.")

    play_again = input("\nWould you like to play again? (y/n): ").strip().lower()
    if play_again == "y" or play_again == "yes":
        print("\n" + "=" * 40)
        main()
    else:
        print("\nThanks for playing! See you next time 👋")


if __name__ == "__main__":
    main()
