import random

options = ["Rock", "Paper", "Scissor"]


def get_user_input():
    key = "0"
    while key not in ["1", "2", "3"]:
        key = input("Choice your action:\n\t1.Rock\n\t2.Paper\n\t3.Scissor\n")
    return options[int(key) - 1]


def get_pc_input():
    pc_choice = random.choice(options)
    print(f"PC choices {pc_choice}")
    return pc_choice


def determain_winner(user, pc):
    if user == pc:
        return "Draw!"

    if (
        (user == "Rock" and pc == "Paper")
        or (user == "Paper" and pc == "Scissor")
        or (user == "Scissor" and pc == "Rock")
    ):
        return "PC was won!"
    else:
        return "User was won!"


def main():
    user_choice = get_user_input()
    pc_choice = get_pc_input()
    print(determain_winner(user_choice, pc_choice))
    print("Round is end")


tmp = "y"

while tmp == "y":
    main()
    tmp = input("Do you want to be continue?\n\ty\n\tn\n")
