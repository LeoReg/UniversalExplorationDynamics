#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <time.h>

#include "tools.h"

int main(int argc, char **argv){

    if (argc!=5){
        printf("Not enough/too many arguments, arguments should be size_of_side nb_bonds seed output_file");
        exit(EXIT_FAILURE);
    }
    //printf("jusque ici tout va bien\n");

    int L = atoi(argv[1]); //Linear dimension of the initial lattice
    int M = atoi(argv[2]); //number of bonds to remove
    int seed=atoi(argv[3]);
    char* filename=argv[4]; //file for outputting the generated graph
    //printf("output filename : %s\n",filename);

    int N=L*L;

    //beware here to use dynamic allloc because stack size is too small to store all these lil guys
    int *ptr=(int *) malloc(sizeof(int)*N);

    int *nn=(int *) malloc(sizeof(int)*4*N);

    int *order=(int *) malloc(sizeof(int)*N);

    int *bonds=(int *) malloc(sizeof(int)*2*N);


    seed+=time(NULL);
    gsl_rng* rng = gsl_rng_alloc(gsl_rng_mt19937);
    gsl_rng_set(rng,seed);

    //initiating boundaries
    boundaries2(nn,L);

    // permutes the order the nodes will be considered in
    permutation(0,order,N,rng);

    //delete bonds
    delete_bonds(bonds,L,M,nn,rng);

    // percolate on the generated lattice --> we are modifying the arrays in place here
    percolate(nn,order,ptr,L);

    //write it to output file

	FILE* f_output=NULL;
	f_output = fopen(filename,"w");
	if((f_output!=NULL)){

        write_graph_to_file_silent(ptr, nn,L,order,f_output);
        fclose(f_output);
    }

    // free all arrays
    gsl_rng_free(rng);
    free(nn);
    free(order);
    free(bonds);
    free(ptr);

    return 0;

}
