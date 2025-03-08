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
    st.session_state.selected_piece = None
    st.session_state.player_color = "white"

st.title("Multiplayer Chess Game")

# Player color selection
st.write("### Choose Your Side:")
color_choice = st.radio("Select your color:", ["White", "Black"], index=0)
if color_choice == "Black":
    st.session_state.player_color = "black"
else:
    st.session_state.player_color = "white"

# Display chessboard with correct orientation
board_svg = chess.svg.board(st.session_state.board, size=400, flipped=(st.session_state.player_color == "black"))
st.write("### Current Game State:")
html(f"""<div style='text-align:center;'>{board_svg}</div>""", height=450)

# Move selection via mouse click simulation
st.write("### Click to move")
col1, col2 = st.columns(2)
with col1:
    selected_square = st.text_input("Select piece position (e.g., e2):", "")
with col2:
    target_square = st.text_input("Select target position (e.g., e4):", "")

if st.button("Move Piece"):
    if selected_square and target_square:
        move = selected_square + target_square
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
    else:
        st.warning("Please select both positions.")

st.write(st.session_state.status)

# Reset game button
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
    st.session_state.game_over = False
    st.session_state.status = "White to move."

