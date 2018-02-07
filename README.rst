==============
 dji-log-data
==============

dji-log-data is a Python package that _just_ contains information about the data format of DJI Flight Record
log data and support for generating code based on that data.

The goals of this project are to:

1. accumulate public knowledge of the data format
2. allow other packages to easily update their code when new information is discovered or a new format is released

-------
 Usage
-------
1. Setup a virtualenv with your preferred python

.. code:: bash

   virtualenv venv

2. Activate it

.. code:: bash

   . venv/bin/activate

3. Install the package and dependencies

.. code:: bash

   pip install .

4. Generate the code

.. code:: bash

   generate_code --language python --frames-out /tmp/frames.py --keys-out /tmp/keys.py

--------------
 Contributing
--------------

Code contributions are welcomed in the form of pull requests.  Pull requests should come with a **detailed** description
of how the new data was found and an example flight log.

--------------
 Future Plans
--------------
* Add tests
* Support extracting images from DJI txt files
* Support different versions of the txt file format.  The data file format is already structured to support this
  (In the object at ``frame_types[].field_definitions[]``, imagine ``start_version`` and ``end_version`` fields.)

---------
 Credits
---------
Almost all of the information about the log format came from two projects:

* Ian Davies' `phantom-decoder <https://github.com/daviesian/phantom-decoder>`_
* Mikeemoo's `dji-log-parser <https://github.com/mikeemoo/dji-log-parser>`_