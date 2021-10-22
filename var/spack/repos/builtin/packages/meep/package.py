# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Meep(AutotoolsPackage):
    """Meep (or MEEP) is a free finite-difference time-domain (FDTD) simulation
    software package developed at MIT to model electromagnetic systems."""

    homepage = "https://meep.readthedocs.io"
    url      = "https://github.com/NanoComp/meep/archive/refs/tags/v1.21.0.tar.gz"

    version('1.21.0', sha256='71911cd2f38b15bdafe9a27ad111f706f24717894d5f9b6f9f19c6c10a0d5896')
    version('1.3',    sha256='564c1ff1b413a3487cf81048a45deabfdac4243a1a37ce743f4fcf0c055fd438')
    version('1.2.1',  sha256='f1f0683e5688d231f7dd1863939677148fc27a6744c03510e030c85d6c518ea5')
    version('1.1.1',  sha256='7a97b5555da1f9ea2ec6eed5c45bd97bcd6ddbd54bdfc181f46c696dffc169f2')

    variant('blas',     default=True, description='Enable BLAS support')
    variant('lapack',   default=True, description='Enable LAPACK support')
    variant('harminv',  default=True, description='Enable Harminv support')
    variant('guile',    default=True, description='Enable Guilde support')
    variant('libctl',   default=True, description='Enable libctl support') # not optional?
    variant('mpi',      default=True, description='Enable MPI support')
    variant('hdf5',     default=True, description='Enable HDF5 support')
    variant('gsl',      default=True, description='Enable GSL support')
    variant('python',   default=True, description='Enable Python wrappers') # not optional?
    variant('libgdsii', default=True, description='Enable libGDSII support')
    variant('mpb',      default=True, description='Enable MPB support')

    depends_on('m4', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')

    depends_on('blas',        when='+blas')
    depends_on('lapack',      when='+lapack')
    depends_on('harminv',     when='+harminv')
    depends_on('guile',       when='+guile')
    depends_on('libctl@3.2:', when='+libctl')
    depends_on('mpi',         when='+mpi')
    depends_on('hdf5~mpi',    when='+hdf5~mpi')
    depends_on('hdf5+mpi',    when='+hdf5+mpi')
    depends_on('gsl',         when='+gsl')
    depends_on('python@3.7:', when='+python')
    depends_on('swig',        when='+python')
    depends_on('libgdsii',    when='+libgdsii')
    depends_on('mpb',         when='+mpb')

    def configure_args(self):
        spec = self.spec

        config_args = [
            '--enable-shared'
        ]

        if '+blas' in spec:
            config_args.append('--with-blas={0}'.format(
                spec['blas'].prefix.lib))
        else:
            config_args.append('--without-blas')

        if '+lapack' in spec:
            config_args.append('--with-lapack={0}'.format(
                spec['lapack'].prefix.lib))
        else:
            config_args.append('--without-lapack')

        if '+libctl' in spec:
            config_args.append('--with-libctl={0}'.format(
                join_path(spec['libctl'].prefix.share, 'libctl')))
        else:
            config_args.append('--without-libctl')

        if '+mpi' in spec:
            config_args.append('--with-mpi')
        else:
            config_args.append('--without-mpi')

        if '+hdf5' in spec:
            config_args.append('--with-hdf5')
        else:
            config_args.append('--without-hdf5')

        if '+guile' in spec:
            config_args.append('--with-guile')
        else:
            config_args.append('--without-guile')

        return config_args

    # custom ./autogen.sh
    @run_before('autoreconf')
    def custom_autogen_sh(self):
        autogen_sh = which('./autogen.sh')
        options = getattr(self, 'configure_flag_args', [])
        options += ['--prefix={0}'.format(prefix)]
        options += self.configure_args()
        autogen_sh(*options)

    def configure(self, spec, prefix):
        # ./autogen.sh does it
        pass

    def check(self):
        spec = self.spec

        # aniso_disp test fails unless installed with harminv
        # near2far test fails unless installed with gsl
        if '+harminv' in spec and '+gsl' in spec:
            # Most tests fail when run in parallel
            # 2D_convergence tests still fails to converge for unknown reasons
            make('check', parallel=False)
