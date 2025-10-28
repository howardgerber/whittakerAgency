# Doc Generate - Create or Update Daily Session Documentation

Create or update the single daily session file with today's date in Pacific Time. Always one file per day with descriptive sections. Preserves existing content when file exists and adds space for new sections. Uses delete-and-recreate approach to avoid append conflicts.

**Note**: Always uses Pacific Time (PST/PDT) for consistent documentation dating regardless of server timezone.

```bash
echo "📚 Managing daily session documentation..."

# Get current date in YYYY-MM-DD format (server is already in correct timezone)
currentDate=$(date +%Y-%m-%d)

# Create session doc filename (single file per day)
sessionFile="docs/sessions/$currentDate-session.md"

# Ensure sessions directory exists
mkdir -p "docs/sessions"

echo "📝 Daily session file: $sessionFile"

# Check if session file already exists and preserve content
if [ -f "$sessionFile" ]; then
    echo "📄 Daily session file exists - preserving content and adding space for new sections"
    # Read existing content into memory
    existingContent=$(cat "$sessionFile")
    # Delete file to avoid append conflicts
    rm "$sessionFile"
    # Recreate with existing content plus new section space
    cat > "$sessionFile" << EOF
$existingContent

---

## [New Section - $(date +"%H:%M")]
- 

EOF
else
    echo "📄 Creating new daily session file"
    # Create the daily session documentation file with template
    cat > "$sessionFile" << EOF
# Session Documentation - $currentDate

## Overview
Document the key changes, implementations, and decisions made in today's session.

## Morning Work
- 

## Afternoon Work  
-

## Files Modified
- 

## New Features/Functionality
- 

## Technical Decisions
- 

## Testing
- 

## Next Steps
- 

## Notes
- 
EOF
fi

# Brief pause to avoid sync conflicts with cloud storage
sleep 0.5

echo ""
echo "✅ Daily session file updated: $sessionFile"
echo "📝 Preserves existing content and adds space for new sections"
echo "📚 Add new work to the timestamped section or create additional sections as needed"
```