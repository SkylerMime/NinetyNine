import monte_carlo_search_tree as mcst
import connect_four as game


def main():
    state = game.ConnectFourState()
    search_tree = mcst.MonteCarloSearchTree(state)

    while not game.is_over(state):
        print("Current board:")
        game.print_board(state.board)

        user_move = int(input("Enter a move: "))
        while user_move not in game.get_legal_moves(state):
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        state = game.make_move(user_move, state)
        search_tree.move(user_move)

        game.print_board(state.board)

        if game.is_over(state):
            print("Player one won!")
            break

        print("Thinking...")

        search_tree.search()
        move = search_tree.best_move()

        print("Search tree chose move: ", move)

        state = game.make_move(move, state)
        search_tree.move(move)

        if game.is_over(state):
            print("Player two won!")
            break


if __name__ == "__main__":
    main()
