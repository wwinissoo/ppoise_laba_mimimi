pytest -v \
            Laba1_Vector/ \
            TicTacToe/ \
            --cov=. --cov-report=term-missing --cov-report=xml
flake8 . --max-line-length=120 --extend-ignore=E203,W503