#!/bin/bash
echo "Testing dataset aggregation and metadata tagging..."
python /app/scripts/aggregate_all.py && echo "Aggregation successful!" || echo "Aggregation failed!"
