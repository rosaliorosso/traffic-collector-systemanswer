SystemAnswerトラフィック取得ツール
=========

目的
---------------

本ツールは、アイビーシー株式会社が提供するSystem Answer G2よりトラフィック情報を自動で取得するためのツールです
PythonにてSystemAnswerに自動ログインし、対象トラフィックのPNG/CSVをダウンロードします。

事前準備
---------------

ツールを実行する前に下記の設定ファイルに必要事項を記入してください

login.json  

| Left align | Right align |
|:-----------|:------------|
| baseurl    | 必須。SystemAnswerのURL |
| username   | 必須。SystemAnswerのユーザID |
| userpass   | 必須。SystemAnswerのユーザパスワード |

node.json

| Left align | Right align |
|:-----------|:------------|
| hostname     | 必須。トラフィック取得対象のホスト名。ファイル保存名に使用 |
| hostid       | 必須。トラフィック取得対象のホストID。SystemAnswerに登録されているホストIDを入力 |
| graphid      | 必須。トラフィック取得対象のグラフID。SystemAnswerに登録されているホストのIFごとに割り当てられるグラフIDを入力 |
| bandwidth    | 必須。トラフィック取得対象の帯域。グラフ描画時の縦軸上限値に使用 |
| description  | 任意。トラフィック取得対象の注釈。日本語名など |

データ取得
---------------

コマンドラインより下記の書式でツールを実行してください。
`[START_DATE]`と`[END_DATE]`は、YYYY/MM/DD形式で取得開始日と取得終了日を指定してください。

```sh
$ python main.py -h
usage: main.py [-h] --start_date [START_DATE] --end_date [END_DATE]

get SystemAnswer graph download as csv and png

optional arguments:
  -h, --help            show this help message and exit
  --start_date [START_DATE]
                        specify a start date of data. Style: YYYY/MM/DD
  --end_date [END_DATE]
                        specify a end date of data. Style: YYYY/MM/DD
```

出力結果
---------------

outputsフォルダに出力ファイルが置かれます。

動作環境
---------------

ツールの実行にあたり下記のインストールが必要です

* Python3
* Selenium
* Chromedriver
