from langchain_core.tools import tool


class CalculatorTools:
    @tool("evaluate calculation")
    def evaluate(data: str):
        """
        Perform given calculation
        The input to this tool should be a text with the plain calculation.
        For example: `3+2-(1+1)`
        Returns: 3
        """
        return eval(data).__str__()

    @tool("numerical conversion")
    def numerical_conversion(data: str):
        """
        Converts a string of numerical data to a floating point number to use it in calculations.
        example input: 1 million
        example output: 1000000
        """
        # Define a dictionary to map words to their numerical values
        word_to_number = {
            'thousand': 1e3,
            'million': 1e6,
            'billion': 1e9,
            'trillion': 1e12,
            # Add more words and their values as needed
        }
        # Split the input string into words
        words = data.split()
        # Initialize the result as a float
        result = word_to_number[words[1].lower()] * float(words[0])

        return result.__str__()
