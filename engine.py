import chess
import chess.engine
import copy

receivedPiece = 'p'
receivedBoard = '1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1'

engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
board = chess.Board(receivedBoard)
print(board.legal_moves)

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
        if(bestMove['cp'].score() > analysis.info['score'].pov(False).score()):
            bestMove['cp'] = analysis.info['score'].pov(False)
            bestMove['move'] = move.uci()
        print('analysis:',analysis.info['score'])
        print("------------------")
print('BestMove:',bestMove['move'])

engine.quit()
