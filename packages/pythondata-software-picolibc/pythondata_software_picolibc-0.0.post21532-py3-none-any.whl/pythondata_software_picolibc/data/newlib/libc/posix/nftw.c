/*
* Copyright © 2005-2020 Rich Felker, et al.
*
* Permission is hereby granted, free of charge, to any person obtaining
* a copy of this software and associated documentation files (the
* "Software"), to deal in the Software without restriction, including
* without limitation the rights to use, copy, modify, merge, publish,
* distribute, sublicense, and/or sell copies of the Software, and to
* permit persons to whom the Software is furnished to do so, subject to
* the following conditions:
*
* The above copyright notice and this permission notice shall be
* included in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
* IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
* CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
* TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
* SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <ftw.h>
#include <dirent.h>
#include <sys/stat.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <pthread.h>
/* Pull in _STDIO_WITH_THREAD_CANCELLATION_SUPPORT */
#include "../stdio/local.h"

struct history
{
	struct history *chain;
	dev_t dev;
	ino_t ino;
	int level;
	int base;
};

#undef dirfd
#define dirfd(d) (*(int *)d)

static int do_nftw(char *path, int (*fn)(const char *, const struct stat *, int, struct FTW *), int fd_limit, int flags, struct history *h)
{
	size_t l = strlen(path), j = l && path[l-1]=='/' ? l-1 : l;
	struct stat st;
	struct history new;
	int type;
	int r;
	struct FTW lev;

	if ((flags & FTW_PHYS) ? lstat(path, &st) : stat(path, &st) < 0) {
		if (!(flags & FTW_PHYS) && errno==ENOENT && !lstat(path, &st))
			type = FTW_SLN;
		else if (errno != EACCES) return -1;
		else type = FTW_NS;
	} else if (S_ISDIR(st.st_mode)) {
		if (access(path, R_OK) < 0) type = FTW_DNR;
		else if (flags & FTW_DEPTH) type = FTW_DP;
		else type = FTW_D;
	} else if (S_ISLNK(st.st_mode)) {
		if (flags & FTW_PHYS) type = FTW_SL;
		else type = FTW_SLN;
	} else {
		type = FTW_F;
	}

	if ((flags & FTW_MOUNT) && h && st.st_dev != h->dev)
		return 0;
	
	new.chain = h;
	new.dev = st.st_dev;
	new.ino = st.st_ino;
	new.level = h ? h->level+1 : 0;
	new.base = j+1;
	
	lev.level = new.level;
	if (h) {
		lev.base = h->base;
	} else {
		size_t k;
		for (k=j; k && path[k]=='/'; k--);
		for (; k && path[k-1]!='/'; k--);
		lev.base = k;
	}

	if (!(flags & FTW_DEPTH) && (r=fn(path, &st, type, &lev)))
		return r;

	for (; h; h = h->chain)
		if (h->dev == st.st_dev && h->ino == st.st_ino)
			return 0;

	if ((type == FTW_D || type == FTW_DP) && fd_limit) {
		DIR *d = opendir(path);
		if (d) {
			struct dirent *de;
			while ((de = readdir(d))) {
				if (de->d_name[0] == '.'
				 && (!de->d_name[1]
				  || (de->d_name[1]=='.'
				   && !de->d_name[2]))) continue;
				if (strlen(de->d_name) >= PATH_MAX-l) {
					errno = ENAMETOOLONG;
					closedir(d);
					return -1;
				}
				path[j]='/';
				strcpy(path+j+1, de->d_name);
				if ((r=do_nftw(path, fn, fd_limit-1, flags, &new))) {
					closedir(d);
					return r;
				}
			}
			closedir(d);
		} else if (errno != EACCES) {
			return -1;
		}
	}

	path[l] = 0;
	if ((flags & FTW_DEPTH) && (r=fn(path, &st, type, &lev)))
		return r;

	return 0;
}

int nftw(const char *path, int (*fn)(const char *, const struct stat *, int, struct FTW *), int fd_limit, int flags)
{
	int r, cs;
	size_t l;
	char pathbuf[PATH_MAX+1];

	if (fd_limit <= 0) return 0;

	l = strlen(path);
	if (l > PATH_MAX) {
		errno = ENAMETOOLONG;
		return -1;
	}
	memcpy(pathbuf, path, l+1);

#ifdef _STDIO_WITH_THREAD_CANCELLATION_SUPPORT
	pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &cs);
#endif
	r = do_nftw(pathbuf, fn, fd_limit, flags, NULL);
#ifdef _STDIO_WITH_THREAD_CANCELLATION_SUPPORT
	pthread_setcancelstate(cs, 0);
#endif
	return r;
}

