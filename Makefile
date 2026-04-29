.PHONY: clean

MAIN = report

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	pdflatex $(MAIN).tex
	bibtex $(MAIN)
	pdflatex $(MAIN).tex
	pdflatex $(MAIN).tex

clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg

distclean: clean
	rm -f $(MAIN).pdf