from textnode import *
from htmlnode import *

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







main()