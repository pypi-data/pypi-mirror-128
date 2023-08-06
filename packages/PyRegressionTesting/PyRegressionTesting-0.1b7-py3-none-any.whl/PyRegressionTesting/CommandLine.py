#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from PyRegressionTesting import PyRegressionTesting
from PyRegressionTesting.Utils.Config import Config
from PyRegressionTesting.Utils.Logger import Logger


def main():
    # parse args
    parser = argparse.ArgumentParser(description='Test your website with ease!')
    parser.add_argument('--config', required=True, type=str, help='Path to the json-config-file')
    parser.add_argument('--threads', required=False, default=1, type=int, help='How many tests should run in parallel?')
    parser.add_argument('--logging', action='store_true', help='Enable logging?')
    parser.add_argument('--headless', action='store_false', help='Execute Tests headless?')

    args = parser.parse_args()

    Logger.LOGGING = args.logging

    config = Config.from_json_file(args.config_file)

    tester = PyRegressionTesting(config, args.driver, args.threads, args.logging, args.headless)
    tester.run_tests()

if __name__ == "__main__":
    main()