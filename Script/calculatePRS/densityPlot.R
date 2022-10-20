# 註解掉的「程式碼」都可無視
library(tidyverse)
library(ggplot2)
library(dplyr)
library(ggpubr)

setwd('C:/Users/ken82/Desktop/digi-project-main/score')

# score density plot (雙峰圖)
pheno <- read.table("HBOC_513.txt", header = T, stringsAsFactors = FALSE) %>% 
  select("ID" = "FID", "PHENO" = "HBOC_513")

score <- read.table("score_PGS000004_list.csv", col.names = c("ID", "SCORE"), stringsAsFactors = FALSE)

score_pheno <- score %>%
  full_join(pheno, by = "ID") %>%
  mutate(Standardized_Score = scale(SCORE)) %>%
  mutate(PHENO = case_when(
    PHENO == 1 ~ "Control",
    PHENO == 2 ~ "Case"
  )) %>%
  mutate(PHENO = factor(PHENO, levels = c("Control", "Case")))
# print(score_pheno)
gd <- ggdensity(score_pheno, x = "Standardized_Score",
   add = "mean", rug = TRUE,
   color = "PHENO", fill = "PHENO",
   palette = c("#0073C2FF", "#FC4E07"))+theme(legend.title=element_blank()) + ggtitle("HBOC_PGS000004_PGS_score")

ggsave(plot = gd, filename=paste0("HBOC_PGS000004_PGS_score.tiff"), height = 4, width = 6)
