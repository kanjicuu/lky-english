#!/usr/bin/env python3
"""Generate workshop summary PDF with Japanese fonts."""

import os, sys
sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

from fpdf import FPDF

# --- Constants ---
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FONT_B = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_L = "/System/Library/Fonts/ヒラギノ角ゴシック W1.ttc"
OUT = os.path.join(os.path.dirname(__file__), "workshop-summary.pdf")
IMG = os.path.join(os.path.dirname(__file__), "images")

# Country colors
C_JAPAN = (198, 40, 40)
C_SINGAPORE = (230, 81, 0)
C_MALAYSIA = (46, 125, 50)
C_BRITAIN = (21, 101, 192)
C_BLUE = (13, 71, 161)
C_GRAY = (100, 100, 100)


class WorkshopPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.add_font("hira", "", FONT_R, uni=True)
        self.add_font("hira", "B", FONT_B, uni=True)
        self.add_font("hira_l", "", FONT_L, uni=True)
        self.set_auto_page_break(auto=True, margin=18)

    # ---- helpers ----
    def section_title(self, text, badge="", r=13, g=71, b=161):
        self.set_font("hira", "B", 15)
        self.set_text_color(r, g, b)
        if badge:
            self.cell(0, 10, f"  {badge}  {text}", new_x="LMARGIN", new_y="NEXT")
        else:
            self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(r, g, b)
        self.set_line_width(0.8)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def sub_title(self, text, r=21, g=101, b=192):
        self.set_font("hira", "B", 12)
        self.set_text_color(r, g, b)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def sub_sub_title(self, text):
        self.set_draw_color(66, 165, 245)
        self.set_line_width(1.2)
        x = self.get_x()
        y = self.get_y()
        self.line(x, y, x, y + 6)
        self.set_x(x + 4)
        self.set_font("hira", "B", 10.5)
        self.set_text_color(50, 50, 50)
        self.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def body(self, text, size=10):
        self.set_font("hira", "", size)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bold_body(self, text, size=10):
        self.set_font("hira", "B", size)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=6, size=10):
        self.set_font("hira", "", size)
        x = self.get_x() + indent
        self.set_x(x)
        self.cell(4, 5.5, "・")
        self.set_x(x + 4)
        self.multi_cell(self.w - self.r_margin - x - 4, 5.5, text)
        self.ln(0.5)

    def numbered(self, num, text, indent=6, size=10):
        self.set_font("hira", "B", size)
        x = self.get_x() + indent
        self.set_x(x)
        self.cell(8, 5.5, f"{num}.")
        self.set_font("hira", "", size)
        self.set_x(x + 8)
        self.multi_cell(self.w - self.r_margin - x - 8, 5.5, text)
        self.ln(0.5)

    def simple_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            w = (self.w - self.l_margin - self.r_margin) / len(headers)
            col_widths = [w] * len(headers)
        # header
        self.set_font("hira", "B", 9)
        self.set_fill_color(227, 242, 253)
        self.set_draw_color(180, 180, 180)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True)
        self.ln()
        # rows
        self.set_font("hira", "", 9)
        for ri, row in enumerate(rows):
            fill = ri % 2 == 1
            if fill:
                self.set_fill_color(248, 248, 248)
            max_h = 7
            # calc heights
            x_start = self.get_x()
            y_start = self.get_y()
            heights = []
            for ci, cell_text in enumerate(row):
                # estimate lines
                nlines = max(1, len(cell_text) * 0.55 / (col_widths[ci] - 2) + 1)
                heights.append(max(7, int(nlines) * 5.5))
            max_h = max(heights)
            if max_h > 7:
                # multi-line row
                for ci, cell_text in enumerate(row):
                    x = x_start + sum(col_widths[:ci])
                    self.set_xy(x, y_start)
                    self.cell(col_widths[ci], max_h, "", border=1, fill=fill)
                    self.set_xy(x + 1, y_start + 1)
                    self.multi_cell(col_widths[ci] - 2, 5, cell_text)
                self.set_xy(x_start, y_start + max_h)
            else:
                for ci, cell_text in enumerate(row):
                    self.cell(col_widths[ci], 7, cell_text, border=1, fill=fill)
                self.ln()
        self.ln(3)

    def country_card(self, name, color, text):
        r, g, b = color
        self.set_draw_color(r, g, b)
        self.set_line_width(1.5)
        x = self.get_x()
        y = self.get_y()
        # left border
        self.line(x, y, x, y + 4)
        self.set_x(x + 4)
        self.set_font("hira", "B", 10)
        self.set_text_color(r, g, b)
        self.cell(0, 5, name, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.set_font("hira", "", 9)
        self.set_x(x + 4)
        self.multi_cell(self.w - self.r_margin - x - 8, 4.8, text)
        self.ln(3)

    def colored_box(self, title, items, bg_color, border_color):
        self.set_fill_color(*bg_color)
        self.set_draw_color(*border_color)
        x = self.get_x()
        y = self.get_y()
        # build content
        content = title + "\n" + "\n".join(items)
        # estimate height
        self.set_font("hira", "", 9)
        lines = 0
        for line in content.split("\n"):
            lines += max(1, int(len(line) * 0.48 / (self.w - self.l_margin - self.r_margin - 12) + 1))
        h = max(12, lines * 5 + 6)
        # draw box
        self.rect(x, y, self.w - self.l_margin - self.r_margin, h, style="DF")
        self.set_xy(x + 4, y + 2)
        self.set_font("hira", "B", 9.5)
        self.cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")
        self.set_font("hira", "", 9)
        for item in items:
            self.set_x(x + 4)
            self.multi_cell(self.w - self.l_margin - self.r_margin - 8, 4.8, item)
        self.ln(3)

    def hint_box(self, items):
        self.colored_box("ディスカッションの問い", items, (255, 248, 225), (255, 224, 130))

    def expect_box(self, items):
        self.colored_box("参加者に期待する反応", items, (232, 245, 233), (165, 214, 167))

    def facilitate_box(self, items):
        self.colored_box("ファシリテーターの働きかけ", items, (227, 242, 253), (144, 202, 249))


def build():
    pdf = WorkshopPDF()

    # ===== COVER =====
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("hira", "B", 28)
    pdf.set_text_color(*C_BLUE)
    pdf.cell(0, 14, "4カ国ロールプレイ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "「国際会議」", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("hira", "", 14)
    pdf.set_text_color(*C_GRAY)
    pdf.cell(0, 8, "ワークショップ全体資料", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("hira", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, "シンガポールの歴史を4つの国の視点から体験する", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "参加型ロールプレイ・ワークショップ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("hira", "", 10)
    pdf.set_text_color(*C_GRAY)
    pdf.cell(0, 6, "対象: 小中学生（10〜15歳）｜所要時間: 約130分（短縮版80分）", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "実施タイミング: シンガポール国立博物館 見学後", align="C", new_x="LMARGIN", new_y="NEXT")

    # ===== TOC =====
    pdf.add_page()
    pdf.section_title("目次")
    toc = [
        "1. ワークショップの目的",
        "2. 当日の準備",
        "    2-a. 会場配置とチーム分け",
        "    2-b. 配布カードの種類と概要",
        "3. プログラム進行",
        "    3-a. タイムテーブル",
        "    3-b. 各ラウンドの進め方",
        "    Round 1 — 日本軍侵略（1941-42）",
        "    Round 2 — 日本軍支配（1942-45）",
        "    Round 3 — 原爆と終戦（1945）",
        "    Round 4 — イギリス再支配（1945-50s）",
        "    Round 5 — 東南アジア独立（1950s-1965）",
        "4. 振り返りと閉会",
    ]
    pdf.set_font("hira", "", 11)
    for item in toc:
        pdf.cell(0, 7, item, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # legend
    pdf.sub_title("凡例")
    pdf.set_font("hira", "B", 9)
    pdf.body("カード色:")
    for name, color in [("日本", C_JAPAN), ("シンガポール", C_SINGAPORE), ("マレーシア", C_MALAYSIA), ("イギリス", C_BRITAIN)]:
        pdf.set_fill_color(*color)
        x = pdf.get_x() + 6
        y = pdf.get_y()
        pdf.rect(x, y, 10, 4, style="F")
        pdf.set_x(x + 14)
        pdf.set_font("hira", "", 9)
        pdf.cell(30, 5, name)
    pdf.ln(8)

    pdf.set_font("hira", "B", 9)
    pdf.body("ボックス色:")
    for name, bg in [("ディスカッションの問い", (255, 248, 225)),
                      ("期待する反応", (232, 245, 233)),
                      ("ファシリテーターの働きかけ", (227, 242, 253))]:
        pdf.set_fill_color(*bg)
        x = pdf.get_x() + 6
        y = pdf.get_y()
        pdf.rect(x, y, 10, 4, style="F")
        pdf.set_x(x + 14)
        pdf.set_font("hira", "", 9)
        pdf.cell(50, 5, name)
        pdf.ln(5)

    # ===== 1. PURPOSE =====
    pdf.add_page()
    pdf.section_title("1  ワークショップの目的")
    pdf.sub_title("3つのゴール")
    pdf.numbered(1, "歴史に「100:0」はないことを体感する — どの国にも理由があり、どの国にも傷がある。善悪の二項対立を超える。")
    pdf.numbered(2, "同じ出来事でも立場によって見え方が全く違うことを知る — 4カ国が同じ歴史的事件をそれぞれの視点で語り、違いを可視化する。")
    pdf.numbered(3, "相手の視点を理解した上で自分の立場を語れるようになる — 「わかってくれ」ではなく「わかった上で伝える」力。グローバル人材の第一歩。")
    pdf.ln(4)
    pdf.sub_title("なぜシンガポールの歴史なのか")
    pdf.bullet("日本・イギリス・マレーシア・シンガポールの4カ国が直接関わる歴史")
    pdf.bullet("日本の子どもたちにとって「加害」と「被害」の両面を学べる")
    pdf.bullet("シンガポール国立博物館の見学と直結し、体験を深められる")

    # ===== 2. SETUP =====
    pdf.add_page()
    pdf.section_title("2  当日の準備")
    pdf.sub_title("2-a. 会場配置とチーム分け")
    pdf.simple_table(
        ["項目", "内容"],
        [
            ["参加人数", "16〜32人（4チーム × 4〜8人）"],
            ["チーム", "日本 / シンガポール / マレーシア / イギリス"],
            ["分け方", "ランダム（友達同士で固まらない）"],
            ["会場", "教室・会議室・ホテルの広めの部屋など"],
        ],
        [45, 130],
    )
    pdf.sub_sub_title("会場レイアウト")
    pdf.bullet("4つの島（テーブルクラスター）を配置。各島に国旗プリントを立てる")
    pdf.bullet("中央にファシリテーター用スペース")
    pdf.bullet("全チームが他チームの発表を聞ける配置にする（扇形や四角形）")
    pdf.ln(2)
    pdf.sub_sub_title("チーム分けの注意点")
    pdf.bullet("日本チーム: 自国の加害を知ることになるため、歴史に興味がある子や冷静に考えられる子を入れると安定する")
    pdf.bullet("役の交換（推奨）: 休憩後（R3の前）に対角で交換（例: 日本⇄シンガポール）。「さっきまで相手だった国を自分が語る」体験が核心")
    pdf.ln(4)

    pdf.sub_title("2-b. 配布カードの種類")
    pdf.simple_table(
        ["種類", "内容", "配布タイミング", "部数"],
        [
            ["初期設定カード（4種）", "各国の1940年時点の状況・立場・気持ち", "開始時に各チームへ", "各1部"],
            ["ラウンドカード（5種×4国）", "共通事実 + 国別ヒント", "各ラウンド開始時", "各R 4部"],
            ["振り返りシート", "6つの設問", "最後の振り返り時", "人数分"],
        ],
        [42, 62, 40, 28],
    )

    pdf.sub_sub_title("初期設定カード概要（4カ国）")
    pdf.body("各チームに配布する初期設定カードの内容です。チームメンバーはこのカードを読んで自国の立場を理解し、「うちの国はこういう国です」と発表します。")

    # --- JAPAN ---
    pdf.add_page()
    pdf.section_title("初期設定カード — 日本チーム", r=198, g=40, b=40)
    # Flag beside title area
    y_img = pdf.get_y()
    pdf.image(f"{IMG}/flag_japan.png", x=pdf.l_margin, y=y_img, w=30)
    pdf.set_xy(pdf.l_margin + 34, y_img + 4)
    pdf.set_font("hira", "B", 11)
    pdf.set_text_color(198, 40, 40)
    pdf.cell(0, 7, "大日本帝国 — 1940年の状況", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(y_img + 22)
    # Map — centered, full width
    map_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.image(f"{IMG}/map_japan.png", x=pdf.l_margin + 10, y=pdf.get_y(), w=map_w - 20)
    pdf.add_page()

    pdf.sub_title("1940年、あなたの国はこんな状況です", r=198, g=40, b=40)

    pdf.bold_body("あなたの国の紹介")
    pdf.body("日本はアジアで唯一、欧米の列強と肩を並べる国です。1868年の明治維新からわずか数十年で、刀と着物の国から近代的な軍事大国へと変貌しました。")
    pdf.bullet("1895年 — 日清戦争に勝利（中国に勝った）")
    pdf.bullet("1905年 — 日露戦争に勝利（ヨーロッパの大国ロシアに勝った）")
    pdf.body("日露戦争の勝利は世界を震撼させました。アジア人がヨーロッパの大国を倒したのは、近代史上これが初めてです。インドのネルー少年は大喜びし、トルコでは「トーゴー」（東郷平八郎）が男の子の名前として流行しました。")
    pdf.ln(2)

    pdf.bold_body("今の問題")
    pdf.body("日本には大きな弱点があります。石油がほとんど出ないのです。国内の産出量は必要量のわずか10%。備蓄は約2年分しかありません。")
    pdf.body("1937年から中国と戦争中ですが決着がつきません。そして1941年、アメリカが日本への石油の全面禁輸を決定しました。石油がなければ軍艦も戦闘機も動きません。日本は追い詰められています。選択肢は2つ:")
    pdf.bullet("中国から撤退してアメリカに屈服する")
    pdf.bullet("東南アジアの石油・ゴム・錫を確保するために南へ進む")
    pdf.ln(2)

    pdf.bold_body("あなたの国の気持ち")
    pdf.bullet("「日本はアジアの盟主だ。欧米に支配されたアジアを解放する」")
    pdf.bullet("「このまま何もしなければ、石油が尽きて国が滅ぶ」")
    pdf.bullet("「白人たちがアジアを植民地にしているのは許せない」")
    pdf.ln(2)

    pdf.simple_table(
        ["項目", "数字"],
        [
            ["明治維新からの年数", "約70年"],
            ["軍の規模", "陸軍約200万人"],
            ["石油の自給率", "約10%"],
            ["石油の備蓄", "約2年分"],
        ],
        [55, 120],
    )
    pdf.simple_table(
        ["覚えておく英語", "意味"],
        [
            ["Greater East Asia Co-Prosperity Sphere", "大東亜共栄圏 — 日本が掲げた「アジア解放」のスローガン"],
            ["Empire of Japan", "大日本帝国"],
            ["oil embargo", "石油禁輸"],
        ],
        [75, 100],
    )

    # --- SINGAPORE ---
    pdf.add_page()
    pdf.section_title("初期設定カード — シンガポールチーム", r=230, g=81, b=0)
    y_img = pdf.get_y()
    pdf.image(f"{IMG}/flag_singapore.png", x=pdf.l_margin, y=y_img, w=30)
    pdf.set_xy(pdf.l_margin + 34, y_img + 4)
    pdf.set_font("hira", "B", 11)
    pdf.set_text_color(230, 81, 0)
    pdf.cell(0, 7, "シンガポール — イギリス直轄植民地", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(y_img + 22)
    map_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.image(f"{IMG}/map_singapore.png", x=pdf.l_margin + 10, y=pdf.get_y(), w=map_w - 20)
    pdf.add_page()

    pdf.sub_title("1940年、あなたの国はこんな状況です", r=230, g=81, b=0)

    pdf.bold_body("あなたの国の紹介")
    pdf.body("シンガポールはイギリスの植民地です。独立した国ではありません。1819年にイギリス人ラッフルズが貿易港として開港して以来、120年間イギリスに支配されてきました。")
    pdf.body("街にはイギリス人が住む立派な洋館があり、アジア人とは別の世界に暮らしています。最高級のホテルやクラブには「ヨーロッパ人専用」の場所があり、アジア人は入れません。")
    pdf.ln(2)

    pdf.bold_body("あなたの国の人々")
    pdf.body("シンガポールの人口は約80万人。いろいろな民族がいます:")
    pdf.bullet("中華系 — 約75%（最も多い）")
    pdf.bullet("マレー系 — 約15%")
    pdf.bullet("インド系 — 約8%")
    pdf.bullet("ヨーロッパ人 — 約2%（支配層）")
    pdf.body("イギリス式の教育を受けたエリート層（\"King's Chinese\" と呼ばれた）はごく少数。大多数の中華系住民はイギリス人とほとんど接点がなく、中国語で暮らしています。")
    pdf.ln(2)

    pdf.bold_body("リー・クアンユー（LKY）という青年")
    pdf.body("1940年、17歳の青年リー・クアンユーがいます。のちにシンガポール建国の父となる人物ですが、今はただの優秀な学生です。イギリス式教育を受け、シンガポールとマラヤの卒業試験で首席になりました。")
    pdf.body("\"There was no question of any resentment. The superior status of the British in government and society was simply a fact of life.\"")
    pdf.body("（不満なんてなかった。政治でも社会でもイギリス人が上にいるのは、ただの事実だった。）", size=9)
    pdf.ln(2)

    pdf.bold_body("あなたの国の気持ち")
    pdf.bullet("「イギリス人が上にいるのは当然。彼らは世界で一番偉い人たちだから」")
    pdf.bullet("「シンガポールは貿易港として栄えているし、生活は安定している」")
    pdf.bullet("「でも、自分たちがこの国を治めるなんて、考えたこともない」")
    pdf.ln(2)

    pdf.simple_table(
        ["項目", "数字"],
        [
            ["イギリス支配の年数", "約120年（1819年〜）"],
            ["人口", "約80万人"],
            ["中華系の割合", "約75%"],
            ["LKYの年齢", "17歳（1940年時点）"],
        ],
        [55, 120],
    )
    pdf.simple_table(
        ["覚えておく英語", "意味"],
        [
            ["Crown Colony", "直轄植民地 — イギリス国王が直接統治する植民地"],
            ["Straits Settlements", "海峡植民地 — シンガポール・ペナン・マラッカの総称"],
            ["Raffles", "ラッフルズ — シンガポールを開港したイギリス人"],
        ],
        [75, 100],
    )

    # --- MALAYSIA ---
    pdf.add_page()
    pdf.section_title("初期設定カード — マレーシアチーム", r=46, g=125, b=50)
    y_img = pdf.get_y()
    pdf.image(f"{IMG}/flag_malaysia.png", x=pdf.l_margin, y=y_img, w=30)
    pdf.set_xy(pdf.l_margin + 34, y_img + 4)
    pdf.set_font("hira", "B", 11)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 7, "マラヤ（現マレーシア）— イギリス植民地", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(y_img + 22)
    map_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.image(f"{IMG}/map_malaysia.png", x=pdf.l_margin + 10, y=pdf.get_y(), w=map_w - 20)
    pdf.add_page()

    pdf.sub_title("1940年、あなたの国はこんな状況です", r=46, g=125, b=50)

    pdf.bold_body("あなたの国の紹介")
    pdf.body("まだ「マレーシア」という国は存在しません。あなたの国は「マラヤ」（Malaya）と呼ばれ、イギリスの植民地です。シンガポールのすぐ北に広がる半島全体がイギリスに支配されています。")
    pdf.body("マラヤは世界のゴムの約40%を生産し、錫（すず）の世界最大の生産地です。イギリスにとって非常に儲かる植民地です。")
    pdf.ln(2)

    pdf.bold_body("あなたの国の人々")
    pdf.body("イギリスは「分割して統治する」（Divide and Rule）という方法を使っています:")
    pdf.bullet("マレー人 → 農業・漁業に従事。イギリスからの奨学金が多く、政治的に優遇されている")
    pdf.bullet("中華系 → 錫の鉱山や商業で働く。お金は稼ぐが政治的な力はない")
    pdf.bullet("インド系 → ゴム農園や鉄道建設で働く")
    pdf.body("3つの民族はそれぞれ別の学校に通い、別の言語を話し、別の地域に住んでいます。イギリスがわざとそうしているのです — みんながバラバラなら、団結してイギリスに逆らうことがないから。")
    pdf.ln(2)

    pdf.bold_body("マレー人の気持ち")
    pdf.body("マレー人は自分たちがこの土地の「本来の持ち主」だと思っています。でも中華系やインド系の移民がどんどん増えて、脅威を感じています。")
    pdf.body("LKYの大学の同級生（マレー人）はこう言いました:")
    pdf.body("\"You Chinese are too energetic and too clever for us. We cannot stand the pressure.\"")
    pdf.body("（君たち中国人はエネルギッシュすぎて賢すぎる。我々はそのプレッシャーに耐えられない。）", size=9)
    pdf.ln(2)

    pdf.bold_body("あなたの国の気持ち")
    pdf.bullet("「この土地は本来マレー人のものだ。でもイギリスが中国人やインド人を連れてきた」")
    pdf.bullet("「中華系は商売が上手すぎて、このままでは追い越される」")
    pdf.bullet("「イギリスの支配は嫌だけど、少なくともマレー人を優遇してくれている」")
    pdf.ln(2)

    pdf.simple_table(
        ["項目", "数字"],
        [
            ["ゴムの世界シェア", "約40%"],
            ["錫の生産", "世界最大"],
            ["主要民族", "マレー系・中華系・インド系"],
            ["イギリス支配下の州", "9つのマレー州 + 海峡植民地"],
        ],
        [55, 120],
    )
    pdf.simple_table(
        ["覚えておく英語", "意味"],
        [
            ["Malaya", "マラヤ — 現在のマレーシア半島部"],
            ["Divide and Rule", "分割統治 — 民族を分断して支配する手法"],
            ["Malay States", "マレー諸州 — イギリスの保護下にあった9つの州"],
        ],
        [75, 100],
    )

    # --- BRITAIN ---
    pdf.add_page()
    pdf.section_title("初期設定カード — イギリスチーム", r=21, g=101, b=192)
    y_img = pdf.get_y()
    pdf.image(f"{IMG}/flag_britain.png", x=pdf.l_margin, y=y_img, w=30)
    pdf.set_xy(pdf.l_margin + 34, y_img + 4)
    pdf.set_font("hira", "B", 11)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 7, "大英帝国 — 太陽の沈まない国", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(y_img + 22)
    map_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.image(f"{IMG}/map_britain.png", x=pdf.l_margin + 10, y=pdf.get_y(), w=map_w - 20)
    pdf.add_page()

    pdf.sub_title("1940年、あなたの国はこんな状況です", r=21, g=101, b=192)

    pdf.bold_body("あなたの国の紹介")
    pdf.body("あなたの国は世界最大の帝国です。「大英帝国」（British Empire）は地球の陸地の24%を支配し、世界人口の約20%がイギリスの支配下にあります。「太陽の沈まない国」と呼ばれています。")
    pdf.body("東南アジアでは、マラヤ（現マレーシア）、シンガポール、ビルマ（現ミャンマー）、香港などを支配しています。マラヤからはゴムと錫、シンガポールは東南アジア全体の貿易拠点として莫大な利益を生んでいます。")
    pdf.ln(2)

    pdf.bold_body("シンガポールの海軍基地")
    pdf.body("シンガポールに巨大な海軍基地を建設しました。1923年から建設を開始し、5億ポンド以上をかけた一大事業です。「東洋のジブラルタル」と呼ばれ、難攻不落と言われています。")
    pdf.body("15インチの巨大砲が海に向けて設置されており、海からの攻撃は不可能 — そう信じられています。")
    pdf.ln(2)

    pdf.bold_body("しかし今、大問題が")
    pdf.body("1940年、イギリス本国はヨーロッパでナチス・ドイツとの戦争のまっただ中です。ロンドンはドイツ空軍に爆撃されています。東南アジアに送る兵力の余裕はほとんどありません。")
    pdf.body("マラヤ・シンガポールには約8万5千〜9万人の兵力（イギリス軍・オーストラリア軍・インド軍の混成）がいますが、訓練も装備も不十分です。")
    pdf.ln(2)

    pdf.bold_body("あなたの国の気持ち")
    pdf.bullet("「我々はこの地域を100年以上統治してきた。アジア人が我々に逆らえるはずがない」")
    pdf.bullet("「日本？あの小さな島国が大英帝国に勝てるわけがない」")
    pdf.bullet("「シンガポールの海軍基地は難攻不落だ」")
    pdf.body("LKYが見た映画では、日本軍の爆弾に \"Made in Japan\" と書いてあり不発弾だった — イギリス人は日本を見くびっていた。")
    pdf.ln(2)

    pdf.simple_table(
        ["項目", "数字"],
        [
            ["大英帝国の面積", "地球の陸地の24%"],
            ["支配下の人口", "世界人口の約20%"],
            ["シンガポール駐留兵力", "約85,000〜90,000人"],
            ["シンガポール海軍基地の建設費", "5億ポンド以上"],
        ],
        [55, 120],
    )
    pdf.simple_table(
        ["覚えておく英語", "意味"],
        [
            ["British Empire", "大英帝国"],
            ["The Empire on which the sun never sets", "太陽の沈まない国"],
            ["Gibraltar of the East", "東洋のジブラルタル — シンガポール海軍基地の異名"],
            ["white supremacy", "白人至上主義 — 白人が他の人種より優れているという考え"],
        ],
        [75, 100],
    )

    # ===== 3. PROGRAM =====
    pdf.add_page()
    pdf.section_title("3  プログラム進行")
    pdf.sub_title("3-a. タイムテーブル（通常版 約130分）")
    pdf.simple_table(
        ["時間", "フェーズ", "内容"],
        [
            ["0:00", "オープニング", "ルール説明・チーム分け"],
            ["0:10", "初期設定", "各チームが自国カードを読み、理解する"],
            ["0:20", "自己紹介", "「うちの国はこういう国です」と発表（各2分）"],
            ["0:30", "Round 1", "日本軍侵略（1941-42）"],
            ["0:50", "Round 2", "日本軍支配（1942-45）"],
            ["1:10", "休憩 10分", "（役の交換をする場合はここで）"],
            ["1:20", "Round 3", "原爆と終戦（1945）"],
            ["1:45", "Round 4", "イギリス再支配（1945-50s）"],
            ["2:05", "Round 5", "東南アジア独立（1950s-1965）"],
            ["2:25", "カード開示", "全チームの初期設定カードを一斉に共有"],
            ["2:35", "振り返り", "個人記入 → 全体共有"],
            ["2:50", "クロージング", "ファシリテーターまとめ"],
        ],
        [20, 35, 120],
    )

    pdf.sub_title("3-b. 各ラウンドの進め方（1ラウンド約20分）")
    pdf.simple_table(
        ["Step", "時間", "内容"],
        [
            ["1", "1分", "カード配布: 全チーム共通の「何が起きたか」を読む"],
            ["2", "2分", "国別ヒント: カード内の「あなたの国では」を読む"],
            ["3", "5分", "作戦会議: 「うちの国はどう感じた？」を話し合い、模造紙にメモ"],
            ["4", "10分", "国際会議: 各チーム発表(2分×4国) + 質問(2分)"],
            ["5", "2分", "ファシリテーターの一言: 見え方の違いを整理、次へ橋渡し"],
        ],
        [14, 16, 145],
    )

    pdf.ln(2)
    pdf.sub_title("3-c. カード開示フェーズ（R5終了後、約10分）")
    pdf.body("全ラウンド終了後、振り返りシート記入の前に行います。ラウンド中は自国のカードしか見ていなかった参加者に、他チームの「出発点」を明かし、後から点がつながる瞬間を作ります。")
    pdf.ln(2)
    pdf.simple_table(
        ["Step", "時間", "内容"],
        [
            ["1", "1分", "全チームの初期設定カードを配布（自チーム以外の3枚）"],
            ["2", "3分", "各チームが他の3カ国のカードを読む"],
            ["3", "5分", "気づきの共有:「他のチームのカードで一番驚いたことは？」"],
            ["4", "—", "振り返りシート記入へ移行"],
        ],
        [14, 16, 145],
    )
    pdf.bold_body("重要なルール", 10)
    pdf.bullet("初期設定カードはラウンド中は絶対に他チームに見せない — 自国の立場に没入するための仕掛け")
    pdf.bullet("口頭で自国の事情を語るのはOK。ただしカード自体の共有は最後まで取っておく")

    # ===== ROUND 1 =====
    pdf.add_page()
    pdf.section_title("Round 1  日本軍侵略 — 1941年12月〜1942年2月", badge="R1", r=191, g=54, b=12)

    pdf.sub_title("提示する事実（全チーム共通）")
    pdf.simple_table(
        ["日付", "出来事"],
        [
            ["1941年12月8日", "マラヤ北東コタバルに日本軍上陸、シンガポール空爆開始"],
            ["12月10日", "英海軍主力艦2隻が航空攻撃で撃沈（世界史上初）"],
            ["12月〜2月", "日本軍が自転車でマレー半島1,100kmを70日で南下"],
            ["1942年2月15日", "シンガポール陥落。英軍降伏（日本軍3.6万 vs 英軍8.5万）"],
        ],
        [35, 140],
    )

    pdf.sub_title("各チームに提示する情報")
    pdf.country_card("日本チーム", C_JAPAN, "山下奉文「マレーの虎」率いる第25軍。自転車部隊（銀輪部隊）がジャングルを駆け抜け、パンクしたリムの音を英兵が「戦車」と勘違い。英軍の見積もり「最低5ヶ月」を70日で達成。")
    pdf.country_card("シンガポールチーム", C_SINGAPORE, "LKY（18歳）: 12月8日午前4時、爆弾で目覚め。最初は「恐怖より興奮」。コーズウェイ爆破の音に\"That's the end of the British Empire!\"と叫ぶ。「イギリスは最強」という世界観が崩壊。")
    pdf.country_card("マレーシアチーム", C_MALAYSIA, "最初の戦場はマラヤ北東コタバル。ペナン島でイギリス人が夜のうちにアジア人を置き去りにして逃亡。「白人至上主義の神話が崩壊した瞬間」。")
    pdf.country_card("イギリスチーム", C_BRITAIN, "チャーチル: \"The fall of Singapore was the worst disaster and largest capitulation in British history.\" 15インチ砲は海（南）向き、日本は陸（北）から。85,000人が36,000人に敗北。")

    pdf.hint_box([
        "1. 日本軍の勝利は「すごいこと」？「怖いこと」？ — 立場によって違うか",
        "2. 「イギリスが負けた」ことは、シンガポールやマラヤの人にとって良いこと？悪いこと？",
        "3. もしあなたがシンガポールの18歳の学生だったら、何を感じる？",
    ])
    pdf.expect_box([
        "・日本チーム: 自国の軍事力に驚き、同時にこの先への不安",
        "・シンガポール/マレーシア: 「守ってくれるはずのイギリスが負けた」衝撃",
        "・イギリス: 「なぜ負けた？」と自問し、慢心に気づく",
        "・全体: 同じ「日本の勝利」が立場によって全く違う意味を持つことに気づく",
    ])
    pdf.facilitate_box([
        "・「人数で2倍以上なのに負けた。なぜ？」と全体に問いかけ",
        "・議論が止まったら「もしその時代のその国に住んでいたら？」と促す",
        "・まとめ: 「イギリスの敗北」の心理的インパクトを整理し、R2へ橋渡し",
    ])

    # ===== ROUND 2 =====
    pdf.add_page()
    pdf.section_title("Round 2  日本軍支配 — 1942年2月〜1945年8月", badge="R2", r=191, g=54, b=12)

    pdf.sub_title("提示する事実（全チーム共通）")
    pdf.body("シンガポールは「昭南島」（Syonan-to）に改名。3年半の占領。")
    pdf.simple_table(
        ["出来事", "内容"],
        [
            ["Sook Ching（粛清）", "中華系男性を集め銃殺。日本側6,000人/SG側推定5万〜10万人"],
            ["憲兵隊（Kempeitai）", "軍事警察による恐怖政治。拷問、密告の奨励"],
            ["飢餓", "物資不足。人口 約80万→60万に減少"],
            ["軍票（バナナ・ノート）", "シリアル番号なしの紙幣。価値が急落"],
        ],
        [45, 130],
    )

    pdf.sub_title("各チームに提示する情報")
    pdf.country_card("日本チーム", C_JAPAN, "「大東亜共栄圏」を掲げたが実際はSook Ching、慰安所、見せしめの処刑。「暴力は日本の軍隊システムの一部だった」。辛い事実だが、事実を知ることが多面的な視点の第一歩。")
    pdf.country_card("シンガポールチーム", C_SINGAPORE, "LKYはSook Chingの検問をぎりぎり通過。日本語を学び、闇市で商売し生き延びた。LKY: \"The three and a half years of Japanese occupation were the most important of my life.\"")
    pdf.country_card("マレーシアチーム", C_MALAYSIA, "捕虜はタイ-ビルマ鉄道で過酷な強制労働。抗日ゲリラ（MPAJA）がジャングル戦。マレー人は「日本が新たな保護者になるかも」と期待する者も。民族により態度が分かれた。")
    pdf.country_card("イギリスチーム", C_BRITAIN, "兵士は「世界中のどこの捕虜よりもひどい」扱い。チャンギ刑務所、泰緬鉄道。イギリスの威信は完全崩壊。ヨーロッパ戦線で手一杯、東南アジア奪還は最終段階まで不可能。")

    pdf.hint_box([
        "1. 日本軍はなぜ降伏直後にSook Chingを行ったのか？",
        "2. LKYは占領を「人生で最も重要な時期」と呼んだ。つらい経験から学べるか？",
        "3. 占領下のシンガポールに住んでいたら、生き延びるために何をする？",
    ])
    pdf.expect_box([
        "・日本チーム: 「解放」と実態のギャップに動揺。個人vs組織の問題を考え始める",
        "・シンガポール: 極限状態での生存本能、LKYの強さに感嘆",
        "・マレーシア: 同じ占領下でも民族により立場が違うことに気づく",
        "・イギリス: 自国兵士の惨状、「守れなかった」責任を感じ始める",
    ])
    pdf.facilitate_box([
        "・感情的になったら: 「つらいよね。でも今感じていること自体がすごく大事」",
        "・「個々の兵士が悪人か？ 軍隊のシステムの問題か？」と構造的に考えるよう促す",
        "・まとめ: 「加害と被害は一面的ではない」を確認し、休憩（＋役の交換）へ",
    ])

    # ===== ROUND 3 =====
    pdf.add_page()
    pdf.section_title("Round 3  原爆と終戦 — 1945年8月〜9月", badge="R3", r=191, g=54, b=12)

    pdf.sub_title("提示する事実（全チーム共通）")
    pdf.simple_table(
        ["日付", "出来事"],
        [
            ["8月6日", "広島に原子爆弾投下（死者約14万人）"],
            ["8月9日", "長崎に原子爆弾投下（死者約7万人）"],
            ["8月15日", "天皇が降伏を発表（玉音放送）"],
            ["8/15〜9/5", "約3週間の権力の空白 — 復讐・リンチが横行"],
            ["9月12日", "シンガポール市庁舎で正式な降伏式典"],
        ],
        [30, 145],
    )

    pdf.sub_title("各チームに提示する情報")
    pdf.country_card("日本チーム", C_JAPAN, "広島・長崎で一般市民約21万人が犠牲。降伏式典でLKYは日本人将校を見た: \"They represented an army that had not been routed in battle.\" 日本にとって — 市民への大量虐殺であり「被害者」でもあることの象徴。")
    pdf.country_card("シンガポールチーム", C_SINGAPORE, "3年半の占領からの解放のきっかけ。LKY: \"I have no doubts about whether the two atom bombs were necessary.\" 権力の空白期間に協力者への復讐が横行。イギリスが戻ってきても、もう以前のようには尊敬できない。")
    pdf.country_card("マレーシアチーム", C_MALAYSIA, "抗日ゲリラ（MPAJA）が姿を現し「人民法廷」を設置。即決処刑やリンチ。日本軍がいなくなった途端に別の武装集団が街を支配。「解放」≠「平和」。")
    pdf.country_card("イギリスチーム", C_BRITAIN, "捕虜にとって原爆は文字通り命を救った。マウントバッテン卿が「勝者」として降伏式典を主導。しかしアジア人の尊敬は得られない。アメリカが圧倒的な力を持ち、世界一の座を明け渡しつつある。")

    pdf.ln(2)
    pdf.bold_body("核心: 同じ「原爆」の見え方が4カ国で全く違う", 10)
    pdf.simple_table(
        ["立場", "原爆の見え方"],
        [
            ["日本", "民間人の大量虐殺。絶対に許されない"],
            ["シンガポール", "解放のきっかけ。LKY: \"I have no doubts\""],
            ["マレーシア", "さらなる苦しみを止めた。しかし終戦後の混乱も"],
            ["イギリス", "捕虜の命を救った。しかし威信は戻らなかった"],
        ],
        [35, 140],
    )

    pdf.hint_box([
        "1. 同じ出来事なのに4カ国でこんなに見え方が違う。なぜだろう？",
        "2. 「原爆は正しかったか？」— この問いに「正解」はあるのか？",
        "3. 「戦争が終わった」のに、すぐには平和にならなかった。なぜ？",
        "4. 「いろんな立場があると知ること」はなぜ大事か？",
    ])
    pdf.expect_box([
        "・日本: 被害と加害の両面に向き合う。「必要だった」という見方との落差に戸惑う",
        "・シンガポール/マレーシア: 「解放」と「復讐の連鎖」のジレンマ",
        "・イギリス: 「勝ったはず」なのに地位が戻らない矛盾",
        "・全体: 「正解がない」ことに初めて本気でぶつかる — ワークショップの核心",
    ])
    pdf.facilitate_box([
        "・役の交換後: 「さっきとは逆の国を語る感覚はどう？」と問う",
        "・正解を出そうとする議論には: 「答えを出さなくていい。見え方の違い自体が学び」",
        "・泣く子がいてもOK。無理に止めず見守る。「真剣に考えた証拠」",
    ])

    # ===== ROUND 4 =====
    pdf.add_page()
    pdf.section_title("Round 4  イギリス再支配 — 1945年〜1950年代", badge="R4", r=191, g=54, b=12)

    pdf.sub_title("提示する事実（全チーム共通）")
    pdf.simple_table(
        ["年", "出来事"],
        [
            ["1945年9月", "BMA（イギリス軍政）開始。運営混乱、汚職横行"],
            ["1946年1月", "シンガポールで大規模ストライキ（17万人参加）"],
            ["1946年", "マラヤ連合案 → マレー人猛反対 → UMNO結成"],
            ["1947年", "インドがイギリスから独立"],
            ["1948年", "マラヤ連邦発足。マラヤ非常事態開始"],
            ["1956年", "スエズ危機 — 大英帝国の終わりを象徴"],
        ],
        [30, 145],
    )

    pdf.sub_title("各チームに提示する情報")
    pdf.country_card("日本チーム", C_JAPAN, "アメリカ占領下で非軍事化・民主化・新憲法（第9条）。戦犯裁判: Sook Chingを計画した辻政信は逃亡し一度も裁かれず。LKY: 「歴代の日本政府はこれらの悪行について語ることを選ばなかった。ドイツとは違う」")
    pdf.country_card("シンガポールチーム", C_SINGAPORE, "BMAの汚職、17万人ストライキ。LKYは23歳でイギリスへ留学。「イギリスに支配され続けるのはもうおかしい」という思いが芽生え始める。")
    pdf.country_card("マレーシアチーム", C_MALAYSIA, "マラヤ連合案（全民族平等）にマレー人が猛反対。UMNO結成。「土地の本来の持ち主」vs「後から来た移民」。1948年、共産党武装蜂起でマラヤ非常事態（12年間）開始。")
    pdf.country_card("イギリスチーム", C_BRITAIN, "BMAは素人の軍人が運営。インド独立（1947）、スエズ危機（1956）で帝国崩壊が始まる。SG防衛費はGDPの約20%、3万人が軍関連雇用 — 撤退すれば経済大打撃。")

    pdf.hint_box([
        "1. イギリスは「戻ってきた」けど、もう以前のイギリスではなかった。何が変わった？",
        "2. マラヤの「全民族平等」問題 — 今の日本にも同じ問題はある？（移民、外国人の権利）",
        "3. 日本は経済復興に全力を注いだ。しかし戦争の歴史とどう向き合った？",
    ])
    pdf.expect_box([
        "・日本: 歴史認識の問題に直面。ドイツとの比較で考えが深まる",
        "・シンガポール: 植民地支配への疑問が芽生え、独立への伏線を感じる",
        "・マレーシア: 「平等」が必ずしも全員に歓迎されない複雑さを体感",
        "・イギリス: 帝国の崩壊は「時代の必然」だったのか考え始める",
    ])
    pdf.facilitate_box([
        "・「全民族平等」を現代に引きつける: 「日本にも外国人が増えている。同じ問題は？」",
        "・歴史認識は結論を押しつけない。ドイツと日本の違いを材料として提示",
        "・まとめ: 「戦後は終わりではなく、新しい問題の始まりだった」とR5へ",
    ])

    # ===== ROUND 5 =====
    pdf.add_page()
    pdf.section_title("Round 5  東南アジア独立 — 1950年代〜1965年", badge="R5", r=191, g=54, b=12)

    pdf.sub_title("提示する事実（全チーム共通）")
    pdf.simple_table(
        ["年", "出来事"],
        [
            ["1957年", "マラヤ独立"],
            ["1963年", "マレーシア連邦結成（マラヤ+SG+サバ+サラワク）"],
            ["1964年", "シンガポールで人種暴動が2回発生"],
            ["1965年8月9日", "マレーシアがシンガポールを追放。望まない独立"],
            ["1968年", "イギリス「スエズ以東からの撤退」宣言"],
        ],
        [30, 145],
    )

    pdf.sub_title("各チームに提示する情報")
    pdf.country_card("日本チーム", C_JAPAN, "敗戦23年で世界第2位のGDP（1968年）。東南アジアに積極投資。しかしLKYの姿勢は「尊敬、しかし許しではない」— 投資は歓迎するが靖国参拝・教科書問題には一貫して批判的。")
    pdf.country_card("シンガポールチーム", C_SINGAPORE, "LKY: \"Singapore had independence thrust upon it.\" 記者会見で泣き崩れた。面積214平方マイル、天然資源ゼロ、水すらマレーシアから輸入。しかしチャイナタウンでは爆竹で祝い、株式市場は上昇。")
    pdf.country_card("マレーシアチーム", C_MALAYSIA, "LKYの「Malaysian Malaysia」（全民族平等）にUMNO反発。人種暴動を経てトゥンクが最終決断 — シンガポール追放。法案は数時間で両院通過。")
    pdf.country_card("イギリスチーム", C_BRITAIN, "帝国解体が加速。SGの独立をわずか17時間で承認。1968年「スエズ以東からの撤退」宣言。かつて地球の24%を支配した帝国がわずか20年で崩壊。")

    pdf.hint_box([
        "1. SGは「独立を押し付けられた」国。資源もない。でも今は世界有数の豊かな国。なぜ？",
        "2. 日本の経済的成功と歴史への向き合い方 — 別の問題か？",
        "3. 全体を振り返って — 「完全に正しかった国」はあるか？",
    ])
    pdf.expect_box([
        "・全体: 5ラウンドを通じて「どの国にも理由がある」ことを実感",
        "・日本: 経済復興の誇りと歴史認識の課題を同時に抱える複雑さ",
        "・シンガポール: 逆境から国を作ったLKYのリーダーシップに感銘",
        "・「完全に正しかった国はない」という結論に自然と辿り着く",
    ])
    pdf.facilitate_box([
        "・「5ラウンドで一番印象に残ったのは？」と個人に短く聞く",
        "・「完全に正しかった国」がないことを確認しつつ「知ることに意味がある」と伝える",
        "・振り返りシートの記入へスムーズに移行",
    ])

    # ===== 4. REFLECTION =====
    pdf.add_page()
    pdf.section_title("4  振り返りと閉会")

    pdf.sub_title("振り返りシート（6つの設問）")
    pdf.simple_table(
        ["#", "設問", "意図"],
        [
            ["1", "ワークショップの前後でイメージはどう変わった？", "before/afterの変化を自覚"],
            ["2", "一番驚いたこと・心に残ったことは？", "印象深い学びの定着"],
            ["3", "「国によって見え方が違う」と感じた場面は？", "多角的視点の核心"],
            ["4", "もし別の国のチームだったら？", "他者の立場への想像力"],
            ["5", "日本の友達や家族に一つだけ伝えるとしたら？", "学びの言語化・持ち帰り"],
            ["6", "自由記述（感想、疑問、モヤモヤ）", "未消化の思いを受け止め"],
        ],
        [8, 85, 75],
    )

    pdf.ln(4)
    pdf.sub_title("クロージング — ファシリテーターのメッセージ")
    pdf.set_fill_color(240, 244, 255)
    pdf.set_draw_color(13, 71, 161)
    x = pdf.get_x()
    y = pdf.get_y()
    msg = (
        "5つのラウンドを通じて、同じ出来事が4つの国でまったく違う意味を持つことを体験しました。\n\n"
        "歴史に100:0はありません。\n\n"
        "どの国にも理由があり、どの国にも傷があります。大事なのは「どっちが正しいか」を決めることではなく、"
        "「相手がなぜそう思うのか」を理解しようとすることです。\n\n"
        "それができる人が、グローバルで信頼される人です。\n\n"
        "今日の体験を、忘れないでください。"
    )
    pdf.rect(x, y, pdf.w - pdf.l_margin - pdf.r_margin, 58, style="DF")
    pdf.set_line_width(1.2)
    pdf.line(x, y, x, y + 58)
    pdf.set_xy(x + 6, y + 4)
    pdf.set_font("hira", "", 10.5)
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 12, 6, msg)
    pdf.set_y(y + 62)

    pdf.ln(6)
    pdf.sub_title("フォローアップ")
    pdf.numbered(1, "当日の夜: 振り返りシートを元にグループで感想共有（夕食時など）")
    pdf.numbered(2, "翌日: 街歩きで「今日見たものは、どの時代の名残か？」を意識して歩く")
    pdf.numbered(3, "帰国後: 学校で発表 — 「シンガポールで学んだこと」")

    pdf.output(OUT)
    print(f"PDF saved: {OUT}")


if __name__ == "__main__":
    build()
