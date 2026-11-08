#
# 外部プログラムのサンプル
#
・使い方（すぺてのプログラム共通）
  利用している通信方式によって，以下の 3パターンのどれかを実施。

a. サブモジュールを利用
  * 使用しているプログラム
    - value_calc.py
  * 設定方法
    .mdf ファイルに以下の1行を追記
      Plugin_AnyScript_Command=..\..\..\python.exe -u (プログラム名）
    （プログラム名）は，value_calc.py とか。
  * 起動方法
    MMDAgent-EX を立ち上げると，自動で起動する
    
b. TCP/IP通信を利用
  * 使用しているプログラム
    - dummy_recognizer.py
    - keyboard_talker.py
    - MMDA_connector.py
    - whisper.py
  * 設定方法
    .mdf ファイルに以下の 2行を追記
      Plugin_Remote_EnableServer = true
      Plugin_Remove_ListenPort = 50001
  * 起動方法
    0. MMDAgent-EX を立ち上げておく
    1. ExternalModules フォルダで，PowerShell を開く
       エクスプローラ上で Ctrl キーを押しながら右クリック
       → 「PowerShell ウィンドウをここで開く」を選択
    2. PowerShell ウィンドウ内で以下のコマンドを実行
       ..\..\python.exe ..\..\python.exe （プログラム名）
       （プログラム名）は，dummy_recognizer.py とか
    3. 終了させるのは，Ctrl-C
    
c. 共有メモリを利用
  * 使用しているプログラム
    - camera_test.py
    - intro1.py
    - intro2.py
  * 設定方法
    何も設定する必要はない。起動方法は b と同じ。
    また，a と同じように設定＆起動してもよい。


・個別の説明と使い方

1. dummy_recognizer.py
  * 機能
    キーボードから文字を入力すると，その内容を音声認識結果として 
    MMDAgent-EX に通知する。
  * 起動方法
    ..\..\python.exe dummy_recognizer.py
  * 注意点
    .mdf で本物の音声認識機能を使わないように設定（Plugin_Julius で
    始まる 2行をコメントアウト）し，かわりに dummy_reconizer.py で
    対話をする事も可能。この場合，認識結果と音声合成テキストが
    画面に表示されなくなるので，dummy_recognizer.py -c として起動する
    こと。

2. MMDA_connector.py
  * 機能
    流れてくる各種メッセージのうち，指定したものだけ画面に表示する
  * 起動方法    
    ..\..\python.exe MMDA_connector.py SYNTH_START MMD_CAMERA_GET
    上記のように，表示したいメッセージを指定すること。いくつでも
    指定可能。
    何も指定しないと，すべてのメッセージを表示する

3. keyboard_talker.py
  * 機能
    MMDAgent-EX側でキーが押されると，それに対応した音声を合成する
  * 起動方法
    ..\..\python.exe keyboard_talker.py
  * 注意点
    どのキーを押すと何と話すかは，プログラム内で定義してある  
  
4. value_calc.py
  * 機能
    VALUE_CALC コマンドを使えるように拡張し，変数の四則演算を可能とする
  * 起動方法
    Plugin_AnyScript_Command を設定し，自動で起動する
  * 注意点
    VALUE_CALC コマンドの使い方については，補足資料の「変数とメニュー」
    part 1 を参照すること
    
5. camera_test.py
  * 機能
    このプログラムは，各種ソフトウェアのインストールが問題なく
    できているかのテストを行うものである。
    詳細は「事前準備」の「インストールメモ」を参照すること
    
6. intro1.py，intro2.py
  * 機能
    これらのプログラムは，導入課題の「画像認識」で用いられている。
    詳細は，画像認識の説明資料を参照すること

7. whisper.py，DaemonClient.py
  * 機能
    julius ではなく，外部の音声認識エンジン（OpenAI の whisper）
    を使用して，音声認識を行う。
  * 起動方法
    python にライブラリを導入する必要があるので，個別に相談すること
  *注意点  
    一度に多数のシステムから使用するとトラブルになる可能性がある
    ことから，どうしても利用したい班だけ鈴木まで相談にくること。
