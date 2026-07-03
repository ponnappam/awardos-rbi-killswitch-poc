.PHONY: demo setup run stop clean
demo: ; @./scripts/setup.sh && docker-compose up -d && sleep 10 &&./scripts/demo.sh
setup: ; @./scripts/setup.sh
run: ; @docker-compose up -d
stop: ; @docker-compose down
clean: ; @docker-compose down -v
