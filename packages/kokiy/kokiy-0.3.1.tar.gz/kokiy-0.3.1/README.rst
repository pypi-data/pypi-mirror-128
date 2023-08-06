``kokiy`` contains utilities to work on 2D and 3D structured grids. Grids can be, among others, cartesian planes (``CartShell``) or axi-cylindrical extrusions from x-r splines (``AxiShell``). ``ThickShell`` are 3D shells built by extruding any of the available 2d objects. Check out the API reference for an extensive list of all available geometries.


Main features include:

* create 2D and 3D structured grids (including axi-cylindrical objects)
* interpolate a solution
* operate (e.g. average) a solution over a direction
* dump shells for fields visualization in `ParaView <https://www.paraview.org/>`_
* export mesh in any format available in `yamio <https://pypi.org/project/yamio/>`_ (e.g. ``hip``-friendly ``.hdf5``, ``xdfm``, ``dolfin-xml``)
* export ``.geo`` files for visualization with `tiny-3d-engine <https://pypi.org/project/tiny-3d-engine/>`_



Installation
------------

Install with


.. code-block:: bash

    pip install kokiy
