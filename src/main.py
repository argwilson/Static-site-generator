import os
import shutil
from copystatic import copy_static
from textnode import TextNode

def main():
	copy_static()
	print(os.listdir("/home/arw74/bootdotdev/Static-site-generator/public"))
	print(os.listdir("/home/arw74/bootdotdev/Static-site-generator/public/images"))

if __name__ == "__main__":
    main()
