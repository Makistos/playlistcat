#!/bin/bash
# Quick release script for PlaylistCat
# Usage: ./create-release.sh v1.0.0

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🐱 PlaylistCat Release${NC} - $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Check if version argument provided
if [ $# -eq 0 ]; then
    print_error "Version required. Usage: $0 v1.0.0"
    exit 1
fi

VERSION=$1

# Validate version format
if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "Invalid version format. Use: v1.0.0"
    exit 1
fi

print_status "Creating release $VERSION"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    print_warning "Uncommitted changes detected"
    echo "Current status:"
    git status --short
    echo
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Aborted"
        exit 1
    fi
fi

# Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    print_error "Tag $VERSION already exists"
    exit 1
fi

# Run local build to verify everything works
print_status "Running local build test..."
if [ -f "build.sh" ]; then
    chmod +x build.sh
    if ! ./build.sh; then
        print_error "Local build failed"
        exit 1
    fi
    print_success "Local build completed"
else
    print_warning "build.sh not found, skipping local build test"
fi

# Update version in files if needed
print_status "Checking version references..."

# Check if we should update version in README or other files
if grep -q "version.*[0-9]\+\.[0-9]\+\.[0-9]\+" README.md 2>/dev/null; then
    print_warning "Version references found in README.md - consider updating manually"
fi

# Create and push tag
print_status "Creating git tag..."
git tag -a "$VERSION" -m "Release $VERSION"

print_success "Tag $VERSION created locally"

echo
print_status "Ready to push release!"
echo
echo "Next steps:"
echo "1. Review the tag: git show $VERSION"
echo "2. Push the tag: git push origin $VERSION"
echo "3. GitHub Actions will automatically:"
echo "   - Build executables for Windows, macOS, and Linux"
echo "   - Run tests on all platforms"
echo "   - Create a GitHub release with all artifacts"
echo
echo "Commands:"
echo "  git push origin $VERSION    # Push tag to trigger release"
echo "  git tag -d $VERSION         # Delete tag if you need to make changes"
echo

# Ask if user wants to push immediately
read -p "Push tag now to trigger release? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Pushing tag to GitHub..."
    git push origin "$VERSION"
    print_success "Tag pushed! Release build started."
    echo
    echo "🔗 Check release progress at:"
    echo "   https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/actions"
    echo
    echo "🎉 Release will be available at:"
    echo "   https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/releases/tag/$VERSION"
else
    print_success "Tag created locally. Push when ready with: git push origin $VERSION"
fi
