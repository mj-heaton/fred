Getting Started
===============

Fred is a python framework designed to help build Monte-Carlo type financial simulations for small or medium sized businesses.

Fred requires python-3.7+

Building From Source
--------------------

It's good practice to build python packages from a clean virtual environment:

    python3 -m venv venv
    source venv/bin/activate
    
    cd fred

Once the virtual environment has been activated you can install the required python packages:

	pip install -r requirements.txt

Then it should be straight-forward to run the source (tarball) and binary (wheel) distribution builds:

    python setup.py sdist bdist_wheel

The output files should appear in the 'dist' directory. 

To install the module so that it is editable run (essential for development):

    pip install -e .
