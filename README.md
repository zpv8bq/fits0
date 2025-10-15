# fits 0

This repository contains some background examples leading up to our discussion of fitting data.  

- CLT.ipynb: example of Central Limit Theorem
- LeastSquareFit[ROOT].ipynb: notebooks describing the exercise using numpy/matplotlib [or ROOT] tools
- LSQFit.cpp(py): **starter code** for the Least Squares Fitting exercise (the .C version is deprecated, but you may run it in ROOT, eg root> .x leastsq.C)
- RandomMeasuresP1.C, RandomGaus.C, RandomMeasuresAndFitP1.C: code to generate movies linked to the class notes <br> Usage:
eg. in root: <br>
root> .X RandomMeasuresP1.C

You will turn in an updated version of either LSQFit.C or PSQFit.py containing your work and the plots in the exercise desc


Other files:
- PlottingReview.ipynb: a review of basic plot making in matplotlib and ROOT
- Interpolate.ipynb: Jupyter notebook illustrating the Lagrange interpolation and cubic splines.
- Lagrange.cpp[py]: code to perform a simple Lagrange interpolation
