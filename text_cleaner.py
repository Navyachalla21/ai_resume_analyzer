import re

def clean_text(text: str) -> str:
    """
    Cleans raw resume text for comparison:
    - Converts to lowercase
    - Removes extra whitespace/newlines
    - Keeps important technical symbols like C++, C#, .NET
    """
    text = text.lower()

    # Temporarily protect important technical symbols so they aren't stripped
    text = text.replace("c++", "cplusplus").replace("c#", "csharp").replace(".net", "dotnet")

    # Remove unwanted characters, but keep letters, numbers, spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Restore protected symbols
    text = text.replace("cplusplus", "c++").replace("csharp", "c#").replace("dotnet", ".net")

    # Collapse multiple spaces/newlines into a single space
    text = re.sub(r"\s+", " ", text).strip()

    return text