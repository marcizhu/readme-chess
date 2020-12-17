import chess
import src.tweaks as tweaks

from collections import defaultdict


def create_link(text, link):
	return "[" + text + "](" + link + ")"


def create_issue_link(source, dest_list):	
	ret = []

	for dest in dest_list:
		ret.append(create_link(dest, tweaks.GITHUB_MOVE_ISSUE_LINK.format(source=source, dest=dest)))

	return ", ".join(ret)


def generate_moves_list(board):
	# Create dictionary and fill it
	moves = list(board.legal_moves)
	moves_dict = defaultdict(list)

	for move in moves:
		source = chess.SQUARE_NAMES[move.from_square].upper()
		dest   = chess.SQUARE_NAMES[move.to_square].upper()

		moves_dict[source].append(dest)

	# Write everything in Markdown format
	markdown = ""

	if board.is_game_over():
		return "**GAME IS OVER!** " + create_link("Click here", tweaks.GITHUB_NEW_GAME_ISSUE_LINK) + " to start a new game :D\n"
	elif board.is_check():
		markdown += "**CHECK!** Choose your move wisely!\n"

	markdown += "|  FROM  | TO (Just click a link!) |\n"
	markdown += "| :----: | :---------------------- |\n"

	for source,dest in moves_dict.items():
		markdown += "| **" + source + "** | " + create_issue_link(source, dest) + " |\n"

	return markdown


def board_to_list(board):
	board_list = []

	for line in board.split('\n'):
		sublist = []
		for item in line.split(' '):
			sublist.append(item)

		board_list.append(sublist)

	return board_list


def get_image_link(piece):
	switcher = {
		"r": "img/black/rook.png",
		"n": "img/black/knight.png",
		"b": "img/black/bishop.png",
		"q": "img/black/queen.png",
		"k": "img/black/king.png",
		"p": "img/black/pawn.png",

		"R": "img/white/rook.png",
		"N": "img/white/knight.png",
		"B": "img/white/bishop.png",
		"Q": "img/white/queen.png",
		"K": "img/white/king.png",
		"P": "img/white/pawn.png",

		".": "img/blank.png"
	}

	return switcher.get(piece, "???")


def board_to_markdown(board):
	l = board_to_list(str(board))
	markdown = ""

	# Write header in Markdown format
	markdown += "|   | A | B | C | D | E | F | G | H |   |\n"
	markdown += "|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"

	# Write board
	for row in range(1, 9):
		markdown += "| **" + str(9 - row) + "** | "
		for elem in l[row - 1]:
			markdown += "<img src=\"{}\" width=50px> | ".format(get_image_link(elem))

		markdown += "**" + str(9 - row) + "** |\n"

	# Write footer in Markdown format
	markdown += "|   | **A** | **B** | **C** | **D** | **E** | **F** | **G** | **H** |   |\n"

	return markdown
