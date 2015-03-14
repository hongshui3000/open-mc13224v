
```
NVM_SetSVar(uint32_t v)
{
0x00007084:     push    {r4, lr}
0x00007086:     lsls    r4, r0, #0
    // call the ROM patch function
    RP_Vector3(0x77);
0x00007088:     push    {r7}
0x0000708a:     movs    r7, #119        ; 0x77
0x0000708c:     bl      0x400060 <__iar_section$$root>
0x00007090:     pop     {r7}
    // save the SVar value in a specific location
    *((uint32_t*) 0x40020b) = v;
0x00007092:     ldr     r0, [pc, #8]    ; (0x709c)
0x00007094:     strb    r4, [r0, #0]
0x00007096:     pop     {r4}
0x00007098:     pop     {r0}
0x0000709a:     bx      r0
0x0000709c:     .w 0x40020b
}
```