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


clts <- read.csv('clts-2.2.0/data/sounds.tsv',sep='\t')

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
CONCEPTS <- readLines('swadesh_100.txt')

all.langs <- c()
all.fams <- c()

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
  
  all.langs <- c(all.langs,languages)
  
  all.fams <- c(all.fams,rep(tree.file,length(languages)))
  
}

glottolog <- read.csv('glottolog_language_metadata.csv')
rownames(glottolog) <- glottolog$Glottocode

glottolog <- glottolog[all.langs,]

all.fams[all.fams=='dravidian'] <- 'Dravidian'
all.fams[all.fams=='indoeuropean'] <- 'Indo-European'
all.fams[all.fams=='sinotibetan'] <- 'Sino-Tibetan'
all.fams[all.fams=='turkic'] <- 'Turkic'
all.fams[all.fams=='utoaztecan'] <- 'Uto-Aztecan'

#glottolog$Family_ID <- sapply(all.fams,function(x){paste(toupper(substr(x,1,1)),substr(x,2,nchar(x)),sep='')})

glottolog$Family_ID <- all.fams

lonlat <- glottolog[,c('Longitude','Latitude','Family_ID')]

lonlat <- na.omit(lonlat)

lonlat$Family <- lonlat$Family_ID

require(ggplot2)
require(ggrepel)

library(rgeos)
library(rgdal) # must be loaded after rgeos! reversed sequence leads to a full crach
require(geosphere)
library(dplyr)

library(ggrastr)
library(tikzDevice)

project_data <-  function(
  df,  # a dataframe with Longitude, Latitude, and  data
  base = "~/Documents/110m_physical", # a base map file path
  base_layer = "ne_110m_land", # name of the layer in the base
  projection = "+proj=eqearth +wktext"
) {
  
  #### Settings:
  proj_setting <- paste(projection, "+lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
  
  #### Base map
  world.sp <- readOGR(dsn = base, layer = base_layer, verbose = F)
  
  # shift central/prime meridian towards west - positive values only
  shift <- 180 + 30
  # create "split line" to split polygons
  WGS84 <- CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")
  split.line = SpatialLines(list(Lines(list(Line(cbind(180 - shift,c(-90,90)))), ID = "line")),
                            proj4string = WGS84)
  
  # intersect line with country polygons
  line.gInt <- gIntersection(split.line, world.sp)
  
  # create a very thin polygon (buffer) out of the intersecting "split line"
  bf <- suppressWarnings(gBuffer(line.gInt, byid = TRUE, width = 0.000001))
  
  # split country polygons using intersecting thin polygon (buffer)
  world.split <- gDifference(world.sp, bf, byid = TRUE)
  
  # transform split country polygons in a data table that ggplot can use
  world.sh.tr.df <- fortify(world.split)
  
  # Shift coordinates
  world.sh.tr.df$long.new <- world.sh.tr.df$long + shift
  world.sh.tr.df$long.new <- ifelse(world.sh.tr.df$long.new  > 180,
                                    world.sh.tr.df$long.new - 360, world.sh.tr.df$long.new)
  world.sh.tr.df[,c('X', 'Y')]  <- project(cbind(world.sh.tr.df$long.new, world.sh.tr.df$lat),
                                           proj = proj_setting)
  
  base_map.df <- subset(world.sh.tr.df, lat > -60 & lat < 85)
  
  #### Graticules
  b.box <- as(raster::extent(-180, 180, -90, 90), "SpatialPolygons")
  
  # assign CRS to box
  proj4string(b.box) <- WGS84
  
  # create graticules/grid lines from box
  grid <- gridlines(b.box,
                    easts  = seq(from = -180, to = 180, by = 20),
                    norths = seq(from = -90,  to = 90,  by = 10))
  
  # transform graticules from SpatialLines to a data frame that ggplot can use
  grid.df <- fortify(SpatialLinesDataFrame(sl = grid, data = data.frame(1:length(grid)),
                                           match.ID = FALSE))
  # assign matrix of projected coordinates as two columns in data table
  grid.df[, c("X","Y")]  <- project(cbind(grid.df$long, grid.df$lat),
                                    proj = gsub("lon_0=0", "lon_0=150", proj_setting))
  
  graticules.df <- subset(grid.df, lat > -60 & lat < 85)
  
  # create labels for graticules
  grid.lbl <- labels(grid, side = 1:4)
  
  # transform labels from SpatialPointsDataFrame to a data table that ggplot can use
  grid.lbl.df <- data.frame(grid.lbl@coords, grid.lbl@data)
  
  # add degree sign and clean up
  grid.lbl.df$labels <- ifelse(grepl("S|W", grid.lbl.df$labels),
                               paste0("-", gsub("\\*degree\\*?([EWSN])?", "", grid.lbl.df$labels), "°"),
                               paste0(gsub("\\*degree\\*?([EWSN])?", "", grid.lbl.df$labels), "°")
  )
  
  # grid.lbl.df$labels <- paste0(grid.lbl.df$labels,"°")
  # grid.lbl.df$labels <- gsub("\\*degree\\*?([EWSN])?", "", grid.lbl.df$labels, perl = T)
  
  # adjust coordinates of labels so that they fit inside the globe
  grid.lbl.df$long <- ifelse(grid.lbl.df$coords.x1 %in% c(-180,180),
                             grid.lbl.df$coords.x1*175/180, grid.lbl.df$coords.x1)
  
  grid.lbl.df$lat <-  ifelse(grid.lbl.df$coords.x2 %in% c(-90,90),
                             grid.lbl.df$coords.x2*60/90, grid.lbl.df$coords.x2)
  grid.lbl.df[, c("X","Y")] <-  project(cbind(grid.lbl.df$long, grid.lbl.df$lat),
                                        proj = gsub("lon_0=0", "lon_0=150", proj_setting))
  grid_label.df <- rbind(subset(grid.lbl.df, pos == 2 & coords.x2 > -70 &
                                  !labels %in% c("-60°", "90°")),
                         subset(grid.lbl.df, pos == 1 & !(abs(coords.x1) == 180 & coords.x2 == -90)))
  
  #### Data
  
  if (any(names(df) %in% c('longitude')) | any(names(df) %in% c('latitude'))) {
    df$Longitude <- df$longitude
    df$Latitude <- df$latitude
  }
  
  if (any(names(df) %in% c('lon')) | any(names(df) %in% c('lat'))) {
    df$Longitude <- df$lon
    df$Latitude <- df$lat
  }
  
  df.sp <- SpatialPointsDataFrame(df[,c("Longitude","Latitude")], df,
                                  proj4string = CRS("+proj=longlat +datum=WGS84"))
  
  df.sp.tr <- spTransform(df.sp, CRS(gsub("lon_0=0", "lon_0=150", proj_setting)))
  
  data.df <- data.frame(df.sp.tr)
  
  data.df$X <- data.df$Longitude.1
  data.df$Y <- data.df$Latitude.1
  
  return(list(base_map = base_map.df,
              graticules = graticules.df,
              graticule_labels = grid_label.df,
              data = data.df))
  
}

df.g.coords <- project_data(df = lonlat,
                            base = "~/Documents/Documents/110m_physical",
                            base_layer = "ne_110m_land",
                            projection = "+proj=eqearth +wktext"
                            # projection = "+proj=robin"
)


g <- ggplot() + theme_void() + 
  
  geom_polygon(data = df.g.coords$base_map,
               aes(x = X, y = Y, group = group),
               fill = 'lightgray',
               color = 'black',
               size = .1
  ) + 
  
  geom_path(data = df.g.coords$graticules,
            aes(x = X, y = Y, group = group),
            linetype = 'dotted',
            colour = 'grey',
            size = .25
  ) + 
  geom_point(data=df.g.coords$data,aes(x = X, y = Y, color=Family),alpha=.5)


tikz('language-locations-cognate-concept.tex',height=7,width=7)
g
dev.off()


