NAME		:= fly_in
PYPROJECT	:= pyproject.toml

SRC		:= src
TEST	:= tests

PYTHON_INSTALL := python3

UV		:= uv
URUN	:= uv run
RM		:= rm -rf

CACHE	:= .cache
VENV	:= .venv-$(NAME)

export UV_PROJECT_ENVIRONMENT	:= $(VENV)
export UV_CACHE_DIR				:= $(CACHE)

# Color
C_RESET		:= \033[0m
C_GREEN		:= \033[032m
C_YELLOW	:= \033[33m
C_BLUE		:= \033[34m
C_MAGENTA	:= \033[35m

.PHONY: all install \
	check init \
	run test \
	lint lint-strict \
	clean fclean \
	add remove \
	re


all			: install


check		:
	@ echo "$(C_BLUE)> Check all dependencies ...$(C_RESET)"
	@ command -v $(PYTHON_INSTALL) > /dev/null 2>&1 || { \
		echo "$(C_YELLOW)Error: $(PYTHON_INSTALL) is not installed$(C_RESET)"; \
		exit 1; \
	}
	@ command -v $(UV) > /dev/null 2>&1 || { \
		echo "$(C_YELLOW)Error: $(UV) is not installed$(C_RESET)"; \
		exit 1; \
	}


init		: check
	@ echo "$(C_BLUE)> Initialization of the project ...$(C_RESET)"
	@ if [ ! -d $(VENV) ]; then \
		$(UV) venv $(VENV); \
		echo "$(C_GREEN)... Virtual Environement Created.$(C_RESET)"; \
	fi
	@ if [ ! -f $(PYPROJECT) ]; then \
		$(UV) init . --name $(NAME); \
		echo "$(C_GREEN)... Project successfully initialized.$(C_RESET)"; \
	else \
		echo "$(C_MAGENTA) ... Project already initialized.$(C_RESET)"; \
	fi


install		: init
	@ echo "$(C_BLUE)> Project Installation/Syncronization ...$(C_RESET)"
	@ $(UV) sync


run			: install
	@ echo "$(C_BLUE)> Launch Project ...$(C_RESET)"
	@ $(URUN) python -m $(SRC)


debug		: install
	@ echo "$(C_BLUE)> Launch Project (debug mode) ...$(C_RESET)"
	@ $(URUN) python -m pdb $(SRC)


test		: install
	@ echo "$(C_BLUE)> Launch Project Test ...$(C_RESET)"
	@ $(URUN) pytest $(TEST)


lint		: install
	@ echo "$(C_BLUE)> Project readability, lint standard ...$(C_RESET)"
	@ $(URUN) flake8 $(SRC)
	@ $(URUN) mypy $(SRC) --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs


lint-strict	: install
	@ echo "$(C_BLUE)> Project readability, lint strict ...$(C_RESET)"
	@ $(URUN) flake8 $(SRC)
	@ $(URUN) mypy $(SRC) --strict


clean		:
	@ echo "$(C_BLUE)> Remove python cache$(C_RESET)"
	@ find . -name "__pycache__" -type d -exec $(RM) {} +
	@ find . -name ".mypy_cache" -type d -exec $(RM) {} +
	@ find . -name "*.pyc" -type d -exec $(RM) {} +


fclean		: clean
	@ echo "$(C_BLUE)> Remove project generated file$(C_RESET)"
	@ $(RM) $(VENV)


re			: fclean all


add			: init
	@ echo "$(C_BLUE)> Add dependencies: $(DEP)$(C_RESET)"
	@ $(UV) add $(DEP)


remove		: init
	@ echo "$(C_BLUE)> Remove dependencies: $(DEP)$(C_RESET)"
	@ $(UV) remove $(DEP)
