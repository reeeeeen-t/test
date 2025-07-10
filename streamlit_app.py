import streamlit as st
import random

# タイトル
st.title("🪨✌️📄 ジャンケンゲーム")

# 選択肢
choices = ["グー", "チョキ", "パー"]
user_choice = st.radio("あなたの手を選んでください", choices, horizontal=True)

# コンピューターの手をランダムに決定
if st.button("勝負！"):
    computer_choice = random.choice(choices)

    # 勝敗判定
    if user_choice == computer_choice:
        result = "あいこ！"
    elif (user_choice == "グー" and computer_choice == "チョキ") or \
         (user_choice == "チョキ" and computer_choice == "パー") or \
         (user_choice == "パー" and computer_choice == "グー"):
        result = "あなたの勝ち！ 🎉"
    else:
        result = "あなたの負け... 😢"

    # 結果表示
    st.write(f"あなたの手：{user_choice}")
    st.write(f"コンピューターの手：{computer_choice}")
    st.subheader(result)
