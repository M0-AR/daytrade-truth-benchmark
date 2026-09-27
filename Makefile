test:
	pytest -q
bench:
	python -m dtb.benchmark --trades 10000 --seed 42 --out results/benchmark.json
up:
	docker compose up --build benchmark
