#!/usr/bin/env python3
import os       # 環境変数アクセス用
import sys      # 標準出力・エラー出力・終了コード用
import json     # JSONデータの処理用
import requests # HTTP通信用
import base64   # Base64エンコード・デコード用

def main():
    """
    メイン関数 - OpenAI APIを使用してPRの差分からQA表を生成する
    """
    # 環境変数から必要な値を取得
    api_key = os.environ.get("OPENAI_API_KEY")    # OpenAI APIキー
    diff_b64 = os.environ.get("DIFF_CONTENT_B64") # Base64エンコードされた差分データ
    
    # APIキーのチェック
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません")
        sys.exit(1)  # エラーコードで終了
    
    # 差分データのチェック
    if not diff_b64:
        print("エラー: DIFF_CONTENT_B64が設定されていません")
        sys.exit(1)  # エラーコードで終了
    
    # Base64エンコードされた差分をデコード
    # errors='replace'は不正なUTF-8シーケンスを置換文字に置き換える
    diff_content = base64.b64decode(diff_b64).decode('utf-8', errors='replace')
    
    # 差分データを3000バイトに制限（APIの文脈長制限対策）
    diff_content = diff_content[:3000]
    
    # デバッグ情報を標準エラー出力に出力
    print(f"デコードした差分の長さ: {len(diff_content)} バイト", file=sys.stderr)
    
    # QA表のフォーマット定義
    qa_format = """# QA表案

| No. | テスト項目 | テスト手順 | 期待結果 |
|-----|------------|----------|------------|
| 1 | ... | ... | ... | □ OK<br>□ NG |"""
    
    # OpenAI APIに送信するプロンプトを構築
    prompt = f"""以下はプルリクエストの変更差分です。
まず、この変更内容の概要を3-5行程度でまとめてください。
次に、この差分からQAすべきテスト項目を抽出し、以下のフォーマットに従ってQA表を作成してください。

期待する出力形式:
```
## 変更概要
（ここに変更の概要を3-5行で記載）

{qa_format}
```

変更差分:
{diff_content}"""
    
    # APIリクエスト用のJSONデータを構築
    data = {
        "model": "gpt-4o-mini-2024-07-18",  # 使用するモデル
        "messages": [{"role": "user", "content": prompt}],  # ユーザーメッセージ
        "temperature": 0.3  # 低い温度で一貫した結果を得る
    }
    
    # リクエストヘッダーを設定
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        # OpenAI APIにリクエスト送信
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data  # ここでrequestsライブラリが自動的にJSONシリアライズを行う
        )
        
        # レスポンスをJSONとしてパース
        response_data = response.json()
        
        # デバッグ情報をログに出力
        print("OpenAIのレスポンス全体:", file=sys.stderr)
        print(json.dumps(response_data), file=sys.stderr)
        
        # エラーチェック
        if "error" in response_data:
            # APIからエラーが返された場合
            error_message = response_data["error"].get("message", "不明なエラー")
            print(f"エラーが発生しました: {error_message}", file=sys.stderr)
            
            # エラーの場合はデフォルトのQA表を返す
            qa_comment = """## 変更概要
変更内容を自動で解析できませんでした。

# QA表案

| No. | テスト項目 | テスト手順 | 期待結果 |
|-----|------------|----------|------------|
| 1 | 機能テスト | 変更された部分の機能を確認 | 機能が正常に動作する |"""
        else:
            # 成功した場合、レスポンスから必要な部分を抽出
            qa_comment = response_data["choices"][0]["message"]["content"]
        
        # 標準出力に結果を出力（GitHub Actions用）
        # GitHub Actionsではこの出力を変数として取得できる
        print(qa_comment)
        
    except Exception as e:
        # 例外処理（ネットワークエラーなど）
        print(f"例外が発生しました: {str(e)}", file=sys.stderr)
        
        # 例外発生時もデフォルトのQA表を返す
        qa_comment = """## 変更概要
APIリクエスト中にエラーが発生したため、変更内容を解析できませんでした。

# QA表案

| No. | テスト項目 | テスト手順 | 期待結果 |
|-----|------------|----------|------------|
| 1 | 機能テスト | 変更された部分の機能を確認 | 機能が正常に動作する |"""
        print(qa_comment)

if __name__ == "__main__":
    # スクリプトが直接実行された場合のみmain関数を実行
    main() 