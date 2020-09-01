# from stockfish import Stockfish
#
# stockfish = Stockfish("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
# stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
# print(stockfish.get_board_visual())
# print('melhor move:')
# print(stockfish.get_best_move())
#
# # print(stockfish)

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

import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")

board = chess.Board()


while not board.is_game_over():
    analysis = engine.analysis(board,chess.engine.Limit(time=0.1),info='INFO_ALL')
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print('ãnalysis',analysis.info)
    print(result)
    board.push(result.move)
    print(board)
    print("--------------------")

engine.quit()

import asyncio
import chess
import chess.engine

async def main() -> None:
    board = chess.Board()
    transport, engine = await chess.engine.popen_uci("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
    print(board)
    with await engine.analysis(board) as analysis:
        async for info in analysis:            # Arbitrary stop condition.
            if info.get("seldepth", 0) == 10:
                print(info.get("pv"))
                for move in info.get("pv"):
                     board.push(move)
                     print(move)
                break

    await engine.quit()

asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())
