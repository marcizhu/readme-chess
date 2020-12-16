import chess
from collections import defaultdict
from urllib.parse import urlencode


GITHUB_USER      = "marcizhu"      # GitHub user where this file is located
GITHUB_REPO_NAME = "readme-chess"  # GitHub repo for this project
GITHUB_ISSUE_CONTENTS = {
	"title": "Chess: Move {source} to {dest}",
	"body": "Please do not change the title. Just click \"Submit new issue\". You don't need to do anything else :D"
}

GITHUB_ISSUE_LINK = "https://github.com/" + GITHUB_USER + "/" + GITHUB_REPO_NAME + "/issues/new?" + urlencode(GITHUB_ISSUE_CONTENTS, safe="{}")

# Markers
BOARD_BEGIN_MARKER = "<!-- BEGIN CHESS BOARD -->\n"
BOARD_END_MARKER = "<!-- END CHESS BOARD -->\n"

MOVES_BEGIN_MARKER = "<!-- BEGIN MOVES LIST -->\n"
MOVES_END_MARKER = "<!-- END MOVES LIST -->\n"

TURN_BEGIN_MARKER = "<!-- BEGIN TURN -->"
TURN_END_MARKER = "<!-- END TURN -->"


def int2square(num):
	cols = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
	return cols[num %  8] + str(num // 8 + 1)


def create_issue_link(source, dest_list):	
	ret = []

	for dest in dest_list:
		ret.append("[" + dest + "](" + GITHUB_ISSUE_LINK.format(source=source, dest=dest) + ")")

	return ", ".join(ret)


def generate_moves_list(moves):
	# Create dictionary and fill it
	moves_dict = defaultdict(list)

	for move in moves:
		source = int2square(move.from_square)
		dest   = int2square(move.to_square)

		moves_dict[source].append(dest)

	# Write everything in Markdown format
	markdown = ""
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
		"P": "img/white/pawn.png"
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
			if elem == ".":
				markdown += "![][_] | "
			else:
				markdown += "<img src=\"{}\" width=50px> | ".format(get_image_link(elem))

		markdown += "**" + str(9 - row) + "** |\n"

	# Write footer in Markdown format
	markdown += "|   | **A** | **B** | **C** | **D** | **E** | **F** | **G** | **H** |   |\n\n"
	markdown += "[_]: img/blank.png\n"

	return markdown


def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
	if originalText.find(delimeterA) == -1 or originalText.find(delimterB) == -1:
		return originalText

	leadingText = originalText.split(delimeterA)[0]
	trailingText = originalText.split(delimterB)[1]

	return leadingText + delimeterA + replacementText + delimterB + trailingText


def main():
	board = chess.Board() # TODO: Load board
	legal_moves = list(board.legal_moves)

	turn = "white" if board.turn == chess.WHITE else "black"
	moves = generate_moves_list(legal_moves)
	board = board_to_markdown(board)

	with open("README.md", "r+") as file:
		readme = file.read()
		readme = replaceTextBetween(readme, BOARD_BEGIN_MARKER, BOARD_END_MARKER, "{chess_board}")
		readme = replaceTextBetween(readme, MOVES_BEGIN_MARKER, MOVES_END_MARKER, "{moves_list}")
		readme = replaceTextBetween(readme, TURN_BEGIN_MARKER, TURN_END_MARKER, "{turn}")
		file.seek(0) # Truncate file
		file.write(readme.format(chess_board=board, moves_list=moves, turn=turn)) # Write new board & list of movements


if __name__ == "__main__":
	main()
