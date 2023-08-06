# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2021. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************
import py_cpu
from importlib import import_module


def import_libutils():
    cpu_info = py_cpu.CPUInfo()
    if "avx2" in cpu_info.features and cpu_info.features.avx2:
        return import_module("snapml.libsnapmlutils_avx2")
    else:
        return import_module("snapml.libsnapmlutils")


def import_libsnapml(mpi_enabled=False):

    cpu_info = py_cpu.CPUInfo()

    if "avx2" in cpu_info.features and cpu_info.features.avx2:
        if mpi_enabled:
            return import_module("snapml.libsnapmlmpi3_avx2")
        else:
            return import_module("snapml.libsnapmllocal3_avx2")
    else:
        if mpi_enabled:
            return import_module("snapml.libsnapmlmpi3")
        else:
            return import_module("snapml.libsnapmllocal3")
