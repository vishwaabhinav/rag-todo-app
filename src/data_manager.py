def read_text_file(file_path):
    """Read text file from the given path and return its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def create_chunks(text, max_length=4096):
    """Create chunks of text with the given maximum length."""
    chunks = []
    for i in range(0, len(text), max_length):
        chunks.append(text[i:i + max_length])
    return chunks
