functions {
  matrix fill_matrix(vector rates, int J, int P) {
    matrix[J,J] Q = rep_matrix(1e-10,J,J);
    Q[1,2] = rates[1];
    Q[1,3] = rates[2];
    Q[2,1] = rates[3];
    Q[3,1] = rates[5];
    if (P == 1) {
      Q[2,3] = rates[4];
      Q[3,2] = rates[6];
    }
    for (j in 1:J) {
      Q[j,j] = 0;
      Q[j,j] = -sum(Q[j,]);
    }
    return(Q);
  }
  //compute likelihood via Felsenstein's Pruning Algorithm
  vector pruning( vector beta , vector theta , data real[] xr , data int[] xi ) {
    int N = xi[1];
    int B = xi[2];
    int J = xi[3];
    int S = xi[4];
    int concept_ID = xi[5];
    int tiplik[N*J] = xi[6:(N*J+5)];
    int tiplik_absent[N*J] = xi[(6+N*J):(2*N*J+5)];
    int child[B] = xi[(2*N*J+6):(2*N*J+5+B)];
    int parent[B] = xi[(2*N*J+6+B):(2*N*J+5+2*B)];
    real brlen[B] = xr;
    vector[J*(J-1)] rates = exp(beta[1:(J*(J-1))] + beta[((concept_ID)*J*(J-1)+1):((concept_ID+1)*J*(J-1))]);
    matrix[J,J] Q = fill_matrix(rates,J,S);
    real log_lik;
    real log_lik_absent;
    real log_lik_corrected;
    matrix[N,J] lambda;
    matrix[N,J] lambda_absent;
    for (j in 1:J) {
      lambda[,j] = to_vector(log(tiplik[((N*j)-(N-1)):(N*j)]));
      lambda_absent[,j] = to_vector(log(tiplik_absent[((N*j)-(N-1)):(N*j)]));
    }
    for (b in 1:B) {
      matrix[J,J] P = matrix_exp(Q*brlen[b]); //via matrix exponentiation
      for (j in 1:J) {
        lambda[parent[b],j] += log_sum_exp(log(P[j])+lambda[child[b],]);
        lambda_absent[parent[b],j] += log_sum_exp(log(P[j])+lambda_absent[child[b],]);
      }
    }
    log_lik = log_sum_exp(-log(J) + lambda[parent[B]]);
    log_lik_absent = log_sum_exp(-log(J) + lambda_absent[parent[B]]);
    log_lik_corrected = log_lik - log(1-exp(log_lik_absent));
    return([log_lik_corrected]');
  }
}
data {
  int<lower=1> D;
  int<lower=1> N;
  int<lower=1> J;
  int<lower=1> B;
  int<lower=1> K;
  int xi[D,5+2*N*J+2*B];                  //likelihoods for data at tips+internal nodes in of each tree
  real xr[D,B];
}
transformed data {
  int xi_[D,5+2*N*J+2*B];
  real xr_[D,B];
  vector[0] theta[D];
  for (d in 1:D) {
    xi_[d] = to_array_1d(xi[d]);
    xr_[d] = to_array_1d(xr[d]);
  }
}
parameters {
  vector[J*(J-1)] mu;
  vector<lower=0>[J*(J-1)] sigma;
  vector[J*(J-1)] eps[K];
}
transformed parameters {
  vector[D] log_lik;
  vector[(K+1)*J*(J-1)] beta;
  beta[1:(J*(J-1))] = mu;
  for (k in 1:K) {
    beta[(k*(J*(J-1))+1):((k+1)*(J*(J-1)))] = eps[k,] .* sigma;
  }
  log_lik = map_rect(pruning,beta,theta,xr,xi);
}
model {
  mu ~ normal(0,1);
  sigma ~ normal(0,1);
  for (k in 1:K) {
    eps[k,] ~ normal(0,1);
  }
  target += sum(log_lik);
}
