# aori-hagemasi-bot
このプログラムはDiscord Botのプログラムです。Discordで渇を入れたり、励ましてくれます。

## 概要
Discord上で動作し、特定のユーザーが発言する度に煽りや励ましのメッセージを一定の確率で返すBotです。元々受験生を対象として作成されたため、受験に向けたメッセージを中心に構成されています。

## 使用技術
- 言語: Python 3.x
- ライブラリ/フレームワーク: discord.py, ndjson, python-dotenv
- データベース: ndjson（ローカルファイルへのJSON保存）
- その他: なし

## 使い方

### 前提条件
- Python 3.x がインストールされていること
- Discord Botのトークンを取得済みであること

### インストール方法
以下の手順に従って、ご自身の環境にプロジェクトをセットアップしてください。

1. リポジトリをクローンします。
```bash
git clone https://github.com/rainyskybow/aori-hagemasi-bot.git
```

2. プロジェクトのディレクトリに移動します。
```bash
cd aori-hagemasi-bot
```

3. 必要なパッケージをインストールします。
```bash
pip install -r requirements.txt
```

### 基本的な使い方
```bash
python main.py
```

## 主な機能
- **`/aori_and_hagemasi [mode]`**
  対象ユーザーへの煽り・励ましのオン・オフを行います。
  - `mode` (必須): `start`（開始）、`stop`（終了）のいずれかを指定します。

- **自動返信機能**
  設定された対象ユーザーが発言した際に、ランダムで受験生向けの煽りや励ましのメッセージを返信します。

## 設定
プロジェクトルートディレクトリにある `.env` ファイルに以下の環境変数を設定してください。
- `token` : Discord Botのトークン

また、`main.py` の以下の部分を書き換えて、対象となるユーザーのIDを設定してください。
```python
# 煽る対象のユーザーのid（int）
user_id = 0 # your target user id
```

## 参考にしたサイト・使用したツール等
- ChatGPT：煽り・励ましメッセージの生成をこれで行いました。（[https://chat.openai.com/](https://chat.openai.com/)）
- note.nkmk.me | Pythonでランダムな小数・整数を生成するrandom, randrange, randintなど：[https://note.nkmk.me/python-random-randrange-randint/](https://note.nkmk.me/python-random-randrange-randint/)

## ライセンス
MIT License
