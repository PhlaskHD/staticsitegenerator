import re
from textnode import *
from htmlnode import *

def markdown_to_html_node(markdown):
    parent_node = ParentNode("div", [])
    split = markdown_to_blocks(markdown)
    for block in split:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            clean_text = " ".join(line.strip() for line in block.split("\n"))
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            paragraph_node = ParentNode("p", [])
            children = text_to_children(clean_text)
            paragraph_node.children = children
            parent_node.children.append(paragraph_node)
        elif block_type == BlockType.HEADING:
            heading_level = 0
            for char in block:
                if char == '#':
                    heading_level += 1
                else:
                    break
            heading_content = block[heading_level:].lstrip()
            heading_tag = f"h{heading_level}"
            heading_node = ParentNode(heading_tag, [])
            children = text_to_children(heading_content)
            heading_node.children = children
            parent_node.children.append(heading_node)
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            if lines[0].strip() == "```":
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code_content = "\n".join(line.strip() for line in lines) + "\n"
            code_text_node = TextNode(code_content, TextType.TEXT)
            code_html_node = text_node_to_html_node(code_text_node)
            pre_node = ParentNode("pre", [])
            code_node = ParentNode("code", [code_html_node])
            pre_node.children = [code_node]
            parent_node.children.append(pre_node)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_lines = []
            for line in lines:
                if line.startswith(">"):
                    cleaned_line = line[1:].lstrip()
                    quote_lines.append(cleaned_line)
                else:
                    quote_lines.append(line)
            quote_content = "\n".join(quote_lines)
            quote_node = ParentNode("blockquote", [])
            children = text_to_children(quote_content)
            quote_node.children = children
            parent_node.children.append(quote_node)
        elif block_type == BlockType.UNORDERED_LIST:
            ul_node = ParentNode("ul", [])
            lines = block.split("\n")
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and (stripped_line.startswith("- ") or stripped_line.startswith("* ")):
                    item_content = stripped_line[2:]
                    li_node = ParentNode("li", [])
                    children = text_to_children(item_content)
                    li_node.children = children
                    ul_node.children.append(li_node)
            parent_node.children.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            ol_node = ParentNode("ol", [])
            lines = block.split("\n")     
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and re.match(r"^\d+\.\s", stripped_line):
                    dot_pos = stripped_line.find(".")
                    if dot_pos != -1 and dot_pos + 1 < len(stripped_line) and stripped_line[dot_pos + 1] == " ":
                        item_content = stripped_line[dot_pos + 2:]
                        li_node = ParentNode("li", [])
                        children = text_to_children(item_content)
                        li_node.children = children
                        ol_node.children.append(li_node)
            parent_node.children.append(ol_node)
    return parent_node




def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_blocks(markdown):
    markdown_list = markdown.split("\n\n")
    new_list = []
    for i in range(len(markdown_list)):
        markdown_list[i] = markdown_list[i].strip()
        if markdown_list[i] == "":
            pass
        else:
            new_list.append(markdown_list[i])
    return new_list

def block_to_block_type(block):
    block_lines = block.split("\n")
    if (
        block[:2] == "# " or
        block[:3] == "## " or
        block[:4] == "### " or
        block[:5] == "#### " or
        block[:6] == "##### " or
        block[:7] == "###### "
    ):
        return BlockType.HEADING
    elif block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    elif is_quote(block_lines):
        return BlockType.QUOTE
    elif is_unordered_list(block_lines):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block_lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

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

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    italics_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italics_nodes, "`", TextType.CODE)
    return split_nodes_link(split_nodes_image(code_nodes))


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

def is_quote(list):
    for each in list:
        if each[:1] != ">":
            return False
    return True

def is_unordered_list(list):
    for each in list:
        if each[:2] != "- ":
            return False
    return True

def is_ordered_list(list):
    for i in range(0, len(list)):
        if list[i][:3] != f"{i + 1}. ":
            return False
    return True


