acd.languages <- read.csv('../acd_data/acd_languages.csv')
acd.protoforms <- read.csv('../acd_data/acd_protoforms.csv')
acd.cognates <- read.csv('../acd_data/acd_cognates.csv')
acd.cognatesets <- read.csv('../acd_data/acd_cognatesets.csv')
acd.forms <- read.csv('../acd_data/acd_forms.csv')
acd.parameters <- read.csv('../acd_data/acd_parameters.csv')

acd.protoforms <- merge(acd.protoforms,acd.forms,by.x='Form_ID',by.y='ID')
acd.protoforms <- acd.protoforms[,c('ID','Proto_Language','Value')]

acd.merged <- merge(acd.forms,acd.parameters,by.x='Parameter_ID',by.y='ID')
acd.merged <- merge(acd.merged,acd.languages,by.x='Language_ID',by.y='ID')
acd.merged <- merge(acd.merged,acd.cognates,by.x='ID',by.y='Form_ID')
acd.merged <- merge(acd.merged,acd.cognatesets,by.x='Cognateset_ID',by.y='ID')

acd.merged <- acd.merged[,c('ID','Cognateset_ID','Glottocode','Value','Name.x','Form','Proto_Language.y','Reconstruction_ID')]

acd.merged <- merge(acd.merged,acd.protoforms,by.x='Reconstruction_ID',by.y='ID')

#acd.merged <- acd.merged[,c('ID','Cognateset_ID','Glottocode','Value','Name.x','Form','Proto_Language.y')]

acd.merged <- acd.merged[,c('ID','Cognateset_ID','Glottocode','Value.x','Name.x','Form','Proto_Language.y','Reconstruction_ID','Value.y','Proto_Language')]

colnames(acd.merged) <- c('ID','root_cognate_ID','glottocode','form','gloss','higher_order_reconstruction','higher_order_protolang','word_cognate_ID','lower_order_reconstruction','lower_order_protolang')

write.table(file='acd_merged.csv',acd.merged,quote = F,row.names = F,sep='\t')

#cognacy.table <- xtabs( ~ Cognateset_ID + basic, acd.merged)