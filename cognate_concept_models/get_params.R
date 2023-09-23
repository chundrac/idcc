require(rstan)

fams <- c(
#  'austronesian',
  'dravidian',
  'indoeuropean',
  'sinotibetan',
  'turkic',
  'utoaztecan'
)

all.betas <- list()

for (i in 1:length(fams)) {
  fam = fams[i]
  files <- dir('output/')
  files <- files[startsWith(files,fam)]
  betas <- NULL
  for (fn in files) {
    fit <- readRDS(paste('output/',fn,sep=''))
    print(fit,'beta')
    if (all(summary(fit,'beta')$summary[,'Rhat'][1:6]<5)) {
      betas <- rbind(betas,extract(fit)$beta[,1:6])
    }
    #print(colMeans(betas))
  }
  all.betas[[i]] <- betas
}

saveRDS(all.betas,file='all_betas.RDS')

all.betas <- list()

for (i in 1:length(fams)) {
  fam = fams[i]
  files <- dir('output/')
  files <- files[startsWith(files,fam)]
  betas <- NULL
  for (fn in files) {
    fit <- readRDS(paste('output/',fn,sep=''))
    print(fit,'beta')
    if (all(summary(fit,'beta')$summary[,'Rhat'][1:6]<5)) {
      betas <- rbind(betas,extract(fit)$beta)
    }
    #print(colMeans(betas))
  }
  all.betas[[i]] <- betas
}

saveRDS(all.betas,file='all_betas_full.RDS')