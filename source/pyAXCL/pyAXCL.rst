pyAXCL
============

.. toctree::
   :maxdepth: 1

   pyAXCL.rt
   pyAXCL.sys
   pyAXCL.pool
   pyAXCL.npu
   pyAXCL.vdec
   pyAXCL.venc
   pyAXCL.ivps
   pyAXCL.dmadim
   pyAXCL.ive
   pyAXCL.utils


Requirement
----------------
python >= 3.9 64bits (Linux)

Install
----------------
1. Extract the ``pyAXCL-X.YY.Z-py3-none-any.whl`` file from ``axcl/out/python/`` directory in ``axcl.tgz`` SDK.
2. install:  ``pip3 install pyAXCL-X.YY.Z-py3-none-any.whl``.

   .. code-block:: bash

      $ pip3 install pyAXCL-X.YY.Z-py3-none-any.whl
      $ pip3 show pyAXCL

3. Open the Python 3 console to verify that the installation was successful.

   .. code-block:: python

      Python 3.9.5 (default, Mar 14 2023, 08:11:14)
      [GCC 9.4.0] on linux
      Type "help", "copyright", "credits" or "license" for more information.
      >>> import axcl
      >>>

4. Uninstall: ``pip3 uninstall pyAXCL -y``.
5. Build whl.

   .. code-block:: bash

      $ pip3 install setuptools wheel
      $ cd axcl/python
      $ ./build.sh


axcl
----------------

.. automodule:: axcl.axcl
   :inherited-members:

axcl.ax_codec_comm
---------------------------

.. automodule:: axcl.ax_codec_comm
   :inherited-members:

axcl.ax_global_type
----------------------------

.. automodule:: axcl.ax_global_type
   :inherited-members:
