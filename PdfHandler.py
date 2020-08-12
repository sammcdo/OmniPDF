import fitz

class PdfHandler():
    def __init__(self, filename):
        self.pdf = fitz.open(filename)

        self.pages = [None] * len(self.pdf)
        for pageNum in range(len(self.pdf)):
            self.pages[pageNum] = self.pdf[pageNum].getDisplayList()

    def getImage(self, pageNum = 0):
        page = self.pages[pageNum]
        if page == None:
            self.pages[pageNum] = self.pdf[pageNum].getDisplayList()
            page = self.pages[pageNum]

        mat_0 = fitz.Matrix(1, 1)
        pixMap = page.getPixmap(matrix=mat_0, alpha=False)

        return pixMap.getImageData("ppm")

    def savePageAsImage(self, filename, pageNum=0):
        page = self.pages[pageNum]
        if page == None:
            self.pages[pageNum] = self.pdf[pageNum].getDisplayList()
            page = self.pages[pageNum]

        mat_0 = fitz.Matrix(1, 1)
        pixMap = page.getPixmap(matrix=mat_0, alpha=False)

        pixMap.writePNG(filename)
    
    def saveAs(self, filename):
        self.pdf.save(filename)
