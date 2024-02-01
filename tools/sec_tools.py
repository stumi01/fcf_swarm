from collections import Counter

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from llm_util import beagle_7B
from tools.document_tools import DocumentTools
from tools.string_tools import StringTools
from tools.web_tools import WebTools


class SECTools:

    @tool("Extract from 10-K form")
    def extract_from_10k(data: str) -> str:
        """
        Useful to search information from the latest 10-K form for a given URL.
        The input to this tool should be a pipe (|) separated text of length two, representing the URL you are interested, searched values separated by a comma ().
        For example, `https://www.sec.gov/ix?doc=/Archives/edgar/data/1234/1234/aapl-20230930.htm|Net Income,Inventory`.
        """
        url, ask = data.split("|")
        list = ask.split(",")
        content = WebTools.load_webpage_to_document(url)
        output = DocumentTools.summarize_custom(list, content)
        print(output)
        for element in list:
            print("########", element, "#######")
            items = StringTools.strip_items(output[element], element)
            counter = Counter(items)
            most_common = counter.most_common(1)
            if most_common[0][1] > 1:
                output[element] = most_common[0][0]
                continue
            prompt_template = """
                        Use the the following context:
                        ------------
                        {context}
                        ------------
                        The format of the given context is:
                        [Search phrase] : [answer] | [scale]
                        Your job is to find the most likely answer to the Search phrase from the given context only!.
                        Filter out items which are not containing numbers.
                        You must include one and ONLY ONE of the items from the context.
                        """
            prompt = PromptTemplate.from_template(prompt_template)
            chain = create_stuff_documents_chain(llm=beagle_7B, prompt=prompt)
            result = chain.invoke({"context": [Document(page_content="".join(items))]})
            output[element] = result
        for element in output:
            output[element] = StringTools.clean_numerical_string(output[element])
        return output.__str__()
