# Copyright (c) 2017 Sean McBane and contributors under the terms of the 
# MIT license; see LICENSE.txt.

"""This module defines the GCMFaces class and all operations on it."""

from warnings import warn
import dask.array as da
import numpy as np

class GridType:
    """
    Substitute for an enum to represent the types of grid that may be
    represented by a GCMFaces object. Note that enum values are equal to the
    number of faces in the corresponding grid type. Grid types are:
     - 'll' => lat-lon
     - 'llpc' => quadripolar grid
     - 'llc' => lat-lon-cap
     - 'cube' => cubed sphere
    """
    ll = 1
    llpc = 4
    llc = 5
    cube = 6

class GCMFacesArgException(Exception):
    """Exception thrown if arguments to gcmfaces constructor are bad."""
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return repr(self.value)

class GCMFaces:
    """
    The GCMFaces object is a representation of a variable field divided into
    faces as is common when creating grids for global models; it supports the
    four types of grid specified above in the GridType class.

    The members of the GCMFaces object are:
        - a number of faces, `nfaces` - one of 1, 4, 5, 6
        - a grid type, `gridtype`, same as above (for readability, comparable
          to the members of `GridType` - e.g. `gridtype == GridType.llc` is 
          valid; `gridtype` should always equal `nfaces`.
        - a list of the face data - this is a simple Python list; its members
          are dask arrays. This class does not handle the chunking of dask
          arrays; it either accepts a list of them as arguments, or it 
          puts empty placeholders that will be replaced.
    """

    def __init__(self, *args):
        """
        A new GCMFaces object may be constructed with the following 
        combinations of arguments:

            (a) Only the number of faces; the list of faces in the object
                will have the appropriate length but individual faces will
                be empty.
            (b) Only the faces; number of faces will be inferred and the 
                object's list of faces is initialized from those passed.
            (c) Number of faces *and* a list of the faces - checks the number
                of faces against length of the list.
            (d) With no argument, equivalent to GCMFaces(1); sets 1 face by
                default.

        ***Note*** If you use one of the options where a list of faces is 
        passed, the list is not deep-copied and modifications made in the 
        returned object will be reflected outside. Since this can be manually
        corrected if needed, I think it's preferable to making copies of 
        dask arrays willy-nilly.
        """
        if len(args) == 2:
            if not isinstance(args[1], list):
                raise(GCMFacesArgException("Expected a list as second "
                                           "positional argument to gcmfaces "
                                           "constructor."))
            elif args[0] != len(args[1]):
                raise(GCMFacesArgException("Specified number of faces does "
                                           "not match the length of the given "
                                           "field list."))

            self.nfaces = args[0]
            self.faces  = args[1]
        elif len(args) == 1:
            if isinstance(args[0], list):
                self.faces  = args[0]
                self.nfaces = len(self.faces)
            else:
                self.nfaces = args[0]
                self.faces = []
        else:
            self.nfaces = 1
            self.faces = []
            warn("in GCMFaces constructor: nfaces set to 1 by default")

        if not self.nfaces in [1, 4, 5, 6]:
            raise(GCMFacesArgException("The specified number of faces does "
                                       "not correspond to a recognized grid "
                                       "type."))

        self.gridtype = self.nfaces
        if len(self.faces) == 0:
            self.faces = [da.from_array(np.array([]), 1000000, name=False) \
                          for i in range(0, self.nfaces)]

        if not isinstance(self.faces[0], da.Array):
            raise(GCMFacesArgException("Provided list of faces does not "
                                       "contain dask arrays as expected."))
