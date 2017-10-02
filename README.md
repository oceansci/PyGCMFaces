PyGCMFaces
==========

A port of the gcmfaces Matlab toolbox for MITgcm post-processing.

This work is derived from Gael Forget's 
[gcmfaces](https://github.com/gaelforget/gcmfaces); the user manual there
explains the toolbox in some detail. In short, this library aims to provide
a GCMFaces class that represents earth variables in a face-oriented approach
as commonly used in global circulation models; this class should implement
arithmetic operators, averaging, etc. so that it can be manipulated just like
a NumPy array for analysis. Additionally, the library should provide plotting
facilities to visualize the results of analysis in a variety of projections
on the globe. To support these goals, we will need a Grid class to store the
representation of the computational grid, as well.

Goals
=====

PyGCMFaces should, eventually, reproduce the full functionality of the
original gcmfaces. It should use out-of-core data structures wherever 
possible, but abstract over this implementation detail, so that analysis of
data sets too large for memory is as seamless as in Matlab. Code documentation
and readability should be a first priority to enable easy future modification
of the library. The use of global variables to store state should be avoided
and that information should instead be encapsulated in local objects (what if
I want to work with more than one grid at once?). Code should be compatible
with both Python 2 and Python 3; we want to be future-ready, but some systems
we work on may not have a Python 3 distribution new enough to support all
dependencies (ICES desktops do not have a Python 3 new enough to support 
NumPy).

License
=======

PyGCMFaces is licensed under the terms of the MIT license; see LICENSE.txt for
the full statement. Copyright (c) 2017 Sean McBane and contributors.

