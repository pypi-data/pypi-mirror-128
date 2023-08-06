from biblioteca.corpora.base import JsonDbCorpusReader


class TrveKvlt(JsonDbCorpusReader):
    def __init__(self):
        super().__init__("ytcat_trveKvlt")

    def entries(self, entry_id=None):
        for db_name, entries in self.corpora.items():
            for e in entries:
                eid = e.get("identifier")
                if not eid:
                    continue
                if entry_id:
                    if eid == entry_id:
                        yield db_name, e
                else:
                    yield eid, e

    def title(self, entry_id=None):
        for db_name, e in self.entries(entry_id):
            yield db_name, e["title"]

    def descriptions(self, entry_id=None):
        for db_name, e in self.entries(entry_id):
            yield db_name, e["description"]

    def tags(self, entry_id=None):
        for db_name, e in self.entries(entry_id):
            yield db_name, e["tags"] or []

