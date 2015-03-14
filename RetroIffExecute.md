
```
uint32_t
IFF_Execute(uint8_t *Data)
// return the number of words consumed
{
0x0000f924:      10 b5  push    {r4, lr}
0x0000f926:      04 00  lsls    r4, r0, #0
    // call the ROM patch function
    RP_Vector3(0x79);
0x0000f928:      80 b4  push    {r7}
0x0000f92a:      79 27  movs    r7, #121        ; 0x79
0x0000f92c:      f0 f3 98 fb    bl      0x400060 <__iar_section$$root>
0x0000f930:      80 bc  pop     {r7}
    // load first word of the read data
    r0 = uint32_t(Data[0]);
0x0000f932:      20 68  ldr     r0, [r4, #0]
0x0000f934:      24 1d  adds    r4, r4, #4

    // check if this is a direct register write
    if (r0 >= 0x00140001)
0x0000f936:      5a 49  ldr     r1, [pc, #360]  ; (0xfaa0)
0x0000f938:      88 42  cmp     r0, r1
0x0000f93a:      03 d3  bcc.n   0xf944
    {
        r1 = uint32_t(Data[4])
0x0000f93c:      21 68  ldr     r1, [r4, #0]
        *r0 = r1;
0x0000f93e:      01 60  str     r1, [r0, #0]
        return 2;
0x0000f940:      02 20  movs    r0, #2
0x0000f942:      17 e0  b.n     0xf974
    }
    
    // check if it is a specific command
    if (r0 < 16)
0x0000f944:      10 28  cmp     r0, #16
0x0000f946:      14 d2  bcs.n   0xf972
    {
        // check if command is 0 (execute delay)
        if (r0 == 0)
0x0000f948:      00 28  cmp     r0, #0
0x0000f94a:      05 d1  bne.n   0xf958
        {
            r0 = uint32_t(Data[4]) >> 2;
0x0000f94c:      20 68  ldr     r0, [r4, #0]
0x0000f94e:      80 08  lsrs    r0, r0, #2
            while (r0 != 0)
                r0--;
0x0000f950:      f6 d0  beq.n   0xf940
0x0000f952:      40 1e  subs    r0, r0, #1
0x0000f954:      fd d1  bne.n   0xf952
            return 2;
0x0000f956:      f3 e7  b.n     0xf940
        }
        // check if it is a write bits command
        if (r0 == 1)
0x0000f958:      01 28  cmp     r0, #1
0x0000f95a:      0a d1  bne.n   0xf972
        {
            uint32_t *ptr;  // r0
            uint32_t bitmask;  // r1
            uint32_t value;
            // retrieve the mask
            bitmask = uint32_t(Data[4]);
0x0000f95c:      21 68  ldr     r1, [r4, #0]
            ptr = uint32_t(Data[8]);
0x0000f95e:      60 68  ldr     r0, [r4, #4]
            value = *ptr;
0x0000f960:      08 34  adds    r4, #8
0x0000f962:      02 68  ldr     r2, [r0, #0]
            // clear the bits of the mask
            value = value & (~bitmask);
0x0000f964:      8a 43  bics    r2, r1
            r3 = uint32_t(Data[12])
0x0000f966:      23 68  ldr     r3, [r4, #0]
            *ptr = value | (uint32_t(Data[12]) & bitmask)
0x0000f968:      19 40  ands    r1, r3
0x0000f96a:      11 43  orrs    r1, r2
0x0000f96c:      01 60  str     r1, [r0, #0]
            return 4;
0x0000f96e:      04 20  movs    r0, #4
0x0000f970:      00 e0  b.n     0xf974
        }
    }
    return 0;
0x0000f972:      00 20  movs    r0, #0
0x0000f974:      10 bc  pop     {r4}
0x0000f976:      02 bc  pop     {r1}
0x0000f978:      08 47  bx      r1
}

0x0000faa0:      .word 0x00140001
```