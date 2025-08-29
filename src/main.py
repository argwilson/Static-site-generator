import sys
from copystatic import copy_source, generate_pages_recursive

static = "/home/arw74/bootdotdev/Static-site-generator/static"
content = "/home/arw74/bootdotdev/Static-site-generator/content"
template = "/home/arw74/bootdotdev/Static-site-generator/template.html"
dest_path = "/home/arw74/bootdotdev/Static-site-generator/docs"


def main():
	copy_source(static, dest_path)
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	else:
		basepath = '/'
	generate_pages_recursive(content, template, dest_path, basepath)

if __name__ == "__main__":
    main()
