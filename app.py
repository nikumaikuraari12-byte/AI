import streamlit as st
import random
import pandas as pd

# --- 1. アプリの見た目とタイトル ---
st.title("🛡️ 自律型サイバー防御AI コントロールパネル")
st.write("「うちの子」の経験値をずっと積み上げながら、防衛判断の進化をグラフで可視化するアプリです。")

# --- 2. AIの頭の中（Qテーブル）の初期化（メモリに保持） ---
if 'q_table' not in st.session_state:
    st.session_state.q_table = {
        0: {0: 0.0, 1: 0.0, 2: 0.0}, # 0: 平和
        1: {0: 0.0, 1: 0.0, 2: 0.0}, # 1: ポートスキャン
        2: {0: 0.0, 1: 0.0, 2: 0.0}  # 2: ブルートフォース
    }

# --- 3. 特訓ボタン ---
training_steps = st.slider("1回あたりの特訓回数（エピソード）", 1000, 50000, 10000, step=1000)

if st.button("🚀 AIに新しい特訓をさせる（経験を積み上げる）"):
    alpha = 0.1
    gamma = 0.9
    
    for _ in range(training_steps):
        state = random.choice([0, 1, 2])
        
        if random.uniform(0, 1) < 0.1:
            action = random.choice([0, 1, 2])
        else:
            action = max(st.session_state.q_table[state], key=st.session_state.q_table[state].get)

        if state == 0:
            reward = 1 if action == 0 else -5
        elif state == 1:
            if action == 2: reward = 8
            elif action == 1: reward = 5
            else: reward = -8
        elif state == 2:
            reward = 15 if action == 1 else -15
            
        next_state = 0
        
        old_q = st.session_state.q_table[state][action]
        next_max = max(st.session_state.q_table[next_state].values())
        st.session_state.q_table[state][action] = old_q + alpha * (reward + gamma * next_max - old_q)
        
    st.success(f"✨ {training_steps}回の追加特訓が完了しました！経験値がさらに積み上がっています。")

# --- 4. グラフによる視覚的ビジュアライズ ---
st.subheader("📊 防衛AIの判断力グラフ（行動ごとのスコア）")
st.write("グラフのバーが高いほど、AIが「この状況ではこの対応が正しい！」と強く確信している状態を表します。")

# データをグラフ用に整形
state_names = {0: "状態0: 平和なとき", 1: "状態1: ポートスキャン", 2: "状態2: ブルートフォース"}
action_names = {0: "何もしない", 1: "ブロックする", 2: "警告・制限"}

chart_data = []
for s, actions in st.session_state.q_table.items():
    for a, score in actions.items():
        chart_data.append({
            "状況": state_names[s],
            "行動": action_names[a],
            "スコア": score
        })

df = pd.DataFrame(chart_data)
df_pivot = df.pivot(index="状況", columns="行動", values="スコア")

# Streamlit標準の美しい棒グラフを表示
st.bar_chart(df_pivot)

# 生データを見たいときの折りたたみメニュー
with st.expander("🔍 詳細な数値データ（Qテーブル）を確認する"):
    st.json(st.session_state.q_table)
