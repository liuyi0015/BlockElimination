from pygame.key import key_code


def ffind(text):
    with open("data", "r", encoding="utf-8") as file:
        alltext = file.read()
        begin = alltext.find(text)+len(text)
        res = ''
        i = begin
        while alltext[i] != '\n':
            res += alltext[i]
            i += 1
        del i
        return res


def fromlinefind(text, line):
    with open("data", "r", encoding="utf-8") as f:
        linetexts = f.readlines()
        i = linetexts[line].find(text)+1
        x = ''
        while linetexts[line][i] != '\n':
            x += linetexts[line][i]
            i += 1
        return x


def keynum(key):
    if key == "ctrl":
        key = "left ctrl"
    elif key == "shift":
        key = "left shift"
    elif key == "esc":
        key = "escape"
    return key_code(key)

