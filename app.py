import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv
load_dotenv()

# LLMからの回答を取得する関数
def get_llm_response(user_input, expert_type):
    """
    LLMに質問を送信し、回答を取得する関数
    
    Args:
        user_input (str): ユーザーからの入力テキスト
        expert_type (str): 専門家のタイプ（「ファッションスタイリスト」または「栄養士」）
    
    Returns:
        str: LLMからの回答
    """
    # 専門家タイプに応じてシステムメッセージを設定
    if expert_type == "ファッションスタイリスト":
        system_message = SystemMessage(content="あなたは優秀なファッションスタイリストです。")
    else:  # 栄養士
        system_message = SystemMessage(content="あなたは優秀な栄養士です。")
    
    # メッセージの作成
    messages = [
        system_message,
        HumanMessage(content=user_input),
    ]
    
    # LLMの初期化と実行
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    result = llm(messages)
    
    return result.content

# ページ設定
st.set_page_config(
    page_title="AI専門家アシスタント",
    page_icon="🤖",
    layout="centered"
)

# タイトルと説明
st.title("🤖 AI専門家アシスタント")
st.markdown("""
### 📝 アプリの概要
このアプリは、LangChainとOpenAI APIを使用して、様々な専門家の視点からあなたの質問に回答します。
専門家のタイプを選択し、質問を入力するだけで、AIが専門的なアドバイスを提供します。

### 🔧 操作方法
1. **サイドバー**でOpenAI APIキーを入力してください
2. **専門家のタイプ**をラジオボタンで選択してください
3. **質問内容**を入力フォームに記入してください
4. **「回答を取得」ボタン**をクリックして、AIからの回答を受け取ってください
""")

st.markdown("---")

# サイドバーでAPIキーを入力
with st.sidebar:
    st.header("⚙️ 設定")
    openai_api_key = st.text_input(
        "OpenAI APIキー", 
        type="password",
        help="OpenAIのAPIキーを入力してください"
    )
    
    if openai_api_key:
        st.success("✅ APIキーが設定されました")
    else:
        st.warning("⚠️ APIキーを入力してください")
    
    st.markdown("---")
    st.markdown("### ℹ️ 情報")
    st.markdown("**使用モデル**: gpt-4o-mini")
    st.markdown("**Temperature**: 0")
    st.markdown("**バージョン**: 1.0.0")

# メインコンテンツ
st.subheader("👨‍⚕️ 専門家を選択")

# ラジオボタンで専門家を選択
expert_type = st.radio(
    "どの専門家に相談しますか？",
    ["ファッションスタイリスト", "栄養士"],
    horizontal=True,
    help="選択した専門家の視点からアドバイスを受けられます"
)

# 選択された専門家に応じたアイコンと説明を表示
if expert_type == "ファッションスタイリスト":
    st.info("👔 **ファッションスタイリスト**: コーディネート、トレンド、ファッションに関するアドバイスを提供します")
else:
    st.info("🥗 **栄養士**: 栄養、食事、健康的な食生活に関するアドバイスを提供します")

st.markdown("---")

st.subheader("💬 質問を入力")

# 入力フォーム
user_input = st.text_area(
    "質問内容",
    placeholder="例：フォーマルな場にふさわしいコーディネートを教えてください。" if expert_type == "ファッションスタイリスト" else "例：筋肉をつけるためにおすすめの食事メニューを教えてください。",
    height=150,
    help="専門家に聞きたい内容を詳しく入力してください"
)

# 回答取得ボタン
if st.button("🚀 回答を取得", type="primary", use_container_width=True):
    # バリデーション
    if not openai_api_key:
        st.error("⚠️ サイドバーからOpenAI APIキーを入力してください。")
    elif not user_input:
        st.error("⚠️ 質問内容を入力してください。")
    else:
        # APIキーを環境変数に設定
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        try:
            with st.spinner(f"{expert_type}が回答を考えています...🤔"):
                # LLMから回答を取得
                response = get_llm_response(user_input, expert_type)
                
                # 結果の表示
                st.success("✨ 回答が生成されました！")
                st.markdown("### 💡 回答")
                st.markdown(f"**{expert_type}からのアドバイス:**")
                st.write(response)
                
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
            st.info("💡 APIキーが正しいか、または必要なパッケージがインストールされているか確認してください。")

# フッター
st.markdown("---")
st.markdown("*Powered by LangChain and OpenAI*")
