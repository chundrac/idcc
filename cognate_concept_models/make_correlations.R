#require(pcaMethods)
require(ggplot2)
require(HDInterval)
require(ggpubr)

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

freqs <- read.csv('Calude-2011-200.tsv',sep='\t') #freqs are already log-transformed
freq.vals <- freqs[,4:20]
freq.vals <- apply(freq.vals,2,as.numeric)
for (i in 1:nrow(freq.vals)) {
  freq.vals[i,is.na(freq.vals[i,])] <- mean(freq.vals[i,],na.rm=T)
}

#IE <- rowMeans(freq.vals[,c(1,2,3,4,5,8,11,13,14)])
#freq.vals <- cbind(freq.vals[,-c(1,2,3,4,5,8,11,13,14)],IE)

rownames(freq.vals) <- freqs$CONCEPTICON_GLOSS
x <- prcomp(freq.vals)
x <- x$x[,1]

pc.df <- data.frame(concept=names(x),PC1=x)

northeuralex <- read.csv("northeuralex-0.9-concept-data.tsv",sep='\t')
ranking <- northeuralex$position_in_ranking
names(ranking) <- northeuralex$concepticon

basic.df <- northeuralex[,c('concepticon','position_in_ranking')]
colnames(basic.df) <- c('concept','basicness')

all.families <- c()
all.concepts <- c()
all.ratios <- c()

for (i in 1:length(fams)) {
  betas.i <- betas[[i]]
  concepts <- readLines(paste('concept_lists/',fams[i],'.txt',sep=''))
  all.concepts <- c(all.concepts,concepts)
  K = (ncol(betas.i)/6)-1
  N <- nrow(betas.i)
  death.rates <- NULL
  for (k in 1:K) {
    death.rates <- cbind(death.rates,exp(betas.i[,5] + betas.i[,5+(k*6)] - (betas.i[,3] + betas.i[,3+(k*6)])))
  }
  CI.med <- apply(death.rates,2,median)
  all.ratios <- c(all.ratios,CI.med)
  all.families <- c(all.families,rep(fam.labels[i],length(CI.med)))
  
}

ratios.df <- data.frame('concept'=all.concepts,'median'=all.ratios,'family'=all.families)

merged.df <- merge(ratios.df,pc.df,by='concept')

merged.df <- merge(merged.df,basic.df,by='concept')

value <- c(merged.df$PC1,merged.df$basicness)

val.method <- c(rep('PC1',nrow(merged.df)),rep('Basicness',nrow(merged.df)))

ratios.df <- rbind(merged.df[,c("concept","median","family")],merged.df[,c("concept","median","family")])

ratios.df$method <- val.method

ratios.df$value <- value

#ggplot(merged.df,aes(x=PC1,y=median)) + geom_point() + stat_cor(method="spearman") + facet_wrap(vars(family))

tikzDevice::tikz('correlations.tex',width=10,height=4)
ggplot(ratios.df,aes(x=value,y=log(median))) + geom_point(aes(color=method),alpha=.6) + stat_cor(method="spearman") + 
  scale_color_manual(values = c("#56B4E9", "#E69F00"), guide="none") + 
  ggh4x::facet_grid2(method ~ family, scales = "free", independent = "x") + ylab('log median ratio') + theme_classic()
#ggplot(ratios.df[ratios.df$method=='PC1',],aes(x=value,y=median)) + geom_point() + stat_cor(method="spearman") + facet_wrap(vars(family))
dev.off()

measures.merged <- merge(pc.df,basic.df,by='concept')

with(measures.merged, cor.test(PC1,basicness,method='spearman'))
