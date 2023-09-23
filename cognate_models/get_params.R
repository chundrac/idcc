require(rstan)

fams <- c(
  'austronesian',
  'semitic',
  'uralic'
)

#austronesian run 20 did not complete within 7 days

all.betas <- list()

for (i in 1:length(fams)) {
  fam = fams[i]
  files <- dir('output/')
  files <- files[startsWith(files,fam)]
  betas <- NULL
  for (fn in files) {
    fit <- readRDS(paste('output/',fn,sep=''))
    print(fit,'beta')
    if (all(summary(fit,'beta')$summary[,'Rhat']<1.5)) {
      betas <- rbind(betas,extract(fit)$beta)
    }
    #print(colMeans(betas))
  }
  all.betas[[i]] <- betas
}

saveRDS(all.betas,file='all_betas.RDS')