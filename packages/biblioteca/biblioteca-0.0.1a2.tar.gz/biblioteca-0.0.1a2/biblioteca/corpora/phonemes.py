from os.path import join

from biblioteca.corpora.base import TextCorpusReader


class YesNoQuestions(TextCorpusReader):
    def __init__(self):
        super().__init__("yesnoquestions_V0.1")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s


class MetalBands(TextCorpusReader):
    def __init__(self):
        super().__init__("metal_bands")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s

    def paragraphs(self, file_id=None):
        for s in self.lines(file_id):
            yield s


class MetalSongs(TextCorpusReader):
    def __init__(self):
        super().__init__("metal_songs")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s

    def paragraphs(self, file_id=None):
        for s in self.lines(file_id):
            yield s


class MetalLyrics(TextCorpusReader):
    def __init__(self):
        super().__init__("metal_lyrics")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s

    def paragraphs(self, file_id=None):
        if file_id:
            yield file_id, self.corpora[file_id].split("\n\n")
        else:
            for f in self.corpora:
                yield f, self.corpora[f].split("\n\n")


class CessBase(TextCorpusReader):
    def load(self):
        self.corpora = []
        for f in self.get_file_names():
            if not f.endswith(".txt"):
                continue
            with open(join(self.folder, f), errors='surrogateescape') as fi:
                lines = fi.read().split("\n\n")
                for l in lines:
                    if not l:
                        continue
                    tagged_words = [tuple(w.split("\t"))
                                    for w in l.split("\n")]
                    self.corpora += [tagged_words]

    def lines(self, *args, **kwargs):
        for f in self.corpora:
            yield f

    def words(self, *args, **kwargs):
        for l in self.lines():
            for w in l:
                yield w[0]

    def sentences(self, *args, **kwargs):
        for l in self.lines():
            yield " ".join([w[0] for w in l])

    def paragraphs(self, *args, **kwargs):
        for l in self.sentences():
            yield l

    def tagged_words(self):
        for l in self.lines():
            for w in l:
                yield w

    def tagged_sentences(self):
        for l in self.lines():
            yield l


class CessCatUniversal(CessBase):
    def __init__(self):
        super().__init__("cess_cat_universal")


class CessEspUniversal(CessBase):
    def __init__(self):
        super().__init__("cess_esp_universal")


