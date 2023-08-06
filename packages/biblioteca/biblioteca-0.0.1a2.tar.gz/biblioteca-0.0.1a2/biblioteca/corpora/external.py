from os.path import join

from biblioteca.corpora import TextCorpusReader


class Aeiouado(TextCorpusReader):
    def __init__(self):
        super().__init__("aeiouado")

    def load(self):
        with open(join(self.folder, "aeiouado-ipa-01.csv"),
                  errors='surrogateescape') as fi:
            self.corpora = [l for l in fi.read().split("\n") if l.strip()]

    def lines(self, *args, **kwargs):
        for f in self.corpora:
            yield f

    def words(self, *args, **kwargs):
        for l in self.lines():
            yield l.split("\t")[0]

    def sentences(self, *args, **kwargs):
        return self.words()

    def paragraphs(self, *args, **kwargs):
        return self.sentences()

    def tagged_words(self):
        for l in self.lines():
            yield l.split("\t")

    def pronounciations(self):
        return {k: v for (k, v) in self.tagged_words()}


class NILC(TextCorpusReader):
    def __init__(self):
        super().__init__("NILC_taggers")

    def load(self):
        with open(join(self.folder, "corpus100.txt"),
                  encoding="latin1") as fi:
            self.corpora = [l for l in fi.read().split("\n") if l.strip()]

    def lines(self, *args, **kwargs):
        for f in self.corpora:
            yield f

    def words(self, *args, **kwargs):
        for tagged in self.tagged_sentences():
            for s in tagged:
                yield s[0]

    def sentences(self, *args, **kwargs):
        for tagged in self.tagged_sentences():
            yield " ".join(s[0] for s in tagged)

    def paragraphs(self, *args, **kwargs):
        return self.sentences()

    def tagged_sentences(self):
        for l in self.lines():
            tagged = []
            for word in l.split(" "):
                if not word:
                    continue
                w = word.split("_")[0]
                t = word[len(w) + 1:]
                tagged.append((w, t))
            yield tagged

    def tag_list(self):
        tags = []
        for tagged in self.tagged_sentences():
            for s in tagged:
                tags.append(s[1])
        return sorted(list(set(tags)))

    def tags(self):
        tags = {}
        for tagged in self.tagged_sentences():
            for s in tagged:
                if s[1] not in tags:
                    tags[s[1]] = []
                if s[0] not in tags[s[1]]:
                    tags[s[1]].append(s[0])
        return tags


class FlorestaBase(TextCorpusReader):
    def load(self):
        self.corpora = []
        for f in self.get_file_names():
            if not f.endswith(".dep"):
                continue
            with open(join(self.folder, f), encoding="latin1") as fi:
                lines = fi.read().split("</s>")
                for l in lines:
                    if not l or l.startswith("<") or l.startswith("$"):
                        continue

                    tagged_words = []
                    for w in l.split("\n"):
                        if "\t" not in w:
                            continue
                        word, tags = w.split("\t")[:2]
                        tags = [t for t in tags.split(" ") if t.isupper()
                                and "<" not in t]
                        if tags:
                            tagged_words.append((word, tags[0]))
                    print(tagged_words)
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


class FlorestaCP(FlorestaBase):
    def __init__(self):
        super().__init__("FlorestaVirgem_CP_3.0")


class FlorestaCF(FlorestaBase):
    def __init__(self):
        super().__init__("FlorestaVirgem_CF_3.0")
