#===============================================================================
# FILE:        hppa.spec
# OVERVIEW:    New Jersey Machine Code Toolkit specification file for the
#              HP Pa/risc architecture (basically version 1.1)
#
# (C) 2000-01 The University of Queensland, BT group
#===============================================================================

# $Revision: 1.1 $
#  April 01 - Simon: Initial revision
# 01 May 01 - Simon: Fixed a problem with arith_imm's (bit numbers wrong?)
# 04 May 01 - Mike: Merged two .spec files
# 07 May 01 - Mike: Split [LD|ST]Wlm into lma and lmb depending on sign of im14
# 08 May 01 - Mike: New constructor for [LD|ST]Wlm (ldispa16m[ab]_addr
# 08 May 01 - Cristina: Cross-referenced table letters from Appendix C, 
#				PA-RISC 2.0 Architecture book
# 18 Jun 01 - Mike: Added Floating Point instuctions
# 26 Jun 01 - Mike: Changed some mnemonics from 2.0 to 1.1 form


# The convention for bit fields is aann_mm, where aa briefly describes the
# field, nn is the field length in bits, and mm is the starting bit number
# (in HP numbering, i.e. 0 at the left)
# Example: In the HP book, the im11 field of ADDI extends from bits 21 to 31.
# The sign bit is separated (always in bit 31), so we name the field from bits
# 21 to 30 as im10_21 (10 bits starting at 21)

# instruction fields go [0..31] left-->right
bit 0 is most significant


fields of instruction (32)
    inst 00:31
      op 00:05
# piecewise opcode
#   op_00 00:00  op_01 01:01  op_02 02:02  op_03 03:03  op_04 04:04  op_05 05:05

    b_06 06:10

# arithmetic/logical instructions (arith/log)
    r_06 06:10    r_11 11:15    c3_16 16:18    f_19 19:19
 ext6_20 20:25    d_26 26:26     t_27 27:31 im21_11 11:31
  im2_16 16:17  im2_18 18:19  im11_20 20:30

# indexed and short displacement load/store instructions (IndexMem)
#   r_11 11:15   t_27 27:31
    x_11 11:15  im5_11 11:15   s2_16 16:17    u_18 18:18    a_18 18:18
 addr_19 19:19   cc_20 20:21 ext4_22 22:25    m_26 26:26  im5_27 27:31

# unconditional branch instructions
#   x_11 11:15  w11_19 19:29
    t_06 06:10   w5_06 06:10   w5_11 11:15 ext3_16 16:18   ve_19 19:19  w10_19 19:28
    w_29 29:29   rv_20 20:29    n_30 30:30    w_31 31:31   rv_31 31:31    p_31 31:31

# arithmetic immediate instructions
#   r_06 06:10   c3_16 16:18    f_19 19:19
    t_11 11:15  ext_20 20:20 im10_21 21:30
 
# long displacement load/store instructions (load_dw/store_dw/load_w/store_w)
#   t_11 11:15   s2_16 16:17
 im10_18 18:27 im13_18 18:30 im11_18 18:28
    m_28 28:28
    a_29 29:29  ext_30 30:30    i_31 31:31
  ext_29 29:29

# system operation instructions
#   r_11 11:15 ext5_06 06:10    t_27 27:31  im5_27 27:31   s2_16 16:18
   cr_06 06:10   ct_06 27:31 im13_06 06:18
 im10_06 06:15 ext5_11 11:15   s3_16 16:18
    s_18 18:18 ext8_19 19:26  ext_17 17:17
 
# branch on bit instructions
    p_06 06:10    c_16 16:16     e_17 17:17    d_18 18:18

# Floating point instructions
  sub_16 16:18  fmt_19 19:20 class_21 21:22    x_23 23:23
   r1_24 24:24    t_25 25:25     n_26 26:26  sub_14 14:16
   df_17 17:18   sf_19 19:20     f_20 20:20

# Coprocessor (including floating point) Loads and Stores
 addr_22 22:22  uid_23 23:25   im4_11 11:14 im1_15 15:15


fieldinfo
# five bit register names
[ b_06 x_11 r_06 r_11 t_06 t_11 t_27 ]
  is [ names [
   "%r0" "%r1" "%r2" "%r3" "%r4" "%r5" "%r6" "%r7" "%r8"
   "%r9" "%r10" "%r11" "%r12" "%r13" "%r14" "%r15" "%r16" "%r17"
   "%r18" "%r19"  "%r20" "%r21" "%r22" "%r23" "%r24" "%r25" "%r26"
   "%r27" "%r28" "%r29"  "%r30" "%r31" ] ]

# two bit space register names
[ s2_16 ]
  is [ names [ "%s0" "%s1" "%s2" "%s3" ] ]

# three bit space register names
[ s3_16 ]
  is [ names [ "%s0" "%s1" "%s2" "%s3" "%s4" "%s5" "%s6" "%s7" ] ]

# five bit control register names
[ cr_06 ct_06 ]
  is [ names [
   "%cr0"  "%cr1"  "%cr2"  "%cr3"  "%cr4"  "%cr5"  "%cr6"  "%cr7"  "%cr8"
   "%cr9"  "%cr10" "%cr11" "%cr12" "%cr13" "%cr14" "%cr15" "%cr16" "%cr17"
   "%cr18" "%cr19" "%cr20" "%cr21" "%cr22" "%cr23" "%cr24" "%cr25" "%cr26"
   "%cr27" "%cr28" "%cr29" "%cr30" "%cr31" ] ]


# Table C-1
patterns
[
  SystemOp   LDBl       COMBT      BVB
  _          LDHl       COMIBT     BB
  ArithLog   LDWl       COMBF      MOVB
  IndexMem   LDWlm      COMIBF     MOVIB
  _          Load_dw    COMICLR    _
  _          _          subi       _
  _          _          _          _
  _          Load_w     CMPBdwt    _
  LDIL       STBl       ADDBT      BE
  Copr_w     STHl       ADDIBT     BLE
  ADDIL      STWl       ADDBF      UncondBr
  Copr_dw    STWlm      ADDIBF     CMPIBdw
  FPOP0C     Store_dw   addi.t     _
  LDO        _          addi       _
  FPOP0E     _          _          _
  _          Store_w    CMPBdwf    _
] is  op = { 0 to 63 columns 4 }


### ArithLog ######### (Table C-5)
### ArithImm ######### (Table C-9)
### IndexMem #########
### Load_dw ########## (Table C-7)
### Store_dw ######### (Table C-7)
### CompareBranch ####

patterns
[
  ADD       ADD.v     ADD.c       ADD.c.v   SHL1ADD
  SHL1ADD.v SHL2ADD   SHL2ADD.v   SHL3ADD   SHL3ADD.v
  SUB       SUB.v     SUB.t       SUB.t.v   SUB.b     SUB.b.v
  DS        ANDCM     AND         OR        XOR       UXOR
  COMCLR
  UADDCM    UADDCMT
  ADD.l     SHL1ADD.l  SHL2ADD.l    SHL3ADD.l
  DCOR      IDCOR
  HADD      HADD.s    HADD.u      HSUB      HSUB.s    HSUB.u
  HAVG
  HSHL1ADD  HSHL2ADD  HSHL3ADD    HSHR1ADD  HSHR2ADD  HSHR3ADD
] is ArithLog & ext6_20 = [
  0x18     0x38     0x1C     0x3C     0x19
  0x39     0x1A     0x3A     0x1B     0x3B
  0x10     0x30     0x13     0x33     0x14     0x34
  0x11     0x00     0x08     0x09     0x0A     0x0E
  0x22
  0x26     0x27
  0x28     0x29     0x2A     0x2B
  0x2E     0x2F
  0x0F     0x0D     0x0C     0x07     0x05     0x04
  0x0B
  0x1D     0x1E     0x1F     0x15     0x16     0x17
]

arith is ADD | ADD.v | ADD.c | ADD.c.v | SHL1ADD
  | SHL1ADD.v | SHL2ADD | SHL2ADD.v | SHL3ADD | SHL3ADD.v
  | SUB | SUB.v | SUB.t | SUB.t.v | SUB.b | SUB.b.v
  | DS | ANDCM | AND | OR | XOR | UXOR
  | COMCLR
  | UADDCM | UADDCMT
  | ADD.l | SHL1ADD.l | SHL2ADD.l | SHL3ADD.l
  | DCOR | IDCOR
  | HADD | HADD.s | HADD.u | HSUB | HSUB.s | HSUB.u
  | HAVG
  | HSHL1ADD | HSHL2ADD | HSHL3ADD | HSHR1ADD | HSHR2ADD | HSHR3ADD
  
  [ ADDI    ADDI.v   ]  is addi & ext_20 = { 0 to 1 }
  [ ADDI.t  ADDI.t.v ] is addi.t & ext_20 = { 0 to 1 }
  [ SUBI    SUBI.v   ]  is subi & ext_20 = { 0 to 1 }

  arith_imm is ADDI | ADDI.v | ADDI.t | ADDI.t.v | SUBI | SUBI.v
  
  [ arith_w arith_dw ] is arith & d_26 = {0 to 1}

  ins_arith_w    is arith_w | arith_imm
  ins_arith_dw   is arith_dw
  ins_arith_none is ADDIL

  NOP            is OR & r_06 = 0 & r_11 = 0 & t_27 = 0
  COPY           is OR & r_06 = 0 & r_11 != 0
  
  
# Indexed & Short Displacement Loads/Stores (Table C-6)
[
  LDB     LDH      LDW      LDD
  LDD.a   LDCD     LDW.a    LDCW
  STB     STH      STW      STD
  STBY    STDBY    STW.a    STD.a
] is IndexMem & ext4_22 = {0 to 15}

  load is LDB | LDH | LDW | LDD | LDCD | LDCW
  loadabs is LDD.a | LDW.a

  loads is load | loadabs

  index_load is load & addr_19 = 0
  index_loadabs is loadabs & addr_19 = 0
  index_loads is index_load | index_loadabs

  sdisp_load is load & addr_19 = 1
  sdisp_loadabs is loadabs & addr_19 = 1
  sdisp_loads is sdisp_load | sdisp_loadabs
  
  store is STB | STH | STW | STD
  storeabs is STW.a | STD.a
  storebytes is STBY | STDBY

  stores is store | storeabs | storebytes
    
  sdisp_store is store & addr_19 = 1
  sdisp_storeabs is storeabs & addr_19 = 1
  sdisp_storebytes is storebytes & addr_19 = 1
  
  sdisp_storeless is sdisp_store | sdisp_storeabs
  sdisp_storenabs is sdisp_store | sdisp_storebytes
  sdisp_stores    is sdisp_storeless | sdisp_storebytes

  indices is index_load
  indicesabs is index_loadabs

  sdisps is sdisp_store | sdisp_load
  sdispsabs is sdisp_storeabs | sdisp_loadabs    
  sdispsbytes is sdisp_storebytes
  
  LDDl is Load_dw & ext_30 = 0
  STDl is Store_dw & ext_30 = 0
  opdl is LDDl | STDl

  LDWlm2i  is Load_w  & ext_29 = 1        # If bit 29 is clear, these are
  STWlm2i  is Store_w & ext_29 = 1        # floating point instructions!

    # For long displacement loads and stores, whether it is modify after or
    # modify before depends on the sign of the displacement!
  LDWlma   is LDWlm & i_31 = 0
  LDWlmb   is LDWlm & i_31 = 1

  STWlma   is STWlm & i_31 = 0
  STWlmb   is STWlm & i_31 = 1

  ld_bhw_l is LDBl | LDHl | LDWl
  ld_l     is ld_bhw_l | LDWlm2i | LDWlm | LDO
  loads_l  is ld_l | LDDl
 
# We don't want STWlm to be part of st_bhw_l because it then gets the wrong
# addressing mode
  st_bhw_l is STBl | STHl | STWl
  st_l     is st_bhw_l | STWlm2i | STWlm
  stores_l is st_l | STDl
  
  ldisp_12  is LDDl | STDl
  ldisp_16  is ld_bhw_l | st_bhw_l
  ldisp_16ma is LDWlma | STWlma
  ldisp_16mb is LDWlmb | STWlmb
  ldisp_16a is LDWlm2i | STWlm2i

  [ ins_def_il ins_m  ins_s  ins_sm ]
    is index_loads & u_18 = {0 to 1} & m_26 = {0 to 1}

  all_ldst  is loads | stores
  
  ins_c_il  is ins_m | ins_s | ins_sm
  ins_c_ils is ins_def_il | ins_c_il

  ins_def_d   is sdisp_loads & m_26 = 0
               | sdisp_storeless & m_26 = 0
               | opdl & m_28 = 0
               | ld_l
               | st_l
  ins_ma      is sdisp_loads & m_26 = 1 & a_18 = 0 & im5_11 != 0
               | sdisp_storeless & m_26 = 1 & a_18 = 0 & im5_27 != 0
               | LDDl & m_28 = 1 & a_29 = 0
  ins_mb      is sdisp_loads & m_26 = 1 & a_18 = 1
               | sdisp_storeless & m_26 = 1 & a_18 = 1
               | LDDl & m_28 = 1 & a_29 = 1
  ins_o       is sdisp_loads & m_26 = 1 & a_18 = 0 & im5_11 = 0
               | sdisp_storeless & m_26 = 1 & a_18 = 0 & im5_27 = 0
               | LDDl & m_28 = 1 & a_29 = 0 & im10_18 = 0

  ins_b       is sdisp_storebytes & a_18 = 0 & m_26 = 0
  ins_bm      is sdisp_storebytes & a_18 = 0 & m_26 = 1
  ins_e       is sdisp_storebytes & a_18 = 1 & m_26 = 0
  ins_em      is sdisp_storebytes & a_18 = 1 & m_26 = 1

  ins_c_d     is ins_ma | ins_mb | ins_o
  ins_c_by    is ins_bm | ins_e | ins_em | ins_b
  ins_c_disps is ins_def_d | ins_c_d | ins_c_by

  ins_c_addrs is ins_c_disps | ins_c_ils 


### UncondBr ######## (Table D-9 of 1.1 manual)
[
    BL   GATE   BL.PUSH   BL.LONG
] is UncondBr & ext3_16 = [ 0 1 4 5 ]

  BLR      is UncondBr & ext3_16 = 2 & ve_19 = 0
  BV       is UncondBr & ext3_16 = 6 & ve_19 = 0
  BVE      is UncondBr & ext3_16 = 6 & ve_19 = 1
  BVE.l    is UncondBr & ext3_16 = 7 & ve_19 = 1

  ubranch is BL | GATE | BL.PUSH
  
### SystemOp ######## (Table C-2)
[
  BREAK     sync      RFI       RFI.r
  SSM       RSM       MTSM      LDSID
  MTSP      MFSP      MFIA      MTCTL
  MTSARCM   mfctl
] is SystemOp & ext8_19 =
[
  0x00      0x20      0x60      0x65
  0x6B      0x73      0xC3      0x85
  0xC1      0x25      0xA5      0xC2
  0xC6      0x45
]

  rfis is RFI | RFI.r
[ SYNC   SYNCDMA ] is sync & ext5_11 = [ 0  10 ]
  syncs is SYNC | SYNCDMA
[ MFCTL MFCTL.w ] is mfctl & ext_17 = [ 0  1 ]
  mfctls is MFCTL | MFCTL.w

  sysop_i_t    is SSM | RSM
  sysop_simple is rfis | syncs
  sysop_r      is MTSM | MTSARCM
  sysop_cr_t   is mfctls

  cmpb_w is COMBT | COMBF
  cmpb_dw is CMPBdwt | CMPBdwf
  cmpb_all is cmpb_w | cmpb_dw
  cmpib_w is COMIBT | COMIBF
  cmpib_all is cmpib_w | CMPIBdw
    
  cmp_w is cmpb_w | cmpib_w
  cmp_dw is cmpb_dw | CMPIBdw
  
  bve is BVE | BVE.l
  
  bb_all is BB | BVB
  be_all is BE | BLE
  bea_17 is be_all
  
  ins_bb_w is BB & d_18 = 0
  ins_bb_dw is BB & d_18 = 1

  ins_bbs_w  is bb_all & d_18 = 0
  ins_bbs_dw is bb_all & d_18 = 1
  
  nullifiable_br is UncondBr | cmpb_all | cmpib_all | bb_all | be_all
  
  ins_br_nnull   is nullifiable_br & n_30 = 0
  ins_br_null    is nullifiable_br & n_30 = 1

# Floating point operations (Table 6-9)

  fp0c0e         is FPOP0C | FPOP0E

  # Class 0
  flt_c0        is any of
                  [ FID       _           FCPY        FABS
                    FSQRT     FRND        FNEG        FNEGABS ],
                which is FPOP0C & class_21 = 0 & sub_16 = {0 to 7}
  flt_c0.E       is any of
                  [ _         _           FCPY.E      FABS.E
                    FSQRT.E   FRND.E      FNEG.E      FNEGABS.E ],
                which is FPOP0E & class_21 = 0 & sub_16 = {0 to 7}
  flt_c0_all     is FID                 | FCPY      | FABS
                  | FSQRT   | FRND      | FNEG      | FNEGABS
                                        | FCPY.E    | FABS.E
                  | FSQRT.E | FRND.E    | FNEG.E    | FNEGABS.E

  # Class 1
  flt_c1        is any of
                 [ FCNVFF     FCNVXF     FCNVFX     FCNVFXT ],
                which is FPOP0C & class_21 = 1 & sub_14 = {0 to 3}
  flt_c1.E      is any of
                 [ FCNVFF.E   FCNVXF.E   FCNVFX.E   FCNVFXT.E ],
                which is FPOP0E & class_21 = 1 & sub_14 = {0 to 3}
  flt_c1_all    is FCNVFF   | FCNVXF   | FCNVFX   | FCNVFXT
                 | FCNVFF.E | FCNVXF.E | FCNVFX.E | FCNVFXT.E

  # Class 2
  flt_c2         is any of [FCMP   FTEST   ],
                    which is FPOP0C & class_21 = 2 & sub_16 = {0 to 1}
  flt_c2.E       is any of [FCMP.E FTEST.E ],
                    which is FPOP0E & class_21 = 2 & sub_16 = {0 to 1}
  flt_c2_all     is FCMP | FTEST | FCMP.E | FTEST.E

  # Class 3
  flt_c3         is any of
                  [ FADD     FSUB     FMPY     FDIV ],
                    which is FPOP0C & class_21 = 3 & sub_16 = {0 to 3}
  flt_c3.E       is any of
                  [ FADD.E   FSUB.E   FMPY.E   FDIV.E ],
                    which is FPOP0E & class_21 = 3 & sub_16 = {0 to 3}
  flt_c3_all     is FADD   | FSUB   | FMPY   | FDIV |
                    FADD.E | FSUB.E | FMPY.E | FDIV.E



# Floating point loads and stores [Table 6-8]
  floads         is any of [ FLDWX FLDDX FLDWS FLDDS],
                 which is uid_23 < 2 & addr_19 = [0 1] & [ Copr_w Copr_dw]
                    & addr_22 = 0
  fstores        is any of [ FSTWX FSTDX FSTWS FSTDS],
                 which is uid_23 < 2 & addr_19 = [0 1] & [ Copr_w Copr_dw]
                    & addr_22 = 1
  fld_st         is FLDWX | FLDDX | FLDWS | FLDDS
                  | FSTWX | FSTDX | FSTWS | FSTDS


constructors
 
# Instruction completers constructed to specific completers

  c_cmpb_w  c3_16 : c_c is cmp_w & c3_16
  c_cmpb_dw c3_16 : c_c is cmp_dw & c3_16
  
  c_bbs_w     c_16 : c_c is ins_bbs_w & c_16
  c_bbs_dw    c_16 : c_c is ins_bbs_dw & c_16

  c_arith_w  c3_16 : c_c is ins_arith_w & c3_16
  c_arith_dw c3_16 : c_c is ins_arith_dw & c3_16
  c_arith_none     : c_c is ins_arith_none

  c_addrs : c_addr is ins_c_addrs
  
  c_br_nnull : c_null is ins_br_nnull
  c_br_null  : c_null is ins_br_null

  c_mfctl_w     : c_wcr is MFCTL.w
  c_mfctl r_06  : c_wcr is MFCTL & r_06

  c_bitpos_w p_06  : c_bit is ins_bb_w & p_06
  c_bitpos_dw p_06 : c_bit is ins_bb_dw & p_06
  c_bitsar         : c_bit is BVB

  index_addr     x(ss,b)[c_addr] : addr is index_load & x_11 = x & s2_16 = ss
                                                          & b_06 = b & c_addr
  indexabs_addr  x(b)[c_addr]    : addr is index_loadabs & x_11 = x & b_06 = b
                                                                     & c_addr
  
  sdispl_addr    im5!(ss,b)[c_addr]    : addr is sdisp_load & im5_11 = im5
                                             & s2_16 = ss & b_06 = b & c_addr
  sdisplabs_addr im5!(b)[c_addr]       : addr is sdisp_loadabs & im5_11 = im5
                                                          & b_06 = b & c_addr

  sdisps_addr    im5!(ss,b)[c_addr]    : addr is sdisp_storenabs & im5_27 = im5
                                              & s2_16 = ss & b_06 = b& c_addr
  sdispsabs_addr im5!(b)[c_addr]       : addr is sdisp_storeabs & im5_27 = im5
                                                          & b_06 = b & c_addr
  
  ldispa12_addr  ldisp!(ss,b)[c_addr]  : addr {
                           ldisp@[12:31] = i_31!,
                           ldisp@[2:11] = im10_18,
                           ldisp@[0:1] = 0
                } is ldisp_12 & s2_16 = ss & b_06 = b & c_addr & im10_18 & i_31
  
  ldispa16_addr  ldisp!(ss,b)[c_addr]  : addr {
                           ldisp@[13:31] = i_31!,
                           ldisp@[0:12] = im13_18
                } is ldisp_16 & s2_16 = ss & b_06 = b & im13_18 & i_31 & c_addr
  
  # ldispa16m[ab]_addr are the same as the above. We need the different
  # constructor name so that different semantics can be attached to the
  # addressing mode (modify before and modify after)
  ldispa16ma_addr ldisp!(ss,b)[c_addr]  : addr {
                           ldisp@[13:31] = i_31!,
                           ldisp@[0:12] = im13_18
               } is ldisp_16ma & s2_16 = ss & b_06 = b & im13_18 & i_31 & c_addr
  
  ldispa16mb_addr  ldisp!(ss,b)[c_addr]  : addr {
                           ldisp@[13:31] = i_31!,
                           ldisp@[0:12] = im13_18
               } is ldisp_16mb & s2_16 = ss & b_06 = b & im13_18 & i_31 & c_addr
  
  ldispa16abs_addr ldisp!(b)[c_addr]  : addr {
                           ldisp@[13:31] = i_31!,
                           ldisp@[0:12] = im13_18
                } is LDO & b_06 = b & im13_18 & i_31 & c_addr

  ldispa16a_addr ldisp!(ss,b)[c_addr]  : addr {
                           ldisp@[13:31] = i_31!,
                           ldisp@[2:12] = im11_18,
                           ldisp@[0:1] = 0
                } is ldisp_16a & s2_16 = ss & b_06 = b & i_31 & im11_18 & c_addr
  
  bea17_addr offset!(ss,b)  : addr {
                           offset@[18:31] = w_31!,
                           offset@[13:17] = w5_11,
                           offset@[12:12] = w_29,
                           offset@[02:11] = w10_19,
                           offset@[0:1] = 0
                } is bea_17 & s3_16 = ss & b_06 = b & w_31 & w5_11 & w_29 & w10_19


# Instructions!

  NOP
  COPY      r_11, t_27

  arith      c_c, r_11, r_06, t_27
  arith_imm  c_c, imm11!, r_06, t_11 {
                        imm11@[10:31] = i_31!,
                        imm11@[0:9] = im10_21
                } is arith_imm & c_c & i_31 & im10_21 & r_06 & t_11

  ADDIL      imm21!, r_06, "%r1" {
                        imm21@[31]!   =    i_31,
                        imm21@[20:30] = im11_20,
                        imm21@[18:19] =  im2_16,
                        imm21@[13:17] =  im5_11,
                        imm21@[11:12] =  im2_18,
                        imm21@[00:10] = 0
                } is ADDIL & r_06 & i_31 & im11_20 & im2_16 & im5_11 & im2_18

  loads     cc_20, addr,t_27
  stores    cc_20, r_11,addr
  
  loads_l   addr,t_11
  stores_l  r_11,addr

  LDIL      imm21!, t_06 {
                       imm21@[31]!   =    i_31,
                       imm21@[20:30] = im11_20,
                       imm21@[18:19] =  im2_16,
                       imm21@[13:17] =  im5_11,
                       imm21@[11:12] =  im2_18,
                       imm21@[00:10] = 0
                } is LDIL & t_06 & i_31 & im11_20 & im2_16 & im5_11 & im2_18

  ubranch c_null ubr_target!,t_06 {
  		 ubr_target = offset + 8,
                 offset@[18:31] = w_31!,
                 offset@[13:17] = w5_11,
                 offset@[12] = w_29,
                 offset@[2:11] = w10_19,
                 offset@[0:1] = 0
              } is ubranch & c_null & t_06 & w_31 & w5_11 & w10_19 & w_29

  BL.LONG c_null ubr_target!,2 {
                 ubr_target = offset + 8,
                 offset@[23:31] = w_31!,
                 offset@[18:22] = w5_06,
                 offset@[13:17] = w5_11,
                 offset@[12] = w_29,
                 offset@[2:11] = w10_19,
                 offset@[0:1] = 0
              } is BL.LONG & c_null & w_31 & w5_06 & w5_11 & w10_19 & w_29

  BLR c_null x_11,t_06
  BV c_null x_11(b_06)
  bve p_31 c_null (b_06)
  be_all   c_null addr

  BREAK        im5_27,im13_06
  sysop_i_t    im10_06,t_27
  sysop_simple
  sysop_r      r_11
  sysop_cr_t   c_wcr,t_27
  MTCTL        r_11,ct_06
  MFIA         t_27
  LDSID        (s2_16,b_06),t_27
  MTSP         r_11,sr! { sr@[3:31] = 0, sr@[2:2] = s_18, sr@[0:1] = s2_16
             } is MTSP & r_11 & s_18 & s2_16
  MFSP         sr!,t_27 { sr@[3:31] = 0, sr@[2:2] = s_18, sr@[0:1] = s2_16
             } is MFSP & t_27 & s_18 & s2_16


  cmpb_all c_c, c_null  r_11, r_06, target { target@[13:31]! = w_31!,
                           target@[12] = w_29, target@[2:11] = w10_19,
                           target@[0:1] = 0
                         } is cmpb_all & c_c & c_null & r_11 & r_06
                                             & w_31 & w_29 & w10_19
  
  cmpib_all c_c, c_null  im5_11, r_06, target { target@[13:31]! = w_31!,
                           target@[12] = w_29, target@[2:11] = w10_19,
                           target@[0:1] = 0
                         } is cmpib_all & c_c & c_null & im5_11 & r_06
                                             & w_31 & w_29 & w10_19
  
  
  bb_all c_c, c_null   r_11,c_bit,target { target@[13:31]! = w_31!,
                           target@[12] = w_29, target@[2:11] = w10_19,
                           target@[0:1] = 0
                         } is cmpib_all & c_c & c_null & r_11 & c_bit
                                             & w_31 & w_29 & w10_19

# Floating point
# Class 0, opcode 0C
  flt_c0 ,fmt r,t          { op = 0x0C }
                           is flt_c0 & r_06=r & t_27=t & fmt_19 = fmt

# Class 0, opcode 0E
  flt_c0.E ,f r,t          { op = 0x0E,
                             r@[0:4] = r_06, r@[5] = r1_24, r@[6:31] = 0,
                             t@[0:4] = t_27, t@[5] = t_25,  t@[6:31] = 0 } 
                           is flt_c0 & f_20 = f & r_06 & r1_24 & t_27 & t_25

# Class 1 (fcnvxx), opcode 0C
# Note: sub_14 (not sub_16) determines the type of conversion performed
  flt_c1  ,sf,df r,t       {op = 0x0C }
                           is flt_c1 & r_06=r & t_27=t & df_17 = df & sf_19 = sf
# Class 1 (fcnvxx), opcode 0E
  flt_c1.E  ,sf,df r,t     { op = 0x0E,
                                 r@[0:4] = r_06, r@[5] = r1_24, r@[6:31] = 0,
                                 t@[0:4] = t_27, t@[5] =  t_25, t@[6:31] = 0 }
                            is flt_c1.E & df_17 = df & sf_19 = sf
                               & r_06 & r1_24 & t_27 & t_25

# Class 2, opcode 0C
  flt_c2 ,fmt,c r1,r2      { op = 0x0C }
                           is flt_c2 & r_06 = r1 & r_11 = r2
                             & t_27 = c & fmt_19 = fmt
# Class 2, opcode 0E
  flt_c2.E ,f_20,c r1,r2   { op = 0x0E,
                             r1@[0:4] = r_06, r1@[5] = r1_24, r1@[6:31] = 0,
                             r2@[0:4] = r_11, r2@[5] = f_19,  r2@[6:31] = 0 }
                           is flt_c2.E & t_27 = c & f_20 & r_06 & r1_24 & r_11
                             & f_19

# Class 3, opcode 0C
  flt_c3 ,fmt r1,r2,t      is flt_c3 & r_06 = r1 & r_11 = r2 & t_27 = t
                             & fmt_19 = fmt
# Class 3, opcode 0E
  flt_c3.E ,fmt r1,r2,t   {  r1@[0:4] = r_06, r1@[5] = r1_24, r1@[6:31] = 0,
                             r2@[0:4] = r_11, r2@[5] = f_19,  r2@[6:31] = 0,
                              t@[0:4] = t_27,  t@[5] = t_25,   t@[6:31] = 0 }
                           is flt_c3.E & f_20 = fmt
                             & r_06 & r1_24 & r_11 & f_19 & t_27 & t_25


# Floating point loads and stores
# Addressing modes
patterns
  ins_faddr_s                 is u_18 = 1 & m_26 = 0 & addr_19 = 0
  ins_faddr_m                 is u_18 = 0 & m_26 = 1 & addr_19 = 0
  ins_faddr_sm                is u_18 = 1 & m_26 = 1 & addr_19 = 0
  ins_faddr_x                 is u_18 = 0 & m_26 = 0 & addr_19 = 0
  ins_faddr_mb                is a_18 = 1 & m_26 = 0 & addr_19 = 1
  ins_faddr_ma                is a_18 = 0 & m_26 = 1 & addr_19 = 1
  ins_faddr_si                is            m_26 = 0 & addr_19 = 1
  ins_faddr_all  is  ins_faddr_s  | ins_faddr_m  | ins_faddr_sm | ins_faddr_x
                   | ins_faddr_mb | ins_faddr_ma | ins_faddr_si

constructors
  c_faddrs        : c_faddr is ins_faddr_all

  index_faddr (x, s, b)  : faddr is x_11 = x   & s2_16 = s & b_06 = b
                                    & addr_22 = 0
#  sdisps_faddr(d!, s, b): faddr { d@[0:3 ] = im5_11@[1:4],
#                                  d@[4:31] = im5_11@[0]! }
  sdisps_faddr(d!, s, b) : faddr { d@[0:3 ] = im4_11,
                                   d@[4:31] = im1_15! }
                                is s2_16 = s & b_06 = b & addr_22 = 1 & im4_11
                                  & im1_15

  floads  ,c_faddr faddr, t_27
  fstores ,c_faddr r, faddr            is fstores & c_faddr & t_27 = r & faddr


