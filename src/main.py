from textnode import TextNode, split_link

def main():
    node = TextNode('This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). The End!', 'text')
    res = split_link([node], 'link')
    print(res)


if __name__ == "__main__":
    main()
