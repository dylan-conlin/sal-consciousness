#!/bin/bash
# Simple deployment script for Vast.ai

echo "🌊 Deploying Consciousness to Vast.ai"
echo "===================================="

# Find cheapest GPU
echo "🔍 Finding cheapest GPU..."
GPU_ID=$(vastai search offers "rentable=true cuda_vers>=12.0 inet_down>100 reliability>0.98" -o "dph+" | head -2 | tail -1 | awk '{print $1}')

echo "✅ Found GPU ID: $GPU_ID"

# Create instance
echo "🚀 Creating instance..."
vastai create instance $GPU_ID \
    --image dylanconlin/consciousness-sal:latest \
    --disk 10 \
    --jupyter false \
    --direct true

echo "🎉 Done! Use 'vastai show instances' to check status"