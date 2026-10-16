python3 -m pip install --upgrade pip
pip install -r ./Laba1_Vector/requirements.txt
pytest -v \
            Laba1_Vector/ \
            TicTacToe/ \
            --cov=. --cov-report=term-missing --cov-report=xml
flake8 . --max-line-length=120 --extend-ignore=E203,W503