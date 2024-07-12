.PHONY: install clean run test test_custom help

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf results
	mkdir -p results

run:
	@echo "Running the backend..."
	python3 app.py

test:
	@echo "Running all tests..."
	python3 test/test_regression.py

test_custom:
	@echo "Running custom tests..."
	python3 test/test_performance_random.py $(RUNS) $(SEED)

help:
	@echo "Available commands:"
	@echo "  install          Install dependencies"
	@echo "  clean            Clean the environment"
	@echo "  run              Run the backend server"
	@echo "  test             Run all tests"
	@echo "  test_custom      Run custom tests with parameters (usage: make test_custom RUNS=<runs> SEED=<seed>)"
	@echo "  help             Display this help message"
