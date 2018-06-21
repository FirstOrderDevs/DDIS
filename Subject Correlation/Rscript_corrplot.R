install.packages('corrplot', repos='http://cran.us.r-project.org')
install.packages('Hmisc', repos='http://cran.us.r-project.org')


grade_6 <- read.csv("/home/adeesha/Documents/Research/grade_6_performance.csv")
grade_7 <- read.csv("/home/adeesha/Documents/Research/grade_7_performance.csv")
grade_8 <- read.csv("/home/adeesha/Documents/Research/grade_8_performance.csv")

library("Hmisc")

res_6 <- rcorr(as.matrix(grade_6))
res_7 <- rcorr(as.matrix(grade_7))
res_8 <- rcorr(as.matrix(grade_8))

library(corrplot)

pdf("grade_6_correlation.pdf")
corrplot(res_6$r, type="upper", order="alphabet",tl.col="black",cl.lim=c(0.4,1),is.corr=FALSE,title="Grade 6",p.mat = res_6$P,sig.level = 0.01, insig = "blank",mar=c(0,0,2,0))
dev.off()

pdf("grade_7_correlation.pdf")
corrplot(res_7$r, type="upper", order="alphabet",tl.col="black",cl.lim=c(0.4,1),is.corr=FALSE,title="Grade 7",p.mat = res_7$P,sig.level = 0.01, insig = "blank",mar=c(0,0,2,0))
dev.off()

pdf("grade_8_correlation.pdf")
corrplot(res_8$r, type="upper", order="alphabet",tl.col="black",cl.lim=c(0.4,1),is.corr=FALSE,title="Grade 8",p.mat = res_8$P,sig.level = 0.01, insig = "blank",mar=c(0,0,2,0))
dev.off()

