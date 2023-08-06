
Start with writing test cases for our program

.. code-block:: python

    def foo(x):
        return x * x

in a file (let's call it :code:`reg_test.py`)

.. code-block:: python

    class RegressiveTest(RegressionTestCase):
        """our regression test case"""

        def test_almost_regressive_equal(self):
            self.assertAlmostRegressiveEqual(foo(1.01))
            self.assertAlmostRegressiveEqual(foo(1.11))

        def test_regressive_equal(self):
            self.assertAlmostRegressiveEqual(foo.__name__)
            self.assertAlmostRegressiveEqual(foo(2) > 0)


At first test run

.. code-block:: bash

    $ python -m untittest reg_test.py

the return values are stored in files
(more precise the argument values of
:code:`assertRegressiveEqual` and :code:`assertAlmostRegressiveEqual`):


.. code-block:: bash

    test/data/RegressiveTest/test_regressive_equal.json.zip
    test/data/RegressiveTest/test_almost_regressive_equal.json.zip

Re-running

.. code-block:: bash

    $ python -m untittest reg_test.py

will now use those data.
If any values have changed :code:`AssertError` will be raised as usual.

If the testcase may have changed (less or resp. more calls of
:code:`assertRegressiveEqual` and :code:`assertAlmostRegressiveEqual`)
some reference data will be left over or resp. missing.

So a :code:`LeftoverAssertValueError` or resp. :code:`MissingAssertValueError`
will be raised.


Note: All file input/outout is done
by the :code:`setUp()` and :code:`tearDown()`
methods of the standard
`unittest <https://docs.python.org/3/library/unittest.html>`_
framework. So on overwrite, don't forget to call either :code:`super` or
enhance

.. code-block:: python

    def setUp(self):
        self.readResults()

    def tearDown(self):
        self.validateResults()
        self.writeResults()


Hint: To avoid compression by zip archives set the class property
:code:`compression` of the :code:`RegressionTestCase` class to :code:`False`

.. code-block:: python

    RegressiveTest.compression=False

Hence

.. code-block:: bash

    test/data/RegressiveTest/test_regressive_equal.json
    test/data/RegressiveTest/test_almost_regressive_equal.json
