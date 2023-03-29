# SPDX-License-Identifier: Apache-2.0

import os
import json
from west.commands import WestCommand
from west import log

class Environment(WestCommand):

    def __init__(self):
        super().__init__(
            'env',               # gets stored as self.name
            'generate kicad enverioment',  # self.help
            # self.description:
            '''Generate kicad_common.json eviroment''')

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('-c', '--config', required=True, help='kicad_common.json file')
        parser.add_argument('-e', '--env', type=str, nargs='+', required=True, help='environment dictionary')

        return parser           # gets stored as self.parser

    def backup_config(self, filename):
        with open(filename, 'r') as f:
            backup = f.read()
            with open(filename + '.backup', 'w+') as b:
                b.write(backup)
                b.close()
            f.close()        
    
    def do_run(self, args, unknown_args):
        self.backup_config(args.config)
        with open(args.config, 'r+') as f:
            kicad_common = json.loads(f.read())
            if kicad_common.get('environment') is None: kicad_common['environment'] = {}
            if kicad_common['environment']['vars'] is None: kicad_common['environment']['vars'] = {}
            env = [ dict([[k, v]]) for k, v in (d.split(':') for d in args.env) ]
            for e in env: kicad_common['environment']['vars'].update(e)
            f.seek(0)
            f.write(json.dumps(kicad_common, sort_keys=True, indent=4,
                               separators=(',', ': '), ensure_ascii=False))
            f.close()
