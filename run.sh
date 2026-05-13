#!/usr/bin/env bash
set -e

VENV_DIR="venv"

PYTHON=""
for cmd in python3 python; do
    if $cmd --version &> /dev/null; then
        PYTHON=$cmd
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Python is not installed. Please install Python 3.10+ first."
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv $VENV_DIR
fi

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    source $VENV_DIR/Scripts/activate
else
    source $VENV_DIR/bin/activate
fi

echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "========================================="
echo "  Job Board API is starting..."
echo "  API:  http://127.0.0.1:8000"
echo "  Docs: http://127.0.0.1:8000/docs"
echo "========================================="
echo ""

uvicorn app.main:app --reload
