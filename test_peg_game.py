from peg_game import BaseSolitaireGame, ManualSolitaireGame, AutomatedSolitaireGame


def test_initial_center_empty():
    game = BaseSolitaireGame("English", 7)
    mid = game.size // 2
    assert game.board[mid][mid] == 0


def test_manual_valid_move_updates_board():
    game = ManualSolitaireGame("English", 7)
    game.board[3][1] = 1
    game.board[3][2] = 1
    game.board[3][3] = 0

    result = game.make_manual_move(3, 1, 3, 3)

    assert result is True
    assert game.board[3][1] == 0
    assert game.board[3][2] == 0
    assert game.board[3][3] == 1
    assert game.move_count == 1


def test_manual_game_over_detection():
    game = ManualSolitaireGame("English", 7)

    for r in range(game.size):
        for c in range(game.size):
            if game.board[r][c] != -1:
                game.board[r][c] = 0

    game.board[3][3] = 1
    assert game.is_game_over() is True


def test_automated_move_changes_board_when_move_exists():
    game = AutomatedSolitaireGame("English", 7)
    before = game.snapshot()

    moved = game.make_automated_move()

    assert moved is True
    assert game.board != before
    assert game.move_count == 1


def test_automated_game_over_when_no_moves_exist():
    game = AutomatedSolitaireGame("English", 7)

    for r in range(game.size):
        for c in range(game.size):
            if game.board[r][c] != -1:
                game.board[r][c] = 0

    game.board[3][3] = 1

    assert game.is_game_over() is True
    assert game.make_automated_move() is False


def test_randomize_changes_board_state_legally():
    game = ManualSolitaireGame("English", 7)
    before = game.snapshot()

    changed = game.randomize_state(steps=3)

    assert changed is True
    assert game.board != before
