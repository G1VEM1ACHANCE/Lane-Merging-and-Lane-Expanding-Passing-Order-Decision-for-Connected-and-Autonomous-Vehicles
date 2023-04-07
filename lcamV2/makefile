Numbers = 1 2 3 4 5 6 7 8 9 10
dir = ./*
ingen:
	for n in $(Numbers); do \
	python3 generate_input.py 0.4 20 > ./input/04_20/$$n;\
	python3 generate_input.py 0.4 40 > ./input/04_40/$$n;\
	python3 generate_input.py 0.4 60 > ./input/04_60/$$n;\
	python3 generate_input.py 0.6 20 > ./input/06_20/$$n;\
	python3 generate_input.py 0.6 40 > ./input/06_40/$$n;\
	python3 generate_input.py 0.6 60 > ./input/06_60/$$n;\
	python3 generate_input.py 0.8 20 > ./input/08_20/$$n;\
	python3 generate_input.py 0.8 40 > ./input/08_40/$$n;\
	python3 generate_input.py 0.8 60 > ./input/08_60/$$n;\
	done

target: 
	mkdir -p output;\
	cd input; \
	for dirs in $(dir); do \
		mkdir -p ../output/$$dirs ;\
		for file in $$dirs/* ;do \
		mkdir -p ../output/$$file ;\
		python3 ../run.py 0 $$file > ../output/$$file/0;\
		python3 ../run.py 1 $$file > ../output/$$file/1;\
		python3 ../run.py 2 $$file > ../output/$$file/2;\
		python3 ../run.py 3 $$file > ../output/$$file/3;\
		done \
	done \
	

clean:
	rm -rf output