#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import dirname, abspath
import os

REGRESSION_TESTING_VERSION_NUMBER = "0.1-B7"

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

GENERATED_IMAGES_DIR = os.path.join(BASE_DIR, 'generated_imgs')

SCREENSHOTS_DIR = os.path.join(GENERATED_IMAGES_DIR, 'screenshots')
COMPARISON_RESULTS_DIR = os.path.join(GENERATED_IMAGES_DIR, 'comparison_results')

CONFIG_DIR = os.path.join(BASE_DIR, 'configs')

WEBSITE_CONFIG_DIR = os.path.join(CONFIG_DIR, 'websites')

CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

SCREEN_SIZE_CONFIGS = [
    {'name': 'desktop', 'width': 1920, 'height': 1080},
    {'name': 'tablet', 'width': 1024, 'height': 1366},  # iPad Pro
    {'name': 'mobile', 'width': 375, 'height': 812}  # iPhone X
]