# Character to Emoji Mapping
char_to_emoji = {
    'a': '😀', 'b': '😁', 'c': '😂', 'd': '😃', 'e': '😄',
    'f': '😅', 'g': '😆', 'h': '😇', 'i': '😈', 'j': '😉',
    'k': '😊', 'l': '😋', 'm': '😌', 'n': '😍', 'o': '😎',
    'p': '😏', 'q': '😐', 'r': '😑', 's': '😒', 't': '😓',
    'u': '😔', 'v': '😕', 'w': '😖', 'x': '😗', 'y': '😘',
    'z': '😙', ' ': '😚', '0': '🤓', '1': '😪', '2': '😷',
    '3': '😵', '4': '😲', '5': '😡', '6': '😳', '7': '🤬',
    '8': '🤯', '9': '😱', '!': '😴', '?': '🤔', '.': '😛',
    ',': '😜', '\'': '😝', '"': '🤗', ':': '😬', ';': '🤒',
    '(': '🤕', ')': '🤡', '-': '🤠', '_': '🥳', '+': '🥴',
    '*': '🥺', '/': '🤥', '=': '🤫', '&': '🤭', '%': '🤢',
    '@': '🤧', '#': '🤮', '$': '🥵', '^': '🥶', '`': '😈',
    '~': '👿', '[': '👻', ']': '💀', '{': '☠️', '}': '👽',
    '|': '👾', '<': '🤖', '>': '😺', '\\': '😸'
}

# Reverse the dictionary for decoding
emoji_to_char = {v: k for k, v in char_to_emoji.items()}

# Encode function
def encode_text(text):
    text = text.lower()
    encoded_text = ''.join(char_to_emoji.get(char, char) for char in text)
    return encoded_text

# Decode function
def decode_text(encoded_text):
    encoded_text = encoded_text.lower()
    decoded_text = ''.join(emoji_to_char.get(char, char) for char in encoded_text)
    return decoded_text