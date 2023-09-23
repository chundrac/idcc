require(ggtree)
require(phytools)
require(phangorn)
require(ggplot2)

trees <- read.nexus('austronesian-mapped.nex')

tree <- maxCladeCred(trees)

data.df <- read.csv('character_data.tsv',row.names=1,sep='\t')

tree <- keep.tip(tree,rownames(data.df))

tikzDevice::tikz('austronesian-tree.tex')

ggtree(tree) + geom_tiplab(size=2.5,align=TRUE)

dev.off()