import streamlit as st
import random

# カードの定義
SUITS = ['♠', '♥', '♣', '♦']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# デッキを作成
def create_deck():
    deck = [f'{rank}{suit}' for suit in SUITS for rank in RANKS]
    deck *= 2  # ペアを作るために2セット
    random.shuffle(deck)  # シャッフルしてランダムに並べる
    return deck

# ゲームの初期化
def initialize_game():
    deck = create_deck()
    board = ['🃏'] * len(deck)  # カードはすべて裏向き
    return deck, board, []

# プレイヤーがカードをめくるアクション
def flip_card(card_idx, board, deck, flipped_cards):
    if card_idx not in flipped_cards:
        flipped_cards.append(card_idx)
        board[card_idx] = deck[card_idx]
    return flipped_cards

# 勝利判定
def check_win(board):
    return '🃏' not in board  # すべてのカードが表向きであれば勝ち

# ストリームリットのインターフェース
def main():
    st.title("真剣衰弱 (Memory Game)")

    # ゲームの初期化
    if 'deck' not in st.session_state:
        st.session_state.deck, st.session_state.board, st.session_state.flipped_cards = initialize_game()
        st.session_state.matched_pairs = 0
        st.session_state.game_over = False

    # ゲームの進行
    if st.session_state.game_over:
        st.success("おめでとうございます！すべてのペアを見つけました！")
        return

    # ボードの表示
    num_cards = len(st.session_state.board)
    cols = st.columns(4)  # 4列にカードを配置

    for i in range(num_cards):
        with cols[i % 4]:  # 4列の中で順番に配置
            if st.button(st.session_state.board[i], key=f'card_{i}'):
                if i not in st.session_state.flipped_cards:
                    # カードをめくる
                    st.session_state.flipped_cards = flip_card(i, st.session_state.board, st.session_state.deck, st.session_state.flipped_cards)

                    # めくったカードが2枚になったらペアチェック
                    if len(st.session_state.flipped_cards) == 2:
                        card1_idx, card2_idx = st.session_state.flipped_cards
                        if st.session_state.deck[card1_idx] == st.session_state.deck[card2_idx]:
                            st.session_state.matched_pairs += 1
                            st.session_state.board[card1_idx] = st.session_state.deck[card1_idx]
                            st.session_state.board[card2_idx] = st.session_state.deck[card2_idx]
                            st.session_state.flipped_cards = []  # カードをリセット
                            if check_win(st.session_state.board):
                                st.session_state.game_over = True  # ゲーム終了
                        else:
                            # ペアが一致しない場合、少し待って裏返す
                            st.session_state.flipped_cards = []

    # ゲーム状況の表示
    st.write(f"一致したペア: {st.session_state.matched_pairs}")
    st.write(f"残りのペア: {(num_cards // 2) - st.session_state.matched_pairs}")

if __name__ == "__main__":
    main()
