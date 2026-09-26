# Build with a local TeX Live:   make
# Or with Docker (no local TeX): make docker
all:
	pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
docker:
	docker run --rm -v "$(CURDIR)":/work -w /work texlive/texlive:latest-small sh -c "pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex"
clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc
