import chess
import chess.engine
import copy
import os
import keyboard
import time
import voice_processing.microphone as mic
import sys
from voice_processing.DtwSpeechReconizer import DtwSpeechReconizer
from threading import Thread

receivedBoard = '1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1'
receivedBoard2 = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
board = chess.Board(receivedBoard2)
recognizer = DtwSpeechReconizer("actions.txt", 25, 50)

def printBoard(board):
    print("===============")
    print(board)
    print("===============")


def chooseMove(board, piece, turn):
    bestMove = {"cp":chess.engine.Cp(-10000),"move":chess.Move.null()}
    for move in board.legal_moves:
        if(board.piece_at(move.from_square).symbol().lower() == piece.lower()):
            board.push(move)

            analysis = engine.analysis(board,chess.engine.Limit(time=0.3,depth=15))
            analysis.get()

            if(bestMove['cp'].score() < analysis.info['score'].pov(turn).score()):
                bestMove['cp'] = analysis.info['score'].pov(turn)
                bestMove['move'] = move
            board.pop()

    print('BestMove:',bestMove['move'].uci(),'Score',bestMove['cp'])
    board.push(bestMove['move'])
    printBoard(board)


def notRecognized():
    print("Não reconhecido")
    pass

def recognized(label, currentMinDist, sample):
    print(label)
    print(currentMinDist)
    print(sample)
    chooseMove(board, label, board.turn)
    pass

def listenToMic():
    while not board.is_game_over():
        if not keyboard.is_pressed('q'):
            time.sleep(0.001)
            continue
        print("ouvindo")
        mic.recordToFile("output.wav")
        recognizer.recognize("output.wav", True)
        os.remove("output.wav")

recognizer.attachDefaultCallback(recognized)
recognizer.attachFailedCallback(notRecognized)

voiceRecognitionThread = Thread(target = listenToMic)
voiceRecognitionThread.start()

print("Initial Board")
printBoard(board)


while (not board.is_game_over()):
    if keyboard.is_pressed('esc'):
        break
    pass

engine.quit()
print("Jogo finalizado")
quit()