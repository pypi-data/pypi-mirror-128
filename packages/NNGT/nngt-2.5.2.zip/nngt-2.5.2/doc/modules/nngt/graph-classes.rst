Graph classes
=============

NNGT provides four main graph classes that provide specific features to work
as conveniently as possible with different object types: topological versus
space-embedded graphs or neuronal networks.

.. autosummary::

    nngt.Graph
    nngt.SpatialGraph
    nngt.Network
    nngt.SpatialNetwork


A summary of the methods provided by these classes as well as more detailed
descriptions are provided below.
Unless specified, child classes can use all methods from the parent class
(the only exception is :meth:`~nngt.Graph.set_types` which is not available
to the :class:`~nngt.Network` subclasses).

.. contents::
   :local:


Summary of the class members and methods
----------------------------------------

Graph
+++++

The main class for topological graphs.

.. autosummary::

    nngt.Graph

    nngt.Graph.adjacency_matrix
    nngt.Graph.clear_all_edges
    nngt.Graph.copy
    nngt.Graph.delete_edges
    nngt.Graph.delete_nodes
    nngt.Graph.edge_attributes
    nngt.Graph.edge_id
    nngt.Graph.edge_nb
    nngt.Graph.edges_array
    nngt.Graph.from_file
    nngt.Graph.from_library
    nngt.Graph.from_matrix
    nngt.Graph.get_attribute_type
    nngt.Graph.get_betweenness
    nngt.Graph.get_degrees
    nngt.Graph.get_delays
    nngt.Graph.get_density
    nngt.Graph.get_edge_attributes
    nngt.Graph.get_edge_types
    nngt.Graph.get_edges
    nngt.Graph.get_node_attributes
    nngt.Graph.get_nodes
    nngt.Graph.get_structure_graph
    nngt.Graph.get_weights
    nngt.Graph.graph
    nngt.Graph.graph_id
    nngt.Graph.has_edge
    nngt.Graph.is_connected
    nngt.Graph.is_directed
    nngt.Graph.is_network
    nngt.Graph.is_spatial
    nngt.Graph.is_weighted
    nngt.Graph.make_network
    nngt.Graph.make_spatial
    nngt.Graph.name
    nngt.Graph.neighbours
    nngt.Graph.new_edge
    nngt.Graph.new_edge_attribute
    nngt.Graph.new_edges
    nngt.Graph.new_node
    nngt.Graph.new_node_attribute
    nngt.Graph.node_attributes
    nngt.Graph.node_nb
    nngt.Graph.num_graphs
    nngt.Graph.set_delays
    nngt.Graph.set_edge_attribute
    nngt.Graph.set_name
    nngt.Graph.set_node_attribute
    nngt.Graph.set_types
    nngt.Graph.set_weights
    nngt.Graph.structure
    nngt.Graph.to_file
    nngt.Graph.to_undirected
    nngt.Graph.type



SpatialGraph
++++++++++++

Subclass of :class:`~nngt.Graph` providing additional tools to work with
spatial graphs. It works together with the :class:`~nngt.geometry.Shape` object
from the :mod:`~nngt.geometry` module.

.. autosummary::

    nngt.SpatialGraph
    nngt.SpatialGraph.get_positions
    nngt.SpatialGraph.set_positions
    nngt.SpatialGraph.shape



Network
+++++++

Subclass of :class:`~nngt.Graph` providing additional tools to work with
neuronal networks. It works together with the
:class:`~nngt.NeuralPop` object.

.. autosummary::

    nngt.Network
    nngt.Network.exc_and_inhib
    nngt.Network.from_gids
    nngt.Network.get_neuron_type
    nngt.Network.id_from_nest_gid
    nngt.Network.nest_gids
    nngt.Network.neuron_properties
    nngt.Network.num_networks
    nngt.Network.population
    nngt.Network.to_nest
    nngt.Network.uniform



SpatialNetwork
++++++++++++++

Subclass of :class:`~nngt.Graph` providing additional tools to work with
spatial neuronal networks. It works together with both
:class:`~nngt.NeuralPop` and the
:class:`~nngt.geometry.Shape` object from the :mod:`~nngt.geometry` module.

.. autosummary::

    nngt.SpatialNetwork
    nngt.SpatialNetwork.exc_and_inhib
    nngt.SpatialNetwork.from_gids
    nngt.SpatialNetwork.get_neuron_type
    nngt.SpatialNetwork.get_positions
    nngt.SpatialNetwork.id_from_nest_gid
    nngt.SpatialNetwork.nest_gids
    nngt.SpatialNetwork.neuron_properties
    nngt.SpatialNetwork.num_networks
    nngt.SpatialNetwork.population
    nngt.SpatialNetwork.set_positions
    nngt.SpatialNetwork.shape
    nngt.SpatialNetwork.to_nest
    nngt.SpatialNetwork.uniform



Details
-------

.. currentmodule:: nngt
.. autoclass:: Graph
   :inherited-members:
   :no-undoc-members:

.. currentmodule:: nngt
.. autoclass:: SpatialGraph
   :members:
   :no-undoc-members:

.. currentmodule:: nngt
.. autoclass:: Network
   :members:
   :no-undoc-members:

.. currentmodule:: nngt
.. autoclass:: SpatialNetwork
   :members:
   :no-undoc-members:
