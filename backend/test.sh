#!/bin/bash
echo "Running auth service tests..."
python -m pytest tests/test_auth.py -v
