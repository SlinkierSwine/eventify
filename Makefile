backend = api db
frontend = 
all = $(backend) $(frontend)

# All frontend/backend services
up-%:
	docker-compose up $($*) -d

down-%:
	docker-compose down $($*)

build-%:
	docker-compose up $($*) -d --build

logs-%:
	docker-compose logs -f $($*)

logs:
	docker-compose logs -f

# Separate services
%-up:
	docker-compose up $* -d

%-down:
	docker-compose down $*

%-build:
	docker-compose up $* -d --build

%-logs:
	docker-compose logs -f $*

# List all services
list:
	@echo $(all)
