#!/bin/bash

# Quick Navigation Update Script for ImmiWatch
# Usage: ./scripts/quick_update.sh "old_text" "new_text"

OLD_TEXT="$1"
NEW_TEXT="$2"

if [ -z "$OLD_TEXT" ] || [ -z "$NEW_TEXT" ]; then
    echo "Usage: $0 \"old_text\" \"new_text\""
    echo "Example: $0 \"Tools\" \"Navigators\""
    exit 1
fi

echo "🔄 Updating navigation across all HTML files..."
echo "Old text: '$OLD_TEXT'"
echo "New text: '$NEW_TEXT'"
echo ""

# Find all HTML files and update them
find . -name "*.html" -type f | while read -r file; do
    if grep -q "$OLD_TEXT" "$file"; then
        echo "✅ Updating: $file"
        sed -i '' "s/$OLD_TEXT/$NEW_TEXT/g" "$file"
    fi
done

echo ""
echo "🎉 Update completed!"
echo "📝 Don't forget to:"
echo "  1. Review the changes"
echo "  2. Test the website"
echo "  3. Commit the changes" 