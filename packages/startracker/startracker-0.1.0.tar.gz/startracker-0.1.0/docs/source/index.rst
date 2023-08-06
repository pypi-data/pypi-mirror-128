.. startracker documentation master file, created by
   sphinx-quickstart on Thu Nov 25 09:23:16 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to StarTracker documentation!
=======================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   startracker
   contributing
   developers

Quick start guide
=================
Prerequisites:
    Please see `development setup <developers.html#a-name-setup-development-setup>`_

Clone the code from the repository::

    git clone https://gitlab.cern.ch/cta-unige/startracker.git && cd startracker

Install the code::

    flit install --user

In order to produce variance images and reconstructed star tables, 
prepare the configuration file (you can use the files under examples/ as a reference) and launch::

     image_producer --config /path/to/image_producer_configuration.json

In order to run the fitter and extract the pointing offset
prepare the configuration file (you can use the files under examples/ as a reference) and launch::

     star_fitter --config /path/to/star_fitter_configuration.json

Enjoy!


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
