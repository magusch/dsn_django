import re


class PostChecker:
    checkers = []

    def __init__(self, post):
        self.post = post
        self.result = {}
        self.start()

    def start(self):
        self.asterisk()
        self.underscore()
        self.length()
        self.title()
        self.place_empty()

    def asterisk(self):
        asterisk_len = len(re.findall(r"\*", self.post))  # how many asterisk in the post
        if asterisk_len % 2 != 0:
            error_message = f"The Post has odd number ({asterisk_len}) of * ."
            self.result['*'] = error_message

    def underscore(self):
        underscore_len = len(re.findall("_", self.post))  # how many underscore in the post
        if underscore_len % 2 != 0:
            error_message = f"The Post has odd number ({underscore_len}) of _ .\n"
            self.result['_'] = error_message

    def length(self):
        if len(self.post) > 1000:
            error_message = f"The Post has {len(self.post)} characters.\n"
            self.result['L'] = error_message

    def title(self):
        title = self.post.split("\n")[0]
        asterisk_len_title = len(re.findall(r"\*", title))
        if asterisk_len_title < 3:
            error_message = f"The title doesn't have enough *."
            self.result['T'] = error_message
        elif asterisk_len_title % 2 != 0:
            error_message = f"The title has odd number ({asterisk_len_title}) of * ."
            self.result['T'] = error_message

    def place_empty(self):
        if self.place is None:
            error_message = f"The place field is empty."
            self.result['P'] = error_message