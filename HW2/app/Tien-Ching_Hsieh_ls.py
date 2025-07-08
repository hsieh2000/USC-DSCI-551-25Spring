import sys
from lxml import etree
import time

def ls_hdfs(xml_file, path):
    """
    Simulate the 'ls' command for an HDFS-like XML structure.

    :param xml_file: Path to the XML file.
    :param path: Directory path to list.
    :return: Formatted string with file or directory information.
    :rtype: str
    :raises FileNotFoundError: If the path does not exist.
    """

    try:
        with open(xml_file, "r"):
            pass
    except:
        raise FileNotFoundError

    # Parse the XML file
    tree = etree.parse(xml_file)

    # Handle trailing slash
    while path.endswith("/") and path!="/":
        path = path[:-1]
    path = '/' + '/'.join(filter(None, path.split('/')))

    # Check path existence
    path_text_lst = tree.xpath(f"/FileSystemMetadata/File[Path/text()='{path}']/Path/text()")
    if not path_text_lst:
        return "No such file or directory"

    # Handle files and directories
    _str = ""
    if "." in path.split("/")[-1]:
        text = tree.xpath(f"/FileSystemMetadata/File[Path/text() = '{path}']/*/text()")
        root = tree.xpath(f"/FileSystemMetadata/File[Path/text() = '{path}']/*")
        lst = [etree.tostring(i, pretty_print=True).decode() for i in root]
        element_tag = [i.split(">")[0].split("<")[-1] for i in lst]
        _dict = {x: y for x, y in zip(element_tag, text)}
        ls_dict_lst = [_dict]

    else:
        ls_dict_lst = []
        len_path = len(path.split("/"))
        sub_path_text_lst = tree.xpath(f"/FileSystemMetadata/File[starts-with(Path/text(), '{path}')]/Path/text()")
        immediate_children_lst = [i for i in sub_path_text_lst if len(i.split("/")) == len_path+1]
        
        if len(immediate_children_lst) > 0:
            for p in immediate_children_lst:
                text = tree.xpath(f"/FileSystemMetadata/File[Path/text() = '{p}']/*/text()")
                root = tree.xpath(f"/FileSystemMetadata/File[Path/text() = '{p}']/*")
                lst = [etree.tostring(i, pretty_print=True).decode() for i in root]
                element_tag = [i.split(">")[0].split("<")[-1] for i in lst]
                _dict = {x: y for x, y in zip(element_tag, text)}

                if "." not in path.split("/")[-1]:
                    _dict.update({"Replication": "-" })
                    _dict.update({"FileSize": "0", })

                ls_dict_lst.append(_dict)
        else:
            return _str

    for x in ls_dict_lst:
        _str += f'{x.get("Permission")} {x.get("Replication")} {x.get("UserName")} {x.get("GroupName")} {x.get("FileSize")} {x.get("ModificationTime")} {x.get("Path")}\n'
        
    return _str
    
def format_output(file_elem):
    """
    Format the file element information for display.

    :param file_elem: XML element containing file information.
    :return: Formatted string representing the file information.
    :rtype: str
    """

    # Extract and format file details

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python firstname_lastname_ls.py <xml_file> <path>")
        sys.exit(1)

    xml_file = sys.argv[1]
    path = sys.argv[2]

    result = ls_hdfs(xml_file, path)
    print(result)
