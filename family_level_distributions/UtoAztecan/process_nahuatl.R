languages <- read.csv('~/Downloads/intercontinental-dictionary-series-ids-4a8810a/cldf/languages.csv')

forms <- read.csv('~/Downloads/intercontinental-dictionary-series-ids-4a8810a/cldf/forms.csv')

merged <- merge(languages,forms,by.x='ID',by.y='Language_ID')

merged <- merged[merged$Name=='Nahuatl (Sierra de Zacapoaxtla variety)',]

writeLines(as.character(merged$Form),con='Nahuatl_wordlist.txt')