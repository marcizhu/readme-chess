import re
import os
import os.path
import sys
import chess
import chess.pgn

from github import Github
from enum import Enum
from datetime import datetime

import src.tweaks as tweaks
import src.markdown as markdown


# TODO:
# - Try to promote to queen if possible
# - Use a custom GitHub app instead of relying on the GitHub User Authentication token (!!)
# - Save list of all players in a match and mention them on a check mate/end of game
# - Add info about winner (who wins, remove "Move a black/while piece" message in that round)
# - Save stats about all players, do Top X players list and add it
# - Use an image instead of a raw link to start new games
# - Cleanup, turn this repo into a template. Add info about how to set it up and open source it
# - Move contents to marcizhu/marcizhu


class Action(Enum):
	UNKNOWN = 0
	MOVE = 1
	NEW_GAME = 2

def update_last_moves(line):
	with open("data/last_moves.txt", 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		f.write(line.rstrip('\r\n') + '\n' + content)


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
	g = Github(os.environ["GH_ACCESS_TOKEN"])
	repo = g.get_repo(tweaks.GITHUB_USER + "/" + tweaks.GITHUB_REPO_NAME)
	issue = repo.get_issue(number=int(os.environ["ISSUE_NUMBER"]))

	issue_title  = issue.title
	issue_author = "@" + issue.user.login

	action = parse_issue(issue_title)
	gameboard = chess.Board()

	if action[0] == Action.NEW_GAME:
		if os.path.exists("games/current.pgn") and issue_author != "@" + tweaks.GITHUB_USER:
			sys.exit("ERROR: A current game is in progress. Only the repo owner can start a new issue")

		print("Start new game")
		issue.create_comment(issue_author + " done! New game successfully started!")
		issue.edit(state='closed')

		with open("data/last_moves.txt", 'w') as f:
			f.write("Start game: " + issue_author)

		# Create new game
		game = chess.pgn.Game()
		game.headers["Event"] = tweaks.GITHUB_USER + "'s Online Open Chess Tournament"
		game.headers["Site"] = "https://github.com/" + tweaks.GITHUB_USER + "/" + tweaks.GITHUB_REPO_NAME
		game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
		game.headers["Round"] = "1"

	elif action[0] == Action.MOVE:
		if not os.path.exists("games/current.pgn"):
			sys.exit("ERROR: There is no game in progress! Start a new game first")

		# Load game from "games/current.pgn"
		pgn_file = open("games/current.pgn")
		game = chess.pgn.read_game(pgn_file)
		gameboard = game.board()

		for move in game.mainline_moves():
			gameboard.push(move)

		print("Perform move " + action[1])

		# TODO: Try to move with promotion to queen, fall back to normal move if invalid
		move = chess.Move.from_uci(action[1])

		# Check if move is valid
		if not move in gameboard.legal_moves:
			issue.create_comment(issue_author + " Whaaaat? The move `" + action[1] + "` is invalid!\nMaybe someone squished a move before you. Please try again.")
			issue.edit(state='closed')
			sys.exit("ERROR: Move is invalid!")

		# Check if board is valid
		if not gameboard.is_valid():
			issue.create_comment(issue_author + " Sorry, I can't perform the specified move. The board is invalid!")
			issue.edit(state='closed')
			sys.exit("ERROR: Board is invalid!")
		
		issue.create_comment(issue_author + " done! Successfully played move `" + action[1] + "` for current game.\nThanks for playing!")
		issue.edit(state='closed')

		update_last_moves(action[1] + ": " + issue_author)

		# Perform move
		gameboard.push(move)
		game.end().add_main_variation(move, comment=issue_author)
		game.headers["Result"] = gameboard.result()

	elif action[0] == Action.UNKNOWN:
		issue.create_comment(issue_author + " Sorry, I can't understand the command. Please try again and do not modify the issue title!")
		issue.edit(state='closed')
		sys.exit("ERROR: Unknown action")

	# Save game to "games/current.pgn"
	print(game, file=open("games/current.pgn", "w"), end="\n\n")

	turn = "white" if gameboard.turn == chess.WHITE else "black"
	moves = markdown.generate_moves_list(gameboard)
	board = markdown.board_to_markdown(gameboard)
	lasts = markdown.generate_last_moves()

	# If it is a game over, archive current game
	if gameboard.is_game_over():
		os.rename("games/current.pgn", datetime.now().strftime("games/game-%Y%m%d-%H%M%S.pgn"))
		os.remove("data/last_moves.txt")

	with open("README.md", "r") as file:
		readme = file.read()
		readme = replaceTextBetween(readme, tweaks.BOARD_BEGIN_MARKER, tweaks.BOARD_END_MARKER, "{chess_board}")
		readme = replaceTextBetween(readme, tweaks.MOVES_BEGIN_MARKER, tweaks.MOVES_END_MARKER, "{moves_list}")
		readme = replaceTextBetween(readme, tweaks.TURN_BEGIN_MARKER,  tweaks.TURN_END_MARKER,  "{turn}")
		readme = replaceTextBetween(readme, tweaks.LAST_MOVES_BEGIN_MARKER, tweaks.LAST_MOVES_END_MARKER, "{last_moves}")
		readme = replaceTextBetween(readme, tweaks.TOP_MOVERS_BEGIN_MARKER, tweaks.TOP_MOVERS_END_MARKER, "{top_moves}")

	with open("README.md", "w") as file:
		# Write new board & list of movements
		file.write(readme.format(chess_board=board, moves_list=moves, turn=turn, last_moves=lasts, top_moves="TODO\n"))


if __name__ == "__main__":
	main()
