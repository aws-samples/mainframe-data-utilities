import argparse
import json
import os

class CommandLine:

    def __init__(self, _arg=[]):

        parser = {}

        with open(os.path.dirname(os.path.realpath(__file__)) + '//config.json', 'r') as configfile:
            config = json.load(configfile)

        main_arg = argparse.ArgumentParser()

        main_function = main_arg.add_subparsers(title="Function", dest="function", required=True)

        for func in config:

            parser[func] = main_function.add_parser(func, help=config[func]['help'])

            for arg in config[func]['argument']:

                parser[func].add_argument(
                    arg,
                    default=config[func]['argument'][arg]['default'],
                    help=config[func]['argument'][arg]['help'],
                    type=type(config[func]['argument'][arg]['default'])
                    )

        if _arg == []:
            self.args = main_arg.parse_args()
        else:
            self.args = main_arg.parse_args(_arg)

        if self.args.verbose:
            self.verbose = True
            print('CLI arguments', vars(self.args))
        else:
            self.verbose = False