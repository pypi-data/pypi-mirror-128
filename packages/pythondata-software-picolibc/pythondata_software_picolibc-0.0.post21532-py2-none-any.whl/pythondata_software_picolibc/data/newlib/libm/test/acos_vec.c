/*
 * Copyright (c) 1994 Cygnus Support.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms are permitted
 * provided that the above copyright notice and this paragraph are
 * duplicated in all such forms and that any documentation,
 * and/or other materials related to such
 * distribution and use acknowledge that the software was developed
 * at Cygnus Support, Inc.  Cygnus Support, Inc. may not be used to
 * endorse or promote products derived from this software without
 * specific prior written permission.
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
 */
#include "test.h"
 one_line_type acos_vec[] = {
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff33333, 0x33333333},	/* nan=f(-1.2)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff30a3d, 0x70a3d70a},	/* nan=f(-1.19)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff2e147, 0xae147ae1},	/* nan=f(-1.18)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff2b851, 0xeb851eb8},	/* nan=f(-1.17)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff28f5c, 0x28f5c28f},	/* nan=f(-1.16)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff26666, 0x66666666},	/* nan=f(-1.15)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff23d70, 0xa3d70a3d},	/* nan=f(-1.14)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff2147a, 0xe147ae14},	/* nan=f(-1.13)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff1eb85, 0x1eb851eb},	/* nan=f(-1.12)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff1c28f, 0x5c28f5c2},	/* nan=f(-1.11)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff19999, 0x99999999},	/* nan=f(-1.1)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff170a3, 0xd70a3d70},	/* nan=f(-1.09)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff147ae, 0x147ae147},	/* nan=f(-1.08)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff11eb8, 0x51eb851e},	/* nan=f(-1.07)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff0f5c2, 0x8f5c28f5},	/* nan=f(-1.06)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff0cccc, 0xcccccccc},	/* nan=f(-1.05)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff0a3d7, 0x0a3d70a3},	/* nan=f(-1.04)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff07ae1, 0x47ae147a},	/* nan=f(-1.03)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff051eb, 0x851eb851},	/* nan=f(-1.02)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff028f5, 0xc28f5c28},	/* nan=f(-1.01)*/
{64, 0,123,__LINE__, 0x400921fb, 0x5170194b, 0xbfefffff, 0xfffffffe},	/* 3.14159=f(-1)*/
{64, 0,123,__LINE__, 0x4008001b, 0xe1bc0117, 0xbfefae14, 0x7ae147ac},	/* 3.00005=f(-0.99)*/
{64, 0,123,__LINE__, 0x400787b2, 0x2ce3f58d, 0xbfef5c28, 0xf5c28f5a},	/* 2.94126=f(-0.98)*/
{64, 0,123,__LINE__, 0x40072b10, 0x466e25ee, 0xbfef0a3d, 0x70a3d708},	/* 2.89603=f(-0.97)*/
{63, 0,123,__LINE__, 0x4006dcc5, 0x7bb565fb, 0xbfeeb851, 0xeb851eb6},	/* 2.8578=f(-0.96)*/
{64, 0,123,__LINE__, 0x4006979e, 0x34f1b08f, 0xbfee6666, 0x66666664},	/* 2.82403=f(-0.95)*/
{64, 0,123,__LINE__, 0x400658f0, 0x0fec9c13, 0xbfee147a, 0xe147ae12},	/* 2.79343=f(-0.94)*/
{64, 0,123,__LINE__, 0x40061f25, 0xfc69b3c5, 0xbfedc28f, 0x5c28f5c0},	/* 2.76521=f(-0.93)*/
{64, 0,123,__LINE__, 0x4005e938, 0x3efad0cf, 0xbfed70a3, 0xd70a3d6e},	/* 2.73888=f(-0.92)*/
{63, 0,123,__LINE__, 0x4005b66f, 0xc75f8f2f, 0xbfed1eb8, 0x51eb851c},	/* 2.71408=f(-0.91)*/
{63, 0,123,__LINE__, 0x40058647, 0x6251e744, 0xbfeccccc, 0xccccccca},	/* 2.69057=f(-0.9)*/
{63, 0,123,__LINE__, 0x4005585a, 0x919e47f7, 0xbfec7ae1, 0x47ae1478},	/* 2.66814=f(-0.89)*/
{64, 0,123,__LINE__, 0x40052c5b, 0x4e51b553, 0xbfec28f5, 0xc28f5c26},	/* 2.64666=f(-0.88)*/
{64, 0,123,__LINE__, 0x4005020b, 0x942d7396, 0xbfebd70a, 0x3d70a3d4},	/* 2.626=f(-0.87)*/
{64, 0,123,__LINE__, 0x4004d939, 0x2170d7e8, 0xbfeb851e, 0xb851eb82},	/* 2.60607=f(-0.86)*/
{64, 0,123,__LINE__, 0x4004b1ba, 0x8ff34d12, 0xbfeb3333, 0x33333330},	/* 2.58678=f(-0.85)*/
{64, 0,123,__LINE__, 0x40048b6d, 0x4a69943d, 0xbfeae147, 0xae147ade},	/* 2.56808=f(-0.84)*/
{64, 0,123,__LINE__, 0x40046634, 0x12ff153e, 0xbfea8f5c, 0x28f5c28c},	/* 2.5499=f(-0.83)*/
{64, 0,123,__LINE__, 0x400441f5, 0xecbeef57, 0xbfea3d70, 0xa3d70a3a},	/* 2.53221=f(-0.82)*/
{64, 0,123,__LINE__, 0x40041e9d, 0x49ea60f0, 0xbfe9eb85, 0x1eb851e8},	/* 2.51495=f(-0.81)*/
{64, 0,123,__LINE__, 0x4003fc17, 0x6b7a855e, 0xbfe99999, 0x99999996},	/* 2.49809=f(-0.8)*/
{64, 0,123,__LINE__, 0x4003da53, 0xe4683a05, 0xbfe947ae, 0x147ae144},	/* 2.48161=f(-0.79)*/
{63, 0,123,__LINE__, 0x4003b944, 0x37710c9e, 0xbfe8f5c2, 0x8f5c28f2},	/* 2.46546=f(-0.78)*/
{64, 0,123,__LINE__, 0x400398db, 0x88c873c7, 0xbfe8a3d7, 0x0a3d70a0},	/* 2.44964=f(-0.77)*/
{64, 0,123,__LINE__, 0x4003790e, 0x5efbaf81, 0xbfe851eb, 0x851eb84e},	/* 2.43411=f(-0.76)*/
{64, 0,123,__LINE__, 0x400359d2, 0x6f93b6c2, 0xbfe7ffff, 0xfffffffc},	/* 2.41886=f(-0.75)*/
{64, 0,123,__LINE__, 0x40033b1e, 0x74e4d7d4, 0xbfe7ae14, 0x7ae147aa},	/* 2.40387=f(-0.74)*/
{63, 0,123,__LINE__, 0x40031cea, 0x0b1e9472, 0xbfe75c28, 0xf5c28f58},	/* 2.38912=f(-0.73)*/
{64, 0,123,__LINE__, 0x4002ff2d, 0x932437fa, 0xbfe70a3d, 0x70a3d706},	/* 2.3746=f(-0.72)*/
{63, 0,123,__LINE__, 0x4002e1e2, 0x1a0d3a1e, 0xbfe6b851, 0xeb851eb4},	/* 2.36029=f(-0.71)*/
{64, 0,123,__LINE__, 0x4002c501, 0x446cd5f0, 0xbfe66666, 0x66666662},	/* 2.34619=f(-0.7)*/
{64, 0,123,__LINE__, 0x4002a885, 0x3cb097c7, 0xbfe6147a, 0xe147ae10},	/* 2.33229=f(-0.69)*/
{64, 0,123,__LINE__, 0x40028c68, 0xa40a5e8a, 0xbfe5c28f, 0x5c28f5be},	/* 2.31856=f(-0.68)*/
{64, 0,123,__LINE__, 0x400270a6, 0x857678d4, 0xbfe570a3, 0xd70a3d6c},	/* 2.30501=f(-0.67)*/
{64, 0,123,__LINE__, 0x4002553a, 0x4a84548e, 0xbfe51eb8, 0x51eb851a},	/* 2.29162=f(-0.66)*/
{64, 0,123,__LINE__, 0x40023a1f, 0xb1993d6b, 0xbfe4cccc, 0xccccccc8},	/* 2.27838=f(-0.65)*/
{64, 0,123,__LINE__, 0x40021f52, 0xc5720bd9, 0xbfe47ae1, 0x47ae1476},	/* 2.26529=f(-0.64)*/
{64, 0,123,__LINE__, 0x400204cf, 0xd5b34454, 0xbfe428f5, 0xc28f5c24},	/* 2.25235=f(-0.63)*/
{64, 0,123,__LINE__, 0x4001ea93, 0x705fa170, 0xbfe3d70a, 0x3d70a3d2},	/* 2.23954=f(-0.62)*/
{64, 0,123,__LINE__, 0x4001d09a, 0x5c13d2e9, 0xbfe3851e, 0xb851eb80},	/* 2.22686=f(-0.61)*/
{63, 0,123,__LINE__, 0x4001b6e1, 0x92ebbe43, 0xbfe33333, 0x3333332e},	/* 2.2143=f(-0.6)*/
{64, 0,123,__LINE__, 0x40019d66, 0x3dfa08c4, 0xbfe2e147, 0xae147adc},	/* 2.20186=f(-0.59)*/
{64, 0,123,__LINE__, 0x40018425, 0xb13e5c9f, 0xbfe28f5c, 0x28f5c28a},	/* 2.18953=f(-0.58)*/
{64, 0,123,__LINE__, 0x40016b1d, 0x6809deac, 0xbfe23d70, 0xa3d70a38},	/* 2.1773=f(-0.57)*/
{64, 0,123,__LINE__, 0x4001524b, 0x01c3c767, 0xbfe1eb85, 0x1eb851e6},	/* 2.16518=f(-0.56)*/
{64, 0,123,__LINE__, 0x400139ac, 0x3f022346, 0xbfe19999, 0x99999994},	/* 2.15316=f(-0.55)*/
{64, 0,123,__LINE__, 0x4001213e, 0xfeec77b2, 0xbfe147ae, 0x147ae142},	/* 2.14123=f(-0.54)*/
{64, 0,123,__LINE__, 0x40010901, 0x3cdf7bcb, 0xbfe0f5c2, 0x8f5c28f0},	/* 2.1294=f(-0.53)*/
{64, 0,123,__LINE__, 0x4000f0f1, 0x0e4a4af2, 0xbfe0a3d7, 0x0a3d709e},	/* 2.11765=f(-0.52)*/
{63, 0,123,__LINE__, 0x4000d90c, 0xa0be7d99, 0xbfe051eb, 0x851eb84c},	/* 2.10598=f(-0.51)*/
{64, 0,123,__LINE__, 0x4000c152, 0x382d7364, 0xbfdfffff, 0xfffffff4},	/* 2.0944=f(-0.5)*/
{64, 0,123,__LINE__, 0x4000a9c0, 0x2d4dd6d1, 0xbfdf5c28, 0xf5c28f50},	/* 2.08289=f(-0.49)*/
{64, 0,123,__LINE__, 0x40009254, 0xec250417, 0xbfdeb851, 0xeb851eac},	/* 2.07145=f(-0.48)*/
{64, 0,123,__LINE__, 0x40007b0e, 0xf2b0873a, 0xbfde147a, 0xe147ae08},	/* 2.06009=f(-0.47)*/
{64, 0,123,__LINE__, 0x400063ec, 0xcfac5c06, 0xbfdd70a3, 0xd70a3d64},	/* 2.04879=f(-0.46)*/
{64, 0,123,__LINE__, 0x40004ced, 0x21730104, 0xbfdccccc, 0xccccccc0},	/* 2.03756=f(-0.45)*/
{64, 0,123,__LINE__, 0x4000360e, 0x94f4c6c4, 0xbfdc28f5, 0xc28f5c1c},	/* 2.0264=f(-0.44)*/
{64, 0,123,__LINE__, 0x40001f4f, 0xe4c4118e, 0xbfdb851e, 0xb851eb78},	/* 2.01529=f(-0.43)*/
{64, 0,123,__LINE__, 0x400008af, 0xd83485fa, 0xbfdae147, 0xae147ad4},	/* 2.00424=f(-0.42)*/
{64, 0,123,__LINE__, 0x3fffe45a, 0x8516a5c6, 0xbfda3d70, 0xa3d70a30},	/* 1.99325=f(-0.41)*/
{64, 0,123,__LINE__, 0x3fffb78e, 0x047dfba1, 0xbfd99999, 0x9999998c},	/* 1.98231=f(-0.4)*/
{64, 0,123,__LINE__, 0x3fff8af8, 0x008a864f, 0xbfd8f5c2, 0x8f5c28e8},	/* 1.97143=f(-0.39)*/
{64, 0,123,__LINE__, 0x3fff5e96, 0x5edb849c, 0xbfd851eb, 0x851eb844},	/* 1.96059=f(-0.38)*/
{64, 0,123,__LINE__, 0x3fff3267, 0x1790a029, 0xbfd7ae14, 0x7ae147a0},	/* 1.94981=f(-0.37)*/
{64, 0,123,__LINE__, 0x3fff0668, 0x342bcf9e, 0xbfd70a3d, 0x70a3d6fc},	/* 1.93906=f(-0.36)*/
{63, 0,123,__LINE__, 0x3ffeda97, 0xce869c0e, 0xbfd66666, 0x66666658},	/* 1.92837=f(-0.35)*/
{64, 0,123,__LINE__, 0x3ffeaef4, 0x0fd91e82, 0xbfd5c28f, 0x5c28f5b4},	/* 1.91771=f(-0.34)*/
{64, 0,123,__LINE__, 0x3ffe837b, 0x2fd13424, 0xbfd51eb8, 0x51eb8510},	/* 1.9071=f(-0.33)*/
{64, 0,123,__LINE__, 0x3ffe582b, 0x73b88c73, 0xbfd47ae1, 0x47ae146c},	/* 1.89653=f(-0.32)*/
{63, 0,123,__LINE__, 0x3ffe2d03, 0x2da855f4, 0xbfd3d70a, 0x3d70a3c8},	/* 1.88599=f(-0.31)*/
{64, 0,123,__LINE__, 0x3ffe0200, 0xbbc96ad4, 0xbfd33333, 0x33333324},	/* 1.87549=f(-0.3)*/
{64, 0,123,__LINE__, 0x3ffdd722, 0x879ff961, 0xbfd28f5c, 0x28f5c280},	/* 1.86502=f(-0.29)*/
{64, 0,123,__LINE__, 0x3ffdac67, 0x0561bb4b, 0xbfd1eb85, 0x1eb851dc},	/* 1.85459=f(-0.28)*/
{63, 0,123,__LINE__, 0x3ffd81cc, 0xb355e3bf, 0xbfd147ae, 0x147ae138},	/* 1.84419=f(-0.27)*/
{64, 0,123,__LINE__, 0x3ffd5752, 0x193dff00, 0xbfd0a3d7, 0x0a3d7094},	/* 1.83382=f(-0.26)*/
{64, 0,123,__LINE__, 0x3ffd2cf5, 0xc7c70f07, 0xbfcfffff, 0xffffffe0},	/* 1.82348=f(-0.25)*/
{64, 0,123,__LINE__, 0x3ffd02b6, 0x58023fbc, 0xbfceb851, 0xeb851e98},	/* 1.81316=f(-0.24)*/
{64, 0,123,__LINE__, 0x3ffcd892, 0x6ae49ae7, 0xbfcd70a3, 0xd70a3d50},	/* 1.80287=f(-0.23)*/
{64, 0,123,__LINE__, 0x3ffcae88, 0xa8cd304f, 0xbfcc28f5, 0xc28f5c08},	/* 1.79261=f(-0.22)*/
{64, 0,123,__LINE__, 0x3ffc8497, 0xc1113153, 0xbfcae147, 0xae147ac0},	/* 1.78237=f(-0.21)*/
{64, 0,123,__LINE__, 0x3ffc5abe, 0x698d895c, 0xbfc99999, 0x99999978},	/* 1.77215=f(-0.2)*/
{64, 0,123,__LINE__, 0x3ffc30fb, 0x5e3d8564, 0xbfc851eb, 0x851eb830},	/* 1.76196=f(-0.19)*/
{63, 0,123,__LINE__, 0x3ffc074d, 0x60d624f9, 0xbfc70a3d, 0x70a3d6e8},	/* 1.75178=f(-0.18)*/
{64, 0,123,__LINE__, 0x3ffbddb3, 0x3865b650, 0xbfc5c28f, 0x5c28f5a0},	/* 1.74163=f(-0.17)*/
{64, 0,123,__LINE__, 0x3ffbb42b, 0xb0f765c6, 0xbfc47ae1, 0x47ae1458},	/* 1.73149=f(-0.16)*/
{64, 0,123,__LINE__, 0x3ffb8ab5, 0x9b3a6eea, 0xbfc33333, 0x33333310},	/* 1.72136=f(-0.15)*/
{64, 0,123,__LINE__, 0x3ffb614f, 0xcc2ca2bb, 0xbfc1eb85, 0x1eb851c8},	/* 1.71126=f(-0.14)*/
{64, 0,123,__LINE__, 0x3ffb37f9, 0x1cc7fb82, 0xbfc0a3d7, 0x0a3d7080},	/* 1.70117=f(-0.13)*/
{64, 0,123,__LINE__, 0x3ffb0eb0, 0x69b2fb1c, 0xbfbeb851, 0xeb851e71},	/* 1.69109=f(-0.12)*/
{64, 0,123,__LINE__, 0x3ffae574, 0x92f3947b, 0xbfbc28f5, 0xc28f5be2},	/* 1.68102=f(-0.11)*/
{64, 0,123,__LINE__, 0x3ffabc44, 0x7ba4649c, 0xbfb99999, 0x99999953},	/* 1.67096=f(-0.1)*/
{64, 0,123,__LINE__, 0x3ffa931f, 0x09ac0277, 0xbfb70a3d, 0x70a3d6c4},	/* 1.66092=f(-0.09)*/
{63, 0,123,__LINE__, 0x3ffa6a03, 0x2576302d, 0xbfb47ae1, 0x47ae1435},	/* 1.65088=f(-0.08)*/
{63, 0,123,__LINE__, 0x3ffa40ef, 0xb9aeba3d, 0xbfb1eb85, 0x1eb851a6},	/* 1.64085=f(-0.07)*/
{64, 0,123,__LINE__, 0x3ffa17e3, 0xb2fdd3d9, 0xbfaeb851, 0xeb851e2d},	/* 1.63083=f(-0.06)*/
{63, 0,123,__LINE__, 0x3ff9eedd, 0xffc5c147, 0xbfa99999, 0x9999990e},	/* 1.62082=f(-0.05)*/
{63, 0,123,__LINE__, 0x3ff9c5dd, 0x8fe1a2ff, 0xbfa47ae1, 0x47ae13ef},	/* 1.61081=f(-0.04)*/
{64, 0,123,__LINE__, 0x3ff99ce1, 0x546535b4, 0xbf9eb851, 0xeb851da0},	/* 1.6008=f(-0.03)*/
{64, 0,123,__LINE__, 0x3ff973e8, 0x3f5d5c96, 0xbf947ae1, 0x47ae1362},	/* 1.5908=f(-0.02)*/
{64, 0,123,__LINE__, 0x3ff94af1, 0x43914c32, 0xbf847ae1, 0x47ae1249},	/* 1.5808=f(-0.01)*/
{64, 0,123,__LINE__, 0x3ff921fb, 0x54442d14, 0x3cd19000, 0x00000000},	/* 1.5708=f(9.74915e-16)*/
{64, 0,123,__LINE__, 0x3ff8f905, 0x64f70df6, 0x3f847ae1, 0x47ae16ad},	/* 1.5608=f(0.01)*/
{64, 0,123,__LINE__, 0x3ff8d00e, 0x692afd91, 0x3f947ae1, 0x47ae1594},	/* 1.55079=f(0.02)*/
{64, 0,123,__LINE__, 0x3ff8a715, 0x54232474, 0x3f9eb851, 0xeb851fd2},	/* 1.54079=f(0.03)*/
{64, 0,123,__LINE__, 0x3ff87e19, 0x18a6b729, 0x3fa47ae1, 0x47ae1508},	/* 1.53079=f(0.04)*/
{64, 0,123,__LINE__, 0x3ff85518, 0xa8c298e1, 0x3fa99999, 0x99999a27},	/* 1.52078=f(0.05)*/
{63, 0,123,__LINE__, 0x3ff82c12, 0xf58a864f, 0x3faeb851, 0xeb851f46},	/* 1.51076=f(0.06)*/
{64, 0,123,__LINE__, 0x3ff80306, 0xeed99feb, 0x3fb1eb85, 0x1eb85232},	/* 1.50074=f(0.07)*/
{64, 0,123,__LINE__, 0x3ff7d9f3, 0x831229fb, 0x3fb47ae1, 0x47ae14c1},	/* 1.49071=f(0.08)*/
{64, 0,123,__LINE__, 0x3ff7b0d7, 0x9edc57b0, 0x3fb70a3d, 0x70a3d750},	/* 1.48067=f(0.09)*/
{64, 0,123,__LINE__, 0x3ff787b2, 0x2ce3f58c, 0x3fb99999, 0x999999df},	/* 1.47063=f(0.1)*/
{63, 0,123,__LINE__, 0x3ff75e82, 0x1594c5ad, 0x3fbc28f5, 0xc28f5c6e},	/* 1.46057=f(0.11)*/
{64, 0,123,__LINE__, 0x3ff73546, 0x3ed55f0c, 0x3fbeb851, 0xeb851efd},	/* 1.45051=f(0.12)*/
{64, 0,123,__LINE__, 0x3ff70bfd, 0x8bc05ea6, 0x3fc0a3d7, 0x0a3d70c6},	/* 1.44043=f(0.13)*/
{63, 0,123,__LINE__, 0x3ff6e2a6, 0xdc5bb76d, 0x3fc1eb85, 0x1eb8520e},	/* 1.43033=f(0.14)*/
{64, 0,123,__LINE__, 0x3ff6b941, 0x0d4deb3d, 0x3fc33333, 0x33333356},	/* 1.42023=f(0.15)*/
{63, 0,123,__LINE__, 0x3ff68fca, 0xf790f462, 0x3fc47ae1, 0x47ae149e},	/* 1.41011=f(0.16)*/
{64, 0,123,__LINE__, 0x3ff66643, 0x7022a3d8, 0x3fc5c28f, 0x5c28f5e6},	/* 1.39997=f(0.17)*/
{64, 0,123,__LINE__, 0x3ff63ca9, 0x47b2352f, 0x3fc70a3d, 0x70a3d72e},	/* 1.38981=f(0.18)*/
{64, 0,123,__LINE__, 0x3ff612fb, 0x4a4ad4c3, 0x3fc851eb, 0x851eb876},	/* 1.37963=f(0.19)*/
{64, 0,123,__LINE__, 0x3ff5e938, 0x3efad0cc, 0x3fc99999, 0x999999be},	/* 1.36944=f(0.2)*/
{64, 0,123,__LINE__, 0x3ff5bf5e, 0xe77728d4, 0x3fcae147, 0xae147b06},	/* 1.35922=f(0.21)*/
{64, 0,123,__LINE__, 0x3ff5956d, 0xffbb29d8, 0x3fcc28f5, 0xc28f5c4e},	/* 1.34898=f(0.22)*/
{64, 0,123,__LINE__, 0x3ff56b64, 0x3da3bf40, 0x3fcd70a3, 0xd70a3d96},	/* 1.33872=f(0.23)*/
{64, 0,123,__LINE__, 0x3ff54140, 0x50861a6b, 0x3fceb851, 0xeb851ede},	/* 1.32843=f(0.24)*/
{64, 0,123,__LINE__, 0x3ff51700, 0xe0c14b20, 0x3fd00000, 0x00000013},	/* 1.31812=f(0.25)*/
{64, 0,123,__LINE__, 0x3ff4eca4, 0x8f4a5b28, 0x3fd0a3d7, 0x0a3d70b7},	/* 1.30777=f(0.26)*/
{63, 0,123,__LINE__, 0x3ff4c229, 0xf5327669, 0x3fd147ae, 0x147ae15b},	/* 1.2974=f(0.27)*/
{64, 0,123,__LINE__, 0x3ff4978f, 0xa3269edc, 0x3fd1eb85, 0x1eb851ff},	/* 1.287=f(0.28)*/
{64, 0,123,__LINE__, 0x3ff46cd4, 0x20e860c6, 0x3fd28f5c, 0x28f5c2a3},	/* 1.27657=f(0.29)*/
{64, 0,123,__LINE__, 0x3ff441f5, 0xecbeef53, 0x3fd33333, 0x33333347},	/* 1.2661=f(0.3)*/
{64, 0,123,__LINE__, 0x3ff416f3, 0x7ae00434, 0x3fd3d70a, 0x3d70a3eb},	/* 1.2556=f(0.31)*/
{64, 0,123,__LINE__, 0x3ff3ebcb, 0x34cfcdb4, 0x3fd47ae1, 0x47ae148f},	/* 1.24507=f(0.32)*/
{64, 0,123,__LINE__, 0x3ff3c07b, 0x78b72603, 0x3fd51eb8, 0x51eb8533},	/* 1.23449=f(0.33)*/
{63, 0,123,__LINE__, 0x3ff39502, 0x98af3ba5, 0x3fd5c28f, 0x5c28f5d7},	/* 1.22388=f(0.34)*/
{63, 0,123,__LINE__, 0x3ff3695e, 0xda01be1a, 0x3fd66666, 0x6666667b},	/* 1.21323=f(0.35)*/
{64, 0,123,__LINE__, 0x3ff33d8e, 0x745c8a89, 0x3fd70a3d, 0x70a3d71f},	/* 1.20253=f(0.36)*/
{64, 0,123,__LINE__, 0x3ff3118f, 0x90f7b9fe, 0x3fd7ae14, 0x7ae147c3},	/* 1.19179=f(0.37)*/
{64, 0,123,__LINE__, 0x3ff2e560, 0x49acd58b, 0x3fd851eb, 0x851eb867},	/* 1.181=f(0.38)*/
{63, 0,123,__LINE__, 0x3ff2b8fe, 0xa7fdd3d8, 0x3fd8f5c2, 0x8f5c290b},	/* 1.17016=f(0.39)*/
{63, 0,123,__LINE__, 0x3ff28c68, 0xa40a5e86, 0x3fd99999, 0x999999af},	/* 1.15928=f(0.4)*/
{63, 0,123,__LINE__, 0x3ff25f9c, 0x2371b461, 0x3fda3d70, 0xa3d70a53},	/* 1.14834=f(0.41)*/
{64, 0,123,__LINE__, 0x3ff23296, 0xf81f4e32, 0x3fdae147, 0xae147af7},	/* 1.13735=f(0.42)*/
{63, 0,123,__LINE__, 0x3ff20556, 0xdf00370b, 0x3fdb851e, 0xb851eb9b},	/* 1.1263=f(0.43)*/
{64, 0,123,__LINE__, 0x3ff1d7d9, 0x7e9ecca0, 0x3fdc28f5, 0xc28f5c3f},	/* 1.1152=f(0.44)*/
{64, 0,123,__LINE__, 0x3ff1aa1c, 0x65a2581f, 0x3fdccccc, 0xcccccce3},	/* 1.10403=f(0.45)*/
{64, 0,123,__LINE__, 0x3ff17c1d, 0x092fa21a, 0x3fdd70a3, 0xd70a3d87},	/* 1.0928=f(0.46)*/
{64, 0,123,__LINE__, 0x3ff14dd8, 0xc3274bb2, 0x3fde147a, 0xe147ae2b},	/* 1.08151=f(0.47)*/
{64, 0,123,__LINE__, 0x3ff11f4c, 0xd03e51f8, 0x3fdeb851, 0xeb851ecf},	/* 1.07014=f(0.48)*/
{64, 0,123,__LINE__, 0x3ff0f076, 0x4decac84, 0x3fdf5c28, 0xf5c28f73},	/* 1.05871=f(0.49)*/
{64, 0,123,__LINE__, 0x3ff0c152, 0x382d735f, 0x3fe00000, 0x0000000b},	/* 1.0472=f(0.5)*/
{64, 0,123,__LINE__, 0x3ff091dd, 0x670b5ef5, 0x3fe051eb, 0x851eb85d},	/* 1.03561=f(0.51)*/
{64, 0,123,__LINE__, 0x3ff06214, 0x8bf3c442, 0x3fe0a3d7, 0x0a3d70af},	/* 1.02395=f(0.52)*/
{64, 0,123,__LINE__, 0x3ff031f4, 0x2ec96290, 0x3fe0f5c2, 0x8f5c2901},	/* 1.0122=f(0.53)*/
{64, 0,123,__LINE__, 0x3ff00178, 0xaaaf6ac2, 0x3fe147ae, 0x147ae153},	/* 1.00036=f(0.54)*/
{64, 0,123,__LINE__, 0x3fefa13c, 0x55082733, 0x3fe19999, 0x999999a5},	/* 0.988432=f(0.55)*/
{63, 0,123,__LINE__, 0x3fef3ec1, 0x4a0196af, 0x3fe1eb85, 0x1eb851f7},	/* 0.976411=f(0.56)*/
{64, 0,123,__LINE__, 0x3feedb77, 0xb0e9399e, 0x3fe23d70, 0xa3d70a49},	/* 0.96429=f(0.57)*/
{64, 0,123,__LINE__, 0x3fee7756, 0x8c1741d0, 0x3fe28f5c, 0x28f5c29b},	/* 0.952068=f(0.58)*/
{63, 0,123,__LINE__, 0x3fee1254, 0x5928913e, 0x3fe2e147, 0xae147aed},	/* 0.939737=f(0.59)*/
{64, 0,123,__LINE__, 0x3fedac67, 0x0561bb41, 0x3fe33333, 0x3333333f},	/* 0.927295=f(0.6)*/
{64, 0,123,__LINE__, 0x3fed4583, 0xe0c168a7, 0x3fe3851e, 0xb851eb91},	/* 0.914736=f(0.61)*/
{63, 0,123,__LINE__, 0x3fecdd9f, 0x8f922e8a, 0x3fe3d70a, 0x3d70a3e3},	/* 0.902054=f(0.62)*/
{64, 0,123,__LINE__, 0x3fec74ad, 0xfa43a2fd, 0x3fe428f5, 0xc28f5c35},	/* 0.889243=f(0.63)*/
{64, 0,123,__LINE__, 0x3fec0aa2, 0x3b4884e6, 0x3fe47ae1, 0x47ae1487},	/* 0.876298=f(0.64)*/
{63, 0,123,__LINE__, 0x3feb9f6e, 0x8aabbe9d, 0x3fe4cccc, 0xccccccd9},	/* 0.863212=f(0.65)*/
{64, 0,123,__LINE__, 0x3feb3304, 0x26ff6214, 0x3fe51eb8, 0x51eb852b},	/* 0.849978=f(0.66)*/
{64, 0,123,__LINE__, 0x3feac553, 0x3b36d0fa, 0x3fe570a3, 0xd70a3d7d},	/* 0.836588=f(0.67)*/
{64, 0,123,__LINE__, 0x3fea564a, 0xc0e73a22, 0x3fe5c28f, 0x5c28f5cf},	/* 0.823034=f(0.68)*/
{63, 0,123,__LINE__, 0x3fe9e5d8, 0x5e4e552d, 0x3fe6147a, 0xe147ae21},	/* 0.809307=f(0.69)*/
{63, 0,123,__LINE__, 0x3fe973e8, 0x3f5d5c89, 0x3fe66666, 0x66666673},	/* 0.795399=f(0.7)*/
{64, 0,123,__LINE__, 0x3fe90064, 0xe8dbcbd3, 0x3fe6b851, 0xeb851ec5},	/* 0.781298=f(0.71)*/
{64, 0,123,__LINE__, 0x3fe88b37, 0x047fd461, 0x3fe70a3d, 0x70a3d717},	/* 0.766994=f(0.72)*/
{64, 0,123,__LINE__, 0x3fe81445, 0x24966281, 0x3fe75c28, 0xf5c28f69},	/* 0.752474=f(0.73)*/
{64, 0,123,__LINE__, 0x3fe79b73, 0x7d7d54f8, 0x3fe7ae14, 0x7ae147bb},	/* 0.737726=f(0.74)*/
{64, 0,123,__LINE__, 0x3fe720a3, 0x92c1d941, 0x3fe80000, 0x0000000d},	/* 0.722734=f(0.75)*/
{64, 0,123,__LINE__, 0x3fe6a3b3, 0xd521f641, 0x3fe851eb, 0x851eb85f},	/* 0.707483=f(0.76)*/
{63, 0,123,__LINE__, 0x3fe6247f, 0x2deee52a, 0x3fe8a3d7, 0x0a3d70b1},	/* 0.691955=f(0.77)*/
{63, 0,123,__LINE__, 0x3fe5a2dc, 0x734c81cf, 0x3fe8f5c2, 0x8f5c2903},	/* 0.676131=f(0.78)*/
{64, 0,123,__LINE__, 0x3fe51e9d, 0xbf6fcc30, 0x3fe947ae, 0x147ae155},	/* 0.659987=f(0.79)*/
{64, 0,123,__LINE__, 0x3fe4978f, 0xa3269ecb, 0x3fe99999, 0x999999a7},	/* 0.643501=f(0.8)*/
{64, 0,123,__LINE__, 0x3fe40d78, 0x29673085, 0x3fe9eb85, 0x1eb851f9},	/* 0.626644=f(0.81)*/
{63, 0,123,__LINE__, 0x3fe38015, 0x9e14f6e7, 0x3fea3d70, 0xa3d70a4b},	/* 0.609385=f(0.82)*/
{63, 0,123,__LINE__, 0x3fe2ef1d, 0x05145f4c, 0x3fea8f5c, 0x28f5c29d},	/* 0.591689=f(0.83)*/
{64, 0,123,__LINE__, 0x3fe25a38, 0x276a634d, 0x3feae147, 0xae147aef},	/* 0.573513=f(0.84)*/
{63, 0,123,__LINE__, 0x3fe1c103, 0x11437ffa, 0x3feb3333, 0x33333341},	/* 0.554811=f(0.85)*/
{63, 0,123,__LINE__, 0x3fe12308, 0xcb4d54a0, 0x3feb851e, 0xb851eb93},	/* 0.535527=f(0.86)*/
{63, 0,123,__LINE__, 0x3fe07fbf, 0x005ae5e8, 0x3febd70a, 0x3d70a3e5},	/* 0.515594=f(0.87)*/
{64, 0,123,__LINE__, 0x3fdfad00, 0x2f93bde1, 0x3fec28f5, 0xc28f5c37},	/* 0.494934=f(0.88)*/
{63, 0,123,__LINE__, 0x3fde4d06, 0x152f28c0, 0x3fec7ae1, 0x47ae1489},	/* 0.473451=f(0.89)*/
{64, 0,123,__LINE__, 0x3fdcdd9f, 0x8f922e58, 0x3feccccc, 0xccccccdb},	/* 0.451027=f(0.9)*/
{64, 0,123,__LINE__, 0x3fdb5c5c, 0x6724eef9, 0x3fed1eb8, 0x51eb852d},	/* 0.427512=f(0.91)*/
{64, 0,123,__LINE__, 0x3fd9c618, 0xaa4ae1f4, 0x3fed70a3, 0xd70a3d7f},	/* 0.402716=f(0.92)*/
{64, 0,123,__LINE__, 0x3fd816aa, 0xbed3ca3c, 0x3fedc28f, 0x5c28f5d1},	/* 0.376383=f(0.93)*/
{64, 0,123,__LINE__, 0x3fd6485a, 0x22bc87c6, 0x3fee147a, 0xe147ae23},	/* 0.348166=f(0.94)*/
{63, 0,123,__LINE__, 0x3fd452e8, 0xfa93e3dc, 0x3fee6666, 0x66666675},	/* 0.31756=f(0.95)*/
{63, 0,123,__LINE__, 0x3fd229ae, 0xc4763874, 0x3feeb851, 0xeb851ec7},	/* 0.283794=f(0.96)*/
{63, 0,123,__LINE__, 0x3fcf6eb0, 0xdd60718e, 0x3fef0a3d, 0x70a3d719},	/* 0.245566=f(0.97)*/
{63, 0,123,__LINE__, 0x3fc9a492, 0x76037759, 0x3fef5c28, 0xf5c28f6b},	/* 0.200335=f(0.98)*/
{64, 0,123,__LINE__, 0x3fc21df7, 0x2882be2e, 0x3fefae14, 0x7ae147bd},	/* 0.141539=f(0.99)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff00000, 0x00000007},	/* nan=f(1)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff028f5, 0xc28f5c30},	/* nan=f(1.01)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff051eb, 0x851eb859},	/* nan=f(1.02)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff07ae1, 0x47ae1482},	/* nan=f(1.03)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff0a3d7, 0x0a3d70ab},	/* nan=f(1.04)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff0cccc, 0xccccccd4},	/* nan=f(1.05)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff0f5c2, 0x8f5c28fd},	/* nan=f(1.06)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff11eb8, 0x51eb8526},	/* nan=f(1.07)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff147ae, 0x147ae14f},	/* nan=f(1.08)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff170a3, 0xd70a3d78},	/* nan=f(1.09)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff19999, 0x999999a1},	/* nan=f(1.1)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff1c28f, 0x5c28f5ca},	/* nan=f(1.11)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff1eb85, 0x1eb851f3},	/* nan=f(1.12)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff2147a, 0xe147ae1c},	/* nan=f(1.13)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff23d70, 0xa3d70a45},	/* nan=f(1.14)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff26666, 0x6666666e},	/* nan=f(1.15)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff28f5c, 0x28f5c297},	/* nan=f(1.16)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff2b851, 0xeb851ec0},	/* nan=f(1.17)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff2e147, 0xae147ae9},	/* nan=f(1.18)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff30a3d, 0x70a3d712},	/* nan=f(1.19)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc01921fb, 0x54442d18},	/* nan=f(-6.28319)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc012d97c, 0x7f3321d2},	/* nan=f(-4.71239)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc00921fb, 0x54442d18},	/* nan=f(-3.14159)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff921fb, 0x54442d18},	/* nan=f(-1.5708)*/
{64, 0,123,__LINE__, 0x3ff921fb, 0x54442d18, 0x00000000, 0x00000000},	/* 1.5708=f(0)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x3ff921fb, 0x54442d18},	/* nan=f(1.5708)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x400921fb, 0x54442d18},	/* nan=f(3.14159)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x4012d97c, 0x7f3321d2},	/* nan=f(4.71239)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc03e0000, 0x00000000},	/* nan=f(-30)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc03c4ccc, 0xcccccccd},	/* nan=f(-28.3)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc03a9999, 0x9999999a},	/* nan=f(-26.6)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc038e666, 0x66666667},	/* nan=f(-24.9)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0373333, 0x33333334},	/* nan=f(-23.2)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0358000, 0x00000001},	/* nan=f(-21.5)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc033cccc, 0xccccccce},	/* nan=f(-19.8)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0321999, 0x9999999b},	/* nan=f(-18.1)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0306666, 0x66666668},	/* nan=f(-16.4)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc02d6666, 0x6666666a},	/* nan=f(-14.7)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc02a0000, 0x00000004},	/* nan=f(-13)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0269999, 0x9999999e},	/* nan=f(-11.3)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0233333, 0x33333338},	/* nan=f(-9.6)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc01f9999, 0x999999a3},	/* nan=f(-7.9)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc018cccc, 0xccccccd6},	/* nan=f(-6.2)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0120000, 0x00000009},	/* nan=f(-4.5)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xc0066666, 0x66666678},	/* nan=f(-2.8)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0xbff19999, 0x999999bd},	/* nan=f(-1.1)*/
{63, 0,123,__LINE__, 0x3fedac67, 0x0561bba8, 0x3fe33333, 0x333332ec},	/* 0.927295=f(0.6)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x40026666, 0x66666654},	/* nan=f(2.3)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x400fffff, 0xffffffee},	/* nan=f(4)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x4016cccc, 0xccccccc4},	/* nan=f(5.7)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x401d9999, 0x99999991},	/* nan=f(7.4)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x40223333, 0x3333332f},	/* nan=f(9.1)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x40259999, 0x99999995},	/* nan=f(10.8)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x4028ffff, 0xfffffffb},	/* nan=f(12.5)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x402c6666, 0x66666661},	/* nan=f(14.2)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x402fcccc, 0xccccccc7},	/* nan=f(15.9)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x40319999, 0x99999997},	/* nan=f(17.6)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x40334ccc, 0xccccccca},	/* nan=f(19.3)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x4034ffff, 0xfffffffd},	/* nan=f(21)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x4036b333, 0x33333330},	/* nan=f(22.7)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x40386666, 0x66666663},	/* nan=f(24.4)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x403a1999, 0x99999996},	/* nan=f(26.1)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x403bcccc, 0xccccccc9},	/* nan=f(27.8)*/
{64, 0, 33,__LINE__, 0x7ff80000, 0x00000000, 0x403d7fff, 0xfffffffc},	/* nan=f(29.5)*/
{0}
};
void test_acos(int m)   {run_vector_1(m,acos_vec,(char *)(acos),"acos","dd");   }	
