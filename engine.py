import chess
import chess.engine
import copy

receivedPiece = 'P'
receivedBoard = '1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1'
receivedBoard2 = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
board = chess.Board(receivedBoard2)
print("Board Inicial")
print(board)
print(board.legal_moves)

receivedPiece = input('Escolha a peça (ex. p, N, k, Q, R, r,..)')
bestMove = {"cp":chess.engine.Cp(0),"move":""}

for move in board.legal_moves:
    if(board.piece_at(move.from_square).symbol() == receivedPiece):
        print('Move: ',move.uci())
        print('Piece: ',board.piece_at(move.from_square))
        boardAux = copy.deepcopy(board)
        boardAux.push(move)
        print(boardAux)
        analysis = engine.analysis(boardAux,chess.engine.Limit(time=0.3,depth=10))
        analysis.get()
        # Esse scoring ta estranho...
        print('haha',analysis.info['score'].white())
        if(bestMove['cp'].score() > analysis.info['score'].pov(analysis.info['score'].white()).score()):
            bestMove['cp'] = analysis.info['score'].pov(False)
            bestMove['move'] = move
        print('analysis:',analysis.info['score'])
        print("------------------")

print('BestMove:',bestMove['move'].uci())
board.push(bestMove['move'])
print(board)




engine.quit()
