import streamlit as st
import random

# カードの定義
SUITS = ['♠', '♥', '♣', '♦']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# カードのデッキを作成
def create_deck():
    return [f'{rank}{suit}' for suit in SUITS for rank in RANKS]

# ゲームの初期化
def initialize_game():
    deck = create_deck()
    random.shuffle(deck)
    player_hand = [deck.pop() for _ in range(7)]  # プレイヤーに7枚配る
    return deck, player_hand

# カードの出し方
def can_play(card, table_cards):
    if not table_cards:
        return True  # 最初はどのカードでも置ける
    top_card = table_cards[-1]
    rank_order = RANKS.index(card[:-1])  # カードのランク部分
    top_rank_order = RANKS.index(top_card[:-1])
    return abs(rank_order - top_rank_order) == 1  # 1つ隣のカードのみ出せる

# ストリームリットのインターフェース
def main():
    st.title("七ならべ (Seven in a Row)")

    if 'deck' not in st.session_state:
        st.session_state.deck, st.session_state.player_hand = initialize_game()
        st.session_state.table_cards = []  # テーブル上のカード
        st.session_state.game_over = False

    st.write("**あなたの手札**:")
    st.write(st.session_state.player_hand)

    st.write("**テーブル上のカード**:")
    st.write(st.session_state.table_cards)

    if st.session_state.game_over:
        st.write("ゲーム終了！")
        return

    # プレイヤーがカードを出すアクション
    card_to_play = st.selectbox("出すカードを選んでください", st.session_state.player_hand)
    if st.button("カードを出す"):
        if can_play(card_to_play, st.session_state.table_cards):
            st.session_state.player_hand.remove(card_to_play)
            st.session_state.table_cards.append(card_to_play)
            st.success(f"カード {card_to_play} を出しました！")
        else:
            st.error("そのカードは出せません。隣のランクのカードを出してください。")

    # プレイヤーがカードを引くアクション
    if st.button("カードを引く"):
        if len(st.session_state.deck) > 0:
            drawn_card = st.session_state.deck.pop()
            st.session_state.player_hand.append(drawn_card)
            st.success(f"カード {drawn_card} を引きました！")
        else:
            st.warning("デッキにカードがありません。")

    # 勝利判定
    if len(st.session_state.player_hand) == 0:
        st.session_state.game_over = True
        st.success("おめでとうございます！あなたは勝ちました！")

if __name__ == "__main__":
    main()
