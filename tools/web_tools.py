from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents import Document

from tools.document_tools import DocumentTools


def _headers():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'Cache-Control': 'max-age=0',
        'Dnt': '1',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }


class WebTools:

    def load_webpage_to_document(url: str) -> list[Document]:
        loader = WebBaseLoader(url, header_template=_headers())
        docs = loader.load()
        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)
        new_documents = []

        for d in docs_transformed:
            new_document = Document(
                page_content=DocumentTools.handle(d.page_content), metadata={**d.metadata}
            )
            new_documents.append(new_document)
        new_documents = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500).split_documents(
            new_documents)
        return new_documents
