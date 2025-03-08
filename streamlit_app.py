import streamlit as st
import chess
import chess.svg
import random
from streamlit.components.v1 import html
import base64

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.status = "White to move."
    st.session_state.selected_square = None
    st.session_state.player_color = "white"

st.title("Multiplayer Chess Game")

# Custom Styling
st.markdown("""
    <style>
        body {background-color: #2E3440; color: white;}
        .stButton>button {background-color: #8FBCBB; color: black; border-radius: 10px; font-size: 16px;}
        .stRadio div {display: flex; gap: 10px;}
    </style>
""", unsafe_allow_html=True)

# Player color selection
st.write("### Choose Your Side:")
color_choice = st.radio("Select your color:", ["White", "Black"], index=0)
if color_choice == "Black":
    st.session_state.player_color = "black"
else:
    st.session_state.player_color = "white"

# Function to get board image
def render_board():
    board_svg = chess.svg.board(st.session_state.board, size=500, flipped=(st.session_state.player_color == "black"))
    return f"""<div style='text-align:center;'>{board_svg}</div>"""

st.write("### Current Game State:")
html(render_board(), height=500)

# Piece selection
st.write("### Click on a piece to move")
selected_square = st.text_input("Click on piece position (e.g., e2):", "")

# Show possible moves
def get_legal_moves(square):
    legal_moves = [move.uci() for move in st.session_state.board.legal_moves if move.uci().startswith(square)]
    return [move[2:4] for move in legal_moves]

if selected_square:
    possible_moves = get_legal_moves(selected_square)
    if possible_moves:
        move_choice = st.radio("Select where to move:", possible_moves)
        if st.button("Confirm Move"):
            move = selected_square + move_choice
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
    else:
        st.warning("No legal moves for this piece!")

st.write(st.session_state.status)

# Reset game button
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.status = "White to move."
