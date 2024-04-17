require(ggplot2)
require(HDInterval)

betas <- readRDS('all_betas_full_thinned.RDS')

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

birth.plots <- list()
gain.plots <- list()
death.plots <- list()

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
    birth.rates <- cbind(birth.rates,exp(betas.i[,1] + betas.i[,1+(k*6)] - (betas.i[,2] + betas.i[,2+(k*6)])))
    gain.rates <- cbind(gain.rates,exp(betas.i[,6] + betas.i[,6+(k*6)] - (betas.i[,4] + betas.i[,4+(k*6)])))
    death.rates <- cbind(death.rates,exp(betas.i[,5] + betas.i[,5+(k*6)] - (betas.i[,3] + betas.i[,3+(k*6)])))
  }
  colnames(birth.rates) <- concepts
  colnames(gain.rates) <- concepts
  colnames(death.rates) <- concepts
  ##death.rates[,names(sort(x))[names(sort(x)) %in% colnames(death.rates)]]
  ##plot(x[names(sort(x)) %in% colnames(death.rates)],apply(death.rates[,names(sort(x))[names(sort(x)) %in% colnames(death.rates)]],2,median))
  
  ##death.wide <- as.data.frame(death.rates) %>% pivot_longer(cols=colnames(death.rates),names_to='concept',values_to='ratio')
  ##death.wide$concept <- factor(death.wide$concept,levels=names(sort(x)))
  ##death.wide$concept <- factor(death.wide$concept,levels=names(sort(apply(death.rates,2,median))))
  ##ggplot(death.wide,aes(x=concept,y=ratio)) + geom_violin()
  
  CI.min <- apply(birth.rates,2,hdi)[1,]
  CI.max <- apply(birth.rates,2,hdi)[2,]
  CI.med <- apply(birth.rates,2,median)
  birth.moments <- data.frame(concept=names(CI.min),min=CI.min,med=CI.med,max=CI.max)
  birth.moments$concept <- factor(birth.moments$concept,levels=names(sort(apply(birth.rates,2,median))))
  p <- ggplot(birth.moments,aes(x=concept,y=med)) + geom_point(color="#56B4E9") + geom_errorbar(aes(ymin=min, ymax=max),color="#56B4E9") + 
    geom_hline(yintercept = 1, col = "darkgray") + 
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + ylab('95\\% HDI') + xlab('')
  
  birth.plots[[i]] <- p
  
  CI.min <- apply(gain.rates,2,hdi)[1,]
  CI.max <- apply(gain.rates,2,hdi)[2,]
  CI.med <- apply(gain.rates,2,median)
  gain.moments <- data.frame(concept=names(CI.min),min=CI.min,med=CI.med,max=CI.max)
  gain.moments$concept <- factor(gain.moments$concept,levels=names(sort(apply(gain.rates,2,median))))
  p <- ggplot(gain.moments,aes(x=concept,y=med)) + geom_point(color="#CC79A7") + geom_errorbar(aes(ymin=min, ymax=max),color="#CC79A7") + 
    geom_hline(yintercept = 1, col = "darkgray") + 
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + ylab('95\\% HDI') + xlab('')
  
  gain.plots[[i]] <- p
  
  CI.min <- apply(death.rates,2,hdi)[1,]
  CI.max <- apply(death.rates,2,hdi)[2,]
  CI.med <- apply(death.rates,2,median)
  death.moments <- data.frame(concept=names(CI.min),min=CI.min,med=CI.med,max=CI.max)
  death.moments$concept <- factor(death.moments$concept,levels=names(sort(apply(death.rates,2,median))))
  p <- ggplot(death.moments,aes(x=concept,y=med)) + geom_point(color="#E69F00") + geom_errorbar(aes(ymin=min, ymax=max),color="#E69F00") + 
    geom_hline(yintercept = 1, col = "darkgray") + 
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + ylab('95\\% HDI') + xlab('')
  
  death.plots[[i]] <- p
  
}

for (i in 1:length(fams)) {
  tikzDevice::tikz(paste('graphics/birth_rates_',fams[i],'.tex',sep=''),width=12,height=10)
  birth.plots[[i]]
  dev.off()

  tikzDevice::tikz(paste('graphics/mutation_rates_',fams[i],'.tex',sep=''),width=12,height=10)
  gain.plots[[i]]
  dev.off()
  
  tikzDevice::tikz(paste('graphics/death_rates_',fams[i],'.tex',sep=''),width=12,height=10)
  death.plots[[i]]
  dev.off()
}





