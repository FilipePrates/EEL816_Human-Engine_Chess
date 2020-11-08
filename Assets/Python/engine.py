# -*- coding: utf-8 -*-
import chess
import chess.engine
import copy
import os
import keyboard
import voice_processing.microphone as mic
import sys
from voice_processing import *
import time
import zmq

receivedBoard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-11-win\Windows\stockfish_20011801_x64")
board = chess.Board(receivedBoard)

#recognizer = DtaiDtwSpeechReconizer("actions.txt", 25, 50)
#recognizer = FastDtwSpeechReconizer("actions.txt", 25, 100)
#recognizer = PyDtwSpeechReconizer("actions.txt", 25, 50) # Ainda n funciona
recognizer = CyDtwSpeechReconizer("actions.txt", 1.5, 5, 5)
context = zmq.Context()
socket = context.socket(zmq.REP)

def sendMessage(message):
    socket.send(bytes(message, 'utf-8'))

def printBoard():
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

    selectedMove = bestMove['move']
    print('BestMove:',selectedMove.uci(),'Score',bestMove['cp'])
    board.push(selectedMove)
    printBoard()
    return selectedMove.uci()

def notRecognized():
    print("Not recognized")
    socket.send(b"Fail")
    pass

def recognized(label, currentMinDist):
    print(label)
    print(currentMinDist)
    move = chooseMove(board, label, board.turn)
    sendMessage(move)
    pass
   
recognizer.attachDefaultCallback(recognized)
recognizer.attachFailedCallback(notRecognized)

print("Initial Board")
printBoard()


socket.bind("tcp://*:5555")

try:
    while (not board.is_game_over()):
        #  Wait for next request from client
        message = socket.recv()

        if (message == b"endGame"):
            sendMessage("finished")
            break
        elif (message == b"printBoard"):
            printBoard()
            sendMessage(board)
        elif (message == b"listen"):
            print("ouvindo")
            mic.recordToFile("output.wav")
            recognizer.recognizeFile("output.wav", True)
            os.remove("output.wav")

        print(message)
        print("Received request: %s" % message)
        time.sleep(0.01)
except KeyboardInterrupt:
    pass

engine.quit()
print("Jogo finalizado")
quit()