import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import random as rand

class Card:
    def __init__(self,number,element,mark,rule):
        self.number = number
        self.element = element
        self.mark = mark
        self.rule = rule

#ゲーム内のフレームにスクロールバーを追加する関数
def create_scrollable_area(frame, i, h):
    container = tk.Frame(frame, width=1252/i, height=h, bg="#003600")
    container.pack(side=tk.LEFT)
    container.pack_propagate(False)
    canvas = tk.Canvas(container, width=1252/i-20, height=h, bg="#003600")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview, bg="#003600")
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas, bg="#003600")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    def frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", frame_configure)
    return scrollable_frame

def text_display():
    if state[3]:
        text_discribe.place(x=200, y=50)
        button_discribe.config(text="戻る", bg="#ffffdd")
        state[3] = False
    else:
        text_discribe.place_forget()
        button_discribe.config(text="ルール確認")
        state[3] = True

def change_N(n):
    cardnum = " "
    if n == 1:
        cardnum = "A"
    elif n == 2:
        cardnum = "B"
    elif n == 3:
        cardnum = "C"
    elif n == 4:
        cardnum = "D"
    elif n == 5:
        cardnum = "E"
    return cardnum
def change_E(n):
    cardcolor = "#000000"
    if n == 1:
        cardcolor = "#a00000"
    elif n == 2:
        cardcolor = "#0000a0"
    elif n == 3:
        cardcolor = "#00a000"
    elif n == 4:
        cardcolor = "#d0d000"
    return cardcolor
def change_E_text(n):
    cardcolor = "黒"
    if n == 1:
        cardcolor = "赤"
    elif n == 2:
        cardcolor = "青"
    elif n == 3:
        cardcolor = "緑"
    elif n == 4:
        cardcolor = "黄"
    return cardcolor
def change_M(n):
    cardmark = " "
    if n == 1:
        cardmark = "●"
    elif n == 2:
        cardmark = "★"
    elif n == 3:
        cardmark = "▲"
    return cardmark
cards = []
rules = []
def game_generate(N,E,M):
    for i in range(N):
        for j in range(E):
            for k in range(M):
                card = Card(i+1, j+1, k+1, "")
                for l in range(3):
                    cards.append(card)
    for i in range(N):
        rules.append(change_N(i+1) + ":3")
        for j in range(E):
            rules.append(change_E_text(j+1) + ":4")
            rules.append(change_N(i+1) + ":2/" + change_E_text(j+1) + ":3")
            for k in range(M):
                    rules.append(change_M(k+1) + ":5")
                    rules.append(change_E_text(j+1) + ":3/" + change_M(k+1) + ":4")
                    rules.append(change_N(i+1) + ":2/" + change_M(k+1) + ":4")
                    rules.append(change_N(i+1) + ":2/" + change_E_text(j+1) + ":2/" + change_M(k+1) + ":3")

#カードの各要素の種類数
N = 5
E = 4
M = 3

#手札<caard>
hands_player = []
hands_cpu1 = []
hands_cpu2 = []
hands_cpu3 = []
#フィールド上のカード<int>
field_player = [0]*(N+E+M)
field_cpu1 = [0]*(N+E+M)
field_cpu2 = [0]*(N+E+M)
field_cpu3 = [0]*(N+E+M)
#フィールド上のカード表示<Label>
field_player_label = []
field_cpu1_label = []
field_cpu2_label = []
field_cpu3_label = []
#フィールド上の勝利条件<str>
rules_player = []
rules_cpu1 = []
rules_cpu2 = []
rules_cpu3 = []
#フィールド上の勝利条件表示<Label>
rules_player_label = []
rules_cpu1_label = []
rules_cpu2_label = []
rules_cpu3_label = []
#プレイヤーの手札情報の表示<Label>
text_hand = []
#消去する勝利条件の情報
delete_rule = []
# state = [0:State<str>, 1:Players<int>, 2:Turn<int>, 3:display<Bool>]
state = ["selectCard", 4, 0, True]
#マウスで選択された情報の保存先
select_rec = [0, 0, 0]

#ゲームスタート
def game_set(players):
    game_generate(5,4,3)
    frame_title.lower()
    name_player.place(x=10, y=3)
    for i in range(players-1):
        cvs.create_line(1252/players*(i+1),0, 1252/players*(i+1),530, fill="white",width=2)
        if i == 0:
            name_cpu1.place(x=1252/players*(i+1)+10, y=3)
        elif i == 1:
            name_cpu2.place(x=1252/players*(i+1)+10, y=3)
        elif i == 2:
            name_cpu3.place(x=1252/players*(i+1)+10, y=3)
    #cvs.create_line(0,530, 1252,530, fill="white",width=3)
    #カードのシャッフル
    rand.shuffle(cards)
    rand.shuffle(rules)
    #カードの要素と勝利条件はゲームごとにランダムな組合せ
    for i in range(len(cards)):
        cards[i].rule = rules[i]
    #PlayerとCPUに手札の配布
    for i in range(3):
        hands_player.append(cards.pop(0))
        for cp in range(players-1):
            if i == 0:
                hands_cpu1.append(cards.pop(0))
            elif i == 1:
                hands_cpu2.append(cards.pop(0))
            elif i == 2:
                hands_cpu3.append(cards.pop(0))
    hands_set_start()

#プレイヤーの手札の表示
def hands_set_start():
    for i in range(3):
        #手札のカード情報を取得
        cardtext = change_N(hands_player[i].number)
        cardtext += " " + change_M(hands_player[i].mark)
        #手札のカード情報を表示
        if i == 0:
            text_hand.append(tk.Label(frame_hand_1, text=cardtext, font=("MSゴシック",24), fg=change_E(hands_player[i].element)))
            text_hand.append(tk.Label(frame_hand_1, text=hands_player[i].rule, font=("MSゴシック",14, "bold"), fg="black"))
            frame_hand_1.pack(padx=15, side=tk.LEFT)
            frame_hand_1.pack_propagate(False)
            text_hand[2*i].bind("<Button-1>", lambda event: game_select_card_player(event, 1))
            text_hand[2*i+1].bind("<Button-1>", lambda event: game_select_card_player(event, 1))
        elif i == 1:
            text_hand.append(tk.Label(frame_hand_2, text=cardtext, font=("MSゴシック",24), fg=change_E(hands_player[i].element)))
            text_hand.append(tk.Label(frame_hand_2, text=hands_player[i].rule, font=("MSゴシック",14, "bold"), fg="black"))
            frame_hand_2.pack(padx=15, side=tk.LEFT)
            frame_hand_2.pack_propagate(False)
            text_hand[2*i].bind("<Button-1>", lambda event: game_select_card_player(event, 2))
            text_hand[2*i+1].bind("<Button-1>", lambda event: game_select_card_player(event, 2))
        elif i == 2:
            text_hand.append(tk.Label(frame_hand_3, text=cardtext, font=("MSゴシック",24), fg=change_E(hands_player[i].element)))
            text_hand.append(tk.Label(frame_hand_3, text=hands_player[i].rule, font=("MSゴシック",14, "bold"), fg="black"))
            frame_hand_3.pack(padx=15, side=tk.LEFT)
            frame_hand_3.pack_propagate(False)
            text_hand[2*i].bind("<Button-1>", lambda event: game_select_card_player(event, 3))
            text_hand[2*i+1].bind("<Button-1>", lambda event: game_select_card_player(event, 3))
        text_hand[2*i].pack(fill=tk.X)
        text_hand[2*i+1].pack(fill=tk.X)
    #手札選択決定ボタンの配置
    button_handSelect.place(x=1162, y=542, width=80, height=70)
    text_loot.config(text="手札のカードを1つ選択 → 決定ボタン")

#i番目の手札1枚入れ替え
def hands_set_ref(card, i):
    if i > 0:
        cardtext = change_N(card.number) + " " + change_M(card.mark)
        hands_player[i-1] = card
        text_hand[2*(i-1)].config(text=cardtext, fg=change_E(card.element), bg="white")
        text_hand[2*(i-1)+1].config(text=card.rule, fg="black", bg="white")

#決定ボタン
def game_button():
    #カード選択決定時
    if state[0] == "selectCard" and select_rec[0] > 0:
        state[0] = "stay"
        playcard = hands_player[select_rec[0]-1]
        if select_rec[0] == 1:
            frame_hand_1.config(highlightbackground="white")
        elif select_rec[0] == 2:
            frame_hand_2.config(highlightbackground="white")
        elif select_rec[0] == 3:
            frame_hand_3.config(highlightbackground="white")
        elif select_rec[0] == 4:
            frame_hand_4.config(highlightbackground="white")
        elif select_rec[0] == 5:
            frame_hand_5.config(highlightbackground="white")
        elif select_rec[0] == 6:
            frame_hand_6.config(highlightbackground="white")
        elif select_rec[0] == 7:
            frame_hand_7.config(highlightbackground="white")
        text_hand[2*(select_rec[0]-1)].config(fg="#108010", bg="#108010")
        text_hand[2*(select_rec[0]-1)+1].config(fg="#108010", bg="#108010")
        playcardtext = change_N(playcard.number) + "  " + change_M(playcard.mark)
        #選択されたカードをフィールドに出す
        game_field_count(field_player, playcard.number, playcard.element, playcard.mark)
        field_player_label.append(tk.Label(frame_field_player, text=playcardtext, font=("MSゴシック",28,"bold"), fg=change_E(playcard.element), bg="#DDFFDD"))
        field_player_label[-1].pack(padx=20, pady=3)
        rules_player.append(playcard.rule)
        rules_player_label.append(tk.Label(frame_rules_player, text=playcard.rule, font=("MSゴシック",12,"bold"), fg="white", bg="#003600"))
        rules_player_label[-1].pack(padx=20, pady=3)
        text_field_player.config(text=game_field_state(field_player))
        #CPUのカード選択
        game_select_card_cpu(state[1])
    #勝利条件選択時
    elif state[0] == "selectRule" and select_rec[1] > 0:
        state[0] = "stay"
        if select_rec[1] == 1:
            rules_cpu1_label[select_rec[2]].config(fg="white")
        elif select_rec[1] == 2:
            rules_cpu2_label[select_rec[2]].config(fg="white")
        elif select_rec[1] == 3:
            rules_cpu3_label[select_rec[2]].config(fg="white")
        delete_rule.append([select_rec[1],select_rec[2]])
        game_select_rule_cpu()

#'state[0] == "selectCard"'のときに実行
def game_select_card_player(event, i):
    if state[0] == "selectCard":
        if select_rec[0] == 1:
            frame_hand_1.config(highlightbackground="white")
        elif select_rec[0] == 2:
            frame_hand_2.config(highlightbackground="white")
        elif select_rec[0] == 3:
            frame_hand_3.config(highlightbackground="white")
        elif select_rec[0] == 4:
            frame_hand_4.config(highlightbackground="white")
        elif select_rec[0] == 5:
            frame_hand_5.config(highlightbackground="white")
        elif select_rec[0] == 6:
            frame_hand_6.config(highlightbackground="white")
        elif select_rec[0] == 7:
            frame_hand_7.config(highlightbackground="white")
        if i == 1:
            select_rec[0] = 1
            frame_hand_1.config(highlightbackground="red")
        elif i == 2:
            select_rec[0] = 2
            frame_hand_2.config(highlightbackground="red")
        elif i == 3:
            select_rec[0] = 3
            frame_hand_3.config(highlightbackground="red")
        elif i == 4:
            select_rec[0] = 4
            frame_hand_4.config(highlightbackground="red")
        elif i == 5:
            select_rec[0] = 5
            frame_hand_5.config(highlightbackground="red")
        elif i == 6:
            select_rec[0] = 6
            frame_hand_6.config(highlightbackground="red")
        elif i == 7:
            select_rec[0] = 7
            frame_hand_7.config(highlightbackground="red")

#CPUがフィールドにカードを出す関数（現状：完全ランダム）
def game_select_card_cpu(players):
    select = [True,True,True]
    for cp in range(players-1):
        rand.shuffle(select)
        if cp == 0:
            playcard = hands_cpu1.pop(0)
            playcardtext = ""
            playcardcolor = "#000000"
            if select[0]:
                playcardtext += change_N(playcard.number)
            else:
                playcardtext += "_"
            if select[1]:
                playcardcolor = change_E(playcard.element)
            if select[2]:
                playcardtext += "  " + change_M(playcard.mark)
            else:
                playcardtext += "  _"
            game_field_count(field_cpu1, playcard.number, playcard.element, playcard.mark)
            field_cpu1_label.append(tk.Label(frame_field_cpu1, text=playcardtext, font=("MSゴシック",28,"bold"), fg=playcardcolor, bg="#DDFFDD"))
            field_cpu1_label[-1].pack(padx=20, pady=3)
            rules_cpu1.append(playcard.rule)
            rules_cpu1_label.append(tk.Label(frame_rules_cpu1, text=playcard.rule, font=("MSゴシック",12,"bold"), fg="white", bg="#003600"))
            rules_cpu1_label[-1].pack(padx=20, pady=3)
            rules_cpu1_label[-1].bind("<Button-1>", lambda event: game_select_rule_player(event, 1))
            text_field_cpu1.config(text=game_field_state(field_cpu1))
        if cp == 1:
            playcard = hands_cpu2.pop(0)
            playcardtext = ""
            playcardcolor = "#000000"
            if select[0]:
                playcardtext += change_N(playcard.number)
            else:
                playcardtext += "_"
            if select[1]:
                playcardcolor = change_E(playcard.element)
            if select[2]:
                playcardtext += "  " + change_M(playcard.mark)
            else:
                playcardtext += "  _"
            game_field_count(field_cpu2, playcard.number, playcard.element, playcard.mark)
            field_cpu2_label.append(tk.Label(frame_field_cpu2, text=playcardtext, font=("MSゴシック",28,"bold"), fg=playcardcolor, bg="#DDFFDD"))
            field_cpu2_label[-1].pack(padx=20, pady=3)
            rules_cpu2.append(playcard.rule)
            rules_cpu2_label.append(tk.Label(frame_rules_cpu2, text=playcard.rule, font=("MSゴシック",12,"bold"), fg="white", bg="#003600"))
            rules_cpu2_label[-1].pack(padx=20, pady=3)
            rules_cpu2_label[-1].bind("<Button-1>", lambda event: game_select_rule_player(event, 2))
            text_field_cpu2.config(text=game_field_state(field_cpu2))
        if cp == 2:
            playcard = hands_cpu3.pop(0)
            playcardtext = ""
            playcardcolor = "#000000"
            if select[0]:
                playcardtext += change_N(playcard.number)
            else:
                playcardtext += "_"
            if select[1]:
                playcardcolor = change_E(playcard.element)
            if select[2]:
                playcardtext += "  " + change_M(playcard.mark)
            else:
                playcardtext += "  _"
            game_field_count(field_cpu3, playcard.number, playcard.element, playcard.mark)
            field_cpu3_label.append(tk.Label(frame_field_cpu3, text=playcardtext, font=("MSゴシック",28,"bold"), fg=playcardcolor, bg="#DDFFDD"))
            field_cpu3_label[-1].pack(padx=20, pady=3)
            rules_cpu3.append(playcard.rule)
            rules_cpu3_label.append(tk.Label(frame_rules_cpu3, text=playcard.rule, font=("MSゴシック",12,"bold"), fg="white", bg="#003600"))
            rules_cpu3_label[-1].pack(padx=20, pady=3)
            rules_cpu3_label[-1].bind("<Button-1>", lambda event: game_select_rule_player(event, 3))
            text_field_cpu3.config(text=game_field_state(field_cpu3))
    state[0] = "selectRule"
    text_loot.config(text="CPUの勝利条件を1つ選択 → 決定ボタン")

#'state[0] == "selectRule"'のときに実行
def game_select_rule_player(event, i):
    if state[0] == "selectRule":
        if select_rec[1] == 1:
            rules_cpu1_label[select_rec[2]].config(fg="white")
        elif select_rec[1] == 2:
            rules_cpu2_label[select_rec[2]].config(fg="white")
        elif select_rec[1] == 3:
            rules_cpu3_label[select_rec[2]].config(fg="white")
        if i == 1:
            index = rules_cpu1_label.index(event.widget)
            select_rec[1] = 1
            select_rec[2] = index
            rules_cpu1_label[index].config(fg="#ffbbff")
        elif i == 2:
            index = rules_cpu2_label.index(event.widget)
            select_rec[1] = 2
            select_rec[2] = index
            rules_cpu2_label[index].config(fg="#ffbbff")
        elif i == 3:
            index = rules_cpu3_label.index(event.widget)
            select_rec[1] = 3
            select_rec[2] = index
            rules_cpu3_label[index].config(fg="#ffbbff")

#CPUが消去したい勝利条件を選択する関数（現状：完全ランダム）
def game_select_rule_cpu():
    players = state[1]
    for cp in range(players-1):
        if cp == 0:
            all = len(rules_player) + len(rules_cpu2) + len(rules_cpu3)
            select = rand.randint(1, all)
            if select <= len(rules_player):
                p = 0
                index = select - 1
            elif select <= (len(rules_player)+len(rules_cpu2)):
                p = 2
                index = select - len(rules_player) - 1
            else:
                p = 3
                index = select - len(rules_player) - len(rules_cpu2) - 1
            delete_rule.append([p, index])
        elif cp == 1:
            all = len(rules_player) + len(rules_cpu1) + len(rules_cpu3)
            select = rand.randint(1, all)
            if select <= len(rules_player):
                p = 0
                index = select - 1
            elif select <= (len(rules_player)+len(rules_cpu1)):
                p = 1
                index = select - len(rules_player) - 1
            else:
                p = 3
                index = select - len(rules_player) - len(rules_cpu1) - 1
            delete_rule.append([p, index])
        elif cp == 2:
            all = len(rules_player) + len(rules_cpu1) + len(rules_cpu2)
            select = rand.randint(1, all)
            if select <= len(rules_player):
                p = 0
                index = select - 1
            elif select <= (len(rules_player)+len(rules_cpu1)):
                p = 1
                index = select - len(rules_player) - 1
            else:
                p = 2
                index = select - len(rules_player) - len(rules_cpu1) - 1
            delete_rule.append([p, index])
    rand.shuffle(delete_rule)
    pl = True
    cp1 = True
    cp2 = True
    cp3 = True
    for i in range(2):
        if delete_rule[i][0] == 0 and pl:
            rules_player_label[delete_rule[i][1]].pack_forget()
            rules_player_label.pop(delete_rule[i][1])
            rules_player.pop(delete_rule[i][1])
            pl = False
        elif delete_rule[i][0] == 1 and cp1:
            rules_cpu1_label[delete_rule[i][1]].pack_forget()
            rules_cpu1_label.pop(delete_rule[i][1])
            rules_cpu1.pop(delete_rule[i][1])
            cp1 = False
        elif delete_rule[i][0] == 2 and cp2:
            rules_cpu2_label[delete_rule[i][1]].pack_forget()
            rules_cpu2_label.pop(delete_rule[i][1])
            rules_cpu2.pop(delete_rule[i][1])
            cp2 = False
        elif delete_rule[i][0] == 3 and cp3:
            rules_cpu3_label[delete_rule[i][1]].pack_forget()
            rules_cpu3_label.pop(delete_rule[i][1])
            rules_cpu3.pop(delete_rule[i][1])
            cp3 = False
    game_judge(0)
    game_judge(1)
    game_judge(2)
    game_judge(3)

#フィールドに出ている要素をカウントする関数
def game_field_count(fieldP, n, e, m):
    if (n-1) >= 0:
        fieldP[n-1] += 1
    if (N+e-1) >= 0:
        fieldP[N+e-1] += 1
    if (N+E+m-1) >= 0:
        fieldP[N+E+m-1] += 1

#フィールドに出ている要素を表示する関数
def game_field_state(fieldP):
    text = ""
    for i in range(len(fieldP)):
        if i < N:
            text += change_N(i+1) + ":"
        elif i < (N+E):
            text += change_E_text(i-N+1) + ":"
        else:
            text += change_M(i-N-E+1) + ":"
        text += str(fieldP[i]) + "\n"
    return text

#勝利条件を満たしているか判定する関数(i=0:Player, i=1~3:CPU1~3)
def game_judge(i):
    jud = False
    if i == 0:
        rulesP = rules_player
        fieldP = field_player
    elif i == 1:
        rulesP = rules_cpu1
        fieldP = field_cpu1
    elif i == 2:
        rulesP = rules_cpu2
        fieldP = field_cpu2
    elif i == 3:
        rulesP = rules_cpu3
        fieldP = field_cpu3
    for l in range(len(rulesP)):
        rule = [item for part in rulesP[l].split("/") for item in part.split(":")]
        for j in range(int(len(rule)/2)):
            if rule[2*j] == "A":
                index = 0
            elif rule[2*j] == "B":
                index = 1
            elif rule[2*j] == "C":
                index = 2
            elif rule[2*j] == "D":
                index = 3
            elif rule[2*j] == "E":
                index = 4
            elif rule[2*j] == "赤":
                index = 5
            elif rule[2*j] == "青":
                index = 6
            elif rule[2*j] == "緑":
                index = 7
            elif rule[2*j] == "黄":
                index = 8
            elif rule[2*j] == "●":
                index = 9
            elif rule[2*j] == "★":
                index = 10
            elif rule[2*j] == "▲":
                index = 11
            if fieldP[index] >= int(rule[2*j+1]):
                jud = True
            else:
                jud = False
                break
        if jud:
            break
    if jud:
        game_result(i)
    else:
        game_turn_end(i)

#ターン終了時の処理
def game_turn_end(i):
    if len(cards) > 0:
        if i == 0:
            newcard = cards.pop(0)
            hands_set_ref(newcard, select_rec[0])
            select_rec[0] = 0
            state[0] = "selectCard"
            state[2] += 1
            delete_rule.clear()
            text_loot.config(text="手札のカードを1つ選択 → 決定ボタン")
        elif i == 1:
            hands_cpu1.append(cards.pop(0))
        elif i == 2:
            hands_cpu2.append(cards.pop(0))
        elif i == 3:
            hands_cpu3.append(cards.pop(0))
    else:
        frame_title.lift()
        text_title.config(text="引き分け", fg="#aa00aa")
        button_start4.config(text="再戦")

#ゲーム終了時の処理
def game_result(i):
    frame_title.lift()
    if i == 0:
        text_title.config(text="勝者：Player", fg="#aa0000")
    elif i == 1:
        text_title.config(text="勝者：CPU1", fg="#0000aa")
    elif i == 2:
        text_title.config(text="勝者：CPU2", fg="#0000aa")
    elif i == 3:
        text_title.config(text="勝者：CPU3", fg="#0000aa")
    button_start4.config(text="再戦")
    #配列の初期化
    hands_player.clear()
    hands_cpu1.clear()
    hands_cpu2.clear()
    hands_cpu3.clear()
    for i in range(5+4+3):
        field_player[i] = 0
        field_cpu1[i] = 0
        field_cpu2[i] = 0
        field_cpu3[i] = 0
    text_field_player.config(text="")
    text_field_cpu1.config(text="")
    text_field_cpu2.config(text="")
    text_field_cpu3.config(text="")
    field_player_label.clear()
    field_cpu1_label.clear()
    field_cpu2_label.clear()
    field_cpu3_label.clear()
    rules_player.clear()
    rules_cpu1.clear()
    rules_cpu2.clear()
    rules_cpu3.clear()
    rules_player_label.clear()
    rules_cpu1_label.clear()
    rules_cpu2_label.clear()
    rules_cpu3_label.clear()
    text_hand.clear()
    delete_rule.clear()
    state[0] = "selectCard"
    state[2] = 0
    state[3] = True
    for i in range(3):
        select_rec[i] = 0
    frame_clear(frame_field_player)
    frame_clear(frame_field_cpu1)
    frame_clear(frame_field_cpu2)
    frame_clear(frame_field_cpu3)
    frame_clear(frame_rules_player)
    frame_clear(frame_rules_cpu1)
    frame_clear(frame_rules_cpu2)
    frame_clear(frame_rules_cpu3)
    frame_clear(frame_hand_1)
    frame_clear(frame_hand_2)
    frame_clear(frame_hand_3)

def frame_clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()



#ウィンドウ
root = tk.Tk()
root.title("抹勝")
root.geometry("1252x620")
root.resizable(False,False)

#フィールド
cvs = tk.Canvas(root, width=1252, height=530, bg="#003600")
cvs.pack()
name_player = tk.Label(text="Player", font=("MSゴシック",18,"bold"), fg="#FFFFDD", bg="#003600")
name_cpu1 = tk.Label(text="CPU-1", font=("MSゴシック",18,"bold"), fg="white", bg="#003600")
name_cpu2 = tk.Label(text="CPU-2", font=("MSゴシック",18,"bold"), fg="white", bg="#003600")
name_cpu3 = tk.Label(text="CPU-3", font=("MSゴシック",18,"bold"), fg="white", bg="#003600")

#フィールドのフレーム
frame_field = tk.LabelFrame(root, text="フィールド", width=1252, height=290, fg="white", bg="#003600")
frame_field.place(x=0, y=40)
frame_field_player = create_scrollable_area(frame_field, state[1], 266)
frame_field_cpu1 = create_scrollable_area(frame_field, state[1], 266)
frame_field_cpu2 = create_scrollable_area(frame_field, state[1], 266)
frame_field_cpu3 = create_scrollable_area(frame_field, state[1], 266)
text_field_player = tk.Label(root, text=" ", font=("MSゴシック",12,"bold"), fg="white", bg="#003600", anchor="e")
text_field_player.place(x=190, y=65)
text_field_player.lift(frame_field_player)
text_field_cpu1 = tk.Label(root, text=" ", font=("MSゴシック",12,"bold"), fg="white", bg="#003600", anchor="e")
text_field_cpu1.place(x=503, y=65)
text_field_cpu1.lift(frame_field_cpu1)
text_field_cpu2 = tk.Label(root, text=" ", font=("MSゴシック",12,"bold"), fg="white", bg="#003600", anchor="e")
text_field_cpu2.place(x=816, y=65)
text_field_cpu2.lift(frame_field_cpu2)
text_field_cpu3 = tk.Label(root, text=" ", font=("MSゴシック",12,"bold"), fg="white", bg="#003600", anchor="e")
text_field_cpu3.place(x=1129, y=65)
text_field_cpu3.lift(frame_field_cpu3)

#勝利条件のフレーム
frame_rules = tk.LabelFrame(root, text="勝利条件", width=1252, height=200, fg="white", bg="#003600")
frame_rules.place(x=0, y=330)
frame_rules_player = create_scrollable_area(frame_rules, state[1], 176)
frame_rules_cpu1 = create_scrollable_area(frame_rules, state[1], 176)
frame_rules_cpu2 = create_scrollable_area(frame_rules, state[1], 176)
frame_rules_cpu3 = create_scrollable_area(frame_rules, state[1], 176)

#手札全体のフレーム
frame_hand = tk.LabelFrame(root, text="手札", width=1152, height=90, fg="white", bg="#108010")
frame_hand.pack(side=tk.LEFT)
frame_hand.pack_propagate(False)
#手札のカードのフレーム 1~7
frame_hand_1 = tk.Frame(frame_hand, width=130, height=85, bg="white", highlightbackground="white", highlightthickness=3)
frame_hand_2 = tk.Frame(frame_hand, width=130, height=85, bg="white", highlightbackground="white", highlightthickness=3)
frame_hand_3 = tk.Frame(frame_hand, width=130, height=85, bg="white", highlightbackground="white", highlightthickness=3)
frame_hand_4 = tk.Frame(frame_hand, width=130, height=85, bg="white", highlightbackground="white", highlightthickness=3)
frame_hand_5 = tk.Frame(frame_hand, width=130, height=85, bg="white", highlightbackground="white", highlightthickness=3)
frame_hand_6 = tk.Frame(frame_hand, width=130, height=85, bg="white", highlightbackground="white", highlightthickness=3)
frame_hand_7 = tk.Frame(frame_hand, width=130, height=85, bg="white", highlightbackground="white", highlightthickness=3)
frame_hand_1.bind("<Button-1>", lambda event: game_select_card_player(event, 1))
frame_hand_2.bind("<Button-1>", lambda event: game_select_card_player(event, 2))
frame_hand_3.bind("<Button-1>", lambda event: game_select_card_player(event, 3))
frame_hand_4.bind("<Button-1>", lambda event: game_select_card_player(event, 4))
frame_hand_5.bind("<Button-1>", lambda event: game_select_card_player(event, 5))
frame_hand_6.bind("<Button-1>", lambda event: game_select_card_player(event, 6))
frame_hand_7.bind("<Button-1>", lambda event: game_select_card_player(event, 7))
#手札選択決定ボタン
button_handSelect = tk.Button(text="決定", font=("MSゴシック",24), command=game_button)

text_loot = tk.Label(root, text="", font=("MSゴシック",12,"bold"), fg="white", bg="#003600")
text_loot.place(x=580, y=525)
text_loot.lift()

frame_title = tk.Frame(root, width=1252, height=620)
frame_title.place(x=0, y=0)
frame_title.pack_propagate(False)
text_title = tk.Label(frame_title, text="抹 勝", font=("MSゴシック",72, "bold"), fg="#003600")
text_title.pack(pady=100)
#button_start3 = tk.Button(frame_title, text="3人プレイ", font=("MSゴシック",30, "bold"), command=lambda: game_set(3))
button_start4 = tk.Button(frame_title, text="ゲームスタート", font=("MSゴシック",30, "bold"), command=lambda: game_set(4))
#button_start3.place(x=200, y=450)
button_start4.pack(pady=100)

text_finish = tk.Label(text="", font=("MSゴシック",48, "bold"), fg="red", bg="#ffffcc")
button_discribe = tk.Button(text="ルール確認", font=("MSゴシック",14, "bold"), fg="#202020", command=text_display)
text_discribeT  = "\n"
text_discribeT += "[ルール説明]\n"
text_discribeT += "各自フィールドに出されたカードの要素で勝利条件を満たそう！\n"
text_discribeT += "相手の勝利条件を消去して相手の勝利を妨害しよう！\n"
text_discribeT += "\n"
text_discribeT += "[ゲームの流れ]\n"
text_discribeT += "1ターンに1枚手札のカードを出す\n"
text_discribeT += "↓\n"
text_discribeT += "他人の勝利条件を1つ選択\n"
text_discribeT += "↓\n"
text_discribeT += "選択された勝利条件からランダムで1～2つを削除\n"
text_discribeT += "↓\n"
text_discribeT += "勝利条件の達成判定\n"
text_discribeT += "↓\n"
text_discribeT += "次のターン\n"
text_discribeT += "\n"
text_discribeT += "山札が無くなった時点で決着がついていない場合は引き分けになります\n"
text_discribe = tk.Label(text=text_discribeT, font=("MSゴシック",20, "bold"), fg="black", bg="#ddddff")
button_discribe.place(x=1130, y=5)

root.mainloop()