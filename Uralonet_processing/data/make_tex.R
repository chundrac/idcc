require(ggtree)
require(phytools)
require(phangorn)
require(ggplot2)

trees <- read.nexus('uralic-10k.nex')

tree <- maxCladeCred(trees)

data.df <- read.csv('character_data.tsv',row.names=1,sep='\t')

tree <- keep.tip(tree,rownames(data.df))

tree$tip.label <- gsub('_',' ',tree$tip.label)

tikzDevice::tikz('uralic-tree.tex')

ggtree(tree) + geom_tiplab(size=2.5,align=TRUE)

dev.off()