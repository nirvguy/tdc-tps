# Makefile for LaTeX files

PDFLATEX=pdflatex
INFORME=informe.pdf
SRC=informe.tex introduccion.tex metodologia.tex resultados.tex conclusiones.tex

all: $(INFORME)

$(INFORME): $(SRC) $(TESTS)
	$(PDFLATEX) $<
	$(PDFLATEX) $<

clean:
	rm -f *.out *.toc *.log $(INFORME)

.PHONY: all clean
