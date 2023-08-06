Installation
============

System Requirements
-------------------

You'll need Python 3.7 or higher on macOS, Windows, or Linux.

The following Tomcat versions are supported:

- 8.0.x
- 8.5.x
- 9.0.x
- 10.0.x

The operating system and Java Virtual Machine don't matter as long as Tomcat
runs on it.

You can double check the list of versions supported by:

.. code-block::

   $ tomcat-manager -v
   4.1.0 (works with Tomcat >= 8.0 and <= 10.0)

or:

.. code-block::

   $ tomcat-manager
   tomcat-manager> version
   4.1.0 (works with Tomcat >= 8.0 and <= 10.0)

These tools should work with newer versions of Tomcat than the ones officially
supported. The Tomcat Manager web application that is part of Tomcat has been
remarkably stable over many versions, with only a few additions.


Install using pip
-----------------

Install using ``pip``:

.. code-block::

  $ pip install tomcatmanager

Works on Windows, macOS, and Linux.

Now what?

First you will need to :doc:`configuretomcat`.

If you are in a hurry to :doc:`get started with the command line tool
<interactive>`, type:

.. code-block::

   $ tomcat-manager -h

Or, you can start :doc:`writing your own python code which imports the
package <package>`.
