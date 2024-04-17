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

phoible.merged$count_consonants <- phoible.merged$count_consonants - 1

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

#chance <- c(
#  aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>cons.inventories['Austronesian',]$count_consonants-1))/length(x))*100),'\\%',sep='')})[1:3,3],
#  aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>cons.inventories['Semitic',]$count_consonants-1))/length(x))*100),'\\%',sep='')})[4:6,3],
#  aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>cons.inventories['Uralic',]$count_consonants-1))/length(x))*100),'\\%',sep='')})[7:9,3]
#)

#chance <- paste(', ',chance,sep='')
#chance[c(3,6,9)] <- ''

colnames(labels.df)[3] <- 'prop'
colnames(labels.df)[4] <- 'max'
colnames(labels.df)[5] <- 'hist.max'

cons.medians <- cons.inventories

cons.intervals <- rbind(
  aggregate(count_consonants ~ Family_Name, phoible.merged, FUN=min),
  aggregate(count_consonants ~ Family_Name, phoible.merged, FUN=max)
)

cons.intervals <- cons.intervals[cons.intervals$Family_Name %in% c('Afro-Asiatic','Austronesian','Uralic'),]

cons.intervals$Family_Name <- as.character(cons.intervals$Family_Name)
cons.intervals[cons.intervals$Family_Name=='Afro-Asiatic',1] <- 'Semitic'

colnames(cons.intervals) <- c('fam.ID','x')

colnames(cons.medians) <- c('fam.ID','x')

#sim.change.old <- read.csv('sound_change_simulations_old.tsv',sep='\t')

sim.change <- read.csv('sound_change_simulations.tsv',sep='\t')

sim.change$ratio <- (sim.change$plus_to_minus + 1)/(sim.change$minus_to_plus + 1)

sim.change <- aggregate(ratio ~ family + lang, sim.change, FUN=mean)

sim.change.intervals <- rbind(
  aggregate(ratio ~ family, sim.change, FUN=min),
  aggregate(ratio ~ family, sim.change, FUN=max)
)

sim.change.medians <- aggregate(ratio ~ family, sim.change, FUN=median)

colnames(sim.change.intervals) <- c('fam.ID','x')

colnames(sim.change.medians) <- c('fam.ID','x')

intervals.df <- rbind(cons.intervals,sim.change.intervals)

intervals.df$rate.type <- c(rep('Birth rate, $-$IC vs.\\ $+$IC',6),rep('Mutation rate to $-$IC vs.\\ $+$IC',6))

colnames(intervals.df)[1:2] <- c('fam.ID','x')

intervals.df$y <- rep(0,nrow(intervals.df))

intervals.df <- data.frame(intervals.df)

print(intervals.df)

#colnames(cons.medians)[2] <- 'value'

medians.df <- rbind(cons.medians,sim.change.medians)

medians.df$rate.type <- c(rep('Birth rate, $-$IC vs.\\ $+$IC',3),rep('Mutation rate to $-$IC vs.\\ $+$IC',3))

intervals.df <- droplevels(intervals.df)

medians.df <- droplevels(medians.df)

print(medians.df)

intervals.df$rate.type <- factor(intervals.df$rate.type,levels=c(
  'Birth rate, $-$IC vs.\\ $+$IC',
  'Mutation rate to $-$IC vs.\\ $+$IC',
  'Loss rate, $+$IC vs.\\ $-$IC'
))

medians.df$rate.type <- factor(medians.df$rate.type,levels=c(
  'Birth rate, $-$IC vs.\\ $+$IC',
  'Mutation rate to $-$IC vs.\\ $+$IC',
  'Loss rate, $+$IC vs.\\ $-$IC'
))

#labels.df$prop <- paste(labels.df$prop,chance,sep='')

x=aggregate(rate ~ fam.ID + rate.type, rate.df, FUN=function(x){sort(x)[length(x)*.999]})

max.rate <- x$rate

names(max.rate) <- paste(x$fam.ID,x$rate.type,sep='&')

max.row <- apply(rate.df,1,function(x){max.rate[paste(as.character(x[1]),as.character(x[2]),sep='&')]})

pastenice <- function(x) {
  xx <- round(c(hdi(x)[1],median(x),hdi(x)[2]),2)
  #xx <- round(quantile(x,probs=c(.025,.5,.975)),2)
  return(
    paste('$',xx[2],'$, [$',xx[1],'$, $',xx[3],'$]',sep='')
  )
}

HDintervals.df <- data.frame(aggregate(exp(rate) ~ rate.type+fam.ID,rate.df,FUN=pastenice))

rate.df <- rate.df[rate.df$rate <= max.row,]

s=1.35

p <- ggplot(rate.df, aes(x = exp(rate))) + 
  geom_histogram(aes(fill=rate.type),alpha=.6) + 
  scale_fill_manual(values = c("#56B4E9", "#CC79A7", "#E69F00"), guide="none") + 
  geom_vline(xintercept = 1,linetype="dashed") + 
  ##geom_vline(data=medians.df,aes(xintercept = value),linetype="dotted") + 
  ##geom_vline(data=medians.df,aes(xintercept = x),color='#E69F00') + 
  ##geom_line(data=intervals.df,aes(x=x,y=y), color='#E69F00') + 
  #geom_vline(data=medians.df,aes(xintercept = x),color='#FED976') + 
  #geom_line(data=intervals.df,aes(x=x,y=y), color='#FED976', lwd=3) + 
  geom_vline(data=medians.df,aes(xintercept = x)) + 
  geom_line(data=intervals.df,aes(x=x,y=y), lwd=3) + 
  facet_grid2(vars(rate.type),vars(fam.ID), scales="free", independent=TRUE) + 
  ylab('Posterior density') + xlab('') + theme_classic() + theme(axis.text.y = element_blank(),axis.ticks.y = element_blank())


tikz('cognate_posterior_rates.tex',width=7*s,height=4.5*s)
p + geom_text(data=labels.df, aes(x=Inf,y=Inf,label=prop), hjust='inward', vjust='inward', size=3.5)
dev.off()
