# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Jq(AutotoolsPackage):
    """jq is a lightweight and flexible command-line JSON processor."""

    homepage = "https://stedolan.github.io/jq/"
    url      = "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-1.6.tar.gz"

    version('1.6', sha256='5de8c8e29aaa3fb9cc6b47bb27299f271354ebb72514e3accadc7d38b5bbaa72')
    version('1.5', sha256='d5667641d28c27d0c1e70de83e7f9bd8b2fed7fbf6a1d68731177d400a533c65')

    depends_on('oniguruma')
    depends_on('bison@3.0:', type='build')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        jq = self.spec['jq'].command
        f = os.path.join(os.path.dirname(__file__), 'input.json')

        assert jq('.bar', input=f, output=str) == '2\n'
