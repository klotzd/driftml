#!/bin/python3

import csv
import os
import sys
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""

purpose:

    creates a CollectorFaces file for the ParticleCollector Class with given mesh coarseness on an x-z plane

definitions:

- coordinate system:
    for points the coord system is (x, y, z)
    with the domain extension being:
    [0, 4] x [0, 1.5] x [0, 2]
    
"""


######################################################################################################################
####   INITIAL DECLARATIONS
######################################################################################################################


filename = "CollectorFaces.txt"        # file header still needs adaptation
mode = 'r+' 
lines_header = 16                      # number of lines taken up by header

target_width = 2                       # z-axis extension of target, centered on center line 
target_length = 6

grid_x = 30                             # number of sections of target grid
grid_z = 10

theta = 0

y_level = 0.1   


######################################################################################################################
####   FUNCTION DEFINITIONS
######################################################################################################################


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
        
def sanity_check(L, W, angle):
    """
    check if the specified target fits within the domain at this rotational angle
    """
    fits = True
    
    if ((W/2 + L) * np.cos(np.radians(angle))  > 0):
        fits = False
        
    return fits
    
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

def write_points(x_1, x_2, z_1, z_2, y_level, f):
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

######################################################################################################################
####   CLEAN THE FILE AND DELETE ALL NON-HEADER ENTRIES
######################################################################################################################


length = file_length(filename)
delete_multiple_lines(filename, list(range(lines_header, length)))


######################################################################################################################
####   CALCULATE STEPSIZES AND DECLARE INITIAL GRID POSITION
######################################################################################################################


#   fits = sanity_check(target_length, target_width, theta)

fits = True

if fits:
    print('length/width/angle ratio makes sense, proceeding')
else:
    sys.exit('a box of this L/W doesnt fit into the domain at this angle, try a different config')
    
theta = np.radians(theta)
c, s = np.cos(theta), np.sin(theta)
Rot = np.array(((c, -s), (s, c)))               # get rotation matrix rot(theta)

x_step = np.array((target_length / grid_x, 0))  # get initial starting point + steps
z_step = np.array((0, target_width / grid_z))
OS = np.array((target_length, -target_width)) * 0.5

x_step = np.matmul(x_step, Rot)                # rotate
z_step = np.matmul(z_step, Rot)
OS     = np.matmul(OS, Rot)


OS += np.array((-target_length, target_width)) * 0.5 # shifting origin to upper corner of target


list_of_cells = []

######################################################################################################################
####   WRITE THE INDIVIDUAL COLLECTOR ENTRIES
######################################################################################################################


with open(filename, mode) as f:
    
    for _ in range(lines_header):
        next(f)
        
    f.write('\n')
    OS_bckup = OS
    
    for zi in range(grid_z):   

        if zi != 0:
            OS = OS_bckup + z_step * zi
            
        for xi in range(grid_x):
            
            name = cellname(xi, zi, f)         # write the name
            list_of_cells.append(name)         # and store in list of cells
            
            type_declaration(f)         # write the type declaration
            
            p_1 = OS
            p_2 = p_1 + z_step          # update x lower corner position:
            p_3 = p_2 + x_step
            p_4 = p_3 - z_step
            
            write_points(p_1, p_2, p_3, p_4, y_level, f)   # write the corner points    
            log_declaration(f)          # write the log file declaration
            
            OS = p_4

# output the list of cells as csv
csvWriter = csv.writer(open('list_of_cells.csv', 'w'), delimiter=';')
csvWriter.writerow(list_of_cells);  
