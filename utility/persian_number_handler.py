# persian_numbers.py
# Utility class for converting between Persian (Farsi) and English numerals,
# and for detecting the numeral language of a string.

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_DIGITS = "0123456789"

class PersianNumberHandler:
    @staticmethod
    def fa_to_en(s: str) -> str:
        """
        Convert all Persian digits in the input string to English digits.
        """
        table = str.maketrans(PERSIAN_DIGITS, ENGLISH_DIGITS)
        return s.translate(table)

    @staticmethod
    def en_to_fa(s: str) -> str:
        """
        Convert all English digits in the input string to Persian digits.
        """
        table = str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS)
        return s.translate(table)

    @staticmethod
    def detect_number_language(s: str) -> str:
        """
        Detect if the string contains Persian digits, English digits, or both.
        Returns: "persian", "english", or "mixed"
        """
        has_en = any(char in ENGLISH_DIGITS for char in s)
        has_fa = any(char in PERSIAN_DIGITS for char in s)
        if has_en and not has_fa:
            return "english"
        elif has_fa and not has_en:
            return "persian"
        elif has_en and has_fa:
            return "mixed"
        else:
            return "none"

# Example usage
if __name__ == "__main__":
    helper = PersianNumberHandler()
    samples = [
        "۱۲۳-۴۵۶",          # Only Persian
        "123456",          # Only English
        "۱۲۳abc456",       # Mixed
        "abc"              # None
    ]
    for s in samples:
        print(f"{s!r}: lang={helper.detect_number_language(s)} fa_to_en={helper.fa_to_en(s)} en_to_fa={helper.en_to_fa(s)}")