import os
import re

class Parser:
    TOC_BLOCK_START = '<!-- TOC -->'
    TOC_BLOCK_END = '<!-- /TOC -->'

    def __init__(self, dir):
        self.dir = dir
        self.files = {}

    def parse(self):
        for file in sorted(os.listdir(self.dir)):
            if file.endswith(".md"):
                self.files[file] = self.parse_file(file)
        return self.files

    def parse_file(self, file):
        with open(self.dir + file, "r") as f:
            lines = Parser.delete_toc_block(f.readlines())
            content = {}
            toplevel = ""
            sublevel = ""

            for line in lines:
                if re.match(r'^#\s\w', line.strip()):
                    toplevel = line.replace("#", "")
                    toplevel = toplevel.strip()
                    content[toplevel] = {}
                elif re.match(r'^##\s\w', line.strip()):
                    sublevel = line.replace("##", "")
                    sublevel = sublevel.strip()
                    content[toplevel][sublevel] = []
                elif re.match(r'^###\s\w', line.strip()):
                    content[toplevel][sublevel].append(line.replace("###", "").strip())

            return content

    def get_files(self):
        return self.files

    def get_dir(self):
        return self.dir

    def pretty_print(self):
        for file in self.files:
            print(file)
            for toplevel in self.files[file]:
                print("\t" + toplevel)
                for sublevel in self.files[file][toplevel]:
                    print("\t\t" + sublevel)
                    for line in self.files[file][toplevel][sublevel]:
                        print("\t\t\t" + line)

    @staticmethod
    def delete_toc_block(lines):
        delete = False
        copy = []
        for i, line in enumerate(lines):
            if line.startswith(Parser.TOC_BLOCK_START):
                delete = True

            if not delete:
                copy.append(line)

            if line.startswith(Parser.TOC_BLOCK_END):
                delete = False
        
        return copy


if __name__ == "__main__":
    parser = Parser("test/res/theory/")
    parser.parse()
