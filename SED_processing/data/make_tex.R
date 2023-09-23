require(ggtree)
require(phytools)
require(phangorn)
require(ggplot2)

trees <- read.nexus('semitic-1k.nex')

tree <- maxCladeCred(trees)

data.df <- read.csv('character_data.tsv',row.names=1,sep='\t')

tree <- keep.tip(tree,rownames(data.df))

tree$tip.label <- gsub('_',' ',tree$tip.label)

tikzDevice::tikz('semitic-tree.tex')

ggtree(tree) + geom_tiplab(size=2.5,align=TRUE)

dev.off()