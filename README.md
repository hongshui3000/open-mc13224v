# Introduction #

The goal of the `open-mc13224v` project is to provide an easy way to start development of applications for the Freescale MC13224V chip.

It provides:
  * a set of source files to build basic applications for the chip
  * the rules to build the applications
  * a set of tools that are necessary to interface the chip from a host computer
  * the libraries of the ROM
  * data files:
    * dumps of the reserved (calibration) area of the flash of the chip I own
    * dump of the ROM of the chips I own

I started this project with the Freescale MC13224V kits from [RedWireLLC](http://www.redwirellc.com/store) and all the targets in this project were tested successfully on these boards.

# Details #

The requirements for this project are:
  * make
  * Python 2.4+
  * gcc for ARM (see [here](../blob/wiki/ArmSuite.md) for build instructions)
  * USB port

Optional:
  * Eclipse 3.2+ : the project is also an eclipse project but it is not required to use it.  I do use it because it integrates in a single application many applications I need (IDE, debugger, SVN interface).  The eclipse project has only one build target (all) that builds all the sample applications.

# Project Structure #
The structure of the project should help locate the files you are looking for:

  * .project
  * .cproject
  * .pydevproject
  * .settings/ : eclipse project related files (can be removed if you don't use eclipse)
  * build/ : all the results of the build processes (not checked in)
  * data/ : data files that are not required by the build process
    * flash/ : content of the last page of the flash of the chips that I own
    * rom/ : chip rom content (in different versions if available)
  * docs/ : documentation files
    * registers/ : register description files
      * Makefile : file that generates the header files from the XLS register files
  * libraries/ : library files
  * scripts/ : script files
    * build/ : build scripts for all the targets of the project (including makefiles)
    * ld/ : link scripts
    * simu/ : simulation scripts (describe the platform, rom and flash content), the SystemC (TLM 2.0) based simulation tool can not be made public for the time being
  * src/ : all the source files necessary for the various targets
  * thirdparty/ : elements that come from other sources
    * BeeKit/ : elements that come from the FreeScale BeekKit environment
      * MyStarNetwork Demo (Coordinator)/ : demo software from MAC codebase
      * Weather Station Controller/ : demo software from SMAC codebase
  * tools/ : set of tools (can be required or not in the build process)
    * buildimages/ : tool that builds RAM and FLASH images from ELF for download on the chip
    * loaduart/ : tool to communicate with chip through the UART
    * reg\_xls2h/ : tool to build the register description header files from register XLS files

# Documentation #
Most of the documentation should be found in the wiki pages:
  * QuickStartupGuide : easy steps to start developing an application fir MC13224V
  * RetroEngineering : main page for retro engineering process of the ROM 2.1 and MACPHY.a functions
  * ArmSuite : how to build the ARM free compilation and debugging suite from GNU
  * [SystemC](SystemC.md) : how to build SystemC for Cygwin

