#!/bin/bash

# Run modal volume get command
modal volume get mochi-outputs /outputs ./mochi_outputs

# Check if command was successful
if [ $? -eq 0 ]; then
    echo "✅ Successfully downloaded mochi outputs"
else
    echo "❌ Failed to download mochi outputs"
fi 