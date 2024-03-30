from PyQt5.Qsci import QsciLexerCPP
from PyQt5.QtGui import QColor, QFont


class CPP_Lexer(QsciLexerCPP):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDefaultColor(QColor("#abb2bf"))
        self.setDefaultFont(QFont("Consolas") , 14)
        self.setDefaultPaper(QColor("#1e1f22"))
        
        self.setColor(QColor("#abb2bf"))
        self.setColor(QColor("#C586C0"), self.PreProcessor)
        self.setColor(QColor("#C586C0"), self.InactivePreProcessor)

        self.setColor(QColor("#569CD6"), self.Keyword)
        self.setColor(QColor("#569CD6"), self.InactiveKeyword)
        self.setColor(QColor("#569CD6"), self.KeywordSet2)
        self.setColor(QColor("#569CD6"), self.InactiveKeywordSet2)

        self.setColor(QColor("#4EC9B0"), self.GlobalClass)
        self.setColor(QColor("#4EC9B0"), self.InactiveGlobalClass)

        self.setColor(QColor("#CE9178"), self.DoubleQuotedString)
        self.setColor(QColor("#CE9178"), self.InactiveDoubleQuotedString)
        self.setColor(QColor("#CE9178"), self.SingleQuotedString)
        self.setColor(QColor("#CE9178"), self.InactiveSingleQuotedString)
        self.setColor(QColor("#CE9178"), self.UnclosedString)
        self.setColor(QColor("#CE9178"), self.InactiveUnclosedString)
        self.setColor(QColor("#CE9178"), self.VerbatimString)
        self.setColor(QColor("#CE9178"), self.InactiveVerbatimString)
        self.setColor(QColor("#CE9178"), self.RawString)
        self.setColor(QColor("#CE9178"), self.InactiveRawString)
        self.setColor(QColor("#CE9178"), self.TripleQuotedVerbatimString)
        self.setColor(QColor("#CE9178"), self.InactiveTripleQuotedVerbatimString)
        self.setColor(QColor("#CE9178"), self.HashQuotedString)
        self.setColor(QColor("#CE9178"), self.InactiveHashQuotedString)

        self.setColor(QColor("#B5CEA8"), self.Number)
        self.setColor(QColor("#B5CEA8"), self.InactiveNumber)

        self.setColor(QColor("#6A9955"), self.Comment)
        self.setColor(QColor("#6A9955"), self.InactiveComment)
        self.setColor(QColor("#6A9955"), self.CommentLine)
        self.setColor(QColor("#6A9955"), self.InactiveCommentLine)
        self.setColor(QColor("#6A9955"), self.CommentDoc)
        self.setColor(QColor("#6A9955"), self.InactiveCommentDoc)
        self.setColor(QColor("#6A9955"), self.CommentLineDoc)
        self.setColor(QColor("#6A9955"), self.InactiveCommentLineDoc)
        self.setColor(QColor("#6A9955"), self.CommentDocKeyword)
        self.setColor(QColor("#6A9955"), self.InactiveCommentDocKeyword)
        self.setColor(QColor("#6A9955"), self.CommentDocKeywordError)
        self.setColor(QColor("#6A9955"), self.InactiveCommentDocKeywordError)
        self.setColor(QColor("#6A9955"), self.PreProcessorComment)
        self.setColor(QColor("#6A9955"), self.InactivePreProcessorComment)
        self.setColor(QColor("#6A9955"), self.PreProcessorCommentLineDoc)
        self.setColor(QColor("#6A9955"), self.InactivePreProcessorCommentLineDoc)

	self.setPaper(QColor("#1e1f22"))
        self.setFont(QFont("Consolas" , 14))
	
