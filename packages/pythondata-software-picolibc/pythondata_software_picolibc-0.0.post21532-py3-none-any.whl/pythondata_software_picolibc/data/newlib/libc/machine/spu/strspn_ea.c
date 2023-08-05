/*
(C) Copyright IBM Corp. 2007, 2008

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of IBM nor the names of its contributors may be
used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

*/

#include <stddef.h>
#include "ea_internal.h"
#include <ea.h>
#include <string.h>
#include <spu_cache.h>

COMPAT_EA_ALIAS (strspn_ea);

size_ea_t
strspn_ea (__ea const char *s, const char *accept)
{
  __ea void *curr_s = (__ea void *) s;
  char *local_s;
  size_ea_t length_of_string = 0;
  size_ea_t s_len;
  int i;

  s_len = strlen_ea (s);

  for (i = 0; i < s_len; i++)
    {
      local_s = (char *) __cache_fetch (curr_s);
      if (!strchr (accept, local_s[0]))
	{
	  return length_of_string;
	}
      else
	{
	  length_of_string++;
	  curr_s++;
	}
    }
  return length_of_string;
}
