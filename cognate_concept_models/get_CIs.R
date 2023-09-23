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


CI.df <- readRDS(file='CIs.RDS')

#ggplot(CI.df,aes(concept.ID,medians,color=fam.ID),alpha=.3) + geom_pointrange(aes(ymin = lower, ymax = upper))

#ggplot(CI.df,aes(concept.ID,medians),alpha=.3) + geom_pointrange(aes(ymin = lower, ymax = upper),size=.25) + 
#  geom_hline(yintercept = 1,linetype="dashed") + 
#  facet_grid2(vars(fam.ID),scales="free") + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))


CI.df$greater <- ifelse(CI.df$lower > 1, TRUE, FALSE)

xtabs( ~ rate.type + fam.ID + greater, CI.df)
xtabs( ~ fam.ID + greater + rate.type, CI.df)

paste(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,1][,1],rowSums(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,1]),sep='/')


birth.rate.string <- paste(paste(rownames(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,1]),paste(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,1][,1],rowSums(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,1]),sep='/'),sep=': '),collapse=', ')
death.rate.string <- paste(paste(rownames(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,2]),paste(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,2][,1],rowSums(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,2]),sep='/'),sep=': '),collapse=', ')
gain.rate.string <- paste(paste(rownames(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,3]),paste(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,3][,1],rowSums(xtabs( ~ fam.ID + greater + rate.type, CI.df)[,,3]),sep='/'),sep=': '),collapse=', ')

write('%<*birthRateIndividual>',file='cognate-concept-CIs.tex',append=TRUE)
write(birth.rate.string,file='cognate-concept-CIs.tex',append=TRUE)
write('%</birthRateIndividual>',file='cognate-concept-CIs.tex',append=TRUE)

write('%<*deathRateIndividual>',file='cognate-concept-CIs.tex',append=TRUE)
write(death.rate.string,file='cognate-concept-CIs.tex',append=TRUE)
write('%</deathRateIndividual>',file='cognate-concept-CIs.tex',append=TRUE)

write('%<*gainRateIndividual>',file='cognate-concept-CIs.tex',append=TRUE)
write(gain.rate.string,file='cognate-concept-CIs.tex',append=TRUE)
write('%</gainRateIndividual>',file='cognate-concept-CIs.tex',append=TRUE)

