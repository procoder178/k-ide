from PyQt5.Qsci import QsciAPIs, QsciLexerLua, QsciScintilla
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QKeyEvent
from utils.keywords import lua_keywords


class LuaEditorTextArea(QsciScintilla):

    def __init__(self):
        super().__init__()
        self.font = QFont("Consolas", 15)
        self.setFont(self.font)

        self.kw = lua_keywords

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

        self.lexer = QsciLexerLua()
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
        for w in self.kw:
            self.api.add(w)
        self.api.prepare()

    def keyPressEvent(self, event: QKeyEvent):
        pairs = {"(": ")", "[": "]", "{": "}", "'": "'", '"': '"'}
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

    def apply_theme(self, lex):
        lex.setPaper(QColor("#282A36"))
        lex.setColor(QColor("#ABB2BF"), 0)  # Default
        lex.setColor(QColor("#7F848E"), 1)  # Comment
        lex.setColor(QColor("#7F848E"), 2)  # LineComment
        lex.setColor(QColor("#D19A66"), 4)  # Number
        lex.setColor(QColor("#C678DD"), 5)  # Keyword
        lex.setColor(QColor("#98C379"), 6)  # String
        lex.setColor(QColor("#98C379"), 7)  # Character
        lex.setColor(QColor("#98C379"), 8)  # LiteralString
        lex.setColor(QColor("#7F848E"), 9)  # Preprocessor
        lex.setColor(QColor("#56B6C2"), 10)  # Operator
        lex.setColor(QColor("#E06C75"), 11)  # Identifier
        lex.setColor(QColor("#E06C75"), 12)  # UnclosedString
        lex.setColor(QColor("#E5C07B"), 13)  # BasicFunctions
        lex.setColor(QColor("#E5C07B"), 14)  # StringTableMathsFunctions
        lex.setColor(QColor("#E5C07B"), 15)  # CoroutinesIOSystemFacilities
        lex.setColor(QColor("#E5C07B"), 16)  # KeywordSet5
        lex.setColor(QColor("#C678DD"), 17)  # KeywordSet6
        lex.setColor(QColor("#C678DD"), 18)  # KeywordSet7
        lex.setColor(QColor("#C678DD"), 19)  # KeywordSet8
        lex.setColor(QColor("#E06C75"), 20)  # Label
