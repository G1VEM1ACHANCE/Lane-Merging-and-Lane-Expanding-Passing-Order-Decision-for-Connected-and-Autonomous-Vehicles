Numbers = 1 2 3 4 5 6 7 8 9 10

ingen:
	for n in $(Numbers); do \
	python3 generate_input.py 0.4 20 > ./input/04_20/$$n;\
	done

target: 
	for n in $(Numbers); do \
	echo $$n;\
	done