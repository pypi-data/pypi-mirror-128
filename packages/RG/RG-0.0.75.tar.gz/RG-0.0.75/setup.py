import setuptools


setuptools.setup(
    name="RG",
    version="0.0.75",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    url="https://www.usherbrooke.ca/gchimiquebiotech/departement/professeurs/ryan-gosselin/",
    packages=["RG"],
    description="Ryan's go-to Python functions",
    long_description="Miscellaneous functions:\
    \n\
    \nMiscellaneous functions:\
    \nreset, loatmat, xlsread\
    \n\
    \nWork with data:\
    \nregress, R2, VIF, lags, pcorrcoef, correlated_matrix, interactions, SAM\
    \n\
    \nDynamic time warping:\
    \nDTW,DTW_batch\
    \n\
    \nPlot data:\
    \ncolorspectra,axaline,corr_reorder\
    \n\
    \nStatistical functions\
    \nnormplot\
    \n\
    \nMultivariate data analysis\
    \nPCA, PLS, VIP, mbPLS, LDA, PCA_ellipse, ICA, MCR, NPLS_cal, NPLS_val\
    \n\
    \nSpectral pretreatments\
    \ncenter, autoscale, SNV, MSC, EMSC, Savitzky Golay, detrend, baseline",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)