# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLlvmlite(PythonPackage):
    """A lightweight LLVM python binding for writing JIT compilers"""

    homepage = "http://llvmlite.readthedocs.io/en/latest/index.html"
    pypi = "llvmlite/llvmlite-0.23.0.tar.gz"

    version('0.37.0', sha256='6392b870cd018ec0c645d6bbb918d6aa0eeca8c62674baaee30862d6b6865b15')
    version('0.36.0', sha256='765128fdf5f149ed0b889ffbe2b05eb1717f8e20a5c87fa2b4018fbcce0fcfc9')
    version('0.35.0', sha256='80e51d5aa02ad72da9870e89d21f9b152b0220ca551b4596a6c0614bcde336fc')
    version('0.34.0', sha256='f03ee0d19bca8f2fe922bb424a909d05c28411983b0c2bc58b020032a0d11f63')
    version('0.33.0', sha256='9c8aae96f7fba10d9ac864b443d1e8c7ee4765c31569a2b201b3d0b67d8fc596')
    version('0.31.0', sha256='22ab2b9d7ec79fab66ac8b3d2133347de86addc2e2df1b3793e523ac84baa3c8')
    version('0.29.0', sha256='3adb0d4c9a17ad3dca82c7e88118babd61eeee0ee985ce31fa43ec27aa98c963')
    version('0.27.1', sha256='48a1c3ae69fd8920cba153bfed8a46ac46474bc706a2100226df4abffe0000ab')
    version('0.26.0', sha256='13e84fe6ebb0667233074b429fd44955f309dead3161ec89d9169145dbad2ebf')
    version('0.25.0', sha256='fd64def9a51dd7dc61913a7a08eeba5b9785522740bec5a7c5995b2a90525025')
    version('0.23.0', sha256='bc8b1b46274d05b578fe9e980a6d98fa71c8727f6f9ed31d4d8468dce7aa5762')
    version('0.20.0', sha256='b2f174848df16bb9195a07fec102110a06d018da736bd9b3570a54d44c797c29')

    variant('skipllvmcheck', default=False, description='skips the llvm version check')

    patch('https://github.com/jschueller/llvmlite/commit/7c14ef015f2f95f264f53404dfcea68b1214d6e9.patch',
          sha256='586f594a850b314800737dff4b12d04d641a96eb94c0507140a50aea5ba2f80e', when='@:0.32.999')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@0.33:')
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3.99')

    # llvmlite compatibility information taken from https://github.com/numba/llvmlite#compatibility
    #                                           and https://github.com/numba/llvmlite/blob/master/CHANGE_LOG
    depends_on('llvm~flang', when='+skipllvmcheck')
    depends_on('llvm@11.0:11.1.999~flang', when='@0.37.0: ~skipllvmcheck')
    for t in ['arm:', 'ppc:', 'ppc64:', 'ppc64le:', 'ppcle:',
              'sparc:', 'sparc64:', 'x86:', 'x86_64:']:
        depends_on('llvm@10.0:10.0.999~flang', when='@0.34.0:0.36.99 ~skipllvmcheck target={0}'.format(t))
    depends_on('llvm@9.0:9.0.99~flang', when='@0.34.0:0.36.99 ~skipllvmcheck target=aarch64:')
    depends_on('llvm@9.0:9.0.99~flang', when='@0.33.0:0.33.99 ~skipllvmcheck')
    depends_on('llvm@7.0:9.0.99~flang', when='@0.29.0:0.32.99 ~skipllvmcheck')
    depends_on('llvm@7.0:7.0.99~flang', when='@0.27.0:0.28.99 ~skipllvmcheck')
    depends_on('llvm@6.0:6.0.99~flang', when='@0.23.0:0.26.99 ~skipllvmcheck')
    depends_on('llvm@4.0:4.0.99~flang', when='@0.17.0:0.20.99 ~skipllvmcheck')
    depends_on('binutils', type='build')

    def setup_build_environment(self, env):
        if self.spec.satisfies('%fj'):
            env.set('CXX_FLTO_FLAGS', '{0}'.format(self.compiler.cxx_pic_flag))
            env.set('LD_FLTO_FLAGS', '-Wl,--exclude-libs=ALL')
        else:
            # Need to set PIC flag since this is linking statically with LLVM
            env.set('CXX_FLTO_FLAGS', '-flto {0}'.format(
                self.compiler.cxx_pic_flag))
            # env.set('CXXFLAGS', '-fPIC')
        if self.spec.satisfies('@0.33.0: +skipllvmcheck'):
            env.set('LLVMLITE_SKIP_LLVM_VERSION_CHECK', 1)
