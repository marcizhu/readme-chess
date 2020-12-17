import re
import os
import os.path
import sys
import chess
import chess.pgn

from enum import Enum
from datetime import datetime

import src.tweaks as tweaks
import src.markdown as markdown


class Action(Enum):
	UNKNOWN = 0
	MOVE = 1
	NEW_GAME = 2


def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
	if originalText.find(delimeterA) == -1 or originalText.find(delimterB) == -1:
		return originalText

	leadingText = originalText.split(delimeterA)[0]
	trailingText = originalText.split(delimterB)[1]

	return leadingText + delimeterA + replacementText + delimterB + trailingText


def parse_issue(title):
	if title.lower() == "chess: start new game":
		return (Action.NEW_GAME, None)
	elif "chess: move" in title.lower():
		matchObj = re.match('Chess: Move ([A-H][1-8]) to ([A-H][1-8])', title, re.I)
		
		source = matchObj.group(1)
		dest   = matchObj.group(2)
		return (Action.MOVE, (source + dest).lower())

	return (Action.UNKNOWN, None)


def main():
	print("Issue title: ", end='')
	issue_title = input()
	print("Issue author: ", end='')
	issue_author = input()

	action = parse_issue(issue_title)
	board = chess.Board()

	if action[0] == Action.NEW_GAME:
		if os.path.exists("games/current.pgn") and issue_author != "@" + tweaks.GITHUB_USER:
			sys.exit("ERROR: A current game is in progress. Only the repo owner can start a new issue")

		print("Start new game")
		# Create new game
		game = chess.pgn.Game()
		game.headers["Event"] = tweaks.GITHUB_USER + "'s Online Open Chess Tournament"
		game.headers["Site"] = "https://github.com/" + tweaks.GITHUB_USER + "/" + tweaks.GITHUB_REPO_NAME
		game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
		game.headers["Round"] = "1"

		# Save new game to "games/current.pgn"
		print(game, file=open("games/current.pgn", "w"), end="\n\n")

	elif action[0] == Action.MOVE:
		if not os.path.exists("games/current.pgn"):
			sys.exit("ERROR: There is no game in progress! Start a new game first")

		# Load game from "games/current.pgn"
		pgn_file = open("games/current.pgn")
		game = chess.pgn.read_game(pgn_file)
		board = game.board()

		for move in game.mainline_moves():
			board.push(move)

		print("Perform move " + action[1])

		# TODO: Try to move with promotion to queen, fall back to normal move if invalid
		move = chess.Move.from_uci(action[1])

		# Check if move is valid
		if not move in board.legal_moves:
			sys.exit("ERROR: Move is invalid!")

		# Check if board is valid
		if not board.is_valid():
			sys.exit("ERROR: Board is invalid!")
		
		# Perform move
		board.push(move)
		game.add_main_variation(move, comment=issue_author)

		# Save game to "games/current.pgn"
		print(game, file=open("games/current.pgn", "w"), end="\n\n")

		# If it is a game over, archive current game
		if board.is_game_over():
			os.rename("games/current.pgn", datetime.now().strftime("games/game-%Y%m%d-%H%M%S.pgn"))

	elif action[0] == Action.UNKNOWN:
		sys.exit("ERROR: Unknown action")

	turn = "white" if board.turn == chess.WHITE else "black"
	moves = markdown.generate_moves_list(board)
	board = markdown.board_to_markdown(board)

	with open("README.md", "r+") as file:
		readme = file.read()
		readme = replaceTextBetween(readme, tweaks.BOARD_BEGIN_MARKER, tweaks.BOARD_END_MARKER, "{chess_board}")
		readme = replaceTextBetween(readme, tweaks.MOVES_BEGIN_MARKER, tweaks.MOVES_END_MARKER, "{moves_list}")
		readme = replaceTextBetween(readme, tweaks.TURN_BEGIN_MARKER,  tweaks.TURN_END_MARKER,  "{turn}")
		file.seek(0) # Truncate file
		file.write(readme.format(chess_board=board, moves_list=moves, turn=turn)) # Write new board & list of movements


if __name__ == "__main__":
	main()
