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







main()