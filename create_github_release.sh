#!/bin/bash

# Script to create GitHub release using gh CLI or curl

OWNER="mutsuki14"
REPO="Nvidia-APP-DLSS-Updater"
TAG="v1.0.0"
RELEASE_NAME="NVIDIA DLSS Updater v1.0.0"
RELEASE_FILE="NvidiaDLSSUpdater_v1.0.0.zip"

# Read release body from JSON
RELEASE_BODY=$(python3 -c "import json; print(json.load(open('release_info.json'))['body'])")

echo "======================================"
echo "Creating GitHub Release"
echo "======================================"
echo ""
echo "Repository: $OWNER/$REPO"
echo "Tag: $TAG"
echo "Release: $RELEASE_NAME"
echo ""

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI (gh) to create release..."
    
    # Create release with gh CLI
    gh release create "$TAG" \
        --repo "$OWNER/$REPO" \
        --title "$RELEASE_NAME" \
        --notes "$RELEASE_BODY" \
        "$RELEASE_FILE" \
        "SHA256SUMS.txt"
    
    if [ $? -eq 0 ]; then
        echo "✓ Release created successfully!"
        echo "View at: https://github.com/$OWNER/$REPO/releases/tag/$TAG"
    else
        echo "✗ Failed to create release"
    fi
else
    echo "GitHub CLI not found. Please install 'gh' or create release manually:"
    echo ""
    echo "Manual steps:"
    echo "1. Go to: https://github.com/$OWNER/$REPO/releases/new"
    echo "2. Tag version: $TAG"
    echo "3. Release title: $RELEASE_NAME"
    echo "4. Upload files:"
    echo "   - $RELEASE_FILE"
    echo "   - SHA256SUMS.txt"
    echo "5. Copy release notes from release_info.json"
    echo ""
    
    # Alternative: Create release using curl and GitHub API
    echo "Alternative: Creating draft release using GitHub API..."
    echo "(You'll need to upload files manually)"
    
    # This would require a GitHub token
    echo ""
    echo "To use API, set GITHUB_TOKEN environment variable and run:"
    echo "curl -X POST -H \"Authorization: token \$GITHUB_TOKEN\" \\"
    echo "  -H \"Content-Type: application/json\" \\"
    echo "  https://api.github.com/repos/$OWNER/$REPO/releases \\"
    echo "  -d @release_info.json"
fi