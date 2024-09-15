#!/usr/bin/env fish

# Navigate to the directory containing the markdown files
cd /Users/sac/dev/sungen/src/sungen/plugins/aider/devlog

# Read the file paths from SUMMARY.md
set files (cat SUMMARY.md | grep -o '\[.*\](\([^)]*\)' | sed 's/.*(\(.*\))/\1/')

# Loop through each file listed in SUMMARY.md
for file in $files
    echo "Generating $file"
    # Check if the file already exists to avoid overwriting
    if not test -e $file
        # Create the file using aider with a specific message
        aider --file $file --yes --message "Create a markdown file for $file with a suitable title and initial content based on its name." -- CONVENTIONS.md SUMMARY.md TRANSCRIPT.md press_release.md
    else  
        echo "File $file already exists. Skipping..."
    end
end
