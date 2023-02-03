from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

import vcr_langchain as vcr


@vcr.use_cassette()
def test_openai_embeddings() -> None:
    with open("tests/resources/state_of_the_union.txt") as f:
        state_of_the_union = f.read()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(state_of_the_union)
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(
        texts, embeddings, metadatas=[{"source": i} for i in range(len(texts))]
    )
    assert len(docsearch.index_to_docstore_id) > 0
