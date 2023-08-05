/*
Copyright (c) 1990 Regents of the University of California.
All rights reserved.
 */
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>
#include <math.h>
#ifndef CYGNUS_NEC
#include <ctype.h>
#endif

#define Ise(c)		((c == 'e') || (c == 'E') || (c == 'd') || (c == 'D'))
#define Isdigit(c)	((c <= '9') && (c >= '0'))
#define Isspace(c)	((c == ' ') || (c == '\t') || (c=='\n') || (c=='\v') \
                         || (c == '\r') || (c == '\f'))
#define Issign(c)	((c == '-') || (c == '+'))
#define Val(c)		((c - '0'))

#define MAXE  308
#define MINE  (-308)

/* flags */
#define SIGN	0x01
#define ESIGN	0x02
#define DECP	0x04
