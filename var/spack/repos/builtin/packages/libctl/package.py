# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libctl(AutotoolsPackage):
    """libctl is a free Guile-based library implementing flexible
    control files for scientific simulations."""

    homepage = "https://github.com/NanoComp/libctl"
    url      = "https://github.com/NanoComp/libctl/archive/refs/tags/v4.5.0.tar.gz"

    version('4.5.0', sha256='5124551b3c9ed9a0ca599179f5e78318b5a7a1daa06220329a3b2963c848ba03')
    version('3.2.2', sha256='8abd8b58bc60e84e16d25b56f71020e0cb24d75b28bc5db86d50028197c7efbc')

    depends_on('m4', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')

    depends_on('guile')

    def configure_args(self):
        spec = self.spec

        return [
            '--enable-shared',
            'GUILE={0}'.format(join_path(
                spec['guile'].prefix.bin, 'guile')),
            'GUILE_CONFIG={0}'.format(join_path(
                spec['guile'].prefix.bin, 'guile-config')),
        ]

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
