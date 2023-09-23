languages <- read.csv('~/Downloads/wold_dataset.cldf/languages.csv')

forms <- read.csv('~/Downloads/wold_dataset.cldf/forms.csv')

merged <- merge(languages,forms,by.x='ID',by.y='Language_ID')

merged <- merged[merged$Name=='Yaqui',]

writeLines(as.character(merged$Form),con='Yaqui_wordlist.txt')