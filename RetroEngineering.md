Elements that were retro engineered from the ROM code:
  * Boot code : RetroBootCode
  * functions published in the ROM interface reference manual:
    * `0x7084 = NVM_SetSVar()` : RetroNvmSetSvar
    * `0x6cb8 = NVM_Detect()` : RetroNvmDetect
  * functions not published in the ROM interface reference manual but that have a published name in the library file LLC.a:
    * `0xe428 = FlashLib_Read()` : RetroFlashLib\_Read
    * `0xf97c = InitFromFlash()` : RetroInitFromFlash
  * functions not published in the ROM interface reference manual but that have a published name in the library file MACPHY.a:
    * `0x109b0 = InitializeMac()` : RetroInitializeMac
  * functions not published in the ROM interface reference manual and that have no library name (ROM address is provided and name is invented by me):
    * `0x70a0 = NVM_Command()` : RetroNvmCommand
    * `0x70c4 = NVM_GetBaseAddr()` : RetroNvmGetBaseAddr
    * `0xf924 = IFF_Execute()` : RetroIffExecute

Elements that were retro engineered from the MACPHY.a code, these elements where chosen because they were called during the initialization process of two examples provided with the Freescale BeeKit:
  * from the initialization process of the "MyStarNetwork Demo (Coordinator)" (example from BeeKit MAC codebase):
    * `InitializePhy()` : RetroInitializePhy
    * `MacPhyInit_Initialize()` : RetroMacPhyInitInitialize
  * from the initialization process of the "Weather Station Controller" (example from BeeKit SMAC codebase):
    * has been done by Mariano Alvira from RedWire LLC