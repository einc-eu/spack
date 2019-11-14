# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAstroid(PythonPackage):
    """A common base representation of python source code for pylint
    and other projects."""

    homepage = "https://github.com/PyCQA/astroid"
    url      = "https://github.com/PyCQA/astroid/archive/astroid-1.4.5.tar.gz"

    version('2.2.5', sha256='232c2cfc72bae18a28de6541bbd560a1a3f42e08c52e41bd3f1f00ed74b0a4a6')
    version('2.2.0', sha256='7e289d0aa4a537b4aa798bd609fdf745de0f3c37e6b67642ed328e1482421a6d')
    version('2.0.4', sha256='e2161452b7a07a4663dba61bfb2191a7b61b792fb8239427581dad43773e071e')
    version('1.6.6', sha256='3fbcc144457ba598fb48e0ddce5eacee62610ab11e6fe374b6eef5f7df2a3fbb')
    # version('1.5.3', sha256='6f65e4ea8290ec032320460905afb828') # has broken unit tests
    version('1.4.5', sha256='28d8f5b898087ecf86fd66ca0934e5c0e51fc0beb5972cfc4e0c11080e0cb6ab')
    version('1.4.4', sha256='a521dfdbb728ec36c4cc7a9287285e2c30233fb19faffcec8d080d1b2b2e7d1e')
    version('1.4.3', sha256='381a8b1a7e3861b0e7f5f25fb8d70fccf5d6b19ed81fcf76f569a5c5affe1bcc')
    version('1.4.2', sha256='f9007d651f4b3514ea5812127677a4bb681ff194164290cea358987920f24ee6')
    version('1.4.1', sha256='f1ab3ee6f17f9d30981399a52b56a7a7d2747ba24f0aa504e411ee6205a01fc0')

    # fixes symlink resolution, already included in 2: but not in 1.6.6
    patch('PR546.patch', when='@1.6.6')

    depends_on('python@2.7:2.8,3.4:', when='@:1.999.999')
    depends_on('python@3.4:', when='@2:')

    depends_on('py-lazy-object-proxy')
    depends_on('py-six')
    depends_on('py-wrapt')
    depends_on('py-enum34@1.1.3:', when='^python@:3.3.99')
    depends_on('py-singledispatch', when='^python@:3.3.99')
    depends_on('py-backports-functools-lru-cache', when='^python@:3.2.99')
    depends_on('py-setuptools@17.1:')
    # typed ast is only needed for CPython but there are no other python implementations in spack
    depends_on('py-typed-ast@1.3.0:', when='@2.2.5: ^python@3.7.0:')
