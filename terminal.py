import Language

while True:
    text = input('icl >>> ')
    if text == 'quit':
        break
    tokens, error = Language.run('<stdin>', text)
    if error:
        print(tokens, error)
    else:
        print(tokens)
