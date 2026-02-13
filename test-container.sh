#!/bin/bash
# Script to build and test the cythonpowered package in containers

set -e

echo "=========================================="
echo "Building Docker images and testing installation"
echo "=========================================="

# Build and run tests for each Python version
docker-compose build --no-cache

echo ""
echo "=========================================="
echo "Running installation tests"
echo "=========================================="

# Run each test service
for service in test-py314 test-py313 test-py312 test-py311 test-py310 test-py39 test-py38; do
    echo ""
    echo "Testing with $service..."
    docker-compose run --rm "$service"
done

echo ""
echo "=========================================="
echo "All tests completed successfully!"
echo "=========================================="
