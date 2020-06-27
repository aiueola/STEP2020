#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

double get_time()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + tv.tv_usec * 1e-6;
}

int main(int argc, char** argv)
{
  if (argc != 2) {
    printf("usage: %s N\n", argv[0]);
    return -1;
  }

  int n = atoi(argv[1]);
  double* a = (double*)malloc(n * n * sizeof(double)); // Matrix A
  double* b = (double*)malloc(n * n * sizeof(double)); // Matrix B
  double* c = (double*)malloc(n * n * sizeof(double)); // Matrix C

  // Initialize the matrices to some values.
  int i, j, k;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      a[i * n + j] = i * n + j; // A[i][j]
      b[i * n + j] = j * n + i; // B[i][j]
      c[i * n + j] = 0; // C[i][j]
    }
  }

  double begin = get_time();

  /**************************************/
  /* Write code to calculate C = A * B. */
  /* i-j-k */
  for (i = 0; i < n; i++) {
      for (j = 0; j < n; j++) {
          for (k = 0; k < n; k++) {
              c[i * n + j] += a[i * n + k] * b[k * n + j];
          }
      }
  }
  double ijk_time = get_time();
  
  for (i = 0; i < n; i++) {
      for (k = 0; k < n; k++) {
          for (j = 0; j < n; j++) {
              c[i * n + j] += a[i * n + k] * b[k * n + j];
          }
      }
  }
  double ikj_time = get_time();
 
  for (j = 0; j < n; j++) {
      for (i = 0; i < n; i++) {
          for (k = 0; k < n; k++) {
              c[i * n + j] += a[i * n + k] * b[k * n + j];
          }
      }
  }
  double jik_time = get_time();
 
  for (j = 0; j < n; j++) {
      for (k = 0; k < n; k++) {
          for (i = 0; i < n; i++) {
              c[i * n + j] += a[i * n + k] * b[k * n + j];
          }
      }
  }
  double jki_time = get_time();
 
  for (k = 0; k < n; k++) {
      for (i = 0; i < n; i++) {
          for (j = 0; j < n; j++) {
              c[i * n + j] += a[i * n + k] * b[k * n + j];
          }
      }
  }
  double kij_time = get_time();
 
  for (k = 0; k < n; k++) {
      for (j = 0; j < n; j++) {
          for (i = 0; i < n; i++) {
              c[i * n + j] += a[i * n + k] * b[k * n + j];
          }
      }
  }
  double kji_time = get_time();

  /**************************************/

  printf("i-j-k time: %.6lf sec\n", ijk_time - begin);
  printf("i-k-j time: %.6lf sec\n", ikj_time - ijk_time);
  printf("j-i-k time: %.6lf sec\n", jik_time - ikj_time);
  printf("j-k-i time: %.6lf sec\n", jki_time - jik_time);
  printf("k-i-j time: %.6lf sec\n", kij_time - jki_time);
  printf("k-j-i time: %.6lf sec\n", kji_time - kij_time);

  /*
  // Print C for debugging. Comment out the print before measuring the execution time.
  double sum = 0;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      sum += c[i * n + j];
      // printf("c[%d][%d]=%lf\n", i, j, c[i * n + j]);
    }
  }
  // Print out the sum of all values in C.
  // This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
  printf("sum: %.6lf\n", sum);
  */

  free(a);
  free(b);
  free(c);
  return 0;
}

/* result
i-j-k time: 32.057913 sec
i-k-j time: 4.595589 sec
j-i-k time: 24.901979 sec
j-k-i time: 41.340265 sec
k-i-j time: 4.687801 sec
k-j-i time: 43.139218 sec
*/
