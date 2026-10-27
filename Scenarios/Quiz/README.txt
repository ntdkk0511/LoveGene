#
# サンプルシナリオ：クイズを行う
#
・使用している機能
  * テキストプロンプトの使い方（PROMPT_SHOW）
  * 変数の使い方（VALUE_SET，VALUE_EVAL）
  * AnyScriptの使用
    - value_calc.py（VALUE_CALC）

・受け付ける対話
  - こんにちは
  - クイズをしましょう
    → クイズを開始する。名前を聞いてきたら，「私の名前は鈴木です」
       のように答える。

・AnyScript の実行方法
  1. quiz.mdf 内の Plugin_AnyScript_Command= の行を有効にする
  2. quiz.fst 内の %INCLUDE(quiz_main.fst) の行をコメントアウトし，
     かわりに %INCLUDE(quiz_main_wCalc.fst) の行を有効にする
     
