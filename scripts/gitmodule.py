# SPDX-License-Identifier: Apache-2.0

import os
import sys
import configparser
from west.commands import WestCommand
from west import log
from urllib.parse import urlparse

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class GitModule(WestCommand):

    def __init__(self):
        super().__init__(
            'gitmodule',               # gets stored as self.name
            'read gitmodule generate submanifests',  # self.help
            # self.description:
            ''' read a git repository submodule to generate submanifests''')
        self.raw_urls = []
        self.urls = []
        self.group = {}

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('-i', '--input', required=True, help='.gitmodules file')
        parser.add_argument('-o', '--output', required=True, help='output directory')

        return parser           # gets stored as self.parser

    def url_cleaning(self):
        for url in self.raw_urls:
            p = urlparse(url.rstrip('/').rstrip('.git'))
            if len(p.path.split('/')) != 3:
                print("Please handle separately: {}".format(url))
                continue
            else:
                self.urls.append(url)

    def get_urls(self, filepath):
        config = configparser.ConfigParser()
        config.read(filepath)
        for cfg in config.sections():
            self.raw_urls.append(config[cfg]['url'])

    def url_group(self):
        for url in self.urls:
            p = urlparse(url)
            user = p.path.split('/')[1]
            self.group.setdefault(user, []).append(url)
            
    def process_item(self, output):
        for key, value in self.group.items():
            contex = {}
            contex['manifest'] = {}
            contex['manifest']['projects'] = []
            contex['manifest']['remotes'] = []
            for url in value:
                obj = {}
                remote = {}
                p = urlparse(url)
                remote['name'] = p.netloc.split('.')[0]
                remote['url-base'] = url.replace(p.path.split('/')[2], "").rstrip("/")
                if remote not in contex['manifest']['remotes']:
                    contex['manifest']['remotes'].append(remote)
                obj['remote'] = p.netloc.split('.')[0]
                obj['name'] = key + '-' + p.path.split('/')[2].rstrip(".git")
                obj['repo-path'] = p.path.split('/')[2].rstrip(".git")
                obj['revision'] = 'master'
                obj['path'] = p.path.lstrip('/').rstrip("/").rstrip(".git").rstrip(".pretty")
                if obj not in contex['manifest']['projects']:
                    contex['manifest']['projects'].append(obj)
            with open(os.path.join(output, key + '.yml'), 'w+') as f:
                f.write(dump(contex))
                f.close()

    def do_run(self, args, unknown_args):
        self.get_urls(args.input)
        self.url_cleaning()
        self.url_group()
        self.process_item(args.output)
