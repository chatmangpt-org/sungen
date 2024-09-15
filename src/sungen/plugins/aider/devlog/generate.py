import os
import subprocess
import re
import yaml  # Add this import

from sungen.plugins.aider.devlog.summary_config import SummaryConfig, FileSource  # Import FileSource


def write_with_aider(chapter):
    """Create a markdown file using the aider command."""
    command = [
        'aider',
        '--file', chapter.path,
        '--yes',
        '--message', f"Create a markdown file for '{chapter.title}' at {chapter.path} with suitable initial content based on its name and provided text.",
        '--', 'CONVENTIONS.md', 'SUMMARY.md', 'TRANSCRIPT.md', 'press_release.md'
    ]
    print(command)
    subprocess.run(command)


def write_chapters(config: SummaryConfig):
    """Write chapters using the aider command based on the configuration."""
    for chapter in config.prefix_chapters + config.numbered_chapters + config.suffix_chapters:
        # Use the chapter object directly
        if chapter.path and not os.path.exists(chapter.path):
            write_with_aider(chapter)  # Pass the entire chapter object
            print(f"Created chapter: {chapter.title} at {chapter.path}")  # Log chapter creation

        # Process subchapters
        for subchapter in chapter.subchapters:
            if subchapter.path and not os.path.exists(subchapter.path):
                write_with_aider(subchapter)  # Pass the entire subchapter object
                print(f"Created subchapter: {subchapter.title} at {subchapter.path}")  # Log subchapter creation


def main():
    # Navigate to the directory containing the markdown files
    os.chdir('/Users/sac/dev/sungen/src/sungen/plugins/aider/devlog')

    # Load the summary configuration using FileSource
    config = SummaryConfig(config_sources=FileSource(file='summary_config.yaml'))  # Initialize SummaryConfig with loaded data

    # Write chapters based on the configuration
    write_chapters(config)


if __name__ == "__main__":
    main()
