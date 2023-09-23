require(phytools)
require(phangorn)

set.seed(1234)

fam = commandArgs(trailingOnly = TRUE)[1]

fams <- c('austronesian','semitic','uralic')

fam.id <- which(fams==fam)

datapaths <- c(
  '../ACD_processing/data/',
  '../SED_processing/data/',
  '../Uralonet_processing/data/'
)

treepaths <- c(
  '../ACD_processing/data/austronesian-mapped.nex',
  '../SED_processing/data/semitic-1k.nex',
  '../Uralonet_processing/data/uralic-10k.nex'
)

datapath <- datapaths[fam.id]
treepath <- treepaths[fam.id]

root.to.singleton<-function(tree){
  if(!inherits(tree,"phylo"))
    stop("tree should be object of class \"phylo\".")
  if(!is.null(tree$root.edge)){
    tree$edge[tree$edge>Ntip(tree)]<-
      tree$edge[tree$edge>Ntip(tree)]+1
    if(attr(tree,"order")%in%c("postorder","pruningwise")){
      tree$edge<-rbind(tree$edge,c(1,2)+Ntip(tree))
      tree$edge.length<-c(tree$edge.length,tree$root.edge)
    } else {
      tree$edge<-rbind(c(1,2)+Ntip(tree),tree$edge)
      tree$edge.length<-c(tree$root.edge,tree$edge.length)
    }
    tree$root.edge<-NULL
    tree$Nnode<-tree$Nnode+1
    if(!is.null(tree$node.label)) 
      tree$node.label<-c("",tree$node.label)
  }
  return(tree)
}

get.proto.mrca <- function(tree,x) {
  present <- which(x[1:(length(tree$tip.label)),1] != 1)
  mrca.x <- getMRCA(tree,present)
  return(mrca.x)
}

get.birth.branches <- function(tree,x) {
  sites <- c()
  C <- length(which(x[1:(length(tree$tip.label)),1] != 1))
  for (i in length(tree$tip.label):(length(tree$tip.label)+tree$Nnode)) {
    y <- getDescendants(tree,i)
    y <- y[y<=length(tree$tip.label)]
    if (length(which(x[tree$tip.label[y],1] != 1)) == C) {
      sites <- c(sites,which(tree$edge[,2]==i))
    }
  }
  return(sites)
}

data.df <- read.csv(paste(datapath,'character_data.tsv',sep=''),row.names=1,sep='\t')

trees <- read.nexus(treepath)

etymon.key <- read.csv(paste(datapath,'etymon_data.tsv',sep=''),sep='\t',header=F)

J = length(unique(lapply(strsplit(colnames(data.df),'\\.'),function(x){x[length(x)]})))
D = ncol(data.df)/J

patterns <- apply(data.df,2,function(x){if (1 %in% x) {1} else {0}})
dim(patterns) <- c(J,D)
patterns <- t(patterns)
patterns <- patterns[,2:J]

P <- apply(patterns,1,function(x){if (all(x == c(1,1))) {1} else if (all(x == c(1,0))) {2} else if (all(x == c(0,1))) {3}})

data.list <- list()

for (i in 1:25) {
  
  print(i)
  
  s <- sample(1:length(trees),1)
  tree <- trees[[s]]
  tree <- keep.tip(tree,rownames(data.df))
  tree$root.edge <- 100
  tree <- reorder.phylo(tree,'pruningwise')
  tree <- root.to.singleton(tree)
  bin.states <- data.df[tree$tip.label,]
  
  xi <- list()
  xr <- list()
  
  for (d in 1:D) {
    bin.states.d <- bin.states[,((J*d)-(J-1)):(J*d)]
    
    mrca.d <- get.proto.mrca(tree,bin.states.d)
    tree.d <- bind.tip(tree, 'PROTO', edge.length=1, where=mrca.d)
    tree.d <- reorder.phylo(tree.d,'postorder')
    
    new.states <- rep(0,3)
    new.states[etymon.key[d,3]+2] <- 1
    bin.states.d <- rbind(bin.states.d,new.states)
    rownames(bin.states.d)[nrow(bin.states.d)] <- 'PROTO'
    
    bin.states.d <- bin.states.d[tree.d$tip.label,]
    
    bin.states.absent.d <- bin.states.d
    bin.states.absent.d[,1] <- 1
    bin.states.absent.d[,2] <- 0
    bin.states.absent.d[,3] <- 0
    rownames(bin.states.absent.d) <- rownames(bin.states.d)
    colnames(bin.states.absent.d) <- colnames(bin.states.d)
    bin.states.absent.d['PROTO',] <- bin.states.d['PROTO',]
    
    bin.states.d <- rbind(as.matrix(bin.states.d),matrix(1,nrow=tree.d$Nnode,ncol=ncol(bin.states.d)))
    bin.states.absent.d <- rbind(as.matrix(bin.states.absent.d),matrix(1,nrow=tree.d$Nnode,ncol=ncol(bin.states.absent.d)))
    
    parent <- tree.d$edge[,1]
    child <- tree.d$edge[,2]
    b.lens <- tree.d$edge.length/1000
    
    N <- length(unique(c(parent,child)))
    T <- length(child[which(!child %in% parent)])
    B=length(parent)
    sites.d <- get.birth.branches(tree.d,bin.states.d)
    sites.d <- ifelse(c(1:B) %in% sites.d, 2, 1)
    dim(bin.states.d) <- c(N*J)
    dim(bin.states.absent.d) <- c(N*J)
    
    
    xi[[d]] <- c(
      N,
      B,
      J,
      P[d],
      bin.states.d,
      bin.states.absent.d,
      child,
      parent,
      sites.d
    )
    
    b.lens[b.lens==0] <- .001
    
    xr[[d]] <- b.lens
    
  }
  
  xi <- matrix(unlist(xi),nrow=D,byrow = T) #dim y = 4+N*J+N*J+B+B+B
  xr <- matrix(unlist(xr),nrow=D,byrow = T) #dim y = B
  
  data.list[[i]] <- list(D=D,
                         N=N,
                         J=J,
                         B=B,
                         xi=xi,
                         xr=xr)
}

saveRDS(data.list,paste('processed_data/',fam,'_data_for_analysis.RDS',sep=''))
