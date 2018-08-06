#!/usr/bin/env bash -xe
umask 0002

modulename=$1
modulespec=$2
compiler=$3

spack fetch -D "$modulespec"
spack spec -I "$modulespec"
if [ "$4" = "local" ]
then
    spack install --only dependencies --show-log-on-error -j4 "$modulespec"
else
    srun -p jenkins -c8 -t6:00:00 spack install --only dependencies --show-log-on-error "$modulespec"
fi
# fancy bash-magic to get the hash of the installed package
# For most builds the last output line of `spack install` reports the installation directory,
# which contains the hash of the package as the last entry after a '-'.
# If the package was previously installed as a dependency there will be a line added containing
# "marking the package explicit" and the second last line contains the hash.
newhash=$(spack install --show-log-on-error -j4 "$modulespec" | tail -n2 | grep -v "marking the package explicit" | tail -n1 | tr "-" "\n" | tail -n1)

viewname="views/${modulename}_$BUILD_ID"
spack view --dependencies yes hardlink -i $viewname /$newhash
spack view --dependencies no hardlink -i $viewname $compiler

DIR="$( cd "$( dirname "$0}" )" && pwd )"
bash $DIR/00_module.sh "${PWD}/$viewname" "${PWD}/modules/${modulename}_$BUILD_ID"
