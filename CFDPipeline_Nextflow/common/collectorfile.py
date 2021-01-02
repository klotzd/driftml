#!/bin/python3

import csv
import os
import sys
import numpy as np


def file_length(filename):
    """
    get the number of lines in file
    """
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def delete_multiple_lines(filename, line_numbers):
    """
    delete all lines in line_numbers of file
        no direct way to do this, creates and selectively copies non-deleted lines to dummyfile, 
        then deletes original file and saves dummy as original
    """
    is_skipped = False
    counter = 0
    # Create name of dummy / temporary file
    dummy_file = filename + '.bak'
    # Open original file in read only mode and dummy file in write mode
    with open(filename, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        for line in read_obj:
            if counter not in line_numbers:
                write_obj.write(line)
            else:
                is_skipped = True
            counter += 1
    if is_skipped:
        os.remove(filename)
        os.rename(dummy_file, filename)
    else:
        os.remove(dummy_file)

    
def cellname(xi, zi, f):
    """
    genereates and writes name of cell to file
    nameformat is XZ where X and Z are counters of cell position
    """
    name = 'A' + '-' + str(xi) + '-' + str(zi)
    f.write( (name + '\n') )
    return name

def type_declaration(f):
    """
    writes all initial ParticleCollector type declarations to file
    """
    f.write( ('{' + '\n' ) )
    f.write( ('type    particleCollector;' + '\n') )
    f.write( ('mode    polygon;' + '\n') )
    f.write( ('polygons' + '\n') ) 
    f.write( ('(' + '\n') )
    f.write( ('(' + '\n') )
    
def log_declaration(f):
    """
    writes all closing ParticleCollector log file declarations to file
    """
    f.write( (')' + '\n') )
    f.write( (');' + '\n') )
    f.write( ('normal    (0 1 0);' + '\n') )
    f.write( ('negateParcelsOppositeNormal    no;' + '\n') )
    f.write( ('removeCollected    no;' + '\n') )
    f.write( ('surfaceFormat    vtk;' + '\n') )
    f.write( ('resetOnWrite    no;' + '\n') )
    f.write( ('log    yes;' + '\n') )
    f.write( ('}' + '\n') )
    f.write( ('\n'))

def write_points(p_1, p_2, p_3, p_4, y_level, f):
    """
    writes the actual current polygon corner coordinates to file
    """
    
    point_1 = '(' + str(p_1[0]) + ' ' + str(y_level) + ' ' + str(p_1[1]) + ')' + '\n'
    point_2 = '(' + str(p_2[0]) + ' ' + str(y_level) + ' ' + str(p_2[1]) + ')' + '\n'
    point_3 = '(' + str(p_3[0]) + ' ' + str(y_level) + ' ' + str(p_3[1]) + ')' + '\n'
    point_4 = '(' + str(p_4[0]) + ' ' + str(y_level) + ' ' + str(p_4[1]) + ')' + '\n'
    
    f.write(point_1)
    f.write(point_2)
    f.write(point_3)
    f.write(point_4)