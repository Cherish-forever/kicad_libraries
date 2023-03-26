# SPDX-License-Identifier: Apache-2.0

import os
from west.commands import WestCommand
from west import log

class Symbol(WestCommand):

    def __init__(self):
        super().__init__(
            'symbol',               # gets stored as self.name
            'generate kicad symbol table',  # self.help
            # self.description:
            ''' Scan and generate a kicad symbol libraries table file''')

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('-o', '--output', required=True, help='an optional argument')

        return parser           # gets stored as self.parser

    def do_run(self, args, unknown_args):
        libs = []
        for project in self.manifest.projects:
            for dirname, dirnames, filenames in os.walk(project.abspath):
                if '.git' in dirnames:
                    dirnames.remove('.git')
                for filename in filenames:
                    if os.path.splitext(filename)[-1] == '.kicad_sym':
                        file_path = os.path.join(dirname, filename).replace('\\', '/')
                        name = os.path.relpath(file_path, self.topdir).replace('.kicad_sym', '')
                        lib = '  (lib (name "{}")(type KiCad) (uri "{}") (options "") (descr ""))\n'.format(name, file_path)
                        libs.append(lib)

        with open(args.output, "w+") as f:
            f.write('(sym_lib_table')
            for lib in libs:
                f.write(lib)
            f.write(')')
            f.close()
