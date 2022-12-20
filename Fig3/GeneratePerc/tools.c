#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <time.h>
#include <string.h>

#include "tools.h"

// fill the 2D symmetric grid, nn is supposed to have the right size
void boundaries(int* nn,int L){

    int N=L*L;

    for (int i=0; i<N; i++) {
        nn[4*i] = (i+1)%N;//droite
        nn[4*i+1]= (i+L)%N; //bas
        nn[4*i+2]= (i+N-1)%N;//gauche
        nn[4*i+3] = (i+N-L)%N;//haut
        if (i%L==0)
            nn[4*i+2] = i+L-1;
        if ((i+1)%L==0)
            nn[4*i] = i-L+1;
    }
    //printf("boundaries built nicely\n");
}

//second version, more readable, maybe less elegant, not sure
void boundaries2(int* nn,int L){

    int N=L*L;
    //printf("N : %d\n",N);


    for (int i=0; i<N; i++) {
        nn[4*i] = (i+1);//droite
        nn[4*i+1]= (i+L); //bas
        nn[4*i+2]= (i-1);//gauche
        nn[4*i+3] = (i-L);//haut
    }

    //correct on the sides of the square
    for (int i=0; i<N; i+=L) {
        nn[4*i+2] = (i+L-1);//gauche
    }
    for (int i=L-1; i<N; i+=L) {
        nn[4*i] = (i-L+1);//droite
    }
    for (int i=0; i<L; i++) {
        nn[4*i+3] = (N-L+i);//haut
    }
    for (int i=N-L; i<N; i++) {
        nn[4*i+1] = (i-(N-L));//bas
    }
    //printf("boundaries built nicely\n");
}

void permutation(int shuffle, int* order,int len,gsl_rng* rng){
    int j;
    int temp;

    for (int i=0; i<len; i++)
        order[i] = i;

    //realise juste une permutation de order
    if (shuffle==1){
        for (int i=0; i<len; i++) {
            j = i + gsl_rng_uniform_int(rng, len-i);
            temp = order[i];
            order[i] = order[j];
            order[j] = temp;
        }
    }
    //printf("permutation built nicely\n");
}

void delete_bonds(int* bonds,int L, int M, int* nn,gsl_rng* rng){
    int N=L*L;
    int p1;
    int p2;
    permutation(1,bonds,2*N,rng);
    for(int i=0;i<M;i++){ //on selectionne les M premiers liens
        p2=bonds[i]%2;
        p1=bonds[i]/2;
        //printf("intial : p1 : %i, p2 : %i\n",p1,p2);
        if(p2==0){ //cas ou c'est le site "de droite""
            if ((p1+1)%L==0) p2=p1-L+1;
            else p2=p1+1;
            nn[4*p1]=p1;
            nn[4*p2+2]=p2;
        }
        else{ //cas ou c'est le site "du bas""
            if (p1/L==(L-1)) p2=(p1+L)%N;
            else p2=p1+L;
            nn[4*p1+1]=p1;
            nn[4*p2+3]=p2;
        }
        //printf("transformed : p1 : %i, p2 : %i\n",p1,p2);
    }
    //printf("bonds deleted nicely\n");
}

int findroot(int* ptr,int i)
{
    if (ptr[i]<0) return i;
    return ptr[i] = findroot(ptr,ptr[i]);
}

void percolate(int* nn,int* order,int* ptr,int L)
{
    int i,j;
    int s1,s2;
    int r1,r2;
    //big represente la taille du plus gros cluster
    int big=0;
    int N=L*L;
    int EMPTY=-N-1;

    for (i=0; i<N; i++) ptr[i] = EMPTY;
    for (i=0; i<N; i++) {
        r1 = s1 = order[i];
        ptr[s1] = -1;
        for (j=0; j<4; j++) { //examine all neighbors
            s2 = nn[4*s1+j];
            if (ptr[s2]!=EMPTY && s2!=s1) {//le node a deja été visité
                r2 = findroot(ptr,s2);//find root of node 2
                //printf("finding root : %i\n",r2);
                if (r2!=r1) {
                    if (ptr[r1]>ptr[r2]){
                        ptr[r2] += ptr[r1];
                        ptr[r1] = r2;
                        r1 = r2;
                    }
                    else {
                        ptr[r1] += ptr[r2];
                        ptr[r2] = r1;
                    }
                    if (-ptr[r1]>big) big = -ptr[r1];
                }
            }
        }
        //printf("%i %i\n",i+1,big);
    }
    int k;
    int a;
    //printf("in here\n");
    //for (k=0; k<N; k++)  printf("%i ",ptr[k]);
    //printf("\n");
    for (k=0; k<N; k++) {
        a=findroot(ptr,k);
    }
    //for (k=0; k<N; k++)  printf("%i ",ptr[k]);
    //printf("\n");
    //printf("percolation done nicely\n");
}

void find_cluster(int* ptr, int* nn,int L,int* order){
    int N=L*L;
    int max=0;
    int i=0;
    int maxindex;
    int relabel=0;

    //prepare order cluster
    for(i=0;i<N;i++){
        order[i]=-1;
    }

    //find index of max cluster
    for(i=0;i<N;i++){
        if (ptr[i]<max){
            max=ptr[i];
            maxindex=i;
        }
    }

    printf("biggest cluster size : %i\n",-max);
    printf("nodes in cluster : \n");
    printf("\n");
    printf("%i : ",maxindex);
    for(i=0;i<4;i++){
        if (nn[4*maxindex+i]!=maxindex) printf("%i ",nn[maxindex*4+i]);
    }
    order[maxindex]=relabel; //first assignation
    relabel+=1;
    printf("\n");
    for(i=0;i<N;i++){
        if (ptr[i]==maxindex){
            printf("%i : ",i);
            for(int l=0;l<4;l++){
                if (nn[4*i+l]!=i) printf("%i ",nn[i*4+l]);
            }
            printf("\n");
            order[i]=relabel;
            relabel+=1;
        }
    }
    printf("\n");

   // for(i=0;i<N;i++){
   //     printf("%i ",order[i]);
   // }
    printf("\n");

    printf("Relabeled graph\n");
    printf("nodes in cluster : \n");
    printf("\n");
    printf("%i : ",order[maxindex]);
    for(i=0;i<4;i++){
        if (nn[4*maxindex+i]!=maxindex) printf("%i ",order[nn[maxindex*4+i]]);
    }
    printf("\n");
    for(i=0;i<N;i++){
        if (ptr[i]==maxindex){
            printf("%i : ",order[i]);
            for(int l=0;l<4;l++){
                if (nn[4*i+l]!=i) printf("%i ",order[nn[i*4+l]]);
            }
            printf("\n");
        }
    }
    printf("\n");
}


void write_graph_to_file(int* ptr, int* nn,int L,int* order,FILE* file){
    int N=L*L;
    int max=0;
    int i=0;
    int maxindex;
    int relabel=0;

    //prepare order cluster
    for(i=0;i<N;i++){
        order[i]=-1;
    }

    //find index of max cluster
    for(i=0;i<N;i++){
        if (ptr[i]<max){
            max=ptr[i];
            maxindex=i;
        }
    }

    printf("biggest cluster size : %i\n",-max);
    printf("nodes in cluster : \n");
    printf("\n");
    printf("%i : ",maxindex);
    for(i=0;i<4;i++){
        if (nn[4*maxindex+i]!=maxindex) printf("%i ",nn[maxindex*4+i]);
    }
    order[maxindex]=relabel; //first assignation
    relabel+=1;
    printf("\n");
    for(i=0;i<N;i++){
        if (ptr[i]==maxindex){ //node is in the cluster
            printf("%i : ",i);
            for(int l=0;l<4;l++){
                if (nn[4*i+l]!=i) printf("%i ",nn[i*4+l]);
            }
            printf("\n");
            order[i]=relabel;
            relabel+=1;
        }
    }
    printf("\n");

    //printf("Relabeled graph\n");
    //printf("nodes in cluster : \n");
    //printf("\n");
    //printf("%i : ",order[maxindex]);
    for(i=0;i<4;i++){
        if (nn[4*maxindex+i]!=maxindex) fprintf(file,"%i ",order[nn[maxindex*4+i]]);
    }
    fprintf(file,"\n");
    for(i=0;i<N;i++){
        if (ptr[i]==maxindex){
            //printf("%i : ",order[i]);
            for(int l=0;l<4;l++){
                if (nn[4*i+l]!=i) fprintf(file,"%i ",order[nn[i*4+l]]);
            }
            fprintf(file,"\n"); //on doit enlever l'espace vide ici
        }
    }
    //printf("\n");
}

void write_graph_to_file_silent(int* ptr, int* nn,int L,int* order,FILE* file){
    int N=L*L;
    int max=0;
    int i=0;
    int maxindex;
    int relabel=0;

    //prepare order cluster
    for(i=0;i<N;i++){
        order[i]=-1;
    }

    //find index of max cluster
    for(i=0;i<N;i++){
        if (ptr[i]<max){
            max=ptr[i];
            maxindex=i;
        }
    }

    order[maxindex]=relabel; //first assignation
    relabel+=1;
    for(i=0;i<N;i++){
        if (ptr[i]==maxindex){ //node is in the cluster
            for(int l=0;l<4;l++){
            }
            order[i]=relabel;
            relabel+=1;
        }
    }
    for(i=0;i<4;i++){
        if (nn[4*maxindex+i]!=maxindex) fprintf(file,"%i ",order[nn[maxindex*4+i]]);
    }
    fprintf(file,"\n");
    for(i=0;i<N;i++){
        if (ptr[i]==maxindex){
            //printf("%i : ",order[i]);
            for(int l=0;l<4;l++){
                if (nn[4*i+l]!=i) fprintf(file,"%i ",order[nn[i*4+l]]);
            }
            fprintf(file,"\n"); //on doit enlever l'espace vide ici
        }
    }
    //printf("\n");
}

void fill_array(int* pos, char* filename){

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char *ptr=NULL;
    int i;
    int j=0;

    fp = fopen(filename, "r");
    if (fp == NULL){
        printf("failed miserably");
        exit(EXIT_FAILURE);
    }
    while ((read = getline(&line, &len, fp)) != -1) {

        char delim[] = " ";
        ptr = strtok(line, delim);

        while(ptr != NULL){
            i=atoi(ptr);
            pos[j]=i;
            j+=1;
            ptr = strtok(NULL, delim);
        }
    }

    fclose(fp);
    if (line)
        free(line);
}

void drop_array(int* matrix,int matsize, char* filename){

    FILE * fp;
    int i;
    int j;

    fp = fopen(filename, "w");
    if (fp == NULL){
        printf("failed miserably");
        exit(EXIT_FAILURE);
    }
    for(i=0;i<matsize;i++){
        for(j=0;j<matsize-1;j++){
            fprintf(fp,"%d ",matrix[matsize*i+j]);
        }
        fprintf(fp,"%d\n",matrix[matsize*i+j]);
    }
    fclose(fp);
}

