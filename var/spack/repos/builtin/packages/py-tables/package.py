# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTables(PythonPackage):
    """PyTables is a package for managing hierarchical datasets and designed to
    efficiently and easily cope with extremely large amounts of data."""
    homepage = "http://www.pytables.org/"
    url      = "https://github.com/PyTables/PyTables/archive/v3.3.0.tar.gz"

    version('3.5.2', '58667a5003838cc5c8773a796bf47632')
    version('3.4.4', '2cd52095ebb097f5bf58fa65dc6574bb')
    version('3.3.0', '056c161ae0fd2d6e585b766adacf3b0b')
    version('3.2.2', '7cbb0972e4d6580f629996a5bed92441',
            url='https://github.com/PyTables/PyTables/archive/v.3.2.2.tar.gz')

    variant('avx2', description='', default=False)
    variant('sse2', description='', default=False)
    variant('auto', description='', default=True)
    variant('bzip2', default=False, description='Support for bzip2 compression')
    variant('lzo', default=False, description='Support for lzo compression')

    depends_on('bzip2', when='+bzip2')
    depends_on('lzo', when='+lzo')

    # Versions prior to 3.3 must build with the internal blosc due to a lock
    # problem in a multithreaded environment.
    depends_on('hdf5-blosc', when="@3.3.0:")

    depends_on('hdf5@1.8.0:1.8.999', when="@:3.3.99")
    depends_on('hdf5@1.8.0:1.10.999', when="@3.4.0:")
    depends_on('py-numpy@1.8.0:1.15.99', type=('build', 'run'), when='@3.4.99')
    depends_on('py-numpy@1.8.0:', type=('build', 'run'))
    depends_on('py-numexpr@2.5.2:', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cpuinfo', type='build')

    patch('microarch.patch', when='~auto@3.3.0')
    patch('microarch_new.patch', when='~auto@3.4.4')
    patch('microarch_35.patch', when='~auto@3.5.2')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('HDF5_DIR', self.spec['hdf5'].prefix)
        cpu_flags = []
        if self.spec.satisfies('+avx2'):
            cpu_flags.append('avx2')
        if self.spec.satisfies('+sse2'):
            cpu_flags.append('sse2')
        if self.spec.satisfies('~auto'):
            cpu_flags = ' '.join(cpu_flags)
            spack_env.set('SPACK_TARGET_FLAGS', cpu_flags)

        if '+bzip2' in self.spec:
            spack_env.set('BZIP2_DIR', self.spec['bzip2'].prefix)
        if '+lzo' in self.spec:
            spack_env.set('LZO_DIR', self.spec['lzo'].prefix)
        if '+hdf5-blosc' in self.spec:
            spack_env.set('BLOSC_DIR', self.spec['c-blosc'].prefix)