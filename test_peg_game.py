
from peg_game import PegSolitaireGame

def test_initial_center_empty():
    game = PegSolitaireGame("English", 7)
    mid = game.size // 2
    assert game.board[mid][mid] == 0

def test_valid_move_updates_board():
    game = PegSolitaireGame("English", 7)

    # Setup custom small move
    game.board[3][1] = 1
    game.board[3][2] = 1
    game.board[3][3] = 0

    result = game.try_move(3,1,3,3)

    assert result is True
    assert game.board[3][1] == 0
    assert game.board[3][2] == 0
    assert game.board[3][3] == 1

def test_game_over_detection():
    game = PegSolitaireGame("English", 7)

    # clear board
    for r in range(game.size):
        for c in range(game.size):
            if game.board[r][c] != -1:
                game.board[r][c] = 0

    game.board[3][3] = 1

    assert game.is_game_over() is True