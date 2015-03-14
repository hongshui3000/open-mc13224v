Several times, I had to recompile the entire GCC for ARM suite (including the link tools, the debugger, the C library and the GCC core).  I have always used the script provided here and I updated the problems encountered at the beginning of the script.

The script was tested with the following tarballs:
  1. mid-2009:
    * binutils-2.19.1.tar.gz
    * gdb-6.8.50.20090912.tar.bz2 (the 6.8 stable release does not support the ARM-THUMB automatic disassembly)
    * gmp-4.2.4.tar.bz2
    * mpfr-2.4.1.tar.bz2
    * gcc-core-4.4.0.tar.bz2
    * newlib-1.17.0.tar.gz
  1. beginning-2010:
    * binutils-2.20.51.tar.bz2
    * gdb-7.1.tar.bz2 (the 6.8 stable release does not support the ARM-THUMB automatic disassembly)
    * gmp-4.3.2.tar.bz2
    * mpfr-2.4.2.tar.bz2
    * gcc-core-4.4.3.tar.bz2
    * newlib-1.18.0.tar.gz
  1. beginning-2014: chose not to recompile the dependency libraries but get them from system install (as advised on http://gcc.gnu.org/wiki/InstallingGCC) and compiled arm-none-eabi rather than arm-elf
    * binutils-2.24
    * gdb-7.7
    * gcc-4.8.2
    * newlib-2.1.0

The script to recompile everything including the dependency libraries is the following:
```
#! /bin/sh

# Problems encountered:
# 1. during binutils/configure:
#    - gcc can not build executables (ld can not find ctr0.o) -> reinstall the Cygwin base package
# 2. during binutils compilation:
#    - libtool: link: cannot find the library `/usr/lib/libiconv.la' or unhandled argument `/usr/lib/libiconv.la' -> install Cygwin libicvon package
# 3. during gdb compilation:
#    -  WARNING: no enhanced curses library found; disabling TUI -> not necessary if I dont use TUI
#    - configure: error: no termcap library found -> install Cygwin libncurses-devel
# 4. during gmp compilation:
#    - checking for suitable m4... configure: error: No usable m4 in $PATH or /usr/5bin (see config.log for reasons). -> install Cygwin m4 (Interpreters)
# 5. during the gcc rest compilation and install, I faced the following issue:
#checking for suffix of object files... configure: error: in '.../libgcc':
#configure: error: cannot compute suffix of object files: cannot compile
#See `config.log' for more details.
#  this problem was hit because I had compiled binutils while the $prefix variable had not been updated
# to the latest gcc  version so recompiling everything fixed the issue, but the error message is
# very confusing and came much later than the gcc successful compilation (and even the newlib)


# Variables
export binutils_version=2.20.51
export gdb_version=7.1
export gmp_version=4.3.2
export mpfr_version=2.4.2
export gcc_version=4.4.3
export newlib_version=1.18.0

export srcdir=$(pwd)
export target=arm-elf
export prefix=/cygdrive/c/${target}-tools/gcc-${gcc_version}
 
export PATH="$prefix/bin":"$PATH"


# Unpack

tar xvf binutils-${binutils_version}.tar.bz2
if [ $? -ne 0 ] ; then \
 # exit -1; \
fi
tar xvf gdb-${gdb_version}.tar.gz
if [ $? -ne 0 ] ; then \
 # exit -1; \
fi
tar xvf gmp-${gmp_version}.tar.bz2
if [ $? -ne 0 ] ; then \
 # exit -1; \
fi
tar xvf mpfr-${mpfr_version}.tar.bz2
if [ $? -ne 0 ] ; then \
 # exit -1; \
fi
tar xvf gcc-core-${gcc_version}.tar.bz2
if [ $? -ne 0 ] ; then \
 # exit -1; \
fi
tar xvf newlib-${newlib_version}.tar.gz
if [ $? -ne 0 ] ; then \
 # exit -1; \
fi

# here, eventually, replace the multilib support description file 
#cp -f t-arm-elf gcc-${gcc_version}/gcc/config/arm

# Build directory
mkdir -p $prefix

# binutils (no dependency)
mkdir build-binutils
cd build-binutils
${srcdir}/binutils-${binutils_version}/configure \
        --target=$target --prefix=$prefix \
        --enable-interwork --enable-multilib --with-float=soft
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make -j 4 all
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make install
if [ $? -ne 0 ] ; then \
   exit -1; \
fi

# gdb (no dependency)
cd $srcdir
mkdir build-gdb
cd build-gdb
${srcdir}/gdb-${gdb_version}/configure \
        --target=$target --prefix=$prefix \
        --enable-interwork --enable-multilib --with-float=soft
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make -j 4 all
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make install
if [ $? -ne 0 ] ; then \
   exit -1; \
fi

# gmp (no dependency)
cd $srcdir
mkdir build-gmp
cd build-gmp
${srcdir}/gmp-${gmp_version}/configure --prefix=$srcdir/build-gmp
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make -j 4
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make install
if [ $? -ne 0 ] ; then \
   exit -1; \
fi

# mpfr (gmp dependency)
cd $srcdir
mkdir build-mpfr
cd build-mpfr
${srcdir}/mpfr-${mpfr_version}/configure --prefix=$srcdir/build-mpfr --with-gmp=$srcdir/build-gmp
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make -j 4
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make install
if [ $? -ne 0 ] ; then \
   exit -1; \
fi

# gcc core (gmp and mpfr dependency)
cd $srcdir
mkdir build-gcc
cd build-gcc
${srcdir}/gcc-${gcc_version}/configure --target=$target --prefix=$prefix \
        --with-gmp=${srcdir}/build-gmp --with-mpfr=${srcdir}/build-mpfr --disable-shared \
        --enable-interwork --enable-multilib --with-float=soft \
        --enable-languages="c" --with-newlib \
        --with-headers=${srcdir}/newlib-${newlib_version}/newlib/libc/include
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make -j 4 all-gcc
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make install-gcc
if [ $? -ne 0 ] ; then \
   exit -1; \
fi


# newlib

# newlib wants arm-elf-cc but there is only arm-elf-gcc, so we make a link
#cd $prefix/bin
#ln -s arm-elf-gcc arm-elf-cc

cd $srcdir
mkdir build-newlib
cd build-newlib
${srcdir}/newlib-${newlib_version}/configure --target=$target --prefix=$prefix \
        --enable-multilib --enable-interwork --with-float=soft
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make -j 4 all
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make install
if [ $? -ne 0 ] ; then \
   exit -1; \
fi

# gcc rest
cd $srcdir/build-gcc
make -j 4 all
if [ $? -ne 0 ] ; then \
   exit -1; \
fi
make install
if [ $? -ne 0 ] ; then \
   exit -1; \
fi


```

The script to use the system installed libraries is the following:
```
#! /bin/sh

# in this version, I chose to use the standard libraries rather than rebuild them.  On cygwin, I had to install:
# - libgmp-devel
# - libcloog-isl-devel
# - libiconv2
# - libisl-devel
# - libmpc-devel
# - libmprf-devel
# - libncurses-devel

# Variables
export binutils_version=2.24
export gdb_version=7.7
export gcc_version=4.8.2
export newlib_version=2.1.0

export srcdir=$(pwd)
export target=arm-none-eabi
export prefix=/cygdrive/c/${target}-tools/gcc-${gcc_version}
 
export PATH="$prefix/bin":"$PATH"

# reset eventually
if test $1 = reset; then
  rm -rf build-binutils;
  rm -rf build-gdb;
fi

# Unpack
if test $1 = unzip; then
  tar xvf binutils-${binutils_version}.tar.bz2;
  if [ $? -ne 0 ] ; then
   exit -1;
  fi
  tar xvf gdb-${gdb_version}.tar.gz;
  if [ $? -ne 0 ] ; then
   exit -1;
  fi
  tar xvf gcc-${gcc_version}.tar.bz2
  if [ $? -ne 0 ] ; then \
   exit -1;
  fi
  tar xvf newlib-${newlib_version}.tar.gz
  if [ $? -ne 0 ] ; then \
   exit -1;
  fi
fi

# here, eventually, replace the multilib support description file 
#cp -f t-arm-elf gcc-${gcc_version}/gcc/config/arm
#

# Build directory
mkdir -p $prefix

if test $1 = binutils -o $1 = all; then
  # binutils (no dependency)
  mkdir build-binutils
  cd build-binutils
  ${srcdir}/binutils-${binutils_version}/configure \
          --target=$target --prefix=$prefix \
          --enable-interwork --enable-multilib --with-float=soft
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  make -j 4 all
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  
  make install
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
fi

if test $1 = gdb-o $1 = all; then
  # gdb (no dependency)
  cd $srcdir
  mkdir build-gdb
  cd build-gdb
  ${srcdir}/gdb-${gdb_version}/configure \
          --target=$target --prefix=$prefix \
          --enable-interwork --enable-multilib --with-float=soft
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  make -j 4 all
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  
  make install
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
fi

if test $1 = gcc -o $1 = all; then
  # gcc core (gmp and mpfr dependency)
  cd $srcdir
  mkdir build-gcc
  cd build-gcc
  
  # when building with local libraries:  
#  ${srcdir}/gcc-${gcc_version}/configure --target=$target --prefix=$prefix \
#          --with-gmp=${srcdir}/build-gmp --with-mpfr=${srcdir}/build-mpfr \
#          --disable-shared --disable-host-shared \
#          --enable-interwork --enable-multilib --with-float=soft \
#          --enable-languages="c" --with-newlib \
#          --with-headers=${srcdir}/newlib-${newlib_version}/newlib/libc/include

  # when using system installed libraries:
  ${srcdir}/gcc-${gcc_version}/configure --target=$target --prefix=$prefix \
          --disable-shared --disable-host-shared \
          --enable-interwork --enable-multilib --with-float=soft \
          --enable-languages="c" --with-newlib \
          --with-headers=${srcdir}/newlib-${newlib_version}/newlib/libc/include
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  make -j 4 all-gcc
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  make install-gcc
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
fi

if test $1 = newlib -o $1 = all; then
  # newlib
  
  # newlib wants arm-elf-cc but there is only arm-elf-gcc, so we make a link
  #cd $prefix/bin
  #ln -s arm-elf-gcc arm-elf-cc
  
  cd $srcdir
  mkdir build-newlib
  cd build-newlib
  ${srcdir}/newlib-${newlib_version}/configure --target=$target --prefix=$prefix \
          --enable-multilib --enable-interwork --with-float=soft
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  make -j 4 all
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  make install
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
fi

if test $1 = gccfull -o $1 = all; then
  # gcc rest
  cd $srcdir/build-gcc
  make -j 4 all
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
  make install
  if [ $? -ne 0 ] ; then \
     exit -1; \
  fi
fi
```