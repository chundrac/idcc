functions {
  matrix[] fill_matrix(vector rates, int J, int P) {
    matrix[J,J] Q[2];
    Q[1,,] = rep_matrix(1e-10,J,J);  //non-birth loci
    Q[2,,] = rep_matrix(1e-10,J,J);  //birth loci
    //prevent births on non-birth loci
    Q[1,2,1] = rates[3];             //mu_{-}
    Q[1,3,1] = rates[5];             //mu_{+}
    if (P == 1) {                    //if there is state variation
      Q[1,2,3] = rates[4];             //rho_{-+}
      Q[1,3,2] = rates[6];             //rho_{+-}
    }
    //prevent deaths and transitions on birth loci
    Q[2,1,2] = rates[1];               //lambda_{-}
    Q[2,1,3] = rates[2];               //lambda_{-}
    for (j in 1:J) {
      for (i in 1:2) {
        Q[i,j,j] = 0;
        Q[i,j,j] = -sum(Q[i,j,]);
      }
    }
    return(Q);
  }
  //compute likelihood via Felsenstein's Pruning Algorithm
  vector pruning( vector beta , vector theta , data real[] xr , data int[] xi ) {
    int N = xi[1];
    int B = xi[2];
    int J = xi[3];
    int S = xi[4];
    int tiplik[N*J] = xi[5:(N*J+4)];
    int tiplik_absent[N*J] = xi[(5+N*J):(2*N*J+4)];
    int child[B] = xi[(2*N*J+5):(2*N*J+4+B)];
    int parent[B] = xi[(2*N*J+5+B):(2*N*J+4+2*B)];
    int branch_type[B] = xi[(2*N*J+5+2*B):(2*N*J+4+3*B)];
    real brlen[B] = xr;
    vector[J*(J-1)] rates = beta;
    matrix[J,J] Q[2];
    real log_lik;
    real log_lik_absent;
    real log_lik_corrected;
    matrix[N,J] lambda;
    matrix[N,J] lambda_absent;
    rates[3:(J*(J-1))] += theta;
    rates = exp(rates);
    Q = fill_matrix(rates,J,S);
    for (j in 1:J) {
      lambda[,j] = to_vector(log(tiplik[((N*j)-(N-1)):(N*j)]));
      lambda_absent[,j] = to_vector(log(tiplik_absent[((N*j)-(N-1)):(N*j)]));
    }
    for (b in 1:B) {
      matrix[J,J] P = matrix_exp(Q[branch_type[b],,]*brlen[b]); //via matrix exponentiation
      for (j in 1:J) {
        lambda[parent[b],j] += log_sum_exp(log(P[j,])+lambda[child[b],]);
        lambda_absent[parent[b],j] += log_sum_exp(log(P[j,])+lambda_absent[child[b],]);
      }
    } 
    log_lik = log_sum_exp(-log(J) + to_vector(lambda[parent[B]]));
    log_lik_absent = log_sum_exp(-log(J) + to_vector(lambda_absent[parent[B]]));
    log_lik_corrected = log_lik - log(1-exp(log_lik_absent));
    return([log_lik_corrected]');
  }
}
data {
  int<lower=1> D;
  int<lower=1> N;
  int<lower=1> J;
  int<lower=1> B;
  int xi[D,4+2*N*J+3*B];                  //likelihoods for data at tips+internal nodes in of each tree
  real xr[D,B];
}
transformed data {
  int xi_[D,4+2*N*J+3*B];
  real xr_[D,B];
  for (d in 1:D) {
    xi_[d] = to_array_1d(xi[d]);
    xr_[d] = to_array_1d(xr[d]);
  }
}
parameters {
  vector[J*(J-1)] beta;
  vector<lower=0>[(J*(J-1))-2] sigma;
  vector[(J*(J-1))-2] eps[D];
}
transformed parameters {
  vector[D] log_lik;
  {
    vector[J*(J-1)-2] theta[D];
    for (d in 1:D) {
      theta[d,] = eps[d,] .* sigma;
    }
    log_lik = map_rect(pruning,beta,theta,xr_,xi_);
  }
}
model {
  beta ~ normal(0,1);
  sigma ~ normal(0,1);
  for (d in 1:D) {
    eps[d,] ~ normal(0,1);
  }
  target += sum(log_lik);
}
