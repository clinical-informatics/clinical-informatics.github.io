## Go deeper

**If you want to understand the tidy data idea before moving on:**
- Hadley Wickham's 2014 paper "Tidy Data," published in the Journal of Statistical Software. The paper that named the pattern. Short (twenty-three pages), readable, and the source the rest of modern data tooling cites when it explains why "one observation per row, one variable per column, one value per cell" is the shape you want. Examples are in R but the pattern is language-independent; you read it for the framing, not the code. [jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10)

**If you want to see the reshaping moves applied in the language you actually use:**
- The pandas user guide chapter on "Reshaping and pivot tables." Walks every operation this track touched (melt, pivot, stack, unstack, pivot_table, wide_to_long, explode) with worked examples and the conceptual diagrams that make the moves intuitive. The clinical examples in this track are deliberately simple; the pandas guide is where you go for the full vocabulary and the edge cases (duplicate keys, multi-level columns, hierarchical reshaping). [pandas.pydata.org/docs/user_guide/reshaping.html](https://pandas.pydata.org/docs/user_guide/reshaping.html)

**If you want to go significantly further:**
- Chapter 12 of *R for Data Science* (first edition) by Hadley Wickham and Garrett Grolemund, available free online. The chapter applies the tidy data framework to real datasets with worked-out cleaning examples in R's tidyverse. The R code is not the point. The point is seeing the framework applied to a half-dozen real-world messes in different domains, which is how you build a vocabulary for spotting the same patterns in clinical data. [r4ds.had.co.nz/tidy-data.html](https://r4ds.had.co.nz/tidy-data.html)
