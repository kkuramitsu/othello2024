!pip install -U kogi-canvas

from kogi_canvas import Canvas
from kogi_canvas import play_othello
import math
import random

BLACK=1
WHITE=2

board = [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,1,2,0,0],
        [0,0,2,1,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False

def can_place(board, stone):
    """
    石を置ける場所を調べる関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def random_place(board, stone):
    """
    石をランダムに置く関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    while True:
        x = random.randint(0, len(board[0]) - 1)
        y = random.randint(0, len(board) - 1)
        if can_place_x_y(board, stone, x, y):
            return x, y

class nekoAI(object):
    def face(self):
        return "🐱"

    # 6×6用の重み付け行列
    WEIGHT_MATRIX = [
        [100, -50, 10, 10, -50, 100],
        [-50, -50, 1, 1, -50, -50],
        [10, 1, 5, 5, 1, 10],
        [10, 1, 5, 5, 1, 10],
        [-50, -50, 1, 1, -50, -50],
        [100, -50, 10, 10, -50, 100]
    ]

    def count_flips(self, board, stone, x, y):
        """
        石を置いたときに裏返せる石の数をカウントする関数。
        """
        if board[y][x] != 0:
            return 0

        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        total_flips = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            flips = 0
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                flips += 1
                nx += dx
                ny += dy
            if flips > 0 and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                total_flips += flips

        return total_flips

    def evaluate_moves(self, board, stone):
        """
        すべての有効な手を評価し、スコア付きでリストを返す。
        """
        moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == 0:  # 空きマス
                    flips = self.count_flips(board, stone, x, y)
                    if flips > 0:  # 裏返せる石がある手のみ評価
                        weight = self.WEIGHT_MATRIX[y][x]  # 重みを取得
                        score = flips + weight  # 石を裏返す数 + 重み
                        moves.append((score, x, y))
        return moves

    def place(self, board, stone):
        moves = self.evaluate_moves(board, stone)
        if moves:
            # スコアが最も高い手を選択
            moves.sort(reverse=True)
            _, x, y = moves[0]
            return x, y
        else:
            # ランダム配置（置ける場所がない場合の保険）
            return random_place(board, stone)

# AIと対戦するゲーム
play_othello(nekoAI())

