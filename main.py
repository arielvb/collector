#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# pylint: disable-msg=W0403
# W0403: relative import
"""Collector main script"""
import sys
import logging
import sip
sip.setapi('QVariant', 2)
from ui.application import CollectorApplication

# The logging format
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


def main():
    """ Starts the application"""

    logging.basicConfig(
        filename='collector.log',
        level=logging.DEBUG,
        format=FORMAT)

    app = CollectorApplication(sys.argv)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
