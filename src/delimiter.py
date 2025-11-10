from textnode import TextNode, TextType
from extractLinks import extract_markdown_images, extract_markdown_links

#Takes in list of old nodes, delimiter and a text type
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #Final list
    returnList = []
    for node in old_nodes:
        #Append the current node if TextType doesn't equal TextType.TEXT
        if node.text_type != TextType.TEXT:
            returnList.append(node)
            continue
        #smaller list
        split_nodes = []
        #splits on passed in delimiter
        node_split = node.text.split(delimiter)
        #If the split text has an even length, it's incorrect
        if len(node_split) % 2 == 0:
            raise ValueError("Unclosed delimiter")
        for i in range(len(node_split)):
            #if the node index is an empty string, continue the loop
            if node_split[i] == "":
                continue
            #If node index is even, as in not the text type, append it as a new node
            #with a text type of TEXT
            if i % 2 == 0:
                split_nodes.append(TextNode(node_split[i], TextType.TEXT))
            #Add new TextNode node with text_type passed in
            else:
                split_nodes.append(TextNode(node_split[i], text_type))
        #extend all the values in the smaller list to the final returned list
        returnList.extend(split_nodes)
    return returnList


def split_nodes_image(old_nodes):
    returnList = []
    #Loop through nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            returnList.append(node)
            continue

        split_nodes = []
        #Get extracted markdown text from regex
        extracted = extract_markdown_images(node.text)
        #Keep track of current text
        current = node.text
        #If extracted is empty append node and break the loop
        if len(extracted) == 0:
            returnList.append(node)
            continue
        #Loop through extracted markdown
        for e in extracted:
            #Split text on markdown text but only split one time
            text = current.split(f"![{e[0]}]({e[1]})", 1)
            #Change current to remaining text
            current = text[1]
            #Make sure text[0] isn't an empty string
            if text[0] != "":
                #Create textnode with first half of split text as a text type
                split_nodes.append(TextNode(text[0], TextType.TEXT))
            #Create textnode with current extracted markdown image text
            split_nodes.append(TextNode(e[0], TextType.IMAGE, e[1]))
        #If there is left over text in current append a new node with remaining text
        if len(current) != 0:
            split_nodes.append(TextNode(current, TextType.TEXT))
        #Extend split nodes into the return list
        returnList.extend(split_nodes)
    return returnList

def split_nodes_link(old_nodes):
    returnList = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            returnList.append(node)
            continue
        split_nodes = []
        #Get extracted markdown text from regex
        extracted = extract_markdown_links(node.text)
        #Keep track of current text
        current = node.text
        #If extracted is empty append node and break the loop
        if len(extracted) == 0:
            returnList.append(node)
            continue
        #Loop through extracted markdown
        for e in extracted:
            #Split text on markdown text but only split one time
            text = current.split(f"[{e[0]}]({e[1]})", 1)
            #Change current to remaining text
            current = text[1]
            #Make sure text[0] isn't an empty string
            if text[0] != "":
                #Create textnode with first half of split text as a text type
                split_nodes.append(TextNode(text[0], TextType.TEXT))
            #Create textnode with current extracted markdown link text
            split_nodes.append(TextNode(e[0], TextType.LINK, e[1]))
        #If there is left over text in current append a new node with remaining text
        if len(current) != 0:
            split_nodes.append(TextNode(current, TextType.TEXT))            
        #Extend split nodes into the return list
        returnList.extend(split_nodes)
    return returnList
