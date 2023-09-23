require(phytools)

set.seed(1234)

get.consonants <- function(s) {
  s <- gsub('ː','',s)
  s <- gsub('(. )\\1+','\\1',s)
  ss <- unlist(strsplit(s, ' + ', fixed = T))
  morphs <- c()
  for (i in 1:length(ss)) {
    t = ss[i]
    tt <- unlist(strsplit(t, ' '))
    tt <- sapply(tt,function(x){ if (grepl('/',x)) {unlist(strsplit(x,'/'))[2]} else {x}})
    tt <- tt[tt%in%consonants]
    tt <- paste(tt,collapse=' ')
    morphs <- c(morphs,tt)
  }
  return(paste(morphs,collapse=' + '))
}


clts <- read.csv('clts-2.2.0/data/sounds.tsv',sep='\t')

consonants <- clts[clts$TYPE=='consonant',]$GRAPHEME

data.sources <- c("dravlex",
                  "dunnielex",
                  "sagartst",
                  "savelyevturkic",
                  "utoaztecan")

#CONCEPTS <- readLines('40_concept_list.txt')
CONCEPTS <- readLines('swadesh_100.txt')

for (i in 1:length(data.sources)) {
  
  data.file <- data.sources[i]
  
  forms <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/forms.csv',sep=''))
  cognates <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/cognates.csv',sep=''))
  params <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/parameters.csv',sep=''))
  langs <- read.csv(paste('~/Documents/Documents/linguisticCharacterMatrices/lexibank/lexibank-analysed/raw/',data.file,'/cldf/languages.csv',sep=''))
  cog.data <- merge(forms,cognates,by.x='ID',by.y='Form_ID')
  cog.data <- merge(cog.data,params,by.x='Parameter_ID',by.y='ID')
  cog.data <- merge(cog.data,langs,by.x='Language_ID',by.y='ID')
  cog.data <- cog.data[,c('Glottocode','Concepticon_Gloss','Segments','Cognateset_ID')]
  cog.data$cons <- sapply(cog.data$Segments,get.consonants)
  cog.data <- cog.data[cog.data$Concepticon_Gloss %in% CONCEPTS,]
  
  cog.data <- cog.data[,c('Glottocode','Concepticon_Gloss','cons')]
  
  write.table(cog.data,file=paste('sound_change_simulations/datasets/',data.file,'.csv',sep=''),sep='\t',quote=F,row.names = F)
  
}

