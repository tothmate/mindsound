library(seewave)
s <- read.table("~/Documents/mindsound/sitting_eating", dec=",", col.names=c("t", "u"))
eat = s$u
s <- read.table("~/Documents/mindsound/sitting_deepbreath", dec=",", col.names=c("t", "u"))
bre = s$u
s <- read.table("~/Documents/mindsound/sitting_smiling", dec=",", col.names=c("t", "u"))
smi = s$u

spectro(bre, f=512, ovlp=0, flim=c(0, 0.05), osc=T)
spectro(eat, f=512, ovlp=99, flim=c(0, 0.05), osc=T)
spectro(smi, f=512, ovlp=99, flim=c(0, 0.05), osc=T)