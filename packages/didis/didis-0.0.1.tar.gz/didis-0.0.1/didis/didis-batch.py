#!/usr/bin/python3

# DIDIS - Desy ITk Database Interaction Script -- DESY's very own framework for interacting with the ITk Production Database
# Based on itkdb: https://gitlab.cern.ch/atlas-itk/sw/db/itkdb
# Created: 2021/11/17, Updated: 2021/11/19
# Written by Maximilian Felix Caspar, DESY HH


from loguru import logger
import argh
import os
import json
import itkdb
import mimetypes


def excel(excelFile):
    pass


def main():
    parser = argh.ArghParser()
    parser.add_commands([batch])
    parser.dispatch()


if __name__ == '__main__':
    main()
