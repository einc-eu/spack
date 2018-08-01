##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

import os.path as osp

class VisionaryCommon(Package):
    """Packages common to all visionary meta packages"""

    # This is a meta-package.  Instructions:
    # $ cd /tmp
    # $ spack install binutils+plugins+gold
    # $ spack find binutils+plugins+gold
    # -- linux-debian8-x86_64 / gcc@4.X.X -----------------------------
    # qxd4ne6 binutils@2.27
    # $ spack install gcc@6.2.0+binutils+gold ^/qxd4ne6
    # $ spack cd -i "gcc@6.2.0+binutils+gold"
    # $ spack compiler find --scope site .
    # $ spack install visionary-defaults %gcc@6.2.0

    homepage = ''
    # some random tarball, to make `spack fetch --dependencies visionary-defaults` work
    url = 'https://github.com/electronicvisions/spack/archive/v0.8.tar.gz'

    # This is only a dummy tarball (see difference between version numbers)
    # TODO: as soon as a MetaPackage-concept has been merged, please update this package
    version('1.0', '372ce038842f20bf0ae02de50c26e85d', url='https://github.com/electronicvisions/spack/archive/v0.8.tar.gz')

    depends_on('py-git-review')
    depends_on('the-silver-searcher')
    depends_on('zsh')

    def install(self, spec, prefix):
        mkdirp(prefix.etc)
        # store a copy of this package.
        filename = osp.basename(osp.dirname(__file__)) # gives name of parent folder
        install(__file__, join_path(prefix.etc, filename + '.py'))

        # we could create some filesystem view here?
