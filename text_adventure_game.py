import random


def print_slow(text):
    """Print text with a small delay for dramatic effect (optional)."""
    print(text)


def start_game():
    print("=" * 60)
    print("          THE ENCHANTED FOREST ADVENTURE")
    print("=" * 60)
    print("\nYou wake up in a mysterious forest.  The trees glow faintly.")
    print("You don't remember how you got here.  You must find a way out.\n")

    input("Press Enter to begin your adventure...")
    main_clearing()


def main_clearing():
    print("\n--- You are in a small clearing  ---")
    print("There are three paths:")
    print("1. Go towards the dark cave")
    print("2. Follow the river")
    print("3. Walk to the ancient glowing tree")

    choice = input("\nWhat do you do? (1/2/3): ").strip()

    if choice == "1":
        cave()
    elif choice == "2":
        river()
    elif choice == "3":
        ancient_tree()
    else:
        print("Invalid choice.  You hesitate and stay in the clearing.")
        main_clearing()


def cave():
    print("\n--- You enter the dark cave ---")
    print("It's cold and damp.  You see a chest and a sleeping wolf.")
    print("What do you do?")
    print("1. Open the chest quietly")
    print("2. Try to sneak past the wolf")
    print("3. Throw a rock to distract the wolf")

    choice = input("\nChoice (1/2/3): ").strip()

    if choice == "1":
        print("\nYou open the chest and find a magical sword! +1 Strength")
        print("But the wolf wakes up...")
        if random.random() > 0.5:
            print("You defeat the wolf with your new sword! You win!")
            good_ending()
        else:
            print("the wolf overpowers you...")
            bad_ending()
    elif choice == "2":
        print("\nYou try to sneak past... The wolf wakes up!")
        bad_ending()
    else:
        print("\nYou distract the wolf and escape deeper into the cave.")
        print("You find an exit! You made it out alive.")
        neutral_ending()


def river():
    print("\n--- You follow the sparking river ---")
    print("The water is crystal clear.  You see a small boat.")
    print("\nWhat do you do?")
    print("1. Take the boat downstream")
    print("2. Swim across the river")
    print("3. Follow the river on foot")

    choice = input("\nChoice (1/2/3): ").strip()

    if choice == "1":
        print("\nYou row downstream and discover a hidden village!")
        print("The villagers welcome you and help you get home.")
        good_ending()
    elif choice == "2":
        print("\nYou attempt to swim... The current is too strong!")
        bad_ending()
    else:
        print("\nYou walk along the river and eventually find a bridge.")
        neutral_ending()


def ancient_tree():
    print("\n--- You approach the ancient glowing tree ---")
    print("The tree whispers: 'Answer my riddle and I shall help you...'")
    print("\nRiddle: What has roots as nobody sees, is taller than trees,")
    print("Up, up it goes, and yet never grows?")

    answer = input("\nYour answer: ").strip().lower()

    if "mountain" == answer:
        print("\nThe tree smiles... 'Correct!'")
        print("It opens a magical portal for you.")
        good_ending()
    else:
        print("\nThe tree shakes sadly...  You are teleported to a dark place.")
        bad_ending()


def good_ending():
    print("\n" + "=" * 60)
    print("🥳 CONGRATULATIONS! You found a happy ending! 🥳")
    print("You safely made it out of the enchanted forest.")
    print("=" * 60)
    play_again()


def neutral_ending():
    print("\n" + "=" * 60)
    print("You made it out of the forest, but the adventure felt incomplete.")
    print("=" * 60)
    play_again()


def bad_ending():
    print("\n" + "=" * 60)
    print("💀 GAME OVER 💀")
    print("Your adventure ended unfortunately...")
    print("=" * 60)
    play_again()


def play_again():
    choice = input("\nWould you like to play again? (y/n): ").strip().lower()

    if choice == "y" or choice == "yes":
        print("\nRestarting the adventure...\n")
        start_game()
    else:
        print("\nThank you for playing The Enchanted Forest!")
        print("See you next time on Coding With Nathan!")


# Start the game

if __name__ == "__main__":
    start_game()
