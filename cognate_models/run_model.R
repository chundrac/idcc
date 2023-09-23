require(rstan)

fam = commandArgs(trailingOnly = TRUE)[1]
i = as.integer(commandArgs(trailingOnly = TRUE)[2])

n_cores = 64

options(mc.cores = parallel::detectCores())
rstan_options(auto_write=FALSE)

rstan_options(threads_per_chain = 32)

data.list.full <- readRDS(paste('processed_data/',fam,'_data_for_analysis.RDS',sep=''))

data.list <- data.list.full[[i]]

fit <- stan(file='hierarchical_model.stan',data=data.list,cores=n_cores,control=list(adapt_delta=.99),pars=c('beta','log_lik'),include=T)

saveRDS(fit,file=paste('output/',fam,'_fit_',i,'.RDS',sep=''))