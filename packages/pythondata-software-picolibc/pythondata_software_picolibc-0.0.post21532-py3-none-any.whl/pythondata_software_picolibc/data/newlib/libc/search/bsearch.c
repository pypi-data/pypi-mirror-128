/*
Copyright (c) 1991, 1993, 1994
The Regents of the University of California.  All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. Neither the name of the University nor the names of its contributors
may be used to endorse or promote products derived from this software
without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
 */
/*
 * bsearch.c
 * Original Author:	G. Haley
 * Rewritten by:	G. Noer
 *
 * Searches an array of nmemb members, the initial member of which is pointed
 * to by base, for a member that matches the object pointed to by key. The
 * contents of the array shall be in ascending order according to a comparison
 * function pointed to by compar. The function shall return an integer less
 * than, equal to or greater than zero if the first argument is considered to be
 * respectively less than, equal to or greater than the second. Returns a
 * pointer to the matching member of the array, or a null pointer if no match
 * is found.
 */

/*
FUNCTION
<<bsearch>>---binary search

INDEX
	bsearch

SYNOPSIS
	#include <stdlib.h>
	void *bsearch(const void *<[key]>, const void *<[base]>,
		size_t <[nmemb]>, size_t <[size]>,
		int (*<[compar]>)(const void *, const void *));

DESCRIPTION
<<bsearch>> searches an array beginning at <[base]> for any element
that matches <[key]>, using binary search.  <[nmemb]> is the element
count of the array; <[size]> is the size of each element.

The array must be sorted in ascending order with respect to the
comparison function <[compar]> (which you supply as the last argument of
<<bsearch>>).

You must define the comparison function <<(*<[compar]>)>> to have two
arguments; its result must be negative if the first argument is
less than the second, zero if the two arguments match, and
positive if the first argument is greater than the second (where
``less than'' and ``greater than'' refer to whatever arbitrary
ordering is appropriate).

RETURNS
Returns a pointer to an element of <[array]> that matches <[key]>.  If
more than one matching element is available, the result may point to
any of them.

PORTABILITY
<<bsearch>> is ANSI.

No supporting OS subroutines are required.
*/

#include <stdlib.h>

void *
bsearch (const void *key,
	const void *base,
	size_t nmemb,
	size_t size,
	int (*compar) (const void *, const void *))
{
  void *current;
  size_t lower = 0;
  size_t upper = nmemb;
  size_t index;
  int result;

  if (nmemb == 0 || size == 0)
    return NULL;

  while (lower < upper)
    {
      index = (lower + upper) / 2;
      current = (void *) (((char *) base) + (index * size));

      result = compar (key, current);

      if (result < 0)
        upper = index;
      else if (result > 0)
        lower = index + 1;
      else
	return current;
    }

  return NULL;
}

