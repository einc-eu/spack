#!/usr/bin/env bash -xe

umask 0002

# ensure that system compiler are available
rm -f etc/linux/compilers.yaml
spack -d compiler add
# ensure that our chosen gcc is there
# make parameter?
spack -d fetch -D gcc@7.2.0
srun -p jenkins -c8 -t6:00:00 spack -d install --source --show-log-on-error gcc@7.2.0
# remove system compiler
rm -f etc/linux/compilers.yaml
# add our gcc
spack -d compiler add $(spack location -i gcc@7.2.0)
