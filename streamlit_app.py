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
    
    # 七のカードを最初に出す
    sevens = [card for card in deck if card.startswith('7')]
    if len(sevens) > 0:
        # プレイヤーに七のカードを配る
        player_hand = [sevens.pop() for _ in range(7)]
    else:
        # 七のカードがなければ再シャッフル
        return initialize_game()
    
    return deck, player_hand, sevens

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
        st.session_state.deck, st.session_state.player_hand, st.session_state.sevens = initialize_game()
        st.session_state.table_cards = []  # テーブル上のカード
        st.session_state.game_over = False

    st.write("**あなたの手札**:")
    st.write(st.session_state.player_hand)

    st.write("**テーブル上のカード**:")
    st.write(st.session_state.table_cards)

    if st.session_state.game_over:
        st.write("ゲーム終了！")
        return

    # 最初に出すカードは「七」のカード
    sevens_in_hand = [card for card in st.session_state.player_hand if card.startswith('7')]
    
    if len(sevens_in_hand) > 0:
        # プレイヤーが「七」のカードを出せる
        card_to_play = st.selectbox("出す七のカードを選んでください", sevens_in_hand)
        if st.button("カードを出す"):
            st.session_state.player_hand.remove(card_to_play)
            st.session_state.table_cards.append(card_to_play)
            st.success(f"カード {card_to_play} を出しました！")
    else:
        st.warning("七のカードを出してください！")

    # プレイヤーが隣り合うカードを出す
    if len(st.session_state.table_cards) > 0:
        last_card = st.session_state.table_cards[-1]
        valid_cards = [card for card in st.session_state.player_hand if can_play(card, st.session_state.table_cards)]
        
        if valid_cards:
            card_to_play = st.selectbox("隣り合うカードを選んでください", valid_cards)
            if st.button("カードを出す"):
                st.session_state.player_hand.remove(card_to_play)
                st.session_state.table_cards.append(card_to_play)
                st.success(f"カード {card_to_play} を出しました！")
        else:
            st.warning("隣り合うカードを選んでください。")

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
