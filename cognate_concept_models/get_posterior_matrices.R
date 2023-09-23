betas <- readRDS('all_betas_full.RDS')

fams <- c(
  #'austronesian',
  'dravidian',
  'indoeuropean',
  'sinotibetan',
  'turkic',
  'utoaztecan'
)

fam.labels <- c(
  #'Austronesian',
  'Dravidian',
  'Indo-European',
  'Sino-Tibetan',
  'Turkic',
  'Uto-Aztecan'
)

set.seed(1234)

all.concepts <- c()

birth.mats <- list()
gain.mats <- list()
death.mats <- list()

for (i in 1:length(fams)) {
  betas.i <- betas[[i]]
  concepts <- readLines(paste('concept_lists/',fams[i],'.txt',sep=''))
  all.concepts <- c(all.concepts,concepts)
  K = (ncol(betas.i)/6)-1
  N <- nrow(betas.i)
  birth.rates <- NULL
  gain.rates <- NULL
  death.rates <- NULL
  for (k in 1:K) {
    birth.rates <- cbind(birth.rates,betas.i[,1] + betas.i[,1+(k*6)] - (betas.i[,2] + betas.i[,2+(k*6)]))
    gain.rates <- cbind(gain.rates,betas.i[,6] + betas.i[,6+(k*6)] - (betas.i[,4] + betas.i[,4+(k*6)]))
    death.rates <- cbind(death.rates,betas.i[,5] + betas.i[,5+(k*6)] - (betas.i[,3] + betas.i[,3+(k*6)]))
  }
  birth.mat <- matrix(nrow=ncol(birth.rates),ncol=ncol(birth.rates))
  for (k in 1:K) {
    for (l in 1:K) {
      birth.mat[k,l] <- length(which(birth.rates[,k]-birth.rates[,l]>0))/nrow(birth.rates)
    }
  }
  gain.mat <- matrix(nrow=ncol(gain.rates),ncol=ncol(gain.rates))
  for (k in 1:K) {
    for (l in 1:K) {
      gain.mat[k,l] <- length(which(gain.rates[,k]-gain.rates[,l]>0))/nrow(gain.rates)
    }
  }
  death.mat <- matrix(nrow=ncol(death.rates),ncol=ncol(death.rates))
  for (k in 1:K) {
    for (l in 1:K) {
      death.mat[k,l] <- length(which(death.rates[,k]-death.rates[,l]>0))/nrow(death.rates)
    }
  }
  colnames(birth.mat) <- rownames(birth.mat) <- concepts
  colnames(gain.mat) <- rownames(gain.mat) <- concepts
  colnames(death.mat) <- rownames(death.mat) <- concepts
  birth.mats[[i]] <- birth.mat
  gain.mats[[i]] <- gain.mat
  death.mats[[i]] <- death.mat
}

all.concepts <- unique(all.concepts)

saveRDS(file='posterior_matrices.RDS',list(birth.mats,gain.mats,death.mats,all.concepts))