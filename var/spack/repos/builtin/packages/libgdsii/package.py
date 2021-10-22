# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgdsii(AutotoolsPackage):
    """libGDSII is a C++ library for working with GDSII binary data files,
    intended primarily for use with the computational electromagnetism codes
    scuff-em and meep but sufficiently general-purpose to allow other uses as
    well."""

    homepage = "https://github.com/HomerReid/libGDSII"
    url      = "https://github.com/HomerReid/libGDSII/archive/refs/tags/v0.21.tar.gz"

    version('0.21', sha256='1adc571c6b53df4c08d108f9ac4f4a7fd6fbefd4bc56f74e0b7b2801353671b8')

    depends_on('m4', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')

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
