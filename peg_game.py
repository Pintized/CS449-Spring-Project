class PegSolitaireGame:
    def __init__(self, board_type="English", size=7):
        if size % 2 == 0 and board_type in ("English", "European"):
            size += 1
        if size < 5:
            size = 5

        self.board_type = board_type
        self.size = size
        self.move_count = 0
        self.board = self._build_board()

    # ---------------- Board Builders ----------------

    def _build_board(self):
        if self.board_type == "English":
            return self._build_english_board(self.size)
        elif self.board_type == "European":
            return self._build_european_board(self.size)
        else:
            return self._build_triangle_board(self.size)

    def _build_english_board(self, n):
        board = [[1 for _ in range(n)] for _ in range(n)]
        arm = n // 2 - 1
        for r in range(n):
            for c in range(n):
                if (r < arm and c < arm) or \
                   (r < arm and c >= n - arm) or \
                   (r >= n - arm and c < arm) or \
                   (r >= n - arm and c >= n - arm):
                    board[r][c] = -1
        board[n//2][n//2] = 0
        return board

    def _build_european_board(self, n):
        board = [[1 for _ in range(n)] for _ in range(n)]
        mid = n // 2
        threshold = mid + (mid // 2)
        for r in range(n):
            for c in range(n):
                if abs(r - mid) + abs(c - mid) > threshold:
                    board[r][c] = -1
        board[mid][mid] = 0
        return board

    def _build_triangle_board(self, n):
        board = []
        for r in range(n):
            row = []
            for c in range(n):
                if c <= r:
                    row.append(1)
                else:
                    row.append(-1)
            board.append(row)
        board[0][0] = 0
        return board

    # ---------------- Game Logic ----------------

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] != -1

    def try_move(self, sr, sc, dr, dc):
        if not self.in_bounds(sr, sc) or not self.in_bounds(dr, dc):
            return False

        if self.board[sr][sc] != 1 or self.board[dr][dc] != 0:
            return False

        rr = dr - sr
        cc = dc - sc

        if self.board_type in ("English", "European"):
            if (abs(rr), abs(cc)) not in [(2, 0), (0, 2)]:
                return False
            mr = sr + rr // 2
            mc = sc + cc // 2
        else:
            if (rr, cc) not in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2)]:
                return False
            mr = sr + rr // 2
            mc = sc + cc // 2

        if not self.in_bounds(mr, mc):
            return False
        if self.board[mr][mc] != 1:
            return False

        # Apply move
        self.board[sr][sc] = 0
        self.board[mr][mc] = 0
        self.board[dr][dc] = 1
        self.move_count += 1
        return True

    def valid_moves_from(self, sr, sc):
        if self.board[sr][sc] != 1:
            return []

        if self.board_type in ("English", "European"):
            steps = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        else:
            steps = [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2)]

        moves = []
        for rr, cc in steps:
            dr, dc = sr + rr, sc + cc
            mr, mc = sr + rr // 2, sc + cc // 2
            if self.in_bounds(dr, dc) and self.in_bounds(mr, mc):
                if self.board[dr][dc] == 0 and self.board[mr][mc] == 1:
                    moves.append((sr, sc, dr, dc))
        return moves

    def is_game_over(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 1 and self.valid_moves_from(r, c):
                    return False
        return True