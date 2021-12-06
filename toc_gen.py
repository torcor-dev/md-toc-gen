from parser import Parser 
from os import path

class TocGenerator:
    def __init__(self, dir):
        self.dir = dir
        self.parser = Parser(dir)
        self.toc = self.parser.parse()

    def generate_toc(self):
        for file in self.toc.keys():
            self.write_sub_toc(file)
        self.write_main_toc()

    def write_main_toc(self):
        with open('toc.md', 'w') as f:
            f.write('# Table of Contents\n')
            for i, (file, toplevel) in enumerate(self.toc.items()):
                for key in toplevel.keys():
                    f.write('{}. [{}]({})\n'.format(i+1, key, path.join(self.dir, file)))

    def write_sub_toc(self, filename):
        filepath = path.join(self.dir, filename)
        with open(filepath, 'r') as f:
            copy = Parser.delete_toc_block(f.readlines())

        with open(filepath, 'w') as f:
            f.write(Parser.TOC_BLOCK_START + '\n')
            f.write('# Table of Contents\n')
            self.write_toc_lines(f, filename)
            f.write(Parser.TOC_BLOCK_END + '\n')
            f.write("".join(copy))

    def write_toc_lines(self, f, filename):
        for i, (file, toplevel) in enumerate(self.toc.items()):
            for h1 in toplevel.keys():
                f.write('{}. [{}]({})\n'.format(i+1, h1, file))
                if (file == filename):
                    self.write_toc_sub_lines(f, toplevel[h1])

    def write_toc_sub_lines(self, f, sublevels):
        for i, (h2, h3s) in enumerate(sublevels.items()):
            f.write('\t{}. [{}](#{})\n'.format(i+1, h2, self.link_formatter(h2)))
            for j, h3 in enumerate(h3s):
                f.write('\t\t{}. [{}](#{})\n'.format(j+1, h3, self.link_formatter(h3)))


    def link_formatter(self, line):
        line = line.replace(".", "")
        return line.replace(" ", "-").lower()

if __name__ == '__main__':
    toc_gen = TocGenerator("testdocs/")
    toc_gen.generate_toc()
