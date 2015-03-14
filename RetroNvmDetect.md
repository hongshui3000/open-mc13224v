
```
nvmErr_t NVM_Detect(nvmInterface_t nvmInterface, nvmType_t* pNvmType)
 nvmInterface in r0, pNvmType in r1
{
    uint32_t baseAddr;
0x00006cb8:      f1 b5  push    {r0, r4, r5, r6, r7, lr}
0x00006cba:      04 00  lsls    r4, r0, #0
0x00006cbc:      0d 00  lsls    r5, r1, #0
    // call the ROM patch function
    RP_Vector3(0x76);
0x00006cbe:      80 b4  push    {r7}
0x00006cc0:      76 27  movs    r7, #118        ; 0x76
0x00006cc2:      f9 f3 cd f9    bl      0x400060 <__iar_section$$root>
0x00006cc6:      80 bc  pop     {r7}
    // init the type
    *pNvmType = 0;
0x00006cc8:      00 20  movs    r0, #0
0x00006cca:      28 70  strb    r0, [r5, #0]
    if (NVM_GetBaseAddr(nvmInterface, &baseAddr) != 0)
0x00006ccc:      69 46  mov     r1, sp
0x00006cce:      20 00  lsls    r0, r4, #0
0x00006cd0:      00 f0 f8 f9    bl      0x70c4
0x00006cd4:      00 28  cmp     r0, #0
0x00006cd6:      01 d0  beq.n   0x6cdc
    {
        return 1;
0x00006cd8:      01 20  movs    r0, #1
0x00006cda:      3e e0  b.n     0x6d5a
    }
    if (pNvmType == NULL)
    {
        return 3;
    }
0x00006cdc:      00 2d  cmp     r5, #0
0x00006cde:      01 d1  bne.n   0x6ce4
0x00006ce0:      03 20  movs    r0, #3
0x00006ce2:      3a e0  b.n     0x6d5a
    if (nvmInterface == 0)
0x00006ce4:      00 2c  cmp     r4, #0
0x00006ce6:      07 d1  bne.n   0x6cf8
    {
        uint32_t reg;
        reg = REG(0x80003048); 
0x00006ce8:      a5 48  ldr     r0, [pc, #660]  ; (0x6f80)
0x00006cea:      00 68  ldr     r0, [r0, #0]
        if ((reg & VREG_1P8V_EN) == 0)
0x00006cec:      80 21  movs    r1, #128        ; 0x80
0x00006cee:      01 40  ands    r1, r0
0x00006cf0:      c8 09  lsrs    r0, r1, #7
0x00006cf2:      01 d1  bne.n   0x6cf8
        {
0x00006cf4:      09 20  movs    r0, #9
0x00006cf6:      30 e0  b.n     0x6d5a
            return 9;
        }
    }
    // force SS high (to reset state machine)
    REG(baseAddr + 0xC) = 3;
0x00006cf8:      03 24  movs    r4, #3
0x00006cfa:      00 98  ldr     r0, [sp, #0]
0x00006cfc:      c4 60  str     r4, [r0, #12]
    // force SS auto
    REG(baseAddr + 0xC) = 1;
0x00006cfe:      01 27  movs    r7, #1
0x00006d00:      00 98  ldr     r0, [sp, #0]
0x00006d02:      c7 60  str     r7, [r0, #12]
    // execute command
    NVM_Command(baseAddr, 0x90000000, 0x000027a0);
0x00006d04:      16 4a  ldr     r2, [pc, #88]   ; (0x6d60)
0x00006d06:      90 21  movs    r1, #144        ; 0x90
0x00006d08:      09 06  lsls    r1, r1, #24
0x00006d0a:      00 98  ldr     r0, [sp, #0]
0x00006d0c:      00 f0 c8 f9    bl      0x70a0
    // read the received byte
    reg = REG(baseAddr+4) & 0xFF
0x00006d10:      ff 26  movs    r6, #255        ; 0xff
0x00006d12:      00 98  ldr     r0, [sp, #0]
0x00006d14:      40 68  ldr     r0, [r0, #4]
0x00006d16:      30 40  ands    r0, r6
    if (reg == 0xBF)
    {
0x00006d18:      bf 28  cmp     r0, #191        ; 0xbf
0x00006d1a:      01 d1  bne.n   0x6d20
        *pNvmType = 1;
0x00006d1c:      2f 70  strb    r7, [r5, #0]
        return 0;
    }
0x00006d1e:      1b e0  b.n     0x6d58
    // execute command
    NVM_Command(baseAddr, 0x9f000000, 0x00000f88);    
0x00006d20:      10 4f  ldr     r7, [pc, #64]   ; (0x6d64)
0x00006d22:      3a 00  lsls    r2, r7, #0
0x00006d24:      9f 21  movs    r1, #159        ; 0x9f
0x00006d26:      09 06  lsls    r1, r1, #24
0x00006d28:      00 98  ldr     r0, [sp, #0]
0x00006d2a:      00 f0 b9 f9    bl      0x70a0
    reg = REG(baseAddr+4) & 0xFF
0x00006d2e:      00 98  ldr     r0, [sp, #0]
0x00006d30:      40 68  ldr     r0, [r0, #4]
0x00006d32:      30 40  ands    r0, r6
    if (reg == 32)
    {
0x00006d34:      20 28  cmp     r0, #32
0x00006d36:      02 d1  bne.n   0x6d3e
        *pNvmType = 2;
0x00006d38:      02 20  movs    r0, #2
0x00006d3a:      28 70  strb    r0, [r5, #0]
        return 0;
    }
0x00006d3c:      0c e0  b.n     0x6d58
    // execute command
    NVM_Command(baseAddr, 0x1D000000, 0x00000F88);    
0x00006d3e:      3a 00  lsls    r2, r7, #0
0x00006d40:      e8 21  movs    r1, #232        ; 0xe8
0x00006d42:      49 05  lsls    r1, r1, #21
0x00006d44:      00 98  ldr     r0, [sp, #0]
0x00006d46:      00 f0 ab f9    bl      0x70a0
    reg = REG(baseAddr+4) & 0xFF
0x00006d4a:      00 98  ldr     r0, [sp, #0]
0x00006d4c:      40 68  ldr     r0, [r0, #4]
0x00006d4e:      06 40  ands    r6, r0
    if (reg != 31)
    {
        *pNvmType = 0;
    }
    else
    {
        *pNvmType = 3;
    }
0x00006d50:      1f 2e  cmp     r6, #31
0x00006d52:      00 d0  beq.n   0x6d56
0x00006d54:      00 24  movs    r4, #0
    return 0;
0x00006d56:      2c 70  strb    r4, [r5, #0]
0x00006d58:      00 20  movs    r0, #0
0x00006d5a:      f8 bc  pop     {r3, r4, r5, r6, r7}
0x00006d5c:      02 bc  pop     {r1}
0x00006d5e:      08 47  bx      r1
0x00006d60:      a0 27  movs    r7, #160        ; 0xa0
0x00006d62:      00 00  lsls    r0, r0, #0
0x00006d64:      88 0f  lsrs    r0, r1, #30
0x00006d66:      00 00  lsls    r0, r0, #0

0x00006f80:      48 30  adds    r0, #72 ; 0x48
0x00006f82:      00 80  strh    r0, [r0, #0]
```