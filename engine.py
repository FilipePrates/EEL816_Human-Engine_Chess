# import chess
# import chess.uci
# print("Hello World")
# # board = chess.Board()
#
# engine = chess.uci.popen_engine("stockfish")
# engine.uci()
# engine.author
# board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
# engine.position(board)
# engine.go(movetime=2000)
# print(board)

# import chess
# import chess.engine
#
# engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")
#
# board = chess.Board()
# while not board.is_game_over():
#     result = engine.play(board, chess.engine.Limit(time=0.1))
#     board.push(result.move)
#
# engine.quit()

from stockfish import Stockfish

stockfish = Stockfish("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
print(stockfish.get_board_visual())
print('melhor move:')
print(stockfish.get_best_move())

# print(stockfish)
