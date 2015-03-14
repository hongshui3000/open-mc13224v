
```
; The following address is called with:
; r0 = SPI controller base address (spi)
; r1 = pointer where to store the read value (ptr)
; r2 = flash address where to read the info (addr)
; r3 = number of bytes to read (nbr)
; 
0x0000e428:     push    {r0, r4, r5, r6, r7, lr}
; r4 <- ptr
0x0000e42a:     lsls    r4, r1, #0
; r1 <- addr
0x0000e42c:     lsls    r1, r2, #0
; r2 <- ptr
0x0000e42e:     lsls    r2, r4, #0
; SPIF_SETUP <- 2 (force select FLASH)
0x0000e430:     movs    r5, #2
0x0000e432:     str     r5, [r0, #12]
; addr <- (addr & 0x00FFFFFF) | 0x03000000
0x0000e434:     lsls    r1, r1, #8
0x0000e436:     lsrs    r1, r1, #8
0x0000e438:     movs    r5, #192        ; 0xc0
0x0000e43a:     lsls    r5, r5, #18
0x0000e43c:     orrs    r5, r1
; SPIF_TX_DATA <- addr
0x0000e43e:     str     r5, [r0, #0]
; SPIF_CLK_CTRL <- 0x1fa0 (start, sck_count = 0x1f, data_length = 0x20) -> 32 clock cycles, MOSI 32 bit
0x0000e440:     movs    r1, #253        ; 0xfd
0x0000e442:     lsls    r1, r1, #5
0x0000e444:     str     r1, [r0, #8]
; while (SPIF_STATUS(SPI_INT) == 0) ;
0x0000e446:     ldr     r1, [r0, #16]
0x0000e448:     lsls    r1, r1, #31
0x0000e44a:     bpl.n   0xe446
; if ((ptr & 3) != 0) 
0x0000e44c:     movs    r1, #3
0x0000e44e:     tst     r4, r1
0x0000e450:     bne.n   0xe46a
0x0000e452:     b.n     0xe472
; {
0x0000e454:     movs    r4, #0
0x0000e456:     str     r4, [r0, #0]
0x0000e458:     movs    r4, #240        ; 0xf0
0x0000e45a:     lsls    r4, r4, #3
0x0000e45c:     str     r4, [r0, #8]
;     while (SPIF_STATUS(SPI_INT) == 0) ;
0x0000e45e:     ldr     r4, [r0, #16]
0x0000e460:     lsls    r4, r4, #31
0x0000e462:     bpl.n   0xe45e
;
0x0000e464:     ldr     r4, [r0, #4]
0x0000e466:     strb    r4, [r2, #0]
0x0000e468:     adds    r2, r2, #1
0x0000e46a:     lsls    r4, r3, #0
0x0000e46c:     subs    r3, r4, #1
0x0000e46e:     cmp     r4, #0
0x0000e470:     bne.n   0xe454
; }
; if (nbr >= 4)
0x0000e472:     cmp     r3, #4
0x0000e474:     bcc.n   0xe4b4
; {
;     SPIF_TX_DATA <- 0
0x0000e476:     movs    r4, #0
0x0000e478:     str     r4, [r0, #0]
;     SPIF_CLK_CTRL <- 0x1f80 (start, sck_count = 0x1f, data_length = 0x0) -> 32 clock cycles, MOSI 0 bit
0x0000e47a:     movs    r5, #252        ; 0xfc
0x0000e47c:     lsls    r5, r5, #5
0x0000e47e:     str     r5, [r0, #8]
;     while (SPIF_STATUS(SPI_INT) == 0) ;
0x0000e480:     ldr     r5, [r0, #16]
0x0000e482:     lsls    r5, r5, #31
0x0000e484:     bpl.n   0xe480
;     r5 <- SPIF_RX_DATA
0x0000e486:     ldr     r5, [r0, #4]
;     r12 <- r5 >> 24
0x0000e488:     lsrs    r6, r5, #24
0x0000e48a:     mov     r12, r6
;     r7 <- (r5 >> 8) & 0xFF00
0x0000e48c:     lsrs    r6, r5, #8
0x0000e48e:     movs    r7, #255        ; 0xff
0x0000e490:     lsls    r7, r7, #8
0x0000e492:     ands    r7, r6
;     r12 <- r7 | r12
0x0000e494:     mov     r6, r12
0x0000e496:     orrs    r7, r6
0x0000e498:     mov     r12, r7
;     r6 <- (r5 << 8) & 0xFF0000
0x0000e49a:     lsls    r7, r5, #8
0x0000e49c:     movs    r6, #255        ; 0xff
0x0000e49e:     lsls    r6, r6, #16
0x0000e4a0:     ands    r6, r7
;     r5 <- r6 | r12 | (r5 <<24)
0x0000e4a2:     mov     r7, r12
0x0000e4a4:     orrs    r6, r7
0x0000e4a6:     lsls    r5, r5, #24
0x0000e4a8:     orrs    r5, r6
;     *ptr <- r5
0x0000e4aa:     str     r5, [r2, #0]
;     ptr += 4
0x0000e4ac:     adds    r2, r2, #4
;     nbr -= 4
0x0000e4ae:     subs    r3, r3, #4
;     if (nbr > 4) goto 0xe478
0x0000e4b0:     cmp     r3, #4
0x0000e4b2:     bcs.n   0xe478
; }
; if (nbr != 0)
0x0000e4b4:     cmp     r3, #0
0x0000e4b6:     beq.n   0xe4d4
; {
0x0000e4b8:     movs    r5, #240        ; 0xf0
0x0000e4ba:     lsls    r5, r5, #3
0x0000e4bc:     movs    r4, #0
0x0000e4be:     subs    r3, r3, #1
0x0000e4c0:     str     r4, [r0, #0]
0x0000e4c2:     str     r5, [r0, #8]
0x0000e4c4:     ldr     r6, [r0, #16]
0x0000e4c6:     lsls    r6, r6, #31
0x0000e4c8:     bpl.n   0xe4c4
0x0000e4ca:     ldr     r6, [r0, #4]
0x0000e4cc:     strb    r6, [r2, #0]
0x0000e4ce:     adds    r2, r2, #1
0x0000e4d0:     cmp     r3, #0
0x0000e4d2:     bne.n   0xe4be
; }
; SPIF_SETUP <- 3 (force unselect FLASH)
0x0000e4d4:     str     r1, [r0, #12]
; SPIF_SETUP <- 1 (auto select FLASH)
0x0000e4d6:     movs    r1, #1
0x0000e4d8:     str     r1, [r0, #12]
0x0000e4da:     pop     {r3, r4, r5, r6, r7}
; return
0x0000e4dc:     pop     {r0}
0x0000e4de:     bx      r0
```