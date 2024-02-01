# region helpers
tip_section = """You MUST do this task only and nothing else. Do not explain your final answer if not asked to.
    If you do your BEST WORK, I'll give you a $10,000 commission!"""
# endregion

task_identify = """
    Identify the components needed for FCF calculation which can be found in a company 10-K filings.
    You MUST not include any data that is not relevant for the calculation of the Free Cash Flow (FCF)
    The final answer MUST be an exhaustive list with the names of the data to search separated by a comma.
    {}""".format(tip_section)


def task_formula(output: str) -> str:
    return """
        Observe the following list:
        '''{}'''
        Using this list give me a formula for calculating the Free Cash Flow (FCF).
        MUST not try to calculate the Free Cash Flow just provide the formula.
        The final answer MUST be between single quotes.
        Example for calculating the area of a rectangle: "A*B" where A and B are the width and height of the rectangle. 
        {}
        """.format(output, tip_section)


def task_selection(list: str, formula: str) -> str:
    return """
        Observe the following list:
        '''{list}'''
        Compare with the following formula:
        "{formula}"
        Return with a list where the only elements are the values of the formula.
        The final answer MUST be a list with the reduced items.
        Example for the list "A,B,C,D,E" and the formula "X = A+C*D" the answer is "A,C,D"
        {tips}
        """.format(list=list, formula=formula, tips=tip_section)


def task_collect(items: str, url: str) -> str:
    return """
    Collect the data for '{items}' from the company's 10-K filings from : {url}
    You MUST answer with all the items and the corresponding financial data in a list.
    You MUST answer with the list only , do not include any other information, dont add explanation to it.
    {tips}
    """.format(items=items, url=url, tips=tip_section)


def task_replace(items: str, formula: str) -> str:
    return """
        Given the following formula '{formula}'
        Replace the formula with the actual values from the following list
        {items}
        You MUST answer with an actionable computation with the numbers only.
        Do not do the calculation.
        {tips}
        """.format(items=items, formula=formula, tips=tip_section)
