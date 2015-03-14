
```
struct FlashPatch
{
    uint32_t value;
    uint32_t patch;
}
uint32_t
InitFromFlash(uint32_t nvmAddr, struct FlashPatch *pPatch, uint8_t patchCount)
// returns the number of read bytes from the NVM
{
0x0000f97c:      f7 b5  push    {r0, r1, r2, r4, r5, r6, r7, lr}
0x0000f97e:      8a b0  sub     sp, #40 ; 0x28
    // stack variables
    uint32_t NvmRegulatorsStarted ; // (r4)
    uint32_t Offset ; // (r5)
    uint32_t NvmType ; // (sp+0)
    uint8_t Data[16] ; // (sp+4))
    uint8_t Buffer[8] ; // (sp+20)
    uint32_t length ; // (sp+28)
    uint8_t patchCount_save ; // (sp+32)
    
    // read register CRM_STATUS_REG
    reg = REG(0x80003018)
0x0000f980:      46 48  ldr     r0, [pc, #280]  ; (0xfa9c)
0x0000f982:      00 68  ldr     r0, [r0, #0]
    NvmRegulatorsStarted = reg & VREG_1P8V_RDY;
    if (NvmRegulatorsStarted == 0)
0x0000f984:      80 21  movs    r1, #128        ; 0x80
0x0000f986:      c9 02  lsls    r1, r1, #11
0x0000f988:      01 40  ands    r1, r0
0x0000f98a:      8c 0c  lsrs    r4, r1, #18
0x0000f98c:      01 d1  bne.n   0xf992
    {
        // probably start NVM regulators
        call 0xf8f0
0x0000f98e:      ff f7 af ff    bl      0xf8f0
    }
    // check internal FLASH type
    if ((NVM_Detect(0, &NvmType) != 0) ||
         (NvmType != 0))
0x0000f992:      69 46  mov     r1, sp
0x0000f994:      00 20  movs    r0, #0
0x0000f996:      f7 f7 8f f9    bl      0x6cb8 (NVM_Detect)
0x0000f99a:      00 28  cmp     r0, #0
0x0000f99c:      03 d1  bne.n   0xf9a6
0x0000f99e:      68 46  mov     r0, sp
0x0000f9a0:      00 78  ldrb    r0, [r0, #0]
0x0000f9a2:      00 28  cmp     r0, #0
0x0000f9a4:      01 d1  bne.n   0xf9aa
    {
        return 0;
0x0000f9a6:      00 20  movs    r0, #0
0x0000f9a8:      72 e0  b.n     0xfa90
    }

    // unlock the last page of the NVM
    NVM_SetSVar(0);
0x0000f9aa:      00 20  movs    r0, #0
0x0000f9ac:      f7 f7 6a fb    bl      0x7084 (NVM_SetSVar)

0x0000f9b0:      82 b0  sub     sp, #8
0x0000f9b2:      08 20  movs    r0, #8
0x0000f9b4:      00 90  str     r0, [sp, #0]
    // read 8 bytes from the NVM
    r0 = NVM_Read(0, NvmType, Buffer, nvmAddr, 8);
0x0000f9b6:      0c 9b  ldr     r3, [sp, #48]   ; 0x30
0x0000f9b8:      07 aa  add     r2, sp, #28
0x0000f9ba:      02 a8  add     r0, sp, #8
0x0000f9bc:      01 78  ldrb    r1, [r0, #0]
0x0000f9be:      00 20  movs    r0, #0
0x0000f9c0:      f7 f7 d2 f9    bl      0x6d68 (NVM_Read)
0x0000f9c4:      02 b0  add     sp, #8

    // check if the read was OK
    if ((r0 != 0) ||
0x0000f9c6:      00 28  cmp     r0, #0
0x0000f9c8:      0c d1  bne.n   0xf9e4
        // check the first word read
        (uint32_t(Buffer[0]) != 0x00000abc) ||
0x0000f9ca:      05 98  ldr     r0, [sp, #20]
0x0000f9cc:      32 49  ldr     r1, [pc, #200]  ; (0xfa98)
0x0000f9ce:      88 42  cmp     r0, r1
0x0000f9d0:      08 d1  bne.n   0xf9e4
        // check the following 2 bytes
        (uint16_t(Buffer[6]) >= 0x0101) ||
0x0000f9d2:      05 a8  add     r0, sp, #20
0x0000f9d4:      c1 88  ldrh    r1, [r0, #6]
0x0000f9d6:      ff 22  movs    r2, #255        ; 0xff
0x0000f9d8:      92 1c  adds    r2, r2, #2
0x0000f9da:      91 42  cmp     r1, r2
0x0000f9dc:      02 d2  bcs.n   0xf9e4
        // check size is aligned
        ((uint16_t(Buffer[4]) & 0x3) != 0)
0x0000f9de:      80 88  ldrh    r0, [r0, #4]
0x0000f9e0:      81 07  lsls    r1, r0, #30
0x0000f9e2:      03 d0  beq.n   0xf9ec
    {
        // re-lock the last page
        NVM_SetSVar(1);
0x0000f9e4:      01 20  movs    r0, #1
0x0000f9e6:      f7 f7 4d fb    bl      0x7084 (NVM_SetSVar)
        return 0;
0x0000f9ea:      dc e7  b.n     0xf9a6
    }
    
    // initialize the offset
    Offset = 8;
0x0000f9ec:      08 25  movs    r5, #8

    // save the length
    length = uint16_t(Buffer[4]) - 4;
0x0000f9ee:      00 1f  subs    r0, r0, #4
0x0000f9f0:      07 90  str     r0, [sp, #28]
    
    patchCount_save = patchCount;
0x0000f9f2:      0c a8  add     r0, sp, #48     ; 0x30
0x0000f9f4:      00 78  ldrb    r0, [r0, #0] ; get patchCount value
0x0000f9f6:      08 90  str     r0, [sp, #32] ; save into stack at patchCount_save

    // assembly way of doing loops
    goto loop1_mark1;
0x0000f9f8:      06 e0  b.n     0xfa08

loop1_mark2:
    // call function with data read
    r0 = IFF_Execute(Data);
0x0000f9fa:      01 a8  add     r0, sp, #4
0x0000f9fc:      ff f7 92 ff    bl      0xf924
    if (r0 == 0) 
        goto loop1_error
0x0000fa00:      00 28  cmp     r0, #0
0x0000fa02:      12 d0  beq.n   0xfa2a

loop1_mark3:
    // increment the offset
    Offset += r0 * 4;
0x0000fa04:      80 00  lsls    r0, r0, #2
0x0000fa06:      2d 18  adds    r5, r5, r0

loop1_mark1:
    if (Offset >= length) 
        goto loop_exit
0x0000fa08:      07 98  ldr     r0, [sp, #28]
0x0000fa0a:      85 42  cmp     r5, r0
0x0000fa0c:      37 d2  bcs.n   0xfa7e
    // read next 2 words
    r0 = NVM_Read(0, NvmType, Data, nvmAddr+offset, 16);
0x0000fa0e:      82 b0  sub     sp, #8
0x0000fa10:      10 20  movs    r0, #16
0x0000fa12:      00 90  str     r0, [sp, #0]
0x0000fa14:      0c 98  ldr     r0, [sp, #48]   ; 0x30
0x0000fa16:      43 19  adds    r3, r0, r5
0x0000fa18:      03 aa  add     r2, sp, #12
0x0000fa1a:      02 a8  add     r0, sp, #8
0x0000fa1c:      01 78  ldrb    r1, [r0, #0]
0x0000fa1e:      00 20  movs    r0, #0
0x0000fa20:      f7 f7 a2 f9    bl      0x6d68 (NVM_Read)
0x0000fa24:      02 b0  add     sp, #8
    // check if read happened correctly
    if (r0 != 0)
0x0000fa26:      00 28  cmp     r0, #0
0x0000fa28:      03 d0  beq.n   0xfa32
    {
loop1_error:
        // re-lock the last page
        NVM_SetSVar(1);
0x0000fa2a:      01 20  movs    r0, #1
0x0000fa2c:      f7 f7 2a fb    bl      0x7084
        return Offset ;
0x0000fa30:      2d e0  b.n     0xfa8e
    }
    
    // get data read content
    r0 = uint32_t(Data[0]);
    if (r0 < 16) 
        goto loop1_mark2
0x0000fa32:      01 98  ldr     r0, [sp, #4]
0x0000fa34:      10 28  cmp     r0, #16
0x0000fa36:      e0 d3  bcc.n   0xf9fa

    if (r0 >= 0x00140001)
        goto loop1_mark2
0x0000fa38:      19 49  ldr     r1, [pc, #100]  ; (0xfaa0)
0x0000fa3a:      88 42  cmp     r0, r1
0x0000fa3c:      dd d2  bcs.n   0xf9fa

    // check if there is a patch table
    if ((pPatch != NULL) &&
0x0000fa3e:      00 20  movs    r0, #0
0x0000fa40:      0b 99  ldr     r1, [sp, #44]   ; 0x2c
0x0000fa42:      00 29  cmp     r1, #0
0x0000fa44:      19 d0  beq.n   0xfa7a
        (patchCount != 0))
0x0000fa46:      0c a9  add     r1, sp, #48     ; 0x30
0x0000fa48:      09 78  ldrb    r1, [r1, #0]
0x0000fa4a:      00 29  cmp     r1, #0
0x0000fa4c:      15 d0  beq.n   0xfa7a
    {
        bool found = False; // r0
        uint32_t counter = 0; // r1
0x0000fa4e:      00 21  movs    r1, #0
        struct FlashPatch *rover = pPatch; // r2
0x0000fa50:      0b 9a  ldr     r2, [sp, #44]   ; 0x2c // get pPatch
        do
        {
            if (rover->value == uint32_t(Data[0]))
0x0000fa52:      13 68  ldr     r3, [r2, #0]
0x0000fa54:      01 9f  ldr     r7, [sp, #4]
0x0000fa56:      bb 42  cmp     r3, r7
0x0000fa58:      02 d1  bne.n   0xfa60
            {
                // patch the data
                uint32_t(Data[0])) = rover->patch;
0x0000fa5a:      50 68  ldr     r0, [r2, #4]
0x0000fa5c:      01 90  str     r0, [sp, #4]
                // mark it was found
                found = True;
0x0000fa5e:      01 20  movs    r0, #1
            }
            // move to the next element in v1 (2 words per element)
            counter++;
0x0000fa60:      49 1c  adds    r1, r1, #1
            rover++;
0x0000fa62:      08 32  adds    r2, #8
        } while ((counter < patchCount_save) &&
0x0000fa64:      08 9b  ldr     r3, [sp, #32]
0x0000fa66:      99 42  cmp     r1, r3
0x0000fa68:      01 d2  bcs.n   0xfa6e
                 (found == False));
0x0000fa6a:      03 00  lsls    r3, r0, #0
0x0000fa6c:      f1 d0  beq.n   0xfa52
        // if it was patched, then execute
        if (found == True)
0x0000fa6e:      01 28  cmp     r0, #1
0x0000fa70:      03 d1  bne.n   0xfa7a
        {
            IFF_Execute(Data);
0x0000fa72:      01 a8  add     r0, sp, #4
0x0000fa74:      ff f7 56 ff    bl      0xf924
            goto loop1_mark3;
0x0000fa78:      c4 e7  b.n     0xfa04
        }
        // otherwise, just give up on this element
    }
    // increment by the number of word read even if not executed
    r0 = 2;
0x0000fa7a:      02 20  movs    r0, #2
    goto loop1_mark3
0x0000fa7c:      c2 e7  b.n     0xfa04

loop1_exit:
    // add the last word read
    Offset += 4;
0x0000fa7e:      2d 1d  adds    r5, r5, #4
    // re-lock the last page
    NVM_SetSVar(1);
0x0000fa80:      01 20  movs    r0, #1
0x0000fa82:      f7 f7 ff fa    bl      0x7084 (NVM_SetSVar)
    if (NvmRegulatorsStarted == 0)
0x0000fa86:      00 2c  cmp     r4, #0
0x0000fa88:      01 d1  bne.n   0xfa8e
    {
        // probably STOP NVM regulators
0x0000fa8a:      ff f7 43 ff    bl      0xf914
    }
   return Offset;
0x0000fa8e:      28 00  lsls    r0, r5, #0
0x0000fa90:      0d b0  add     sp, #52 ; 0x34
0x0000fa92:      f0 bc  pop     {r4, r5, r6, r7}
0x0000fa94:      02 bc  pop     {r1}
0x0000fa96:      08 47  bx      r1
}
0x0000fa98:      .word 0x00000abc
0x0000fa9c:      .word 0x80003018
0x0000faa0:      .word 0x00140001
```