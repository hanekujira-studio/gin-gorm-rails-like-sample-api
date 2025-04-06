#!/usr/bin/env python3
import os
import sys
import json
import requests
import base64

def main():
    # 環境変数から値を取得
    api_key = os.environ.get("OPENAI_API_KEY")
    diff_b64 = os.environ.get("DIFF_CONTENT_B64")
    
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません")
        sys.exit(1)
    
    if not diff_b64:
        print("エラー: DIFF_CONTENT_B64が設定されていません")
        sys.exit(1)
    
    # Base64エンコードされた差分をデコード
    diff_content = base64.b64decode(diff_b64).decode('utf-8', errors='replace')
    # 3000バイトに制限
    diff_content = diff_content[:3000]
    
    print(f"デコードした差分の長さ: {len(diff_content)} バイト")
    
    # QA表フォーマット
    qa_format = """# QA表

| No. | テスト項目 | テスト手順 | 期待結果 | 結果 |
|-----|------------|----------|------------|----------|
| 1 | ... | ... | ... | □ OK<br>□ NG |"""
    
    # プロンプト作成
    prompt = f"""以下はプルリクエストの変更差分です。この差分からQAすべきテスト項目を抽出し、以下のフォーマットに従ってQA表を作成してください：

{qa_format}

変更差分:
{diff_content}"""
    
    # APIリクエスト用のデータ
    data = {
        "model": "gpt-4o-mini-2024-07-18",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    # リクエスト送信
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        response_data = response.json()
        print("OpenAIのレスポンス全体:", file=sys.stderr)
        print(json.dumps(response_data), file=sys.stderr)
        
        # エラーチェック
        if "error" in response_data:
            error_message = response_data["error"].get("message", "不明なエラー")
            print(f"エラーが発生しました: {error_message}", file=sys.stderr)
            # エラーの場合はデフォルトのQA表を返す
            qa_comment = """# QA表

| No. | テスト項目 | テスト手順 | 期待結果 | 結果 |
|-----|------------|----------|------------|----------|
| 1 | 機能テスト | 変更された部分の機能を確認 | 機能が正常に動作する | □ OK<br>□ NG |"""
        else:
            # レスポンスから必要な部分を抽出
            qa_comment = response_data["choices"][0]["message"]["content"]
        
        # 標準出力に結果を出力（GitHub Actions用）
        print(qa_comment)
        
    except Exception as e:
        print(f"例外が発生しました: {str(e)}", file=sys.stderr)
        # 例外発生時はデフォルトのQA表を返す
        qa_comment = """# QA表

| No. | テスト項目 | テスト手順 | 期待結果 | 結果 |
|-----|------------|----------|------------|----------|
| 1 | 機能テスト | 変更された部分の機能を確認 | 機能が正常に動作する | □ OK<br>□ NG |"""
        print(qa_comment)

if __name__ == "__main__":
    main() 