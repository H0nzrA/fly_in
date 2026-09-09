# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trakotoz <trakotoz@student.42antananarivo  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 03:18:43 by trakotoz          #+#    #+#              #
#    Updated: 2026/09/09 19:02:40 by trakotoz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME		:= fly-in
PYPROJECT	:= pyproject.toml

SRC		:= src/fly_in
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

.PHONY: all install check \
	run test \
	lint lint-strict \
	clean fclean \
	add remove \
	re tree \
	help build


help		:
	@ echo "$(C_BLUE)Usage: make [target] $(C_RESET)"
	@ echo "$(C_GREEN)make install$(C_RESET)        Install all the dependencies"
	@ echo "$(C_GREEN)make run$(C_RESET)            Run the Applications"
	@ echo "$(C_GREEN)make test$(C_RESET)           Run all Applications test under pytest module"
	@ echo "$(C_GREEN)make lint$(C_RESET)           Run flake8 and mypy (standard version)"
	@ echo "$(C_GREEN)make lint-strict$(C_RESET)    Run flake8 and mypy (strict version)"
	@ echo "$(C_GREEN)make clean$(C_RESET)          Remove python and mypy cache"
	@ echo "$(C_GREEN)make fclean$(C_RESET)         clean + remove virtualenv/dist"
	@ echo "$(C_GREEN)make re$(C_RESET)             fclean + install (rebuild of the project)"
	@ echo "$(C_GREEN)make build$(C_RESET)          Build project as a distribution package"


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


install		: check
	@ echo "$(C_BLUE)> Project Installation/Syncronization ...$(C_RESET)"
	@ $(UV) sync


run			: install
	@ echo "$(C_BLUE)> Launch Project ...$(C_RESET)"
	@ $(URUN) $(NAME) $(ARGS)


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
	@ find . -name ".pytest_cache" -type d -exec $(RM) {} +
	@ find . -name "*.pyc" -type f -exec $(RM) {} +


fclean		: clean
	@ echo "$(C_BLUE)> Remove project generated file$(C_RESET)"
	@ $(RM) $(VENV)


re			: fclean all


add			: check
	@ echo "$(C_BLUE)> Add dependencies: $(DEP)$(C_RESET)"
	@ $(UV) add $(DEP)


remove		: check
	@ echo "$(C_BLUE)> Remove dependencies: $(DEP)$(C_RESET)"
	@ $(UV) remove $(DEP)


tree		: check
	@ $(UV) tree


build		: check
	@ $(UV) build
