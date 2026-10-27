#
# サンプルシナリオ：外部モジュールのテスト
#
・使用している機能
  * TCP/IPを使った外部モジュールとの通信（Plugin_Remote）

・実行方法
  0. python をインストールしておく
  1. module_test.mdf をダブルクリックし，MMDAgent-EX を立ち上げる
  2. ../../ExternalModules/ に行き，コマンドプロンプトを 3つ立ち上げる
  3. 立ち上げたコマンドプロンプトで，それぞれ以下のコマンドを実行する
     3-1. ../../python.exe dummy_recognizer.py
     3-2. ../../python.exe keyboard_talker.py
     3-3. ../../python.exe MMDA_connector.py all

・受け付ける対話
  - こんにちは

・外部モジュールの説明
  * dummy_recognizer.py
    音声認識モジュールのかわり。
    キーボードから文字を入力すると，それを音声認識結果として RECOG_EVENT_STOP
    メッセージを流す。
    Plugin_Julius が指定されていない時は，音声認識結果が画面に表示されないので，
    その時は dummy_recognizer.py -c とすると表示されるようになる。

  * keyboard_talker.py
    KEY メッセージを受けとり，プログラム内で定義した文章を SYNTH_START 
    メッセージで流す。
    定義されている文章はみっつ。1〜3 のキーに割り当てられているので，
    MMDAgent-EX の画面で，1〜3のキーを押すとジェネが話す。
    それ以外のキーを押すと，「定義されていません」と話す。

  * MMDA_connector.py
    流れてくるメッセージを表示する。
    立ち上げ時，引数にメッセージ名を列挙すると，それらのメッセージ
    だけ表示する。
    例） python.exe MMDA_connector.py RECOG_EVENT_STOP SYNTH_START KEY

・おまけ
  module_test.mdf 内の Plugin_Julis_lang と Plugin_Julius_conf をコメントアウト
  し，かわりに Plugin_AnyScript_Command の行を有効にすると，
  外部の音声認識エンジン（whisper）を利用することができる。
  ただし，これを使う場合は，事前に pyaudio をインストールしておく必要がある。
    1. media2v1 のフォルダでコマンドプロンプトを立ち上げる
    2. ./python.exe -m pip install --upgrade pip
    3. ./python.exe -m pip install pyaudio

  また，複数で同時に whisper を使うとうまく認識してくれない場合があるので
  使用は推奨しない。

