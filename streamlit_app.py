import streamlit as st
import chess
import chess.svg
import random
from streamlit.components.v1 import html

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.status = "White to move."

st.title("Multiplayer Chess Game")

# Display chessboard
board_svg = chess.svg.board(st.session_state.board, size=400)
st.write("### Current Game State:")
html(f"""<div style='text-align:center;'>{board_svg}</div>""", height=450)

# Input move
if not st.session_state.game_over:
    move = st.text_input("Enter your move (e.g., e2e4):", "")
    if st.button("Make Move"):
        try:
            chess_move = chess.Move.from_uci(move)
            if chess_move in st.session_state.board.legal_moves:
                st.session_state.board.push(chess_move)
                if st.session_state.board.is_game_over():
                    st.session_state.game_over = True
                    st.session_state.status = "Game Over! " + st.session_state.board.result()
                else:
                    st.session_state.status = "Next move..."
            else:
                st.warning("Illegal move! Try again.")
        except:
            st.warning("Invalid move format! Use standard notation like e2e4.")

st.write(st.session_state.status)

# Reset game button
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.status = "White to move."
