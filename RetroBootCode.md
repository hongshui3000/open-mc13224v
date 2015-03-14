
```
* if comes out of doze or hibernate -> jump to SRAM (0x400000)
* disable IRQ and FIQ
* bypass the buck regulator (because after POR it assumes being powered by buck regulator)
* initialize the SRAM (0x4000 words at 0x400000)
* enable NVM 1V8 regulator
* finish initializing the SRAM (0x2000 more words)
* bl 0x10850:
** bx 0x000100ec (switch to thumb)
*** bl 0xe3d0 (FlashLib_Init):
**** SPIF_SETUP <- 3 (force high to reset)
**** SPIF_SETUP <- 1 (automatic low when active)
**** SPIF_TXDATA <- 0x90000000
**** SPIF_CLK_CTRL <- 0x27a0 (start, sck_count = 0x27, data_length = 0x20) -> 40 clock cycles, MOSI 32 bit
**** while SPIF_STATUS(SPI_INT) == 0, loop
**** byte <- SPIF_RX_DATA & 0xFF
**** if the received byte is equal to 0xBF (SST manufacturer)
***** return 1
**** SPIF_TXDATA <- 0x9F000000
**** SPIF_CLK_CTRL <- 0xf88 (start, sck_count = 0xf, data_length = 8) -> 16 clock cycles, MOSI 8 bit
**** while SPIF_STATUS(SPI_INT) == 0, loop
**** byte <- SPIF_RX_DATA & 0xFF
**** if the received byte is equal to 0x20 (SGS/Thomson manufacturer)
***** return 2
**** return 0
*** if flash different than sst -> goto unknown place
*** value <- GPIO_FUNC_SEL2 (0x8000000c + 20 = 0x80000020)
*** value <- value & 0xffff0fff
*** GPIO_FUNC_SEL2 <- value (clear function for GPIOs GPIO38/ADC2_VREFH and GPIO39/ADC2_VREFL)
*** value <- GPIO_PAD_PU_SEL1
*** value <- value | 0x40
*** GPIO_PAD_PU_SEL1 <- value (weak PU on GPIO 38)
*** value <- GPIO_PAD_PU_SEL1
*** value <- value & 0xffffff7f
*** GPIO_PAD_PU_SEL1 <- value (weak PD on GPIO 39)
*** value <- GPIO_PAD_PU_EN1
*** value <- value | 0xc0
*** GPIO_PAD_PU_EN1 <- value (enable pulls on GPIOs 38 and 39)
*** GPIO_PAD_DIR_RESET1 <- 0xc0 (set GPIOs 38 and 29 as inputs)
*** value <- GPIO_DATA_SEL1
*** value <- value & (~0xc0)
*** GPIO_DATA_SEL1 <- value (force GPIO 38 and 39 to be read directly from the PAD)
*** value <- GPIO_DATA1
*** value <- value & 0xc0
*** if value == 0x80 (ADC2_VREFL high, ADC2_VREFH low -> control for erase of the flash)
**** call 0x100cc
**** while (1)
*** else
**** bl e428 (FlashLib_Read) (r0=SPI base address, r1=pointer where to store the read value, r2=flash address where to read the info, r3=number of bytes to read):
***** SPIF_SETUP <- 2 (force select FLASH)
***** SPIF_TXDATA <- 0x3000000
***** SPIF_CLK_CTRL <- 0x1fa0 (start, sck_count = 0x1f, data_length = 0x20) -> 32 clock cycles, MOSI 32 bit
***** while SPIF_STATUS(SPI_INT) == 0, loop
***** perform checks on the value of the parameters passed to the function ???
***** SPIF_TXDATA <- 0x0
***** SPIF_CLK_CTRL <- 0x1f80 (start, sck_count = 0x1f, data_length = 0x0) -> 32 clock cycles, MOSI 0 bit
***** while SPIF_STATUS(SPI_INT) == 0, loop
***** value <- SPIF_RX_DATA
***** manipulate value ???
***** SPIF_SETUP <- 3 (force unselect FLASH)
***** SPIF_SETUP <- 1 (auto select FLASH)
***** return SPIF_RX_DATA
**** if return == "SECU"
***** xxx
**** elif return == "OKOK"
***** value <- SYS_CNTL
***** value <- value | 0x10
***** SYS_CNTL <- value (set JTAG_SECU_OFF)
***** 
```