#!/bin/bash
mkdir -p jurassic
pipenv run ./jurassic_tm.py --dfd | dot -Tpng -o jurassic/sample.png
pipenv run ./jurassic_tm.py --report docs/basic_template.md | pandoc -f markdown -t html > jurassic/report.html

#PLANTUML_PATH=plantuml.jar
#pipenv run ./jurassic_tm.py --seq | java -Djava.awt.headless=true -jar $PLANTUML_PATH -tpng -pipe > jurassic/seq.png