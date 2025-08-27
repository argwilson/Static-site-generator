import os
import shutil
from textnode import TextNode


def static_to_public():
	static = "/home/arw74/bootdotdev/Static-site-generator/static"
	public = "/home/arw74/bootdotdev/Static-site-generator/public"

	if os.path.exists(public):
		shutil.rmtree(public)
	os.mkdir(public)
	def get_source_paths(source, drc):
		item_paths = []
		for item in os.listdir(source):
			item_path = os.path.join(source, item)
			if not os.path.isfile(item_path):
				new_drc = os.path.join(drc, item)
				os.mkdir(new_drc)
				new_path = get_source_paths(item_path, new_drc)
				item_paths.extend(new_path)
			else:
				item_paths.append(item_path)
		return item_paths
	paths = get_source_paths(static, public)
	for path in paths:
		new_path = path.replace('static', 'public')
		shutil.copy(path, new_path)

def main():
	static_to_public()
	print(os.listdir("/home/arw74/bootdotdev/Static-site-generator/public"))
	print(os.listdir("/home/arw74/bootdotdev/Static-site-generator/public/images"))

if __name__ == "__main__":
    main()
