require(phytools)
require(phangorn)
require(ggtree)

set.seed(1234)

detect.idcc <- function(s) {
  s <- gsub('ː','',s)
  s <- gsub('(. )\\1+','\\1',s)
  ss <- unlist(strsplit(s, ' + ', fixed = T))
  counter <- 0
  for (t in ss) {
    tt <- unlist(strsplit(t, ' '))
    tt <- sapply(tt,function(x){ if (grepl('/',x)) {unlist(strsplit(x,'/'))[2]} else {x}})
    tt <- tt[tt%in%consonants]
    if (length(tt) > 1) {
      for (i in 2:length(tt)) {
        if (tt[i] == tt[i-1]) {
          counter <- counter + 1
        }
      }
    }
  }
  if (counter > 0) {
    return(1)
  }
  else {
    return(0)
  }
}


clts <- read.csv('../clts-2.2.0/data/sounds.tsv',sep='\t')

consonants <- clts[clts$TYPE=='consonant',]$GRAPHEME

#dir('~/Documents/Documents/')

tree.samples <- c("dravidian",
                  "indoeuropean",
                  "sinotibetan",
                  "turkic",
                  "utoaztecan")

data.sources <- c("dravlex",
                  "dunnielex",
                  "sagartst",
                  "savelyevturkic",
                  "utoaztecan")

tree.key <- cbind(tree.samples,data.sources)

#CONCEPTS <- readLines('40_concept_list.txt')
CONCEPTS <- readLines('../swadesh_100.txt')

for (i in 1:length(tree.samples)) {
  
  tree.file <- tree.key[i,1]
  data.file <- tree.key[i,2]
  
  trees <- read.nexus(paste('~/Documents/Documents/cognacy-based-trees/phylogenetic-trees-v2/mapped_trees_2023/',tree.file,'.nex',sep=''))
  
  forms <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/forms.csv',sep=''))
  cognates <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/cognates.csv',sep=''))
  params <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/parameters.csv',sep=''))
  langs <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/languages.csv',sep=''))
  cog.data <- merge(forms,cognates,by.x='ID',by.y='Form_ID')
  cog.data <- merge(cog.data,params,by.x='Parameter_ID',by.y='ID')
  cog.data <- merge(cog.data,langs,by.x='Language_ID',by.y='ID')
  cog.data <- cog.data[,c('Glottocode','Concepticon_Gloss','Segments','Cognateset_ID')]
  cog.data$Cognateset_ID <- as.factor(paste(cog.data$Concepticon_Gloss,paste(tree.file,cog.data$Cognateset_ID,sep='_'),sep='|'))
  cog.data$IDCC <- sapply(cog.data$Segments,detect.idcc)
  
  cog.data$coding <- as.factor(paste(cog.data$Cognateset_ID,cog.data$IDCC))
  cog.data <- cog.data[cog.data$Concepticon_Gloss %in% CONCEPTS,]
  
  #CONCEPTS <- sort(unique(cog.data$Concepticon_Gloss))
  
  data.df <- NULL
  
  languages <- levels(cog.data$Glottocode)
  
  print(languages)
  
  for (concept in CONCEPTS) {
    
    if (concept %in% cog.data$Concepticon_Gloss) {
      
      cog.data.curr <- cog.data[cog.data$Concepticon_Gloss==concept,]
      cog.data.curr <- droplevels(cog.data.curr)
      #levels(cog.data.curr$coding) <- expand.grid(cog.data.curr$Cognateset_ID,c(0,1))
      comb.pairs <- expand.grid(c(0,1),levels(cog.data.curr$Cognateset_ID))
      comb.pairs <- paste(comb.pairs[,2],comb.pairs[,1],sep=' ')
      #levels(cog.data.curr$coding) <- comb.pairs
      
      cog.data.bin <- to.matrix(cog.data.curr$coding,seq=comb.pairs)
      rownames(cog.data.bin) <- cog.data.curr$Glottocode
      cog.data.bin <- t(sapply(by(cog.data.bin,rownames(cog.data.bin),colSums),identity))
      cog.data.bin[cog.data.bin >= 1] <- 1
      curr.names <- rownames(cog.data.bin)
      cog.data.bin <- rbind(cog.data.bin,matrix(0,nrow=length(which(!languages %in% curr.names)),ncol=ncol(cog.data.bin)))
      rownames(cog.data.bin) <- c(curr.names,languages[!languages %in% curr.names])
      
      missing <- which(rowSums(cog.data.bin)==0)
      
      cog.data.bin.new <- NULL
      
      D <- ncol(cog.data.bin)/2
      
      for (d in 1:D) {
        char <- cog.data.bin[,((d-1)*2+1):(d*2)]
        char <- cbind(ifelse(rowSums(char)==0,1,0),char)
        colnames(char)[1] <- paste(levels(cog.data.curr$Cognateset_ID)[d],'absent')
        cog.data.bin.new <- cbind(cog.data.bin.new,char)
      }
      
      absent <- which(colSums(cog.data.bin.new)==0)
      
      cog.data.bin.new[missing,] <- 1
      rownames(cog.data.bin.new) <- rownames(cog.data.bin)
      languages[languages==''] <- 'dummy'
      rownames(cog.data.bin.new)[rownames(cog.data.bin.new)==''] <- 'dummy'
      cog.data.bin.new <- cog.data.bin.new[languages,]
      
      cog.data.bin.new[,absent] <- 0
      
      data.df <- cbind(data.df,cog.data.bin.new)
      
    }
    
  }
  
  J = length(unique(lapply(strsplit(colnames(data.df),' '),function(x){x[length(x)]})))
  D = ncol(data.df)/J
  
  patterns <- apply(data.df,2,function(x){if (1 %in% x) {1} else {0}})
  dim(patterns) <- c(J,D)
  patterns <- t(patterns)
  patterns <- patterns[,2:J]
  
  P <- apply(patterns,1,function(x){if (all(x == c(1,1))) {1} else if (all(x == c(1,0))) {2} else if (all(x == c(0,1))) {3}})
  
  data.list <- list()
  
  tree <- maxCladeCred(trees)
  tree <- keep.tip(tree,which(tree$tip.label %in% rownames(data.df)))
  
  tikzDevice::tikz(paste('MCC_trees/',tree.file,'-tree.tex',sep=''))
  
  ggtree(tree) + geom_tiplab(size=1.5,align=TRUE)
  
  dev.off()
  
}