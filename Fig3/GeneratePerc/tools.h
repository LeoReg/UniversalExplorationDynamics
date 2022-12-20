#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>

// fill the 2D symmetric grid
void boundaries(int* nn,int L);

void boundaries2(int* nn,int L);

// cree un tableau permuté de 0 à len
void permutation(int shuffle, int* order,int len,gsl_rng* rng);

// enleve M bonds de la grille 2D symmetrique au hasard
void delete_bonds(int* bonds,int L, int M, int* nn,gsl_rng* rng);

// trouve la racine du node i
int findroot(int* ptr,int i);

// Performe l'algorithme de percolation et modifier les tableaux en place
void percolate(int* nn,int* order,int* ptr,int L);

// renvoie le nouveau graphe créé après la percolation
void find_cluster(int* ptr, int* nn,int L,int* order);

// writes the relabeled graph to FILE* file
void write_graph_to_file(int* ptr, int* nn,int L,int* order,FILE* file);

void write_graph_to_file_silent(int* ptr, int* nn,int L,int* order,FILE* file);

void fill_array(int* pos, char* filename);

void drop_array(int* matrix,int matsize, char* filename);
