/*
 * CXSPARSE: a Concise Sparse Matrix package - Extended.
 * Copyright (c) 2006-2009, Timothy A. Davis.
 * http://www.cise.ufl.edu/research/sparse/CXSparse
 * 
 * CXSparse is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 * 
 * CXSparse is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public
 * License along with this Module; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include "cs.h"
/* x=A\b where A is unsymmetric; b overwritten with solution */
CS_INT cs_lusol (CS_INT order, const cs *A, CS_ENTRY *b, double tol)
{
    CS_ENTRY *x ;
    css *S ;
    csn *N ;
    CS_INT n, ok ;
    if (!CS_CSC (A) || !b) return (0) ;     /* check inputs */
    n = A->n ;
    S = cs_sqr (order, A, 0) ;              /* ordering and symbolic analysis */
    N = cs_lu (A, S, tol) ;                 /* numeric LU factorization */
    x = cs_malloc (n, sizeof (CS_ENTRY)) ;    /* get workspace */
    ok = (S && N && x) ;
    if (ok)
    {
        cs_ipvec (N->pinv, b, x, n) ;       /* x = b(p) */
        cs_lsolve (N->L, x) ;               /* x = L\x */
        cs_usolve (N->U, x) ;               /* x = U\x */
        cs_ipvec (S->q, x, b, n) ;          /* b(q) = x */
    }
    cs_free (x) ;
    cs_sfree (S) ;
    cs_nfree (N) ;
    return (ok) ;
}
