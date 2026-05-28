# Go deeper: Longitudinal and time-series data

**If you want to understand longitudinal visualization better before moving on:**

- [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/), Chapter 13 "Visualizing time series and other functions of an independent variable," is the most accessible introduction to time-series chart construction. The discussion of when to draw a line vs when to add points and how to handle multiple series on a shared axis covers the decisions this track presents.
- The [Datawrapper Academy](https://academy.datawrapper.de/) chart-type articles are short, well-written, and free. The articles on line charts and on annotated time series describe the annotation patterns the track uses (vertical reference lines for medication changes, shaded bands for reference ranges).

**If you want to see this applied clinically:**

- The [BMJ Statistics Notes series](https://www.bmj.com/specialties/statistics-notes) is the canonical free reference for clinical chart construction. The notes on "Plotting basic statistical data" and "Presenting statistical information" cover the choices clinical authors face when displaying longitudinal data. The full archive is available through PubMed Central.

**If you want to go significantly further:**

- [ggplot2: Elegant Graphics for Data Analysis](https://ggplot2-book.org/), free online by Hadley Wickham, has the most rigorous treatment of layered grammar for time-series charts. Chapter 4 "Collective geoms" addresses the cohort-of-trajectories pattern (multiple patients on one chart) and Chapter 5 "Statistical summaries" addresses the smoothing decisions the track presents.
