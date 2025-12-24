from PyQt5.Qsci import QsciAPIs, QsciLexerJava, QsciScintilla
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QKeyEvent
from utils.keywords import java_keywords


class JavaEditorTextArea(QsciScintilla):
    def __init__(self):
        super().__init__()
        self.font = QFont("Consolas", 15)
        self.setFont(self.font)

        self.keyword = java_keywords

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

        self.lexer = QsciLexerJava()
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
        lex.setColor(QColor("#7F848E"), 1)
        lex.setColor(QColor("#98C379"), 3)
        lex.setColor(QColor("#C678DD"), 17)
        lex.setColor(QColor("#C678DD"), 18)
        lex.setColor(QColor("#7F848E"), 2)
        lex.setColor(QColor("#98C379"), 15)
        lex.setColor(QColor("#ABB2BF"), 0)
        lex.setColor(QColor("#98C379"), 6)
        lex.setColor(QColor("#98C379"), 27)
        lex.setColor(QColor("#E5C07B"), 19)
        lex.setColor(QColor("#98C379"), 22)
        lex.setColor(QColor("#E06C75"), 11)
        lex.setColor(QColor("#C678DD"), 5)
        lex.setColor(QColor("#E5C07B"), 16)
        lex.setColor(QColor("#D19A66"), 4)
        lex.setColor(QColor("#56B6C2"), 10)
        lex.setColor(QColor("#7F848E"), 9)
        lex.setColor(QColor("#7F848E"), 26)
        lex.setColor(QColor("#98C379"), 24)
        lex.setColor(QColor("#98C379"), 20)
        lex.setColor(QColor("#98C379"), 14)
        lex.setColor(QColor("#98C379"), 7)
        lex.setColor(QColor("#56B6C2"), 26)
        lex.setColor(QColor("#98C379"), 21)
        lex.setColor(QColor("#E06C75"), 8)
        lex.setColor(QColor("#98C379"), 12)
        lex.setColor(QColor("#E06C75"), 25)
        lex.setColor(QColor("#98C379"), 13)

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
