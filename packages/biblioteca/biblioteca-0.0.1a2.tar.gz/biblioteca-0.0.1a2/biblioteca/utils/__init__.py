import json
import logging
import shutil
import tarfile
from os import listdir, makedirs, removedirs
from os.path import isfile, dirname, isdir, basename

import requests
from xdg import BaseDirectory as XDG

from biblioteca.corpora import *
from biblioteca.corpora.base import JsonDbCorpusReader, JsonCorpusReader, \
    TextCorpusReader, AbstractCorpusReader
from biblioteca.corpora.external import *

LOG = logging.getLogger("JarbasBiblioteca")
LOG.setLevel("DEBUG")

RESOURCE_DIR = join(dirname(dirname(__file__)), "res")
CORPUS_IDS = []
CORPUS_META = {}
_BASE_URL = "https://github.com/OpenJarbas/biblioteca/releases/download"
_VERSION = "0.0.1a1"
CORPUS2URL = {}

def _load_meta():
    global CORPUS_META, CORPUS_IDS
    for f in listdir(RESOURCE_DIR):
        if not f.endswith(".json"):
            continue
        c = f.replace(".json", "")
        CORPUS_IDS.append(c)
        with open(join(RESOURCE_DIR, f)) as fi:
            CORPUS_META[c] = json.load(fi)

        CORPUS2URL[c] = CORPUS_META[c].get("download_url") or \
                        _BASE_URL + f"/{ _VERSION}/{c}.tar.gz"


CORPUS2CLASS = {
    "yesnoquestions_V0.1": YesNoQuestions,
    "metal_songs": MetalSongs,
    "metal_bands": MetalBands,
    "metal_lyrics": MetalLyrics,
    "ytcat_trveKvlt": TrveKvlt,
    "cess_esp_udep": CessEspUniversal,
    "cess_cat_udep": CessCatUniversal,
    "nilc_udep": NILC,
    # external datasets
    "aeiouado": Aeiouado,
    "NILC_taggers": NILC
}

_load_meta()


# external corpus
EXTERNAL_CORPORA = {
    # portuguese
    "FlorestaVirgem_CF_3.0": "https://www.linguateca.pt/Floresta/ficheiros/FlorestaVirgem_CF_3.0.dep",
    "FlorestaVirgem_CP_3.0": "https://www.linguateca.pt/Floresta/ficheiros/FlorestaVirgem_CP_3.0.dep",
    "NILC_taggers": "http://www.nilc.icmc.usp.br/nilc/download/corpus100.txt",
    "macmorpho_v3": "http://www.nilc.icmc.usp.br/macmorpho/macmorpho-v3.tgz",
    "macmorpho_v2": "http://www.nilc.icmc.usp.br/macmorpho/macmorpho-v2.tgz",
    "macmorpho_v1": "http://www.nilc.icmc.usp.br/macmorpho/macmorpho-v1.tgz",
    "aeiouado": "http://www.nilc.icmc.usp.br/aeiouado/media/aeiouado-ipa-01.csv",

    # other
    "contraCAT": "https://github.com/BennoKrojer/ContraCAT/archive/refs/heads/master.tar.gz",
    "inclusivecoref": "https://github.com/TristaCao/into_inclusivecoref/archive/refs/heads/master.tar.gz",
    "gap_coreference": "https://github.com/google-research-datasets/gap-coreference/archive/refs/heads/master.tar.gz"
}


def untar(src, dst_folder):
    with tarfile.open(src) as tar:
        tar.extractall(path=dst_folder)


def download(corpus_id, force=False):
    base_folder = join(XDG.save_data_path("JarbasBiblioteca"), corpus_id)

    if not isdir(base_folder):
        makedirs(base_folder)

    if corpus_id in CORPUS_IDS:
        url = CORPUS2URL[corpus_id]
        path = join(XDG.save_data_path("JarbasBiblioteca"),
                    corpus_id + ".tar.gz")
    elif corpus_id in EXTERNAL_CORPORA:
        url = EXTERNAL_CORPORA[corpus_id]
        path = join(XDG.save_data_path("JarbasBiblioteca"),
                    url.split("/")[-1])
    else:
        raise ValueError("invalid corpus_id")

    if isfile(path) and not force:
        if (path.endswith(".tar.gz") or path.endswith(".tgz")) and \
                (not isdir(base_folder) or len(listdir(base_folder)) == 0):
            # not extracted ?
            try:
                untar(path, base_folder)
            except:  # corrupted download?
                if not force:
                    return download(corpus_id, force=True)
        LOG.info("Already downloaded " + corpus_id)
        return base_folder
    LOG.info("downloading " + corpus_id)
    LOG.info(url)
    LOG.info("this might take a while...")
    with open(path, "wb") as f:
        f.write(requests.get(url).content)

    # extract .tar.gz to folder
    if path.endswith(".tar.gz") or path.endswith(".tgz"):
        if isdir(base_folder):
            removedirs(base_folder)
        untar(path, base_folder)
    else:
        # move or copy ?
        shutil.copy(path, join(base_folder, basename(path)))
    return base_folder

def load_corpus(corpus_id):
    if corpus_id not in CORPUS_META:
        raise ValueError("unknown corpus_id")

    base_folder = join(XDG.save_data_path("JarbasBiblioteca"), corpus_id)
    if not isdir(base_folder):
        raise FileNotFoundError(f"run biblioteca.download('{corpus_id}')")
    # dedicated class for this corpus
    if corpus_id in CORPUS2CLASS:
        return CORPUS2CLASS[corpus_id]()

    fmt = CORPUS_META[corpus_id]["format"]

    LOG.debug("loading: " + base_folder)

    if fmt == "text":
        return TextCorpusReader(corpus_id)
    elif fmt == "json":
        return JsonCorpusReader(corpus_id)
    elif fmt == "jsondb":
        return JsonDbCorpusReader(corpus_id)
    return AbstractCorpusReader(corpus_id)
