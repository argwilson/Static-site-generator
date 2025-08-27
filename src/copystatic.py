import os
import shutil

def copy_static():
	static = "/home/arw74/bootdotdev/Static-site-generator/static"
	public = "/home/arw74/bootdotdev/Static-site-generator/public"

	# If public directory already exists, deletes it.
	if os.path.exists(public):
		shutil.rmtree(public)
	# Creates a new empty public directory
	os.mkdir(public)
	# Inner function to help copy files from static to public, returns path location to each file found and creates subdirectories in location where files are to be copied
	def get_source_paths(source, drc):
		item_paths = []
		for item in os.listdir(source):
			# Creates a new path for each subdirectory or file in source 
			item_path = os.path.join(source, item)
			if not os.path.isfile(item_path):
				# Creates a copy of a subdirectory from source path to directory path (will happen on each recursion)
				new_drc = os.path.join(drc, item)
				os.mkdir(new_drc)
				# Recursion of function to find any files in their respective subdirectories and adds them to the items_paths list
				new_path = get_source_paths(item_path, new_drc)
				item_paths.extend(new_path)
			else:
				# Adds file to item_paths list
				item_paths.append(item_path)
		return item_paths
	# Calls inner function on static and public
	paths = get_source_paths(static, public)
	# Finds appropriate location in public directory to create copy of static directory
	for path in paths:
		new_path = path.replace('static', 'public')
		shutil.copy(path, new_path)