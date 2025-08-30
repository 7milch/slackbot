# Slack Bot

Slackのリアクションイベントに反応するシンプルなボットアプリケーション。

## 機能

- `:eyes:` リアクションが付けられたメッセージに自動で返信
- Socket Modeを使用したリアルタイムイベント処理

## 必要なSlack App権限

### Bot Token Scopes
- `chat:write` - メッセージを送信する権限
- `reactions:read` - リアクションを読み取る権限

### Event Subscriptions
- `reaction_added` - リアクションが追加された時のイベント

## セットアップ

1. 環境変数を設定
```bash
export SLACK_APP_TOKEN="xapp-xxxxxxxxxxxxx"
export SLACK_BOT_TOKEN="xoxb-xxxxxxxxxxxxx"
```

2. 依存関係をインストール
```bash
pip install slack-sdk
```

3. アプリケーションを実行
```bash
python app.py
```

## 動作

`:eyes:` リアクションが付けられたメッセージに対して、スレッドで自動返信します。
