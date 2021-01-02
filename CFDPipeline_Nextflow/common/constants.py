#!/bin/usr/env python3

import yaml
import os


def read_config(fname, fallback="../params_fallback.yml"):

    if os.path.exists(fname):
        source = fname
    else:
        source = fallback

    with open(source, 'r') as stream:
        content = yaml.load(stream,                                                                                                                                                       
                      Loader = yaml.FullLoader)
        return content
