require(ggplot2)
library(HDInterval)
library(ggridges)
require(ggh4x)
require(tikzDevice)

betas <- readRDS('all_betas.RDS')

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

fam.ID <- c()
rate.type <- c()
rate <- c()
for (i in 1:length(fams)) {
  betas.i <- betas[[i]]
  #  betas.i <- betas.i[sample(1:nrow(betas.i),4000),]
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

#aggregate(exp(rate) ~ rate.type+fam.ID,rate.df,FUN=function(x){round(quantile(x,probs=c(.025,.5,.975)),2)})

labels.df <- #data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){round(length(which(x>1))/length(x),2)}),
  #data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){as.integer((length(which(x>1))/length(x))*100)}),
  #data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){(length(which(x>1))/length(x))*100}),
  data.frame(cbind(aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){paste(as.integer((length(which(x>1))/length(x))*100),'\\%',sep='')}),
                   aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){max(x)})[,3],
                   aggregate(exp(rate) ~ rate.type + fam.ID, rate.df, FUN=function(x){max(table(cut(x,seq(min(x),max(x),dist(range(x))/30))))})[,3]
  ))

colnames(labels.df)[3] <- 'prop'
colnames(labels.df)[4] <- 'max'
colnames(labels.df)[5] <- 'hist.max'

prop.idcc <- read.csv('../family_level_distributions/IDCC_counts_by_family.tsv',sep='\t')
prop.idcc$ratio <- prop.idcc$NoIDCC/prop.idcc$IDCC

#prop.idcc.agg <- cbind(aggregate(ratio ~ Family, prop.idcc, FUN=median),aggregate(ratio ~ Family, prop.idcc, FUN=min)[,2],aggregate(ratio ~ Family, prop.idcc, FUN=max)[,2])
#colnames(prop.idcc.agg) <- c('fam.ID','median','min','max')

prop.idcc.intervals <- rbind(
  aggregate(ratio ~ Family, prop.idcc, FUN=min),
  aggregate(ratio ~ Family, prop.idcc, FUN=max)
)

prop.idcc.medians <- aggregate(ratio ~ Family, prop.idcc, FUN=median)

sim.change <- read.csv('sound_change_simulations/sound_change_simulations.tsv',sep='\t')

sim.change.intervals <- rbind(
  aggregate(mean ~ family, sim.change, FUN=min),
  aggregate(mean ~ family, sim.change, FUN=max)
)

sim.change.medians <- aggregate(mean ~ family, sim.change, FUN=median)

colnames(sim.change.intervals) <- c('Family','ratio')

intervals.df <- rbind(prop.idcc.intervals,sim.change.intervals)

intervals.df$rate.type <- c(rep('Birth rate, $-$IC vs.\\ $+$IC',10),rep('Mutation rate to $-$IC vs.\\ $+$IC',10))

colnames(intervals.df)[1:2] <- c('fam.ID','x')

intervals.df$y <- rep(0,nrow(intervals.df))

intervals.df <- data.frame(intervals.df)

print(intervals.df)

colnames(prop.idcc.medians) <- c('fam.ID','value')

colnames(sim.change.medians) <- c('fam.ID','value')

medians.df <- rbind(prop.idcc.medians,sim.change.medians)

medians.df$rate.type <- c(rep('Birth rate, $-$IC vs.\\ $+$IC',5),rep('Mutation rate to $-$IC vs.\\ $+$IC',5))

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

x=aggregate(rate ~ fam.ID + rate.type, rate.df, FUN=function(x){sort(x)[length(x)*.999]})
max.rate <- x$rate
names(max.rate) <- paste(x$fam.ID,x$rate.type,sep='&')
max.row <- apply(rate.df,1,function(x){max.rate[paste(as.character(x[1]),as.character(x[2]),sep='&')]})

pastenice <- function(x) {
  xx <- round(c(hdi(x)[1],median(x),hdi(x)[2]),2)
  #xx <- round(c(hdi(x,credMass=.89)[1],median(x),hdi(x,credMass=.89)[2]),2)
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
  ##geom_vline(data=medians.df,aes(xintercept = value),color='#E69F00') + 
  ##geom_line(data=intervals.df,aes(x=x,y=y), color='#E69F00') + 
  #geom_vline(data=medians.df,aes(xintercept = value),color='#FED976') + 
  #geom_line(data=intervals.df,aes(x=x,y=y), color='#FED976', lwd=3) + 
  geom_vline(data=medians.df,aes(xintercept = value)) + 
  geom_line(data=intervals.df,aes(x=x,y=y), lwd=3) + 
  facet_grid2(vars(rate.type),vars(fam.ID), scales="free", independent=TRUE) + 
  ylab('Posterior density') + xlab('') + theme_classic() + theme(axis.text.y = element_blank(),axis.ticks.y = element_blank())

tikz('cognate_concept_posterior_rates.tex',width=7*s,height=4.5*s)
p + geom_text(data=labels.df, aes(x=Inf,y=Inf,label=prop), hjust='inward', vjust='inward')
dev.off()

birth.df <- HDintervals.df[HDintervals.df$rate.type=='Birth rate, $-$IC vs.\\ $+$IC',]

curr.string <- paste(paste(birth.df$fam.ID,birth.df$exp.rate.,sep=': '),collapse='; ')

write('%<*birthRate>',file='cognate-concept-CIs.tex')
write(curr.string,file='cognate-concept-CIs.tex',append=TRUE)
write('%</birthRate>',file='cognate-concept-CIs.tex',append=TRUE)

gain.df <- HDintervals.df[HDintervals.df$rate.type=='Mutation rate to $-$IC vs.\\ $+$IC',]

curr.string <- paste(paste(gain.df$fam.ID,gain.df$exp.rate.,sep=': '),collapse='; ')

write('%<*gainRate>',file='cognate-concept-CIs.tex',append=TRUE)
write(curr.string,file='cognate-concept-CIs.tex',append=TRUE)
write('%</gainRate>',file='cognate-concept-CIs.tex',append=TRUE)

death.df <- HDintervals.df[HDintervals.df$rate.type=='Loss rate, $+$IC vs.\\ $-$IC',]

curr.string <- paste(paste(death.df$fam.ID,death.df$exp.rate.,sep=': '),collapse='; ')

write('%<*deathRate>',file='cognate-concept-CIs.tex',append=TRUE)
write(curr.string,file='cognate-concept-CIs.tex',append=TRUE)
write('%</deathRate>',file='cognate-concept-CIs.tex',append=TRUE)

