from PyQt5.Qsci import QsciAPIs, QsciLexerCPP, QsciScintilla
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QKeyEvent
from utils.keywords import cpp_keywords


class CppEditorTextArea(QsciScintilla):
    def __init__(self):
        super().__init__()
        self.font = QFont("Consolas", 15)
        self.setFont(self.font)

        self.keyword = cpp_keywords

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

        self.lexer = QsciLexerCPP()
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
        lex.setColor(QColor("#7F848E"), 1)  # Comment
        lex.setColor(QColor("#7F848E"), 2)  # CommentLine
        lex.setColor(QColor("#7F848E"), 3)  # CommentDoc
        lex.setColor(QColor("#D19A66"), 4)  # Number
        lex.setColor(QColor("#C678DD"), 5)  # Keyword
        lex.setColor(QColor("#98C379"), 6)  # DoubleQuotedString
        lex.setColor(QColor("#98C379"), 7)  # SingleQuotedString
        lex.setColor(QColor("#E06C75"), 8)  # UUID
        lex.setColor(QColor("#7F848E"), 9)  # PreProcessor
        lex.setColor(QColor("#56B6C2"), 10)  # Operator
        lex.setColor(QColor("#E06C75"), 11)  # Identifier
        lex.setColor(QColor("#E06C75"), 12)  # UnclosedString
        lex.setColor(QColor("#98C379"), 13)  # VerbatimString
        lex.setColor(QColor("#98C379"), 14)  # Regex
        lex.setColor(QColor("#7F848E"), 15)  # CommentLineDoc
        lex.setColor(QColor("#C678DD"), 16)  # KeywordSet2
        lex.setColor(QColor("#E5C07B"), 17)  # CommentDocKeyword
        lex.setColor(QColor("#E06C75"), 18)  # CommentDocKeywordError
        lex.setColor(QColor("#E5C07B"), 19)  # GlobalClass
        lex.setColor(QColor("#98C379"), 20)  # RawString
        lex.setColor(QColor("#98C379"), 21)  # TripleQuotedVerbatimString
        lex.setColor(QColor("#98C379"), 22)  # HashQuotedString
        lex.setColor(QColor("#7F848E"), 23)  # PreProcessorComment
        lex.setColor(QColor("#7F848E"), 24)  # PreProcessorCommentLineDoc
        lex.setColor(QColor("#E06C75"), 25)  # UserLiteral
        lex.setColor(QColor("#E5C07B"), 26)  # TaskMarker
        lex.setColor(QColor("#98C379"), 27)  # EscapeSequence
        lex.setColor(QColor("#ABB2BF"), 64)  # InactiveDefault
        lex.setColor(QColor("#7F848E"), 65)  # InactiveComment
        lex.setColor(QColor("#7F848E"), 66)  # InactiveCommentLine
        lex.setColor(QColor("#7F848E"), 67)  # InactiveCommentDoc
        lex.setColor(QColor("#D19A66"), 68)  # InactiveNumber
        lex.setColor(QColor("#C678DD"), 69)  # InactiveKeyword
        lex.setColor(QColor("#98C379"), 70)  # InactiveDoubleQuotedString
        lex.setColor(QColor("#98C379"), 71)  # InactiveSingleQuotedString
        lex.setColor(QColor("#E06C75"), 72)  # InactiveUUID
        lex.setColor(QColor("#7F848E"), 73)  # InactivePreProcessor
        lex.setColor(QColor("#56B6C2"), 74)  # InactiveOperator
        lex.setColor(QColor("#E06C75"), 75)  # InactiveIdentifier
        lex.setColor(QColor("#E06C75"), 76)  # InactiveUnclosedString
        lex.setColor(QColor("#98C379"), 77)  # InactiveVerbatimString
        lex.setColor(QColor("#98C379"), 78)  # InactiveRegex
        lex.setColor(QColor("#7F848E"), 79)  # InactiveCommentLineDoc
        lex.setColor(QColor("#C678DD"), 80)  # InactiveKeywordSet2
        lex.setColor(QColor("#E5C07B"), 81)  # InactiveCommentDocKeyword
        lex.setColor(
            QColor("#E06C75"), 82
        )  # InactiveCommentDocKeywordError
        lex.setColor(QColor("#E5C07B"), 83)  # InactiveGlobalClass
        lex.setColor(QColor("#98C379"), 84)  # InactiveRawString
        lex.setColor(
            QColor("#98C379"), 85
        )  # InactiveTripleQuotedVerbatimString
        lex.setColor(QColor("#98C379"), 86)  # InactiveHashQuotedString
        lex.setColor(QColor("#7F848E"), 87)  # InactivePreProcessorComment
        lex.setColor(
            QColor("#7F848E"), 88
        )  # InactivePreProcessorCommentLineDoc
        lex.setColor(QColor("#E06C75"), 89)  # InactiveUserLiteral
        lex.setColor(QColor("#E5C07B"), 90)  # InactiveTaskMarker
        lex.setColor(QColor("#98C379"), 91)  # InactiveEscapeSequence

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
