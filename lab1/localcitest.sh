pytest -v \
            Laba1_Vector/test.py \
            TicTacToe/test_game.py \
            --cov=. --cov-report=term-missing --cov-report=xml
flake8 . --max-line-length=120 --extend-ignore=E203,W503