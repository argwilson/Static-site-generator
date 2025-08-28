import os
import shutil
from copystatic import copy_source
from textnode import TextNode

static = "/home/arw74/bootdotdev/Static-site-generator/static"
public = "/home/arw74/bootdotdev/Static-site-generator/public"

def main():
	copy_source(static, public)
	print(os.listdir("/home/arw74/bootdotdev/Static-site-generator/public"))
	print(os.listdir("/home/arw74/bootdotdev/Static-site-generator/public/images"))

if __name__ == "__main__":
    main()
