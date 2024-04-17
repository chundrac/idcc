sims <- read.csv('simulations.csv',sep='\t')

prop.table(xtabs( ~ sims$label))

prop.table(xtabs( ~ sims[sims$label=='TP',]$true.in.CI))

extreme <- c()

sub.df <- sims[sims$label=='TP' & sims$true.in.CI==0,]

for (i in 1:nrow(sub.df)) {
  if (sub.df[i,]$ratio > 1) {
    if (sub.df[i,]$hdi.upper < sub.df[i,]$ratio) {
      extreme <- c(extreme,0)
    }
    else {
      extreme <- c(extreme,1)
    }
  }
  if (sub.df[i,]$ratio < 1) {
    if (sub.df[i,]$hdi.lower > sub.df[i,]$ratio) {
      extreme <- c(extreme,0)
    }
    else {
      extreme <- c(extreme,1)
    }
  }
}

sub.df$extreme <- extreme

prop.table(xtabs( ~ sub.df$extreme))