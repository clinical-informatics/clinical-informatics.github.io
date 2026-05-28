# Glossary: 08 Clinical visualization

The terms below appear in the four track notebooks and in the capstone. The curriculum-wide glossary lives in the [start-here repo](https://github.com/clinical-informatics/start-here/blob/main/GLOSSARY.md); terms unique to visualization are defined here.

**Confidence interval (CI).** An interval constructed to contain the population parameter on a stated proportion of repeated samples drawn from the same population. A 95% confidence interval contains the parameter in 95 of every 100 such samples. The width of the interval is determined by the sample standard error and the chosen confidence level.

**Dual axis.** A chart in which two distinct variables are plotted against two different y-axes that share a common x-axis. Dual-axis charts are easy to construct and easy to misread, since the relationship between the two y-scales is set by the chart author and not by the data.

**Encoding (visual encoding).** The mapping from a data field to a visual property of a mark. Position, color, length, area, and shape are the common visual encodings. The accuracy with which a reader can decode each one differs; position is the most accurate, area and color are the least.

**LOESS (locally estimated scatterplot smoothing).** A non-parametric regression technique that fits a smooth curve to a series by locally regressing on small subsets of the data. LOESS surfaces a trend without imposing a global functional form. Used on noisy longitudinal lab data when the underlying trajectory is the question.

**Prediction interval (PI).** An interval constructed to contain a single future observation on a stated proportion of repeats. A 95% prediction interval is wider than a 95% confidence interval on the same data, since it accounts for both the uncertainty in the population mean and the variability of an individual observation.

**Reference range.** The interval that contains the central 95% of values from a healthy reference population, typically reported as the central 95% (lower bound to upper bound) on the laboratory report. Reference ranges are population-level, not individual-level; an in-range value can still represent a deviation from a patient's own baseline.

**Sparkline.** A small, label-free line chart designed for inline use, typically inside a table cell. Sparklines are useful when the shape of a trend is more important than the exact values.

**Standard error (SE).** The standard deviation of a sample statistic. The standard error of the mean shrinks as the sample size grows, since adding observations refines the estimate of the population mean. SE is the basic uncertainty unit from which confidence intervals are constructed.

**Truncated axis.** An axis whose origin is set above zero (for the y-axis) or after the natural start of the time period (for the x-axis). A truncated y-axis exaggerates small absolute changes; a truncated x-axis can omit the part of the trajectory that gives context to a recent value.
