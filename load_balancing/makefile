Numbers = 1 2 3 4 5 6 7 8 9 10
dir = ./3
dir1 = ./4
makedir:
	mkdir -p input;\
	mkdir ./input/04_3_20/ \
	mkdir ./input/04_3_40/ \
	mkdir ./input/04_3_60/ \
	mkdir ./input/04_4_20/ \
	mkdir ./input/04_4_40/ \
	mkdir ./input/04_4_60/ \
	mkdir ./input/06_3_20/ \
	mkdir ./input/06_3_40/ \
	mkdir ./input/06_3_60/ \
	mkdir ./input/06_4_20/ \
	mkdir ./input/06_4_40/ \
	mkdir ./input/06_4_60/ \
	mkdir ./input/08_3_20/ \
	mkdir ./input/08_3_40/ \
	mkdir ./input/08_3_60/ \
	mkdir ./input/08_4_20/ \
	mkdir ./input/08_4_40/ \
	mkdir ./input/08_4_60/ \
	done
ingen:
	for n in $(Numbers); do \
	python3 generate_input.py 0.4 3 20 > ./input/04_3_20/$$n;\
	python3 generate_input.py 0.4 3 40 > ./input/04_3_40/$$n;\
	python3 generate_input.py 0.4 3 60 > ./input/04_3_60/$$n;\
	python3 generate_input.py 0.4 4 20 > ./input/04_4_20/$$n;\
	python3 generate_input.py 0.4 4 40 > ./input/04_4_40/$$n;\
	python3 generate_input.py 0.4 4 60 > ./input/04_4_60/$$n;\
	python3 generate_input.py 0.6 3 20 > ./input/06_3_20/$$n;\
	python3 generate_input.py 0.6 3 40 > ./input/06_3_40/$$n;\
	python3 generate_input.py 0.6 3 60 > ./input/06_3_60/$$n;\
	python3 generate_input.py 0.6 4 20 > ./input/06_4_20/$$n;\
	python3 generate_input.py 0.6 4 40 > ./input/06_4_40/$$n;\
	python3 generate_input.py 0.6 4 60 > ./input/06_4_60/$$n;\
	python3 generate_input.py 0.8 3 20 > ./input/08_3_20/$$n;\
	python3 generate_input.py 0.8 3 40 > ./input/08_3_40/$$n;\
	python3 generate_input.py 0.8 3 60 > ./input/08_3_60/$$n;\
	python3 generate_input.py 0.8 4 20 > ./input/08_4_20/$$n;\
	python3 generate_input.py 0.8 4 40 > ./input/08_4_40/$$n;\
	python3 generate_input.py 0.8 4 60 > ./input/08_4_60/$$n;\
	done

target: 
	mkdir -p output;\
	cd input; \
	for dirs in $(dir); do \
		for subdirs in $$dirs/* ;do \
			for file in $$subdirs/*; do\
				mkdir -p ../output/$$file ;\
				python3 ../two_phase.py $$file 3 4 > ../output/$$file/3_4;\
				python3 ../two_phase.py $$file 3 5 > ../output/$$file/3_5;\
			done\
		done \
	done \

target1:
	mkdir -p output;\
	cd input; \
	for dirs in $(dir1); do \
		for subdirs in $$dirs/* ;do \
			for file in $$subdirs/*; do\
				mkdir -p ../output/$$file ;\
				python3 ../two_phase.py $$file 4 5 > ../output/$$file/4_5;\
				python3 ../two_phase.py $$file 4 6 > ../output/$$file/4_6;\
			done\
		done \
	done \

target2:
	mkdir -p output;\
	cd input; \
	for dirs in $(dir); do \
		for subdirs in $$dirs/* ;do \
			for file in $$subdirs/*; do\
				mkdir -p ../output/$$file ;\
				python3 ../two_phase.py $$file 3 6 > ../output/$$file/3_6;\
			done\
		done \
	done \
	

clean:
	rm -rf output