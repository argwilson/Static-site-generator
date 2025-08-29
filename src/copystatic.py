import os
import re
import shutil
from blocktypes import markdown_to_html_node, extract_title
import htmlnode

# Function that will be used to copy from static directory to public directory 
def copy_source(source, directory):
	# If directory already exists, deletes it.
	if os.path.exists(directory):
		shutil.rmtree(directory)
	# Creates a new empty directory
	os.mkdir(directory)
	# Inner function to help copy files from source to directory, returns path location to each file found and creates subdirectories in location where files are to be copied
	def get_source_paths(src, drc):
		item_paths = []
		for item in os.listdir(src):
			# Creates a new path for each subdirectory or file in source 
			item_path = os.path.join(src, item)
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
	# Calls inner function on source and directory
	paths = get_source_paths(source, directory)
	# Finds appropriate location in directory to create copy of source
	_, source_name = os.path.split(source)
	_, direct_name = os.path.split(directory)
	for path in paths:
		new_path = path.replace(source_name, direct_name)
		shutil.copy(path, new_path)

def generate_page(from_path, template_path, dest_path, base_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	md_file = open(from_path, 'r')
	md = md_file.read()
	md_file.close()
	temp_file = open(template_path, 'r')
	template = temp_file.read()
	temp_file.close()
	node = markdown_to_html_node(md)
	html_string = node.to_html()
	title = extract_title(md)
	template = template.replace(r"{{ Title }}", title)
	template = template.replace(r"{{ Content }}", html_string)
	if base_path != '/':
		template = template.replace(r'href="/', rf'href="{base_path}')
		template = template.replace(r'src="/', rf'src="{base_path}')
	f = open(dest_path, 'w')
	f.write(template)
	f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
	for item in os.listdir(dir_path_content):
		new_path = os.path.join(dir_path_content, item)
		if not item.endswith('.md'):
			new_dest = os.path.join(dest_dir_path, item)
			os.mkdir(new_dest)
			generate_pages_recursive(new_path, template_path, new_dest, base_path)
		else:
			md_file = open(new_path, 'r')
			md = md_file.read()
			md_file.close()
			temp_file = open(template_path, 'r')
			template = temp_file.read()
			temp_file.close()
			node = markdown_to_html_node(md)
			html_string = node.to_html()
			title = extract_title(md)
			template = template.replace(r"{{ Title }}", title)
			template = template.replace(r"{{ Content }}", html_string)
			if base_path != '/':
				template = template.replace(r'href="/', rf'href="{base_path}')
				template = template.replace(r'src="/', rf'src="{base_path}')
			filename = dest_dir_path + '/index.html'
			f = open(filename, 'w')
			f.write(template)
			f.close()
			return
		