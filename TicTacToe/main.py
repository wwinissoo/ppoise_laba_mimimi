from game import TicTacToe
def print_board(game):
    print()
    print(game)
    print()
def input_size():
    while True:
        try:
            return TicTacToe(int(input("Enter board size: ")))
        except ValueError:
            print("Error: board size must be an integer of at least 3.")

def input_position(size):
    row = int(input("Row: "))
    col = int(input("Column: "))

    if row < 1 or row > size or col < 1 or col > size:
        raise IndexError("Row or column index is outside the board.")

    return row - 1, col - 1


def next_player(game):
    """Determine whose turn it is by counting X and O marks."""
    size = game.get_size()
    count_x = 0
    count_o = 0
    for row in range(size):
        for col in range(size):
            if game[row, col] == "X":
                count_x += 1
            elif game[row, col] == "O":
                count_o += 1
    if count_x > count_o:
        return "O"
    return "X"


def game_result(game):
    """Return the game-over message, or None while the game is in progress."""
    result = game.winner()
    if result is not None:
        return f"Player {result} wins!"
    if game.is_full():
        return "Draw!"
    return None


def print_menu():
    print("========== TIC-TAC-TOE ==========")
    print("1 - Show board")
    print("2 - Make a move")
    print("3 - Check winner")
    print("4 - Check whether board is full")
    print("5 - Show board as text")
    print("6 - Load board from text")
    print("7 - Copy board")
    print("8 - Save board to file")
    print("9 - Load board from file")
    print("10 - New game")
    print("0 - Exit")
    print("======================================")


def main():
    print("Tic-Tac-Toe")
    game = input_size()

    while True:
        print_menu()
        command = input("Choose an option: ").strip()

        if command == "0":
            print("Program finished.")
            return

        elif command == "1":
            print_board(game)

        elif command == "2":
            finished = game_result(game)
            if finished is not None:
                print(f"Game over. {finished} Start a new game (10).")
                continue

            current = next_player(game)
            print_board(game)
            print(f"Turn: player {current}")

            try:
                position = input_position(game.get_size())

                if not game.can_set(position, current):
                    print("Cannot place a mark in this cell.")
                    continue

                game[position] = current

                finished = game_result(game)
                if finished is not None:
                    print_board(game)
                    print(finished)

            except (ValueError, TypeError, IndexError) as error:
                print(f"Error: {error}")

        elif command == "3":
            result = game.winner()
            if result is None:
                print("No winner yet.")
            else:
                print(f"Player {result} wins.")

        elif command == "4":
            if game.is_full():
                print("The board is full.")
            else:
                print("The board has empty cells.")

        elif command == "5":
            print("Board as text:")
            print(game.to_text())

        elif command == "6":
            print("Enter board rows separated by ';'.")
            print("Example: X - -;- O -;- - X")
            text = input("Board: ")

            try:
                game = TicTacToe.from_text(text.replace(";", "\n"))
                print("Board loaded.")
                print_board(game)
            except ValueError as error:
                print(f"Error: {error}")

        elif command == "7":
            duplicate = TicTacToe(game)
            print("Board copy:")
            print_board(duplicate)
            print("Copy equals original:", duplicate == game)

        elif command == "8":
            filename = input("File name: ")
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    game.write(file)
                print("Board saved.")
            except OSError as error:
                print(f"Error: {error}")

        elif command == "9":
            filename = input("File name: ")
            try:
                with open(filename, encoding="utf-8") as file:
                    game.assign(TicTacToe.read(file))
                print("Board loaded.")
                print_board(game)
            except (OSError, ValueError) as error:
                print(f"Error: {error}")

        elif command == "10":
            game = input_size()

        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram finished.")
