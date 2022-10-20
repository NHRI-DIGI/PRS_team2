.libPaths("~/R/x86_64-redhat-linux-gnu-library/3.6")
library(dplyr)
library(stringr)
library(tidyr)
cat("load library complete.")
setwd('/NovaSeq_128/team2/HBOC/Data/')

HBOC_313_adjusted <- read.table("/NovaSeq_128/team2/HBOC/Data/paperAdjusted/HBOC_PGS000028_adjusted.txt", header = T, stringsAsFactors = FALSE)
cat("read paper complete.")

# Make all VCF lists
ff <- list.files(path="/NovaSeq_128/team2/HBOC/Data/test", full.names=TRUE)
cat(ff)
myfilelist <- lapply(ff, read.table, header = TRUE, fill = TRUE, stringsAsFactors = FALSE)
cat("lapply complete.")
names(myfilelist) <- list.files(path="/NovaSeq_128/team2/HBOC/Data/test", full.names=FALSE)
cat("vcf list complete.")

# Count scores
for (i in 1:length(myfilelist)) {
  Innerjoin <- HBOC_313_adjusted %>%
    inner_join(myfilelist[[i]], by = c("Chr" = "CHROM", "POS", "REF"), suffix = c("_pgs", "_vcf"))
  # replace NA with not match
  Innerjoin[, 6] <- str_match(Innerjoin[, 6], Innerjoin[, 4])
  # remove ALT_vcf = NA
  Innerjoin <- drop_na(Innerjoin)
  # Calculate score
  score <- Innerjoin %>%
    mutate(count_allele = case_when(
      str_count(Innerjoin[ , 7], "0") == 1 ~ 1,
      str_count(Innerjoin[ , 7], "0") == 0 ~ 2,
    ), score = OR * count_allele) %>%
    summarize(sum(score))
  write(paste(names(myfilelist[[i]][5]), sum(score), sep = "\t"), file = "score_PGS000028_list.csv", append = TRUE)
}
cat("well done!")
