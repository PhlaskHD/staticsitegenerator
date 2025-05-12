from textnode import *
from htmlnode import *
import re

def main():
    tester = TextNode("testing123", TextType.LINK, "fakeurl.com")
    ht_tester = HTMLNode("bullshit", "dogshit", ["idfk"], {"href":"www.google.com", "target":"myass"})



def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            if "![" in text_node.text:
                alt_text = text_node.text[2:text_node.text.find("]")]
            else:
                alt_text = text_node.text
            if text_node.url == None:
                just_img_text = text_node.text[text_node.text.find("](")+2:]
                img_txt = just_img_text[:just_img_text.find(")")]
                return LeafNode("img", "", {"src":img_txt, "alt":alt_text})
            return LeafNode("img", "", {"src":text_node.url, "alt":alt_text})
        case _:
            raise Exception("Invalid text_type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for each in old_nodes:
        if each.text_type is not TextType.TEXT:
            new_nodes.append(each)
        else:
            if each.text.find(delimiter) == -1:
                new_nodes.append(each)
            else:
                temp_list = each.text.split(delimiter)
                if len(temp_list) % 2 == 0:
                    raise Exception("No closing delimiter detected")
                for i in range(0, len(temp_list)):
                    if temp_list[i] == "":
                        pass
                    elif i % 2 == 0:
                        new_nodes.append(TextNode(temp_list[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(temp_list[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for each in old_nodes:
        if each.text_type != TextType.TEXT:
            new_nodes.append(each)
            continue
        tups = extract_markdown_images(each.text)
        if tups == []:
            new_nodes.append(each)
            continue
        else:
            remaining_text = each.text
            for i in range(len(tups)):
                alt, img = tups[i]
                split_text = remaining_text.split(f"![{alt}]({img})", 1)
                if split_text[0] == "":
                    pass
                else:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, img))
                if i == len(tups)-1 and split_text[1] != "":
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))
                remaining_text = split_text[1]
    return new_nodes

            



def split_nodes_link(old_nodes):
    new_nodes = []
    for each in old_nodes:
        if each.text_type != TextType.TEXT:
            new_nodes.append(each)
            continue
        tups = extract_markdown_links(each.text)
        if tups == []:
            new_nodes.append(each)
            continue
        else:
            remaining_text = each.text
            for i in range(len(tups)):
                text, url = tups[i]
                split_text = remaining_text.split(f"[{text}]({url})", 1)
                if split_text[0] == "":
                    pass
                else:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINK, url))
                if i == len(tups)-1 and split_text[1] != "":
                    new_nodes.append(TextNode(split_text[1], TextType.TEXT))
                remaining_text = split_text[1]
    return new_nodes


def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    italics_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italics_nodes, "`", TextType.CODE)
    return split_nodes_link(split_nodes_image(code_nodes))

main()