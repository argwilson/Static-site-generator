import os
import shutil
from copystatic import copy_source, generate_page

static = "/home/arw74/bootdotdev/Static-site-generator/static"
public = "/home/arw74/bootdotdev/Static-site-generator/public"
md = "/home/arw74/bootdotdev/Static-site-generator/content/index.md"
template = "/home/arw74/bootdotdev/Static-site-generator/template.html"
dest_path = "/home/arw74/bootdotdev/Static-site-generator/public/index.html"


def main():
	copy_source(static, public)
	generate_page(md, template, dest_path)

if __name__ == "__main__":
    main()
