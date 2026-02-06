#!/usr/bin/env python3
import random
import os


words = [
    "tungtung",
    "trallalero",
    "filippo boschi",
    "zaza",
    "lakaka",
    "gubbio",
    "cucinato"
]

phrase = " ".join(random.sample(words, k=random.randint(3, 5)))
steps = random.randint(2, 5)

flag = os.getenv("FLAG", "pascalCTF{REDACTED}")


def encoder(phrase, steps):
    encoded_phrase = ""

    for i in range(len(phrase)):
        if phrase[i] == " ":
            encoded_phrase += phrase[i]

        elif i % steps == 0:
            encoded_phrase += str(ord(phrase[i]))

        else:
            encoded_phrase += phrase[i]

    return encoded_phrase


def questions(name):
    gained_aura = 0

    questions_list = [
        "Do you believe in the power of aura? (yes/no)",
        "Do you have a JerkMate account? (yes/no)",
        "Are you willing to embrace your inner alpha? (yes/no)",
        "Do you really like SHYNE from Travis Scott? (yes/no)",
    ]

    aura_values = [(150, -50), (-1000, 50), (450, -80), (-100, 50)]

    for i in range(len(questions_list)):
        print(f"{name}, {questions_list[i]}")
        answer = input("> ").strip().lower()

        if answer == "yes":
            gained_aura += aura_values[i][0]

        elif answer == "no":
            gained_aura += aura_values[i][1]

    return gained_aura


def aura_test(name):
    print(f"{name}, you have reached the final AuraTest!")
    print("If you want to win your prize you need to decode this secret phrase:")
    print(encoder(phrase, steps))

    guess = input("Type the decoded phrase to prove your worth:\n> ")

    if guess == phrase:
        print(
            f"Congratulations {name}! You have proven your worth and gained the ultimate aura!"
        )
        print(f"Here's your prize:\n{flag}")
        exit()

    else:
        print(
            f"Don't waste my time {name}, you failed the AuraTest. Try again but this time use all your aura!"
        )


print("Welcome to the AuraTester2000!")
aura = 0

name = input("First of all, we need to know your name.\n> ")

if name.strip() == "":
    print("You didn't start very well, I asked your name.")
else:
    print(f"Welcome {name} to the AuraTester2000!")

while True:
    print(
        "\n1. Answer questions to gain or lose aura.\n"
        "2. Check your current aura.\n"
        "3. Take the final AuraTest to prove your worth.\n"
        "4. Exit the AuraTester2000."
    )

    choice = input("What do you want to do?\n> ")

    if choice == "1":
        print("You chose to answer questions.")
        gained_aura = questions(name)

        if gained_aura >= 0:
            print(f"Congratulations {name}! You gained {gained_aura} aura points.")
        else:
            print(f"Sorry {name}, you lost {gained_aura} aura points.")

        aura += gained_aura

    elif choice == "2":
        print(f"Your current aura is {aura}.")

    elif choice == "3":
        if aura < 500:
            print("You need more aura to even try the final AuraTest.")
        else:
            aura_test(name)

    elif choice == "4":
        print("Exiting the AuraTester2000. Goodbye!")
        exit()

    else:
        print("Invalid option. Please try again.")
