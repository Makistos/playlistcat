# GitHub Releases Guide 🚀

## Latest Release: v0.4.1 (August 31, 2025)

### 🎯 **Position Preservation Enhancement:**

**Original Track Order Preservation**
- Position numbers now always reflect original YouTube Music playlist order
- Sorting by Artist or Track Name preserves original position numbers
- Enhanced user experience with accurate position tracking throughout all operations

**Improved Position Handling**
- Position gaps after track removal accurately show which tracks were deleted
- No automatic renumbering - maintains YouTube Music sequence fidelity
- Clear instructions explaining position behavior for user understanding

**Technical Refinements**
- Modified sort_table() method to maintain original position numbers during sorting
- Updated remove_track() method to preserve YouTube Music sequence integrity
- Enhanced workflow formatting and documentation clarity

This patch release focuses on improving the position handling behavior to provide users with a more accurate representation of their original YouTube Music playlists, ensuring track positions remain meaningful regardless of sorting or modification operations.

---

## Previous Release: v0.4.0 (August 29, 2025)

### 🎉 **Major Features Added:**

**YouTube Music Authentication System**
- Full YouTube Music integration with browser header extraction
- SAPISIDHASH authorization header generation for secure API access
- Multi-method authentication fallback system for reliability
- Automatic OAuth detection prevention for seamless setup

**Comprehensive Token Refresh System**
- 30-minute automatic token monitoring with QTimer integration
- Multi-method refresh strategies (headers, auth file, session)
- Automatic retry logic with health checks
- Background token maintenance without user interruption

**Server-Side Playlist Management**
- Real playlist modification using YouTube Music's official API
- Remove tracks from actual playlists (not just local display)
- Enhanced `remove_playlist_items` API integration with proper error handling
- Smart fallback to local-only mode for public/read-only playlists

**Enhanced User Interface**
- 5-column table layout with styled remove buttons
- Server vs local removal status differentiation
- Comprehensive confirmation dialogs with track details
- Automatic position renumbering after modifications
- Clear visual feedback for all operations

### 🔧 **Technical Improvements:**

- **Authentication Architecture**: Robust auth manager with multiple verification methods
- **API Integration**: Full ytmusicapi integration with proper setVideoId handling
- **Error Handling**: Comprehensive error recovery and user guidance
- **Status Tracking**: Real-time feedback for all playlist operations
- **Data Synchronization**: Seamless sync between local display and server state

### 📱 **User Experience Enhancements:**

- **Seamless Authentication**: One-click login with browser header extraction
- **Automatic Maintenance**: Token refresh happens transparently in background
- **Real Playlist Control**: Actual modification of YouTube Music playlists
- **Smart Error Recovery**: Graceful handling of network issues and auth problems
- **Clear Status Messages**: Always know what's happening with your playlists

### 🚀 **Migration from v0.3.0:**

PlaylistCat v0.4.0 transforms from a read-only playlist viewer to a full playlist management tool:

- **Before**: View playlist contents only
- **After**: Full playlist management with server synchronization
- **Authentication**: From anonymous access to full YouTube Music integration
- **Modifications**: From display-only to real playlist editing capabilities

This release represents a major evolution in PlaylistCat's capabilities, providing professional-grade playlist management tools with seamless YouTube Music integration.

---

This document explains how to create releases for PlaylistCat with cross-platform artifacts.

## Overview

PlaylistCat uses GitHub Actions to automatically build executables for Windows, macOS, and Linux, then creates releases with all platform artifacts.

## Release Methods

### 1. Automatic Release (Recommended)

Releases are automatically created when you push a version tag:

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

This triggers the `release.yml` workflow which:
- Builds executables for all platforms
- Runs basic tests on each platform
- Creates a GitHub release with all artifacts
- Generates release notes automatically

### 2. Manual Release

You can also trigger releases manually via GitHub Actions:

1. Go to **Actions** tab in your GitHub repository
2. Select **Manual Release** workflow
3. Click **Run workflow**
4. Enter version (e.g., `v1.0.0`)
5. Choose release options (draft/prerelease)
6. Click **Run workflow**

## Release Artifacts

Each release includes the following artifacts:

### Windows (`playlistcat-windows-x64.zip`)
- `playlistcat.exe` - GUI application
- `run-gui.bat` - GUI launcher script
- Documentation and examples

### macOS (`playlistcat-macos-x64.tar.gz`)
- `playlistcat` - GUI application
- `run-gui.sh` - GUI launcher script
- Documentation and examples

### Linux (`playlistcat-linux-x64.tar.gz`)
- `playlistcat` - GUI application
- `run-gui.sh` - GUI launcher script
- Documentation and examples

## Version Numbering

Use semantic versioning (SemVer):
- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.0.1` - Patch release (bug fixes)

## Pre-release Process

For testing releases:

1. Create a pre-release tag:
   ```bash
   git tag v1.0.0-beta.1
   git push origin v1.0.0-beta.1
   ```

2. Or use manual release with "pre-release" checked

Pre-releases are marked as "Pre-release" on GitHub and won't notify users.

## Draft Releases

Create draft releases for internal review:

1. Use manual release workflow
2. Check "Create as draft"
3. Review the draft release
4. Publish when ready

## Release Notes

Release notes are automatically generated with:
- Version information
- Download links for each platform
- Installation instructions
- Feature highlights

You can edit release notes after creation if needed.

## Troubleshooting

### Build Failures

If builds fail:

1. Check the Actions tab for error logs
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Import errors (check `src/` imports)
   - Platform-specific build issues

### Missing Artifacts

If artifacts are missing from releases:

1. Verify the build completed successfully
2. Check artifact upload step in workflow logs
3. Ensure file paths in workflow match actual build outputs

### Testing Releases

Before major releases:

1. Download artifacts from a test release
2. Test on each target platform
3. Verify all features work correctly
4. Check executable sizes are reasonable

## Manual Testing Checklist

Before releasing:

- [ ] GUI application starts without errors
- [ ] GUI application works with test playlists
- [ ] Playlist fetching works with valid URL/ID
- [ ] Table sorting functions correctly
- [ ] All launcher scripts work
- [ ] Documentation is up to date
- [ ] No console errors in GUI mode

## Release Promotion

After creating a release:

1. Update README.md with latest version info
2. Announce on relevant channels/forums
3. Update package managers if applicable
4. Monitor for user feedback and issues

## Security Considerations

- Releases are built in GitHub's secure runners
- All dependencies are installed fresh for each build
- No secrets or API keys are included in artifacts
- Users should verify checksums for critical deployments

## Continuous Integration

The release workflow includes:
- Multi-platform builds
- Basic smoke tests
- Artifact validation
- Automated release creation

This ensures consistent, reliable releases across all supported platforms.
