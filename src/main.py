from textnode import TextNode, split_link
import shutil
import os

def do_job():
    shutil.rmtree('public')
    shutil.copytree('static', 'public')

    

def main():
    do_job()


if __name__ == "__main__":
    main()
