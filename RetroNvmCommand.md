
```
void NVM_Command(uint32_t baseAddr, uint32_t data, uin32_t ctrl)
{
0x000070a0:      70 b5  push    {r4, r5, r6, lr}
0x000070a2:      04 00  lsls    r4, r0, #0
0x000070a4:      0d 00  lsls    r5, r1, #0
0x000070a6:      16 00  lsls    r6, r2, #0
    // call the ROM patch function
    RP_Vector3(0x23);
0x000070a8:      80 b4  push    {r7}
0x000070aa:      17 27  movs    r7, #23
0x000070ac:      f8 f3 b8 ff    bl      0x400020 <__iar_section$$root>
0x000070b0:      80 bc  pop     {r7}
    // write the data to send
    REG(baseAddr) = data;
0x000070b2:      25 60  str     r5, [r4, #0]
    // write the control
    REG(baseAddr+8) = ctrl;
0x000070b4:      a6 60  str     r6, [r4, #8]
    // loop until done
    while ((REG(baseAddr+0x10) & 1) == 0) ;
0x000070b6:      20 69  ldr     r0, [r4, #16]
0x000070b8:      c0 07  lsls    r0, r0, #31
0x000070ba:      fc d5  bpl.n   0x70b6
    return;
0x000070bc:      70 bc  pop     {r4, r5, r6}
0x000070be:      01 bc  pop     {r0}
0x000070c0:      00 47  bx      r0
}
```