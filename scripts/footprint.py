# SPDX-License-Identifier: Apache-2.0

import os
from west.commands import WestCommand
from west import log

class Footprint(WestCommand):

    def __init__(self):
        super().__init__(
            'footprint',               # gets stored as self.name
            'generate kicad footprint table',  # self.help
            # self.description:
            ''' Scan and generate a kicad footprint libraries table file''')

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('-k', '--keep', required=False, default=False, type=bool,
                            help='Keep kicad-official footprints as default search path')
        parser.add_argument('-o', '--output', required=True, help='an optional argument')

        return parser           # gets stored as self.parser

    def do_run(self, args, unknown_args):
        libs = []
        for project in self.manifest.projects:
            for dirname, dirnames, filenames in os.walk(project.abspath):
                if '.git' in dirnames:
                    dirnames.remove('.git')
                for filename in filenames:
                    if os.path.splitext(filename)[-1] == '.kicad_mod':
                        if os.path.join(self.topdir, 'kicad', 'footprints') in dirname and args.keep:
                            name = os.path.relpath(dirname, self.topdir).replace('\\', '/').replace("kicad/footprints/", '').replace('.pretty', '')
                        else:
                            name = os.path.relpath(dirname, self.topdir).replace('\\', '/').replace('.pretty', '')
                        uri = os.path.abspath(dirname).replace('\\', '/')
                        lib = '  (lib (name "{}")(type KiCad) (uri "{}") (options "") (descr ""))\n'.format(name, uri)
                        libs.append(lib)
                        break
        with open(args.output, "w+") as f:
            f.write('(fp_lib_table')
            for lib in libs:
                f.write(lib)
            f.write(')')
            f.close()
