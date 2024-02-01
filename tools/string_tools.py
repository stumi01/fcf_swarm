import re


class StringTools:

    def strip_items(strings: list[str], prefix: str) -> list[str]:
        """
        Strip prefix from all the items in the strings parameter
        remove items which are not matching the [number] | [scale] pattern
        """
        cleaned_strings = []
        for s in strings:
            new_string = \
                s.replace(prefix, "").replace(":", "").replace("$", "").replace("(", '').replace(")", "").splitlines()[
                    0].strip()
            if new_string.count("|") == 1:
                cleaned_strings.append(new_string)
        return cleaned_strings

    def clean_items(strings: list[str]):
        cleaned_strings = []
        for s in strings:
            # Use a regular expression to remove non-alphabetical characters
            cleaned_string = re.sub(r'[^a-zA-Z, ]', '', s)
            cleaned_strings.append(cleaned_string.strip())
        return cleaned_strings

    @classmethod
    def clean_numerical_string(cls, param: str) -> str:
        res = param.strip().replace("|", "").replace("  ", " ").replace(",", "").lower()
        words = res.split(" ")
        if len(words) >= 2:
            return ' '.join(words[:2])
        else:
            return res
