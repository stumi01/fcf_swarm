from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from llm_util import beagle_7B


class DocumentTools:

    def handle(page_content: str) -> str:
        return page_content.replace('\n', ' ').replace('\t', ' ').replace('/s/', '').lower()

    def summarize_custom(asks: list[str], documents: list[Document]):
        prompt_template = """
            You are a financial expert who is well versed on reading company filings.
            Use the the following context:
            ------------
            {context}
            ------------
            You have to answer the following question: What is the company's 2023 '{ask}' ?:
            If you find a value for the item return using the following pattern: {ask} : [The number you found] | [scale]
            Example of an answer if you found: Sales: 200 | million 
            If you dont find a value for the item return: {ask} : ? | NA
            Always return based on the pattern! Dont every modify it. Do NOT give any other information!
            You MUST not forget that in finance documents a number in a parenthesis means negative value.
            In your answer use negative sign instead of parenthesis. example: (1234) will become: -1234.
            You MUST find if a value is meant to be in a specific units, example thousands.
            If there are more than one data give a formula using all the numbers.
            You MUST focus on the task only dont return extra information.
            """
        prompt = PromptTemplate.from_template(prompt_template)
        chain = create_stuff_documents_chain(llm=beagle_7B, prompt=prompt)
        result: dict = {key: [] for key in asks}
        for i_d, document in enumerate(documents):
            for i, ask in enumerate(asks):
                ret: str = chain.invoke({"context": [document], "ask": ask})
                if "NA" not in ret:
                    result[ask].append(ret.split("\n")[0])
            print("Progress {}%".format((i_d + 1) / (len(documents) / 100)))
        return result
