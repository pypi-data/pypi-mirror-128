Side classes
============

The following side classes are used to structure graphs into groups that
can then be used to generate specific connectivity patterns via the
:func:`~nngt.generation.connect_groups` function or to assign specific
properties to neuronal assemblies to use them in simulations with NEST_.

.. autosummary::

    nngt.Group
    nngt.MetaGroup
    nngt.MetaNeuralGroup
    nngt.NeuralGroup
    nngt.NeuralPop
    nngt.Structure



Summary of the classes
----------------------

A summary of the methods provided by these classes as well as more detailed
descriptions are provided below.
Unless specified, child classes can use all methods from the parent class
(:class:`~nngt.MetaGroup`, :class:`~nngt.NeuralGroup`, and
:class:`~nngt.MetaNeuralGroup` inherit from :class:`~nngt.Group` while
:class:`~nngt.NeuralPop` inherits from :class:`~nngt.Structure`).

.. contents::
   :local:


Group
+++++

.. autosummary::

    nngt.Group
    nngt.Group.add_nodes
    nngt.Group.copy
    nngt.Group.ids
    nngt.Group.is_metagroup
    nngt.Group.is_valid
    nngt.Group.name
    nngt.Group.parent
    nngt.Group.properties
    nngt.Group.size



NeuralGroup
+++++++++++

.. autosummary::

    nngt.NeuralGroup
    nngt.NeuralGroup.has_model
    nngt.NeuralGroup.nest_gids
    nngt.NeuralGroup.neuron_model
    nngt.NeuralGroup.neuron_param
    nngt.NeuralGroup.neuron_type



Structure
+++++++++

.. autosummary::

    nngt.Structure
    nngt.Structure.add_meta_group
    nngt.Structure.add_to_group
    nngt.Structure.copy
    nngt.Structure.create_group
    nngt.Structure.create_meta_group
    nngt.Structure.from_groups
    nngt.Structure.get_group
    nngt.Structure.get_properties
    nngt.Structure.ids
    nngt.Structure.is_valid
    nngt.Structure.meta_groups
    nngt.Structure.parent
    nngt.Structure.set_properties
    nngt.Structure.size



NeuralPop
+++++++++

.. autosummary::

    nngt.NeuralPop
    nngt.NeuralPop.exc_and_inhib
    nngt.NeuralPop.excitatory
    nngt.NeuralPop.from_network
    nngt.NeuralPop.get_param
    nngt.NeuralPop.has_models
    nngt.NeuralPop.inhibitory
    nngt.NeuralPop.nest_gids
    nngt.NeuralPop.set_model
    nngt.NeuralPop.set_neuron_param
    nngt.NeuralPop.syn_spec
    nngt.NeuralPop.uniform



Details
-------

.. currentmodule:: nngt

.. autoclass:: Group
    :members:

.. autoclass:: MetaGroup
    :members:

.. autoclass:: MetaNeuralGroup
    :members:

.. autoclass:: NeuralGroup
    :members:

.. autoclass:: NeuralPop
    :members:

.. autoclass:: Structure
    :members:


.. _NEST: nest-simulator.readthedocs.io/
