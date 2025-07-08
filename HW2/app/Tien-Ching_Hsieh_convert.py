import pandas as pd
from lxml import etree
import sys

def convert(fsimage_csv, output_xml):
    """
    Convert a CSV file to an XML file.

    :param fsimage_csv: Path to the input CSV file.
    :param output_xml: Path to the output XML file.
    :return: None
    :raises FileNotFoundError: If the CSV file is not found.
    """
    try:
        with open(fsimage_csv, "r"):
            pass
    except:
        raise FileNotFoundError
        # return "No such file or directory"
        
    #Convert a CSV to XML by reading data
    df = pd.read_csv(f"{fsimage_csv}")

    #Create elements from rows
    #Save with pretty printing
    with open(f"{output_xml}", "w") as f:
        f.write("<FileSystemMetadata>\n")
        for i in range(0, len(df)):
            f.write("\t<File>\n")
            for j in list(df.columns):
                if j in ["PreferredBlockSize", "BlocksCount", "FileSize"]:
                    if "." in df.loc[i]["Path"].split("/")[-1]:
                        f.write(f"\t\t<{j}>{df.loc[i][j]}</{j}>\n")
                elif j in ["NSQUOTA", "DSQUOTA"]:
                    pass
                else:
                    f.write(f"\t\t<{j}>{df.loc[i][j]}</{j}>\n")
            f.write("\t</File>\n")
        f.write("</FileSystemMetadata>\n")
    return None

if __name__=="__main__":
    # Input and output file paths

    if len(sys.argv) != 3:
        print("Usage: python firstname_lastname_convert.py <csv_path> <xml_file>")
        sys.exit(1)

    fsimage_csv = sys.argv[1]
    output_xml = sys.argv[2]

    convert(fsimage_csv, output_xml)