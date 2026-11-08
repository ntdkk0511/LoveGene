#
# Making userdic for MMDAgent-EX
#
import re
import sys
import argparse 

HTKDIC = "C:\\Program Files (x86)\\Osaka Institute of Technology\\MMDAgentEX\\AppData\\Julius\\dictation_kit_ja\\lang_m\\bccwj.60k.pdp.htkdic"

yomi2roma = []
yomi2roma.append({
    "う゛ぁ" : "b a ",
    "う゛ぃ" : "b i ",
    "う゛ぇ" : "b e ",
    "う゛ぉ" : "b o ",
    "う゛ゅ" : "by u ",
})

yomi2roma.append({
    "ぅ゛" : "b u ",
    "あぁ" : "a a ",
    "いぃ" : "i i ",
    "いぇ" : "i e ",
    "いゃ" : "y a ",
    "うぅ" : "u: ",
    "えぇ" : "e e ",
    "おぉ" : "o: ",
    "かぁ" : "k a: ",
    "きぃ" : "k i: ",
    "くぅ" : "k u: ",
    "くゃ" : "ky a ",
    "くゅ" : "ky u ",
    "くょ" : "ky o ",
    "けぇ" : "k e: ",
    "こぉ" : "k o: ",
    "がぁ" : "g a: ",
    "ぎぃ" : "g i: ",
    "ぐぅ" : "g u: ",
    "ぐゃ" : "gy a ",
    "ぐゅ" : "gy u ",
    "ぐょ" : "gy o ",
    "げぇ" : "g e: ",
    "ごぉ" : "g o: ",
    "さぁ" : "s a: ",
    "しぃ" : "sh i: ",
    "すぅ" : "s u: ",
    "すゃ" : "sh a ",
    "すゅ" : "sh u ",
    "すょ" : "sh o ",
    "せぇ" : "s e: ",
    "そぉ" : "s o: ",
    "ざぁ" : "z a: ",
    "じぃ" : "j i: ",
    "ずぅ" : "z u: ",
    "ずゃ" : "zy a ",
    "ずゅ" : "zy u ",
    "ずょ" : "zy o ",
    "ぜぇ" : "z e: ",
    "ぞぉ" : "z o: ",
    "たぁ" : "t a: ",
    "ちぃ" : "ch i: ",
    "つぁ" : "ts a ",
    "つぃ" : "ts i ",
    "つぅ" : "ts u: ",
    "つゃ" : "ch a ",
    "つゅ" : "ch u ",
    "つょ" : "ch o ",
    "つぇ" : "ts e ",
    "つぉ" : "ts o ",
    "てぇ" : "t e: ",
    "とぉ" : "t o: ",
    "だぁ" : "d a: ",
    "ぢぃ" : "j i: ",
    "づぅ" : "d u: ",
    "づゃ" : "zy a ",
    "づゅ" : "zy u ",
    "づょ" : "zy o ",
    "でぇ" : "d e: ",
    "どぉ" : "d o: ",
    "なぁ" : "n a: ",
    "にぃ" : "n i: ",
    "ぬぅ" : "n u: ",
    "ぬゃ" : "ny a ",
    "ぬゅ" : "ny u ",
    "ぬょ" : "ny o ",
    "ねぇ" : "n e: ",
    "のぉ" : "n o: ",
    "はぁ" : "h a: ",
    "ひぃ" : "h i: ",
    "ふぅ" : "f u: ",
    "ふゃ" : "hy a ",
    "ふゅ" : "hy u ",
    "ふょ" : "hy o ",
    "へぇ" : "h e: ",
    "ほぉ" : "h o: ",
    "ばぁ" : "b a: ",
    "びぃ" : "b i: ",
    "ぶぅ" : "b u: ",
    "ふゃ" : "hy a ",
    "ぶゅ" : "by u ",
    "ふょ" : "hy o ",
    "べぇ" : "b e: ",
    "ぼぉ" : "b o: ",
    "ぱぁ" : "p a: ",
    "ぴぃ" : "p i: ",
    "ぷぅ" : "p u: ",
    "ぷゃ" : "py a ",
    "ぷゅ" : "py u ",
    "ぷょ" : "py o ",
    "ぺぇ" : "p e: ",
    "ぽぉ" : "p o: ",
    "まぁ" : "m a: ",
    "みぃ" : "m i: ",
    "むぅ" : "m u: ",
    "むゃ" : "my a ",
    "むゅ" : "my u ",
    "むょ" : "my o ",
    "めぇ" : "m e: ",
    "もぉ" : "m o: ",
    "やぁ" : "y a: ",
    "ゆぅ" : "y u: ",
    "ゆゃ" : "y a: ",
    "ゆゅ" : "y u: ",
    "ゆょ" : "y o: ",
    "よぉ" : "y o: ",
    "らぁ" : "r a: ",
    "りぃ" : "r i: ",
    "るぅ" : "r u: ",
    "るゃ" : "ry a ",
    "るゅ" : "ry u ",
    "るょ" : "ry o ",
    "れぇ" : "r e: ",
    "ろぉ" : "r o: ",
    "わぁ" : "w a: ",
    "をぉ" : "o: ",
    "う゛" : "b u ",
    "でぃ" : "d i ",
    "でぇ" : "d e: ",
    "でゃ" : "dy a ",
    "でゅ" : "dy u ",
    "でょ" : "dy o ",
    "てぃ" : "t i ",
    "てぇ" : "t e: ",
    "てゃ" : "ty a ",
    "てゅ" : "ty u ",
    "てょ" : "ty o ",
    "すぃ" : "s i ",
    "ずぁ" : "z u a ",
    "ずぃ" : "z i ",
    "ずぅ" : "z u ",
    "ずゃ" : "zy a ",
    "ずゅ" : "zy u ",
    "ずょ" : "zy o ",
    "ずぇ" : "z e ",
    "ずぉ" : "z o ",
    "きゃ" : "ky a ",
    "きゅ" : "ky u ",
    "きょ" : "ky o ",
    "しゃ" : "sh a ",
    "しゅ" : "sh u ",
    "しぇ" : "sh e ",
    "しょ" : "sh o ",
    "ちゃ" : "ch a ",
    "ちゅ" : "ch u ",
    "ちぇ" : "ch e ",
    "ちょ" : "ch o ",
    "とぅ" : "t u ",
    "とゃ" : "ty a ",
    "とゅ" : "ty u ",
    "とょ" : "ty o ",
    "どぁ" : "d o a ",
    "どぅ" : "d u ",
    "どゃ" : "dy a ",
    "どゅ" : "dy u ",
    "どょ" : "dy o ",
    "どぉ" : "d o: ",
    "にゃ" : "ny a ",
    "にゅ" : "ny u ",
    "にょ" : "ny o ",
    "ひゃ" : "hy a ",
    "ひゅ" : "hy u ",
    "ひょ" : "hy o ",
    "みゃ" : "my a ",
    "みゅ" : "my u ",
    "みょ" : "my o ",
    "りゃ" : "ry a ",
    "りゅ" : "ry u ",
    "りょ" : "ry o ",
    "ぎゃ" : "gy a ",
    "ぎゅ" : "gy u ",
    "ぎょ" : "gy o ",
    "ぢぇ" : "j e ",
    "ぢゃ" : "j a ",
    "ぢゅ" : "j u ",
    "ぢょ" : "j o ",
    "じぇ" : "j e ",
    "じゃ" : "j a ",
    "じゅ" : "j u ",
    "じょ" : "j o ",
    "びゃ" : "by a ",
    "びゅ" : "by u ",
    "びょ" : "by o ",
    "ぴゃ" : "py a ",
    "ぴゅ" : "py u ",
    "ぴょ" : "py o ",
    "うぁ" : "u a ",
    "うぃ" : "w i ",
    "うぇ" : "w e ",
    "うぉ" : "w o ",
    "ふぁ" : "f a ",
    "ふぃ" : "f i ",
    "ふぅ" : "f u ",
    "ふゃ" : "hy a ",
    "ふゅ" : "hy u ",
    "ふょ" : "hy o ",
    "ふぇ" : "f e ",
    "ふぉ" : "f o ",
})
yomi2roma.append({
    "あ" : "a ",
    "い" : "i ",
    "う" : "u ",
    "え" : "e ",
    "お" : "o ",
    "か" : "k a ",
    "き" : "k i ",
    "く" : "k u ",
    "け" : "k e ",
    "こ" : "k o ",
    "さ" : "s a ",
    "し" : "sh i ",
    "す" : "s u ",
    "せ" : "s e ",
    "そ" : "s o ",
    "た" : "t a ",
    "ち" : "ch i ",
    "つ" : "ts u ",
    "て" : "t e ",
    "と" : "t o ",
    "な" : "n a ",
    "に" : "n i ",
    "ぬ" : "n u ",
    "ね" : "n e ",
    "の" : "n o ",
    "は" : "h a ",
    "ひ" : "h i ",
    "ふ" : "f u ",
    "へ" : "h e ",
    "ほ" : "h o ",
    "ま" : "m a ",
    "み" : "m i ",
    "む" : "m u ",
    "め" : "m e ",
    "も" : "m o ",
    "ら" : "r a ",
    "り" : "r i ",
    "る" : "r u ",
    "れ" : "r e ",
    "ろ" : "r o ",
    "が" : "g a ",
    "ぎ" : "g i ",
    "ぐ" : "g u ",
    "げ" : "g e ",
    "ご" : "g o ",
    "ざ" : "z a ",
    "じ" : "j i ",
    "ず" : "z u ",
    "ぜ" : "z e ",
    "ぞ" : "z o ",
    "だ" : "d a ",
    "ぢ" : "j i ",
    "づ" : "z u ",
    "で" : "d e ",
    "ど" : "d o ",
    "ば" : "b a ",
    "び" : "b i ",
    "ぶ" : "b u ",
    "べ" : "b e ",
    "ぼ" : "b o ",
    "ぱ" : "p a ",
    "ぴ" : "p i ",
    "ぷ" : "p u ",
    "ぺ" : "p e ",
    "ぽ" : "p o ",
    "や" : "y a ",
    "ゆ" : "y u ",
    "よ" : "y o ",
    "わ" : "w a ",
    "ゐ" : "i ",
    "ゑ" : "e ",
    "ん" : "N ",
    "っ" : "q ",
    "ー" : ": ",
    "ぁ" : "a ",
    "ぃ" : "i ",
    "ぅ" : "u ",
    "ぇ" : "e ",
    "ぉ" : "o ",
    "ゎ" : "w a ",
    "ぉ" : "o ",
    "を" : "o ",
})

argparser = argparse.ArgumentParser()
argparser.add_argument('-o', '--output', help="output filename (default: stdout)")
argparser.add_argument('-t', '--truncate', action='store_true', help="overwrite existing file (default: False)")
args = argparser.parse_args()

words = set()
with open(HTKDIC, encoding="utf-8" ) as f:
    for line in f:
        a = re.match(r'.*\[([^\]]*)\].*', line)
        word = a.group(1)
        words.add(word)

output_lines = []
while True:
    word = input("単語を入力（空行で終了）：")
    if len(word) == 0:
        break
    if word in words:
        print(word +"は，すでに登録されています")
    else:
        yomi = input(word + "の読みをひらがなで入力：")
        for n in yomi2roma:
            for k, v in n.items():
                yomi = yomi.replace(k, v)
        yomi = yomi.replace(" :", ":")
        yomi = re.sub(r'::+', ':', yomi)
        if re.match(r'^[a-zA-Z: ]+$', yomi) is None:
            print(word +"の変換に失敗しました", file=sys.stderr)
        else:
            yomi_ary = []
            yomi = yomi.split()
            c = yomi.pop(0)
            if len(yomi) > 0 :
                yomi_ary.append(c+"_B")
                last_c = yomi.pop()
                for c in yomi:
                    yomi_ary.append(c + "_I")
                yomi_ary.append(last_c + "_E")
            else:
                yomi_ary.append(c + "_S")
            out_line = word + "+名詞\t[" + word + "]\t" + " ".join(yomi_ary)
            if args.output is None:
                print(out_line)
            else:
                output_lines.append(out_line)

if args.output is not None:
    write_mode = "a"
    if args.truncate:
        write_mode = "w"
    with open(args.output, mode=write_mode, encoding="utf-8", newline="\n") as f:
        f.write("\n".join(output_lines))
        f.write("\n")

