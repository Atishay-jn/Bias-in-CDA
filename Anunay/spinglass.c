/* -*- mode: C -*-  */
/* vim:set ts=4 sts=4 sw=4 et: */
/*
   IGraph library.
   Copyright (C) 2006-2012  Gabor Csardi <csardi.gabor@gmail.com>
   334 Harvard street, Cambridge, MA 02139 USA

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc.,  51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301 USA

*/

#include <igraph.h>

void show_results(igraph_t *g, igraph_vector_t *membership, igraph_matrix_t *memberships, igraph_vector_t *modularity, FILE* f) {
    long int i, j, no_of_nodes = igraph_vcount(g);

    j = igraph_vector_which_max(modularity);
    for (i = 0; i < igraph_vector_size(membership); i++) {
        if (VECTOR(*membership)[i] != MATRIX(*memberships, j, i)) {
            // fprintf(f, "WARNING: best membership vector element %li does not match the best one in the membership matrix\n", i);
        }
    }

    // fprintf(f, "Modularities:\n");
    // igraph_vector_print(modularity);

    for (i = 0; i < igraph_matrix_nrow(memberships); i++) {
        for (j = 0; j < no_of_nodes; j++) {
            fprintf(f, "%ld ", (long int)MATRIX(*memberships, i, j));
        }
        fprintf(f, "\n");
    }

    // fprintf(f, "\n");
}

int main() {

    igraph_t g;
    igraph_vector_t modularity, membership, edges;
    igraph_matrix_t memberships;
    int i, j, k;

    igraph_vector_init(&modularity, 0);
    igraph_vector_init(&membership, 0);
    igraph_matrix_init(&memberships, 0, 0);

    /* Unweighted test graph from the paper of Blondel et al */
    igraph_vector_init(&edges, 0);

    int num_vert,edges1;
    double gamma;
    scanf("%d %d %lf",&num_vert,&edges1,&gamma);
    int u,v;
    for (int i = 0; i < edges1; ++i)
    {
        scanf("%d %d",&u,&v);
        igraph_vector_push_back(&edges, u);
        igraph_vector_push_back(&edges, v);
        
    }

    igraph_create(&g, &edges, num_vert, 0);
    igraph_community_multilevel(&g, 0, &membership, &memberships, &modularity,gamma);
    show_results(&g, &membership, &memberships, &modularity, stdout);
    igraph_destroy(&g);

    igraph_vector_destroy(&modularity);
    igraph_vector_destroy(&membership);
    igraph_vector_destroy(&edges);
    igraph_matrix_destroy(&memberships);

    return 0;
}
