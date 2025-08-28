import os
import shutil
from copystatic import copy_source, generate_pages_recursive

static = "/home/arw74/bootdotdev/Static-site-generator/static"
public = "/home/arw74/bootdotdev/Static-site-generator/public"
content = "/home/arw74/bootdotdev/Static-site-generator/content"
template = "/home/arw74/bootdotdev/Static-site-generator/template.html"
dest_path = "/home/arw74/bootdotdev/Static-site-generator/public"


def main():
	copy_source(static, public)
	generate_pages_recursive(content, template, dest_path)

if __name__ == "__main__":
    main()
