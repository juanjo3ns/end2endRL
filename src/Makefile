#DOUBLE DQN
dqn:
	python3 main.py --version dqn.comp.1 --seed 0 --iterations 8000 --batch_size 1000 --health 20 --env 6 --h 20 --w 10 --numAgents 1 --alg DQN --tbX True --show False --save True --onnx False --save_freq 1000 --po False --visibleRad 1
	# python3 main.py --version final.0.3 --seed 3 --iterations 25000 --batch_size 1000 --health 40 --env 6 --h 10 --w 3 --numAgents 1 --alg DQN --tbX True --show False --save True --onnx False --save_freq 1000 --po False --visibleRad 1
	# python3 main.py --version final.1.0 --seed 0 --iterations 30000 --batch_size 1000 --health 50 --env 6 --h 10 --w 10 --numAgents 1 --alg DQN --tbX True --show False --save False --onnx False --save_freq 1000 --po False --visibleRad 1
	# python3 main.py --version final.2.0 --seed 0 --iterations 35000 --batch_size 1000 --health 60 --env 6 --h 20 --w 10 --numAgents 1 --alg DQN --tbX True --show False --save False --onnx False --save_freq 1000 --po False --visibleRad 1

eval_dqn:
	python3 eval.py --version bs.4.2.3 --seed 2 --stats False --health 1 --env 6 --h 20 --w 10 --iterations 100 --numAgents 1 --alg DQN


#GENETIC ALGORITHMS
ga:
	# python3 main.py --version 0.0.3 --iterations 500 --seed 0 --sigma 0.02 --env 6 --h 10 --w 3 --numAgents 150 --alg GA --tbX True --show False --onnx False --save True --save_freq 30 --po False --visibleRad 1
	# python3 main.py --version 0.1.2 --iterations 250 --seed 4 --sigma 0.02 --env 7 --h 10 --w 10 --numAgents 200 --alg GA --tbX False --show False --onnx False --save True --save_freq 20 --po False --visibleRad 1
	python3 main.py --version 0.2.10 --iterations 1000 --seed 0 --sigma 0.02 --env 8 --h 20 --w 10 --numAgents 200 --alg GA --tbX True --show False --onnx False --save True --save_freq 40 --po False --visibleRad 1

eval_ga:
	# python3 eval.py --version 0.0.3 --seed 0 --sigma 0.02 --env 6 --h 10 --w 3 --numAgents 150 --alg GA
	python3 eval.py --version 0.1.2 --seed 0 --stats False --health 1 --sigma 0.02 --env 6 --h 10 --w 10 --numAgents 150 --alg GA
	# python3 eval.py --version 0.2.9 --seed 0 --stats False --health 1 --sigma 0.02 --env 6 --h 20 --w 10 --iterations 100 --numAgents 150 --alg GA

#POLICY GRADIENT METHODS
pgm:
	python3 main.py --version final.2.0 --iterations 500000 --health 1 --env 7 --h 15 --w 15 --numAgents 1 --alg PGM --tbX True --show False --save True --onnx False --save_freq 10000 --po True --visibleRad 3
	# python3 main.py --version 0.0. --iterations 300000 --env 9 --h 6 --w 6 --numAgents 1 --alg PGM --tbX True --show False --save False --onnx False --save_freq 20 --po True --visibleRad 1
	# python3 main.py --version 0.0. --iterations 300000 --env 9 --h 6 --w 6 --numAgents 1 --alg PGM --tbX True --show False --save False --onnx False --save_freq 20 --po True --visibleRad 1

eval_pgm:
	python3 eval.py --version final.1.0 --stats False --iterations 20 --health 1 --env 7 --h 10 --w 10 --numAgents 1 --alg PGM --po True --visibleRad 2
	# python3 eval.py --version 0.0. --env 7 --h 10 --w 10 --numAgents 1 --alg PGM --po True --visibleRad 1
	# python3 eval.py --version 0.0. --env 8 --h 20 --w 10 --numAgents 1 --alg PGM --po True --visibleRad 1

# ACTOR CRITIC
a2c:
	python3 main.py --version a2c.0.2 --iterations 300000 --health 1 --env 7 --h 6 --w 6 --numAgents 1 --alg A2C --tbX True --show False --save False --onnx False --save_freq 10000 --po True --visibleRad 1


health:
	python3 main.py --version final.1.0 --seed 4 --iterations 15000 --batch_size 1000 --health 20 --env 6 --h 10 --w 10 --numAgents 1 --alg DQN --tbX True --show False --save False --onnx False --save_freq 1000 --po False --visibleRad 1
	python3 main.py --version final.1.1 --seed 4 --iterations 15000 --batch_size 1000 --health 30 --env 6 --h 10 --w 10 --numAgents 1 --alg DQN --tbX True --show False --save False --onnx False --save_freq 1000 --po False --visibleRad 1
	python3 main.py --version final.1.2 --seed 4 --iterations 15000 --batch_size 1000 --health 40 --env 6 --h 10 --w 10 --numAgents 1 --alg DQN --tbX True --show False --save False --onnx False --save_freq 1000 --po False --visibleRad 1


snake:
	python3 main.py --version snake.0.7 --seed 2 --batch_size 1000 --iterations 35000 --health 70 --env 8 --h 21 --w 10 --numAgents 1 --alg DQN --tbX True --show False --save True --onnx False --save_freq 2000 --po False --visibleRad 1
snake_eval:
	python3 eval.py --version snake.0.6 --seed 2 --stats False --health 4 --env 8 --h 17 --w 17 --iterations 100 --numAgents 1 --alg DQN
