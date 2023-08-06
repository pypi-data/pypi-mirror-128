# pyspark_kernel

A PySpark Jupyter kernel that utilizes [metakernel](https://github.com/Calysto/metakernel) to create an easy to initialize pyspark kernel for Python. This package resembles the [spylon-kernel](https://github.com/vericast/spylon-kernel) that utilizes metakernel as well.

## Prerequisites

* Apache Spark
* Jupyter Notebook
* Python 3.5+

## Install Package

You can install the pyspark_kernel package using `pip`.

```bash
pip install pyspark_kernel
```

## Install Kernel to use in Jupyter

To use pyspark_kernel as PySpark kernel for Jupyter Notebook run the following command:

```bash
python -m pyspark_kernel install
```

Once Jupyter launches and you should see `PySpark` as an option in the `New` dropdown menu.

## Packaging
To package to deploy simply run the following command from the top level of the package.

```bash
python setup.py sdist
```