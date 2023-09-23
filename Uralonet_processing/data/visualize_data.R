require(ggtree)
require(phytools)
require(phangorn)
require(ggplot2)

trees <- read.nexus('uralic-10k.nex')

data.df <- read.csv('character_data.tsv',row.names=1,sep='\t')

data.full <- read.csv('character_data_string.tsv',row.names=1,sep='\t',check.names = F,quote="")

tree <- maxCladeCred(trees)

J = length(unique(lapply(strsplit(colnames(data.df),'\\.'),function(x){x[length(x)]})))

D = ncol(data.df)/J

tree <- keep.tip(tree,which(tree$tip.label %in% rownames(data.df)))

data.df <- data.df[tree$tip.label,]

data.full <- data.full[tree$tip.label,]

plottree <- function(d) {
  etymon <- colnames(data.full)[d]
  sub.df <- data.df[,((J*d)-(J-1)):(J*d)]
  colnames(sub.df) <- c('absent','-IC','+IC')
  sub.df.full <- data.full[,d]
  sub.df.full[is.na(sub.df.full)] <- ''
  rnames <- paste(tree$tip.label,sub.df.full,sep='\t')
  rownames(sub.df) <- rnames
  
  tree$tip.label <- rnames
  
  g <- ggtree(tree) + geom_tiplab(size=2.5,align=TRUE) + ggtitle(etymon)
  
  gheatmap(g,apply(sub.df,2,as.factor), offset=1500, width=0.5, font.size=3, 
           colnames_angle=-45, hjust=0) + 
    scale_fill_manual(breaks=c("0","1"), 
                      #values=alpha(c("#00BFC4","#F8766D"),.25),name="trait")
                      values=alpha(c("lightgray","darkgray"),.25),name="trait")
}

d <- 1
while (d <= D) {
  #pdf(paste('plots/',d,'.pdf',sep=''))
  p <- plottree(d)
  p
  ggsave(filename = paste('../../data_plots/uralic/',d,'.pdf',sep=''), plot = p, device=cairo_pdf)
  #dev.off()
  d <- d + 1
}

#pdf('character-plots.pdf', onefile = TRUE)
#for (d in 1:D) {
#  plottree(d)
#}
#
#dev.off()