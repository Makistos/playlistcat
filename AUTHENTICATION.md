# Authentication Guide for PlaylistCat 🐱

This guide explains how to use PlaylistCat's authentication features to access your personal YouTube Music playlists.

## Overview

PlaylistCat supports two modes of operation:

1. **Unauthenticated Mode** (Default)
   - Access to public playlists only
   - No login required
   - Works out of the box

2. **Authenticated Mode** ✅ **WORKING**
   - Access to your personal playlists
   - Browse your library
   - Requires one-time setup
   - **Authentication system verified and functional**
   - **Automatic token refresh and monitoring**

## Authentication Features ✨

### **Automatic Token Refresh**
- **Background monitoring** every 30 minutes
- **Automatic retry** when authentication fails
- **Smart refresh** using multiple fallback methods
- **SAPISIDHASH regeneration** for session renewal
- **No manual intervention** required in most cases

### **Authentication Methods**
- **Browser header extraction** from Firefox/Chrome
- **Session-based authentication** with cookie management
- **Fallback support** for different authentication states
- **Health monitoring** with automatic recovery

## Getting Started (Unauthenticated)

1. Launch PlaylistCat
2. Enter any public YouTube Music playlist ID
3. Click "Fetch Playlist"

This mode works immediately without any setup and is perfect for exploring public playlists.

## Setting Up Authentication

To access your personal playlists, you need to authenticate once:

### Step 1: Launch PlaylistCat
```bash
./run.sh  # or run the executable
```

### Step 2: Click "Login"
- Click the "Login" button in the Authentication section
- This opens the authentication setup dialog

### Step 3: Extract Browser Headers
1. **Open YouTube Music** in your web browser
2. **Login** to your YouTube Music account
3. **Open Developer Tools** (F12 or right-click → Inspect)
4. **Go to Network tab**
5. **Refresh the page** (F5)
6. **Find a request** to `music.youtube.com`
7. **Right-click** on the request
8. **Copy → Copy as cURL**

### Step 4: Complete Setup
1. **Paste the cURL command** into the text area in PlaylistCat
2. **Click "Setup Authentication"**
3. Wait for verification
4. You should see "Successfully logged in!"

## Using Authenticated Features

Once authenticated, you'll see:

### Authentication Status
- Green "Logged in - Access to personal playlists" indicator
- "Logout" button to sign out

### Personal Playlists Section
- Dropdown list of your playlists
- Shows playlist name and track count
- "Refresh Playlists" button to update the list

### How to Use
1. **Select from dropdown**: Choose one of your playlists
2. **Auto-fetch**: The playlist loads automatically
3. **Manual entry**: You can still enter playlist IDs manually

## Authentication Details

### What Gets Stored
- Authentication headers (cookies, tokens)
- Stored locally in `~/.playlistcat_auth.json`
- **Encrypted storage recommended for production use**

### Session Management
- **Automatic**: Login persists between app sessions
- **Manual logout**: Click "Logout" to clear credentials
- **Auto-cleanup**: Invalid credentials are automatically removed

### Security Notes
- Authentication data is stored locally
- No passwords are ever stored
- Only session cookies and tokens are saved
- Data is tied to your specific browser session

## Troubleshooting

### "Login Failed" or "Could not parse authentication data"
- **Check cURL command format**: Ensure you copied the complete command
- **Try different request**: Use a different network request from the browser
- **Look for /youtubei/v1/ requests**: These often have better authentication headers
- **Verify cookies**: Make sure the request includes Cookie headers with SID, HSID, SSID, APISID, SAPISID

### "No playlists found"
- **Check account**: Ensure you have playlists in your YouTube Music account
- **Refresh**: Click "Refresh Playlists" to reload
- **Logout/Login**: Try logging out and logging in again

### "Authentication expired"
- **Re-authenticate**: Your session may have expired
- **Clear and retry**: Logout and setup authentication again

### Common cURL Issues
- **Multi-line commands**: Commands with backslashes (\\) for line continuation are supported
- **Missing cookies**: Make sure the cURL includes a Cookie header
- **Browser differences**: Different browsers format cURL differently - all are supported
- **Incomplete copy**: Ensure you copied the entire cURL command including all headers

### cURL Command Examples
**Good cURL (includes authentication cookies):**
```bash
curl 'https://music.youtube.com/youtubei/v1/browse' \
  -H 'Cookie: SID=...; HSID=...; SSID=...; APISID=...; SAPISID=...'
```

**Poor cURL (missing authentication):**
```bash
curl 'https://music.youtube.com/static/...' \
  -H 'Accept: text/css'
```

## Fallback Mode

If authentication isn't working:

1. **Use manual playlist IDs**: You can still access public playlists
2. **Public mode**: The app continues to work normally
3. **No loss of functionality**: All core features remain available

## Token Refresh & Session Management 🔄

### Automatic Features
- **Background Monitoring**: Checks authentication health every 30 minutes
- **Smart Refresh**: Automatically refreshes tokens when they expire
- **Multiple Fallback Methods**:
  - SAPISIDHASH regeneration with fresh timestamps
  - Auth file recreation and validation
  - Session cookie refresh
  - Automatic retry with exponential backoff

### Manual Options
- **Force Refresh**: Use "Refresh Playlists" button to manually trigger refresh
- **Re-authentication**: Logout and login again for complete reset
- **Health Check**: Authentication status is continuously monitored

### Session Lifetime
- **Typical Duration**: Sessions last several hours to days
- **Automatic Renewal**: Tokens are refreshed before expiration
- **Graceful Degradation**: Falls back to public mode if refresh fails

### Token Security
- **Local Storage**: Authentication data saved securely in user home directory
- **Automatic Cleanup**: Old tokens removed on logout
- **No Password Storage**: Only session tokens stored, never passwords

## Advanced Usage

### Finding Your Playlist IDs
1. Go to YouTube Music
2. Open any of your playlists
3. Copy the URL
4. Extract the part after `list=`
5. Use this ID manually if needed

### Browser Compatibility
- **Chrome/Chromium**: ✓ Fully supported
- **Firefox**: ✓ Supported
- **Safari**: ✓ Supported
- **Edge**: ✓ Supported

### Multiple Accounts
- Only one account at a time
- To switch accounts: logout and re-authenticate
- Each authentication is tied to the specific Google account

## Privacy and Security

### What We Access
- **Playlist metadata**: Names, descriptions, track counts
- **Track information**: Artist, title, YouTube Music links
- **Library access**: Only your playlists and library

### What We Don't Access
- **No personal data**: Names, emails, or profile information
- **No modification**: Read-only access to your music library
- **No sharing**: Data stays on your computer

### Security Best Practices
- **Regular logout**: Logout when sharing computers
- **Monitor access**: Check your Google account activity
- **Update regularly**: Keep PlaylistCat updated

## API Rate Limits

YouTube Music API has rate limits:
- **Normal usage**: No issues for typical use
- **Heavy usage**: May encounter temporary limits
- **Retry logic**: App automatically handles temporary errors

## Support

If you encounter issues:

1. **Check this guide**: Most issues are covered here
2. **Try unauthenticated mode**: Verify basic functionality works
3. **Clear authentication**: Logout and re-authenticate
4. **Restart app**: Sometimes helps with temporary issues

## Technical Details

### Authentication Flow
1. Extract browser session cookies
2. Create temporary authentication file
3. Test access with YouTube Music API
4. Store validated credentials locally
5. Use stored credentials for future sessions

### Supported Features (Authenticated)
- ✅ Personal playlist browsing
- ✅ Library playlist access
- ✅ Real-time playlist updates
- ✅ Track-level information
- ✅ Playlist metadata

### Future Enhancements
- 🔄 Playlist creation/editing
- 🔄 Track management
- 🔄 Liked songs access
- 🔄 Advanced search
- 🔄 Sync capabilities

---

*Remember: Authentication is optional. PlaylistCat works great for public playlists without any setup!*
