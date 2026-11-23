pytest -v \
            Laba1_Vector/test.py \
            TicTacToe/test_game.py \
            --cov=. --cov-report=term-missing --cov-report=xml
flake8 . --max-line-length=120 --extend-ignore=E203,W503
pdoc -o docs/html Laba1_Vector/vector.py TicTacToe/game.py
