require(ggplot2)
library(HDInterval)
library(ggridges)
require(ggh4x)
require(tikzDevice)

betas <- readRDS('all_betas.RDS')

fams <- c(
  'austronesian',
  'semitic',
  'uralic'
)

fam.labels <- c(
  'Austronesian',
  'Semitic',
  'Uralic'
)

set.seed(1234)

fam.ID <- c()
rate.type <- c()
rate <- c()
for (i in 1:length(fams)) {
  betas.i <- betas[[i]]
  #betas.i <- betas.i[sample(1:nrow(betas.i),4000),]
  N <- nrow(betas.i)
  fam.ID <- c(fam.ID,rep(fam.labels[i],3*N))
  rate.type <- c(rate.type,c(rep('Birth rate, $-$IC vs.\\ $+$IC',N),rep('Mutation rate to $-$IC vs.\\ $+$IC',N),rep('Loss rate, $+$IC vs.\\ $-$IC',N)))
  rate <- c(rate,c(
    betas.i[,1]-betas.i[,2],
    betas.i[,6]-betas.i[,4],
    betas.i[,5]-betas.i[,3]
  ))
}

rate.type <- factor(rate.type,levels=c(
  'Birth rate, $-$IC vs.\\ $+$IC',
  'Mutation rate to $-$IC vs.\\ $+$IC',
  'Loss rate, $+$IC vs.\\ $-$IC'
))

rate.df <- data.frame(fam.ID,rate.type,rate)

phoible.langs <- read.csv('../family_level_distributions/phoible/languages.csv')
phoible.data <- read.csv('../family_level_distributions/phoible/inventories.csv')

phoible.merged <- merge(phoible.langs,phoible.data,by='Name')

cons.inventories <- aggregate(count_consonants ~ Family_Name, phoible.merged, FUN=median)
cons.inventories <- cons.inventories[cons.inventories$Family_Name %in% c('Afro-Asiatic','Austronesian','Uralic'),]
cons.inventories$Family_Name <- as.character(cons.inventories$Family_Name)
cons.inventories[cons.inventories$Family_Name=='Afro-Asiatic',1] <- 'Semitic'
rownames(cons.inventories) <- cons.inventories$Family_Name

labels.df <- #data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){round(length(which(x>1))/length(x),2)}),
      #data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){as.integer((length(which(x>1))/length(x))*100)}),
      #data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){(length(which(x>1))/length(x))*100}),
  data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>1))/length(x))*100),'\\%',sep='')}),
      aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){max(x)})[,3],
      aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){max(table(cut(x,seq(min(x),max(x),dist(range(x))/30))))})[,3]
      ))

chance <- c(
  aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>cons.inventories['Austronesian',]$count_consonants-1))/length(x))*100),'\\%',sep='')})[1:3,3],
  aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>cons.inventories['Semitic',]$count_consonants-1))/length(x))*100),'\\%',sep='')})[4:6,3],
  aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>cons.inventories['Uralic',]$count_consonants-1))/length(x))*100),'\\%',sep='')})[7:9,3]
)

chance <- paste(', ',chance,sep='')
chance[c(3,6,9)] <- ''

colnames(labels.df)[3] <- 'prop'
colnames(labels.df)[4] <- 'max'
colnames(labels.df)[5] <- 'hist.max'

labels.df$prop <- paste(labels.df$prop,chance,sep='')

s=1.35

tikz('cognate_posterior_rates.tex',width=7*s,height=4.5*s)
ggplot(rate.df, aes(x = exp(rate))) + 
  geom_histogram(aes(fill=rate.type),alpha=.6) + 
  scale_fill_discrete(guide="none") + 
  #scale_fill_manual(values = c("blue", "red", "green"), guide=F) + 
  geom_vline(xintercept = 1,linetype="dashed") + 
  #facet_grid(vars(model.type),vars(contrast),scales = "free_x") + 
  #facet_grid(vars(),vars(contrast)) + 
  facet_grid2(vars(rate.type),vars(fam.ID), scales="free", independent=TRUE) + 
  #scale_fill_manual(values = c("transparent", "lightblue", "transparent"), guide = "none") + 
  ylab('Posterior density') + xlab('')
dev.off()



p <- ggplot(rate.df, aes(x = exp(rate))) + 
  geom_histogram(aes(fill=rate.type),alpha=.6) + 
  scale_fill_discrete(guide="none") + 
  geom_vline(xintercept = 1,linetype="dashed") + 
  facet_grid2(vars(rate.type),vars(fam.ID), scales="free", independent=TRUE) + 
  ylab('Posterior density') + xlab('')

#p + geom_text(data=labels.df, aes(x=max,y=hist.max,label=prop))

tikz('cognate_posterior_rates.tex',width=7*s,height=4.5*s)
#p + geom_text(data=labels.df, aes(x=max,y=1,label=prop), hjust=1, vjust = -15) 
p + geom_text(data=labels.df, aes(x=max,y=1,label=prop), hjust='inward', vjust='inward') 
dev.off()

aggregate(exp(rate) ~ rate.type+fam.ID,rate.df,FUN=function(x){quantile(x,probs=c(.025,.5,.975))})

