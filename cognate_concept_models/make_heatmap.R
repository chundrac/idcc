library(reshape2)
library(ggplot2)
library(ggridges)
require(ggh4x)
require(RColorBrewer)

my.objects <- readRDS('posterior_matrices.RDS')

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

birth.mats <- my.objects[[1]]
gain.mats <- my.objects[[2]]
death.mats <- my.objects[[3]]
all.concepts <- my.objects[[4]]

northeuralex <- read.csv("northeuralex-0.9-concept-data.tsv",sep='\t')
ranking <- northeuralex$position_in_ranking
names(ranking) <- northeuralex$concepticon
brewer.scale <- colorRampPalette(brewer.pal(9,"YlGnBu"))(length(ranking))
rank.colors <- brewer.scale[ranking]
names(rank.colors) <- northeuralex$concepticon

my.order <- rank(ranking[gsub(' ','_',all.concepts)])
brewer.scale <- colorRampPalette(brewer.pal(9,"YlGnBu"))(length(my.order))
rank.colors <- brewer.scale[my.order]
names(rank.colors) <- names(my.order)

#for (i in 1:length(fams)) {
#  mat.i <- death.mats[[i]]
#  names.i <- names(sort(my.order))
#  names.i <- names.i[names.i %in% rownames(mat.i)]
#  mat.i <- mat.i[names.i,names.i]
#  mat.i[!upper.tri(mat.i)] <- NA
#}

#mat.melt <- melt(mat.i, na.rm = TRUE)

#mat.melt$cutoff <- rep(.05,nrow(mat.melt))

#mat.melt$cutoff[mat.melt$value >= .95] <- 1

#mat.melt <- na.omit(mat.melt)

#ggplot(data = mat.melt, aes(Var2, Var1)) + geom_tile(aes(fill = cutoff)) + 
#  #geom_text(aes(label = round(value, 3))) + 
#  scale_y_discrete(limits=rev(levels(mat.melt$Var1))) + 
#  ##scale_fill_manual(values = c("#F8766D1A","#F8766D4C","#F8766DE6","#00BFC41A","#00BFC44C","#00BFC4E6"))
#  #scale_fill_manual(name='Speed',values = c("#F8766D1A","#F8766D99","#F8766DE6","#00BFC41A","#00BFC499","#00BFC4E6")) + 
#  #theme_classic() + theme(axis.title.x=element_blank(),axis.title.y=element_blank(),legend.position=c(.8,.9))
#  theme_classic() + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

#ggplot(data = mat.melt, aes(Var2, Var1)) + geom_tile(aes(fill = value,alpha = cutoff)) + 
#  #geom_text(aes(label = round(value, 3))) + 
#  #scale_y_discrete(limits=rev(levels(mat.melt$Var1))) + 
#  ##scale_fill_manual(values = c("#F8766D1A","#F8766D4C","#F8766DE6","#00BFC41A","#00BFC44C","#00BFC4E6"))
#  #scale_fill_manual(name='Speed',values = c("#F8766D1A","#F8766D99","#F8766DE6","#00BFC41A","#00BFC499","#00BFC4E6")) + 
#  #theme_classic()# + theme(axis.title.x=element_blank(),axis.title.y=element_blank(),legend.position=c(.8,.9))
#  theme_classic() + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + coord_flip()


mat.melt.all <- NULL
for (i in 1:length(fams)) {
  mat.i <- birth.mats[[i]]
  names.i <- names(sort(my.order))
  names.i <- names.i[names.i %in% rownames(mat.i)]
  mat.i <- mat.i[names.i,names.i]
  #mat.i[!upper.tri(mat.i)] <- NA
  ##mat.i[lower.tri(mat.i)] <- NA
  mat.melt <- melt(mat.i, na.rm = TRUE)
  mat.melt$cutoff <- rep(.05,nrow(mat.melt))
  mat.melt$cutoff[mat.melt$value >= .95] <- 1
  mat.melt$family <- rep(fam.labels[i],nrow(mat.melt))
  mat.melt$type <- rep('Birth rate',nrow(mat.melt))
  mat.melt.all <- rbind(mat.melt.all,mat.melt)
  mat.i <- gain.mats[[i]]
  names.i <- names(sort(my.order))
  names.i <- names.i[names.i %in% rownames(mat.i)]
  mat.i <- mat.i[names.i,names.i]
  #mat.i[!upper.tri(mat.i)] <- NA
  ##mat.i[lower.tri(mat.i)] <- NA
  mat.melt <- melt(mat.i, na.rm = TRUE)
  mat.melt$cutoff <- rep(.05,nrow(mat.melt))
  mat.melt$cutoff[mat.melt$value >= .95] <- 1
  mat.melt$family <- rep(fam.labels[i],nrow(mat.melt))
  mat.melt$type <- rep('Mutation rate',nrow(mat.melt))
  mat.melt.all <- rbind(mat.melt.all,mat.melt)
  mat.i <- death.mats[[i]]
  names.i <- names(sort(my.order))
  names.i <- names.i[names.i %in% rownames(mat.i)]
  mat.i <- mat.i[names.i,names.i]
  #mat.i[!upper.tri(mat.i)] <- NA
  ##mat.i[lower.tri(mat.i)] <- NA
  mat.melt <- melt(mat.i, na.rm = TRUE)
  mat.melt$cutoff <- rep(.05,nrow(mat.melt))
  mat.melt$cutoff[mat.melt$value >= .95] <- 1
  mat.melt$family <- rep(fam.labels[i],nrow(mat.melt))
  mat.melt$type <- rep('Loss rate',nrow(mat.melt))
  mat.melt.all <- rbind(mat.melt.all,mat.melt)
}

cutoff <- rep(NA,nrow(mat.melt.all))

cutoff[mat.melt.all$value < .05] <- 'Greater in $<$5\\% of samples'
cutoff[mat.melt.all$value > .95] <- 'Greater in $>$95\\% of samples'
cutoff[is.na(cutoff)] <- 'No decisive difference'

mat.melt.all$Cutoff <- cutoff

mat.melt <- mat.melt.all

mat.melt$type <- factor(mat.melt$type,levels=c(
  'Birth rate',
  'Mutation rate',
  'Loss rate'
))

#ggplot(data = mat.melt, aes(Var2, Var1)) + geom_tile(aes(fill = cutoff)) + 
#  #geom_text(aes(label = round(value, 3))) + 
#  scale_y_discrete(limits=rev(levels(mat.melt$Var1))) + 
#  scale_fill_manual(values=c('gray','pink','lightblue')) + 
#  ##scale_fill_manual(values = c("#F8766D1A","#F8766D4C","#F8766DE6","#00BFC41A","#00BFC44C","#00BFC4E6"))
#  #scale_fill_manual(name='Speed',values = c("#F8766D1A","#F8766D99","#F8766DE6","#00BFC41A","#00BFC499","#00BFC4E6")) + 
#  #theme_classic() + theme(axis.title.x=element_blank(),axis.title.y=element_blank(),legend.position=c(.8,.9))
#  theme_classic() + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + 
#  facet_grid2(rows=vars(type),cols=vars(family), scales="free")



tikzDevice::tikz('pairwise_CI_cutoffs.tex',width=7,height=3)
ggplot(data = mat.melt, aes(Var2, Var1)) + ggrastr::geom_tile_rast(aes(fill = Cutoff)) + 
  #geom_text(aes(label = round(value, 3))) + 
  scale_y_discrete(limits=rev(levels(mat.melt$Var1))) + 
  scale_fill_manual(values=c('#56B4E9','#E69F00','lightgray')) + 
  ##scale_fill_manual(values = c("#F8766D1A","#F8766D4C","#F8766DE6","#00BFC41A","#00BFC44C","#00BFC4E6"))
  #scale_fill_manual(name='Speed',values = c("#F8766D1A","#F8766D99","#F8766DE6","#00BFC41A","#00BFC499","#00BFC4E6")) + 
  #theme_classic() + theme(axis.title.x=element_blank(),axis.title.y=element_blank(),legend.position=c(.8,.9))
  theme_classic() + theme(axis.title.x=element_blank(), axis.title.y=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank(), axis.text.y=element_blank(),  axis.ticks.y=element_blank()) + 
  facet_grid2(rows=vars(type),cols=vars(family), scales="free", independent = T)

dev.off()





