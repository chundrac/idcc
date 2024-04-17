require(phytools)
require(rstan)
require(HDInterval)

#false negatives vs. false positives

birth <- as.numeric(commandArgs(trailingOnly = TRUE)[1])
mutation <- as.numeric(commandArgs(trailingOnly = TRUE)[2])
death <- as.numeric(commandArgs(trailingOnly = TRUE)[3])
my.seed <- as.numeric(commandArgs(trailingOnly = TRUE)[4])

set.seed(my.seed)

S <- 100

#tree <- rtree(sample(25:50,1))
tree <- rtree(100)
tree <- chronos(tree)
tree <- collapse.singles(tree)
tree <- reorder.phylo(tree,order='pruningwise')

Q <- matrix(0,nrow=3,ncol=3)
{
  if (birth==1) {
    r1 <- rgamma(1,1,1)
    r2 <- rgamma(1,1,1)
    Q[1,2] <- r1
    Q[1,3] <- r2
  }
  else {
    r1 <- rgamma(1,1,1)
    Q[1,2] <- r1
    Q[1,3] <- r1
  }
  if (death==1) {
    r1 <- rgamma(1,1,1)
    r2 <- rgamma(1,1,1)
    Q[2,1] <- r1
    Q[3,1] <- r2
  }
  else {
    r1 <- rgamma(1,1,1)
    Q[2,1] <- r1
    Q[3,1] <- r1
  }
  if (mutation==1) {
    r1 <- rgamma(1,1,1)
    r2 <- rgamma(1,1,1)
    Q[2,3] <- r1
    Q[3,2] <- r2
  }
  else {
    r1 <- rgamma(1,1,1)
    Q[2,3] <- r1
    Q[3,2] <- r1
  }
}

diag(Q) <- -rowSums(Q)

parent <- tree$edge[,1]
child <- tree$edge[,2]
b.lens <- tree$edge.length
B <- length(b.lens)
J <- ncol(Q)
N <- length(unique(c(parent,child)))
T <- length(child[which(!child %in% parent)])

states.bin.all <- array(dim=c(S,N,J))

for (s in 1:S) {
  states <- sim.history(tree, Q)$states
  bin.data <- to.matrix(states,seq=c('1','2','3'))
  states.bin <- rbind(bin.data,matrix(1,nrow=N-T,ncol=J))
  states.bin.all[s,,] <- states.bin
}

model_code = "functions {
  matrix fill_matrix(vector beta, int J) {
    matrix[J,J] Q = rep_matrix(0,J,J);
    {int k = 1;
      for (i in 1:J) {
        for (j in 1:J) {
          if (i != j) {
            Q[i,j] = beta[k];
            k += 1;
          }
        }
      }
    }
    for (i in 1:J) {
      Q[i,i] = -sum(Q[i,]);
    }
    return(Q);
  }
  //compute likelihood via Felsenstein's Pruning Algorithm
  vector pruning_likelihood( vector beta , vector theta , data real[] xr , data int[] xi ) {
    int N = xi[1];
    int B = xi[2];
    int J = xi[3];
    int child[B] = xi[4:(B+3)];
    int parent[B] = xi[(4+B):(2*B+3)];
    int tiplik[N*J] = xi[(2*B+4):(2*B+3)+N*J];
    matrix[J,J] Q = fill_matrix(beta, J);
    matrix[N,J] lambda;
    for (j in 1:J) {
      lambda[,j] = to_vector(log(tiplik[((N*j)-(N-1)):(N*j)]));
    }
    for (b in 1:B) {
      matrix[J,J] P = matrix_exp(Q); //via matrix exponentiation
      for (d in 1:J) {
        lambda[parent[b],d] += log(dot_product(P[d],exp(lambda[child[b]])));
      }
    }
    return([log_sum_exp(-log(J) + lambda[parent[B]])]');
  }
}
data {
  int<lower=1> N; //number of tips+internal nodes+root
  int<lower=1> T; //number of tips
  int<lower=1> B; //number of branches
  int<lower=1> J; //number of states
  int<lower=1> S; //number of characters
  int<lower=1> child[B];                //child of each branch
  int<lower=1> parent[B];               //parent of each branch
  real<lower=0> brlen[B];                //length of each branch
  int<lower=0,upper=1> tiplik[S,N,J];     //likelihoods for data at tips in tree
}
transformed data {
  //pack phylogenetic data into S 1-dim vectors
  vector[0] theta[S]; //empty local params
  int xi[S,3+2*B+N*J];
  real xr[S,B];
  for (i in 1:S) {
    xr[i] = to_array_1d(brlen);
    xi[i,1] = N;
    xi[i,2] = B;
    xi[i,3] = J;
    xi[i,4:(B+3)] = child;
    xi[i,(4+B):(2*B+3)] = parent;
    for (j in 1:J) {
      xi[i,(2*B+4)+(j-1)*N:(2*B+3)+j*N] = tiplik[i,,j];
    }
    xi[i] = to_array_1d(xi[i]);
  }
}
parameters {
  vector<lower=0>[J*(J-1)] beta;
}
transformed parameters {
  vector[S] log_lik;
  log_lik = map_rect(pruning_likelihood,beta,theta,xr,xi);
}
model {
  beta ~ gamma(1,1);     //any priors defined on [0,inf) are possible
  target += sum(log_lik);
}"

data.list <- list(N=N,
                  T=T,
                  B=B,
                  J=J,
                  S=S,
                  brlen=b.lens,
                  child=child,
                  parent=parent,
                  tiplik=states.bin.all)

fit <- stan(model_code=model_code,data=data.list,chains=1)

rates <- extract(fit)$beta

#print(c(Q[1,2]/Q[1,3],hdi(rates[,1]/rates[,2])))
#print(c(Q[2,1]/Q[3,1],hdi(rates[,3]/rates[,5])))
#print(c(Q[2,3]/Q[3,2],hdi(rates[,4]/rates[,6])))
#print(c(Q[1,3]/Q[1,2],hdi(rates[,2]/rates[,1])))
#print(c(Q[3,1]/Q[2,1],hdi(rates[,5]/rates[,3])))
#print(c(Q[3,2]/Q[2,3],hdi(rates[,6]/rates[,4])))

rate1 <- c(
  Q[1,2],
  Q[3,2],
  Q[3,1]
)

rate2 <- c(
  Q[1,3],
  Q[2,3],
  Q[2,1]
)

ratio <- c(
  Q[1,2]/Q[1,3],
  Q[3,2]/Q[2,3],
  Q[3,1]/Q[2,1]
)

HDIs <- rbind(
  hdi(rates[,1]/rates[,2]),
  hdi(rates[,6]/rates[,4]),
  hdi(rates[,5]/rates[,3])
)

rate.df <- cbind(rep(my.seed,3),rep(birth,3),rep(mutation,3),rep(death,3),rate1,rate2,ratio,HDIs)
colnames(rate.df) <- c('seed','birth','mutation','death','rate1','rate2','ratio','hdi.lower','hdi.upper')
rate.df <- as.data.frame(rate.df)

outcome <- function(x) {
  label = ''
  lower = x[8]
  upper = x[9]
  true = x[7]
  if (true == 1) {
    if ((upper > 1 & lower > 1)|(upper < 1 & lower < 1)) {
      label <- 'FP'
    }
    else {
      label <- 'TN'
    }
  }
  else {
    if (true < 1) {
      if (upper < 1 & lower < 1) {
        label = 'TP'
      }
      else if (upper > 1 & lower > 1) {
        label = 'SE'
      }
      else {
        label = 'FN'
      }
    }
    if (true > 1) {
      if (upper < 1 & lower < 1) {
        label = 'SE'
      }
      else if (upper > 1 & lower > 1) {
        label = 'TP'
      }
      else {
        label = 'FN'
      }
    }
  }
  return(label)
}

in.CI <- function(x) {
  lower = as.numeric(x[8])
  upper = as.numeric(x[9])
  true = as.numeric(x[7])
  #print(c(true,upper,lower))
  #print(true - lower)
  #print(true - upper)
  if ((true > lower) && (true < upper)) {
    label = 1
  }
  else {
    label = 0
  }
  return(label)
}

rate.df$label <- apply(rate.df,1,outcome)
rate.df$true.in.CI <- apply(rate.df,1,in.CI)

if ('simulations.csv' %in% dir()) {
  colnames(rate.df) <- NULL
}

write.table(rate.df, "simulations.csv", row.names = F, quote = F, sep = '\t', append = TRUE)

