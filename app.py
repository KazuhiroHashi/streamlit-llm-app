import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# --- 環境変数をロード ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- LLM関数定義 ---
def get_llm_response(expert_type: str, user_input: str) -> str:
    """ラジオボタンと入力値をもとにLLM応答を返す関数"""
    if not user_input:
        return "質問内容を入力してください。"

    # 選択された専門家ごとにプロンプトを変える
    if expert_type == "健康アドバイザー":
        system_prompt = "あなたは健康や生活習慣の専門家です。何を聞かれても、必ず健康に関連するアドバイスを日本語で提供してください。"
    elif expert_type == "旅行プランナー":
        system_prompt = "あなたは旅行プランナーです。相談内容に対して、何を聞かれても必ず旅行提案に繋げた回答を日本語で行ってください。"
    else:
        system_prompt = "あなたは博識な一般アシスタントです。親切で簡潔に答えてください。"

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, api_key=OPENAI_API_KEY)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input),
    ]

    try:
        response = llm(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {e}"

# --- Streamlit UI構築 ---
st.title("💬 LangChain × LLM 専門家アシスタント")

st.markdown("""
このアプリでは、質問内容に応じて異なる専門家（例：健康アドバイザー・キャリアコンサルタント）が回答します。  
1️⃣ ラジオボタンで専門家を選択  
2️⃣ 質問を入力  
3️⃣ 「実行」ボタンを押して結果を確認  
""")

st.divider()

# --- 専門家の選択 ---
expert_type = st.radio(
    "専門家を選択してください：",
    ["健康アドバイザー", "旅行プランナー"],
    horizontal=True
)

# --- 入力フォーム ---
user_input = st.text_area("質問を入力してください（例：最近眠れないのですが、どうしたらいいですか？）", height=120)

# --- 実行ボタン ---
if st.button("実行"):
    with st.spinner("AIが回答を作成中です..."):
        result = get_llm_response(expert_type, user_input)
    st.divider()
    st.subheader("回答結果")
    st.write(result)
