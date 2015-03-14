# Introduction #

Steps to quickly start up on the MC13224V using this project.


# Steps #

  * open a terminal (Cygwin under Windows)
  * download the project locally
  * edit the file scripts/build/Makefile to update:
    * the GCC and LD locations (should be GCC for ARM processors)
    * the LOAD\_FLAGS -c option which indicates the com port number on which the RedBee module enumerated
  * clean a sample application (gen\_pattern):
    * `make gen_pattern_clean`
  * build a sample application (gen\_pattern):
    * `make gen_pattern`
  * run a sample application (gen\_pattern):
    * `make gen_pattern_install`
    * follow the instructions
  * flash the sample application in the module embedded flash (gen\_pattern):
    * `make gen_pattern_flash`
  * erase the module embedded flash:
    * set the S2 switch 1-OFF, 2-ON (S2 is labeled ERASE on the RedBee module)
    * press the "RESET" button on the RedBee module
    * the LED should now be bright white indicating that it is likely to run on the ROM