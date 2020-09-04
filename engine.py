import chess
import chess.engine
import copy


def chooseMove(board, piece):
    for move in board.legal_moves:
        if(board.piece_at(move.from_square).symbol().lower() == piece.lower()):
            board.push(move)

            analysis = engine.analysis(board,chess.engine.Limit(time=0.3,depth=15))
            analysis.get()

            if(bestMove['cp'].score() < analysis.info['score'].pov(analysis.info['score'].turn).score()):
                bestMove['cp'] = analysis.info['score'].pov(analysis.info['score'].turn)
                bestMove['move'] = move
            board.pop()

    print('BestMove:',bestMove['move'].uci())
    board.push(bestMove['move'])
    print("===============")
    print(board)

receivedPiece = 'P'
receivedBoard = '1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1'
receivedBoard2 = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
board = chess.Board(receivedBoard2)





print("Board Inicial")
print("===============")
print(board)
while(not board.is_game_over()):
    print("===============")
    if(board.turn):
        receivedPiece = input('Escolha a peça (ex. P, N, k, Q, r, B):\n')
    else:
        receivedPiece = input('Escolha a peça (ex. P, N, k, Q, r, B.):\n')
    bestMove = {"cp":chess.engine.Cp(-10000),"move":chess.Move.null()}
    chooseMove(board,receivedPiece)



engine.quit()
