import streamlit as st
import numpy as np

# 初期設定
ROWS, COLS = 8, 8
MINES_COUNT = 10

# セッション状態の初期化
if "board" not in st.session_state:
    # -1 は地雷、0以上は周囲の地雷数
    board = np.zeros((ROWS, COLS), dtype=int)
    # 地雷をランダム配置
    mines = np.random.choice(ROWS * COLS, MINES_COUNT, replace=False)
    for m in mines:
        r, c = divmod(m, COLS)
        board[r, c] = -1

    # 周囲の地雷数をカウント
    for r in range(ROWS):
        for c in range(COLS):
            if board[r, c] == -1:
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if board[nr, nc] == -1:
                            count += 1
            board[r, c] = count
    st.session_state.board = board
    st.session_state.revealed = np.zeros((ROWS, COLS), dtype=bool)
    st.session_state.game_over = False
    st.session_state.win = False
    st.session_state.selected_cell = None  # 追加: 選択されたセルを記録する

board = st.session_state.board
revealed = st.session_state.revealed

st.title("💣 マインスイーパー")

def reveal_cell(r, c):
    if st.session_state.game_over:
        return
    if revealed[r, c]:
        return
    revealed[r, c] = True
    if board[r, c] == -1:
        st.session_state.game_over = True
        st.error("💥 地雷を踏みました！ゲームオーバー！")
        return
    elif board[r, c] == 0:
        # 周囲の0のセルも再帰的に開く
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if not revealed[nr, nc]:
                        reveal_cell(nr, nc)

def check_win():
    # 地雷以外の全セルが開かれたら勝ち
    total_cells = ROWS * COLS
    opened_cells = np.sum(revealed)
    if opened_cells == total_cells - MINES_COUNT:
        st.session_state.win = True
        st.success("🎉 おめでとう！地雷を全て避けました！")

# グリッド表示
cols = st.columns(COLS)

for r in range(ROWS):
    for c in range(COLS):
        with cols[c]:
            # ボタンに一意のkeyを追加
            button_key = f"{r}_{c}"
            cell_id = (r, c)  # セルのID（行、列）
            is_selected = st.session_state.selected_cell == cell_id  # セルが選択されているかチェック
            # セルの背景色を変更
            cell_style = f"background-color: {'black' if is_selected else 'white'}; color: {'white' if is_selected else 'black'};"

            if st.session_state.game_over or st.session_state.win:
                # ゲーム終了時は地雷も表示
                if board[r, c] == -1:
                    st.markdown(f'<button style="{cell_style}">💣</button>', unsafe_allow_html=True)
                elif revealed[r, c]:
                    st.markdown(f'<button style="{cell_style}">{str(board[r, c]) if board[r, c] > 0 else ""}</button>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<button style="{cell_style}"></button>', unsafe_allow_html=True)
            else:
                if revealed[r, c]:
                    st.markdown(f'<button style="{cell_style}">{str(board[r, c]) if board[r, c] > 0 else ""}</button>', unsafe_allow_html=True)
                else:
                    # ボタンを押したときにそのセルを選択
                    if st.button("", key=button_key):
                        reveal_cell(r, c)
                        check_win()
                        st.session_state.selected_cell = cell_id  # 選択したセルを記録

# リセットボタン
if st.button("リセット"):
    # セッション状態をリセット
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # 自動でページをリフレッシュ
    st.experimental_rerun()
