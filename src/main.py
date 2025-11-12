from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from delimiter import split_nodes_delimiter, split_nodes_link, split_nodes_image
from extractLinks import extract_markdown_images, extract_markdown_links
from converter import *
from block import *
from htmlconverter import *

import os, shutil


def main():
    #Copy static files to public directory
    static_to_public("static/", "public/")
    #Grabs H1 header title from index.md
    generate_pages_recursive("content/", "template.html", "public/")


#Recursive function that copies all contents from sourceDir to destDir
def static_to_public(sourceDir, destDir):
    #First Verify sourceDir exists
    if os.path.exists(sourceDir):
        #Check if destDir exists, if so, delete it
        if os.path.exists(destDir):
            print(f"{destDir} exists, deleting and recreating...")
            shutil.rmtree(destDir, ignore_errors=True)
            os.mkdir(destDir)
        else:
            print(f"{destDir} does not exist, creating...")
            os.mkdir(destDir)
        #List contents of source directory
        srcContents = os.listdir(sourceDir)
        #Loop through items in the source directory
        for item in srcContents:
            #Create item path
            itemPath = os.path.join(sourceDir, item)
            #If its a file, copy to destination dir
            if os.path.isfile(itemPath):
                print(f"Copying {itemPath} to {destDir}{item}")
                shutil.copy(itemPath, destDir)
            else:
                #If it's a folder, recurse
                static_to_public(f"{itemPath}/", f"{destDir}{item}/")
    else:
        print(f"{sourceDir} does not exist")

#Pulls H1 header from markdown file, raises exception if header is not found
def extract_title(markdown):
    with open(markdown) as file:
        first_line = file.readline()
    if first_line.startswith("# "):
        stripped = first_line.strip("# ")
        stripped = stripped.rstrip()
        return stripped
    else:
        raise Exception("Not a valid header")
    

#
def generate_page(from_path, template_path, dest_path):
    #Print message "Generating page from from_path to dest_path using template_path"
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #Read markdown file
    with open(from_path) as file:
        md_content = file.read()
    #Read template file
    with open(template_path) as file:
        temp_content = file.read()
    #Convert markdown to html
    convertedMarkdown = markdown_to_html_node(md_content)
    #Convert html nodes to html
    mdHTML = convertedMarkdown.to_html()
    #Get title of markdown
    title = extract_title(from_path)
    #Replace title and content with extracted title and generated content
    titleReplace = temp_content.replace("{{ Title }}", title)
    contentReplace = titleReplace.replace("{{ Content }}", mdHTML)
    print(f"Creating index.html with {from_path} content at {dest_path}")
    with open(dest_path, "w") as file:
        file.write(contentReplace)

#Generate pages recursively
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(dest_dir_path)
    if os.path.exists(dir_path_content):
        #Get files/directories in current directory
        currentPath = os.listdir(dir_path_content)
        #loop through items
        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)
        for item in currentPath:
            itemPath = os.path.join(dir_path_content, item)
            #If it's a file, create the file at the destination directory path
            if os.path.isfile(itemPath):
                print(f"Creating {itemPath} with template {template_path} at {dest_dir_path}")
                #Read markdown file
                with open(itemPath) as file:
                    md_content = file.read()
                #Read template file
                with open(template_path) as file:
                    temp_content = file.read()
                #Convert markdown to html
                convertMD = markdown_to_html_node(md_content)
                #Convert html nodes to html
                mdHTML = convertMD.to_html()
                #Get title of markdown
                title = extract_title(itemPath)
                #Replace title and content with extracted title and generated content
                temp = temp_content.replace("{{ Title }}", title)
                contentReplace = temp.replace("{{ Content }}", mdHTML)
                #Create path to place new file
                newFile = item.replace(".md", ".html")
                dest_dir_path_item = dest_dir_path + newFile
                #Write the file
                with open(dest_dir_path_item, "w") as file:
                    file.write(contentReplace)
            else:
                #Create new dir path
                new_dir_path = itemPath + "/"
                #Create new destination path
                new_dest = dest_dir_path + item + "/"
                #Recursively iterate over folders
                generate_pages_recursive(new_dir_path, template_path, new_dest)
                

    else:
        raise Exception("Path does not exist")
    
    










    

if __name__ == "__main__":
    main()