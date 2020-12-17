import chess

import src.tweaks as tweaks
import src.markdown as markdown


def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
	if originalText.find(delimeterA) == -1 or originalText.find(delimterB) == -1:
		return originalText

	leadingText = originalText.split(delimeterA)[0]
	trailingText = originalText.split(delimterB)[1]

	return leadingText + delimeterA + replacementText + delimterB + trailingText


def main():
	# A game in progress will always be saved inside "current.pgn"
	board = chess.Board() # TODO: Load board
	# If pgn file exists, load and perform specified move. If not, just create new default game and exit
	# Check if this move generated a check mate. If so, also specify this in the README file and as a response
	# in the GH issue. Also, rename the file to something like "chess-yyyymmdd-hhmmss.pgn" so that it is archived & a new round can start

	#from_sq = "A2"
	#to_sq   = "A3"
	#move = chess.Move.from_uci(from_sq.lower() + to_sq.lower()) # TODO: Try to move with promotion to queen, fall back to normal move if invalid
	#valid = move in board.legal_moves
	#print("Board is valid: " + str(board.is_valid()))
	#print("Move is valid: " + str(valid))

	#if valid:
	#	board.push(move)

	legal_moves = list(board.legal_moves)

	turn = "white" if board.turn == chess.WHITE else "black"
	moves = markdown.generate_moves_list(legal_moves) # TODO: if no moves can be played, add a button to start a new game
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
