#!/bin/bash

# Script to push Hall Collins Listing Packet Combiner to GitHub
# Run this AFTER creating the GitHub repository

echo "🏡 Hall Collins Listing Packet Combiner - GitHub Push"
echo "=================================================="
echo ""
echo "⚠️  IMPORTANT: Make sure you've created the GitHub repository first!"
echo "    Repository name: hall-collins-listing-packet-combiner"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Prompt for GitHub username to construct the URL
echo "🔗 Enter your GitHub username (press Enter for 'hcfcollins'):"
read -r github_username
github_username=${github_username:-hcfcollins}

echo ""
echo "📡 Adding GitHub remote..."
git remote add origin "https://github.com/${github_username}/hall-collins-listing-packet-combiner.git"

echo ""
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🌐 Your repository is now available at:"
echo "    https://github.com/${github_username}/hall-collins-listing-packet-combiner"
echo ""
echo "🎉 Next steps:"
echo "   • Visit the GitHub repository to verify everything uploaded correctly"
echo "   • Add collaborators if needed"
echo "   • Set up branch protection rules if desired"
echo "   • Consider adding GitHub Actions for automated testing"
echo ""

read -p "Press Enter to close..."
