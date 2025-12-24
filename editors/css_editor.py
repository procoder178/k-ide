from PyQt5.Qsci import QsciAPIs, QsciLexerCSS, QsciScintilla
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QKeyEvent
from utils.keywords import css_keywords, css_values


class CssEditorTextArea(QsciScintilla):
    def __init__(self):
        super().__init__()
        self.font = QFont("Consolas", 15)
        self.setFont(self.font)

        self.keyword = css_keywords + css_values

        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsBackgroundColor(QColor("#383838"))
        self.setMarginsForegroundColor(QColor("#949494"))

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(183, 181, 190, 40))
        self.setCaretForegroundColor(QColor("#FFFFFF"))

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#282A36"))
        self.setMatchedBraceForegroundColor(QColor("#00DA1F"))
        self.setUnmatchedBraceBackgroundColor(QColor("#282A36"))
        self.setUnmatchedBraceForegroundColor(QColor("#D22439"))

        self.lexer = QsciLexerCSS()
        self.lexer.setFont(QFont(self.font))
        self.setLexer(self.lexer)
        self.apply_theme(self.lexer)

        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)
        self.setTabIndents(True)

        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(True)
        self.setAutoCompletionFillupsEnabled(True)
        self.setAutoCompletionFillups("():")
        self.api = QsciAPIs(self.lexer)
        for w in self.keyword:
            self.api.add(w)
        self.api.prepare()

    def apply_theme(self, lex):
        lex.setPaper(QColor("#282A36"))
        lex.setColor(QColor("#ABB2BF"), 0)  # Default
        lex.setColor(QColor("#E06C75"), 1)  # Tag
        lex.setColor(QColor("#E06C75"), 2)  # ClassSelector
        lex.setColor(QColor("#C678DD"), 3)  # PseudoClass
        lex.setColor(QColor("#E06C75"), 4)  # UnknownPseudoClass
        lex.setColor(QColor("#56B6C2"), 5)  # Operator
        lex.setColor(QColor("#E06C75"), 6)  # CSS1Property
        lex.setColor(QColor("#E06C75"), 7)  # UnknownProperty
        lex.setColor(QColor("#E06C75"), 15)  # CSS2Property
        lex.setColor(QColor("#E06C75"), 17)  # CSS3Property
        lex.setColor(QColor("#E06C75"), 19)  # ExtendedCSSProperty
        lex.setColor(QColor("#E06C75"), 20)  # ExtendedPseudoClass
        lex.setColor(QColor("#E06C75"), 21)  # ExtendedPseudoElement
        lex.setColor(QColor("#E06C75"), 18)  # PseudoElement
        lex.setColor(QColor("#98C379"), 8)  # Value
        lex.setColor(QColor("#7F848E"), 9)  # Comment
        lex.setColor(QColor("#E06C75"), 10)  # IDSelector
        lex.setColor(QColor("#C678DD"), 11)  # Important
        lex.setColor(QColor("#C678DD"), 12)  # AtRule
        lex.setColor(QColor("#C678DD"), 22)  # MediaRule
        lex.setColor(QColor("#E06C75"), 16)  # Attribute
        lex.setColor(QColor("#98C379"), 13)  # DoubleQuotedString
        lex.setColor(QColor("#98C379"), 14)  # SingleQuotedString
        lex.setColor(QColor("#E06C75"), 23)  # Variable

    def keyPressEvent(self, event: QKeyEvent):
        pairs = {
            "(": ")",
            "[": "]",
            "{": "}",
            "'": "'",
            '"': '"',
            ":": ";",
        }
        key = event.text()
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            line, idx = self.getCursorPosition()
            text = self.text(line)
            prev_char = text[idx - 1] if idx > 0 else None
            next_char = text[idx] if idx < len(text) else None
            super().keyPressEvent(event)
            if (
                prev_char in ["{", "[", "("]
                and next_char == pairs[prev_char]
            ):
                indent = " " * 4
                self.insert(indent + "\n")
                new_line = line + 1
                self.setCursorPosition(new_line, len(indent))
        elif key.isprintable():
            super().keyPressEvent(event)
            if key in pairs.keys():
                self.insert(pairs[key])
        else:
            super().keyPressEvent(event)
