# Lecture 9: historical market figures

Retrieved 13 October 2026. These are cropped excerpts of published charts,
not synthetic data or newly estimated volatility curves. Attribution and
methodological qualifications also appear in the lecture slides and notes.

## S&P 500 downside skew

- File: `spx_skew_2024-08-02_2024-08-05.png`
- Publisher: Cboe; author: Edward K. Tom.
- Report: *The VIX Index Decomposition*, 1 August 2025.
- Source: https://cdn.cboe.com/resources/vix/VIX-Decomposition-2025-08-01.pdf
- Location: PDF page 9, Exhibit 7; chart only.
- Observation dates: 2 and 5 August 2024, end of day.
- Tenor: 30 days, interpolated in variance from the relevant option expiries
  (method described on PDF page 8).
- Horizontal axis: SPX strike in index points.
- Vertical axis: annualized implied volatility in percent.
- Blue segments are puts; orange/red segments are calls. Pale and dark
  curves distinguish observation dates. They are not four separate tenors.
- The original exhibit heading erroneously says 2025. The chart title,
  legend, introductory discussion and surrounding text establish 2024.
  The crop keeps the correct chart title and legend; it excludes the
  erroneous exhibit heading. No plotted values or labels were changed.
- The put side is strongly skewed near the money; the far call wing also
  rises. The notes explicitly explain that skew and smile can coexist.
- Crop box in PDF points, lower-left coordinates: `40 228 532 506`.

## EUR/USD smile

- File: `eurusd_smile_2025-04-23.png`
- Author: Uwe Wystup, MathFinance AG.
- Article: *Why Digitals don't Have all Percentage Price Quotes*, 2025.
- Source: https://www.mathfinance.com/wp-content/uploads/2025/06/FX-Column_2025-07_Why-digitals-dont-have-percentage-prices.pdf
- Location: PDF page 2, Figure 2; chart only.
- Observation date: 23 April 2025.
- Tenor: six months.
- Original market data provider: ICE Data Services, Table 1 on page 1.
- Horizontal axis: strike in USD per EUR.
- Vertical axis: annualized implied volatility in percent.
- This is the author's educational parabolic interpolation in delta,
  converted to strike. The reference spot is deliberately fixed at 1.1000;
  the article says the actual spot had already risen further. Do not label
  1.1000 as the observed market spot or the curve as raw trade observations.
- Crop box in PDF points, lower-left coordinates: `140 557.92 450 749.92`.

## Reproducing the excerpts

After downloading the two linked PDFs, use Poppler `pdfseparate` to extract
page 9 of the Cboe report and page 2 of the MathFinance article. Run
`pdfcrop --bbox '40 228 532 506'` on the Cboe page and
`pdfcrop --bbox '140 557.92 450 749.92'` on the MathFinance page, passing
the respective input and output file paths. Render each crop with
`pdftoppm -singlefile -scale-to 2200 -png` and the input/output paths.
Rasterization prevents invisible text outside the crop from appearing in
the lecture PDFs' extracted text. All axes and curve labels are retained;
page prose and unrelated figures are omitted. The final lecture documents
compile offline using the two local PNG excerpts.
