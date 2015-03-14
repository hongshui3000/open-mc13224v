# Introduction #

Build steps.


# Details #

The following steps:
  * download openocd-0.8.0
  * download libusb-1.0.9

Compile libusb-1.0.9:
  * ./configure --enable-static
  * make

Compile openocd:
  * Build configuration:
```
./configure --enable-jlink --enable-ftdi LIBUSB1_CFLAGS="-I<yourpathtolibusb>/libusb-1.0.9/libusb" LIBUSB1_LIBS="-L<yourpathtolibusb>/libusb-1.0.9/libusb -lusb-1.0
```

  * build: `make`
  * install: `sudo make install`

At this point, the following information was populated:
  * `/usr/local/bin/` : openocd executable
  * `/usr/local/share/openocd` : all scripts, definition files, firmwares for openocd