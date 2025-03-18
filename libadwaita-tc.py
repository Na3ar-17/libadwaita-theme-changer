#!/bin/python3
# filepath: /home/nazar/Theme changer/libadwaita-tc.py
import sys
import os
import argparse

THEME_ITEMS = ["gtk-4.0/gtk.css", "gtk-4.0/gtk-dark.css", "gtk-4.0/assets", "assets"]

# Theme locations
THEME_LOCATIONS = {
    "local": ".local/share/themes",
    "home": ".themes"
}

def remove_if_exists(path):
    """Remove a symlink if it exists."""
    if os.path.islink(path):
        print(f"Removing: {path}")
        os.remove(path)

def remove_current_theme(config_dir):
    """Remove all symlinks for the current theme."""
    for item in THEME_ITEMS:
        remove_if_exists(os.path.join(config_dir, item))

def set_new_theme(theme_dir, config_dir):
    """Create symlinks for the new theme."""
    for item in THEME_ITEMS:
        source = os.path.join(theme_dir, item)
        target = os.path.join(config_dir, item)
        
        if not os.path.exists(source):
            print(f"Warning: {source} not found, skipping...")
            continue
            
        try:
            os.symlink(source, target)
            print(f"Linked: {target}")
        except FileExistsError:
            print(f"Error: {target} already exists")

def select_theme_location():
    """Present menu to select theme location."""
    print("\nSelect theme folder:")
    for i, (name, path) in enumerate(THEME_LOCATIONS.items()):
        print(f"{i}. {path} ({name})")
    
    while True:
        choice = input("Choose your theme folder [0-1]: ")
        if choice.isdigit() and 0 <= int(choice) < len(THEME_LOCATIONS):
            return list(THEME_LOCATIONS.values())[int(choice)]
        print("Invalid choice, try again.")

def select_theme(themes_dir):
    """Present menu to select a theme from the themes directory."""
    try:
        all_themes = sorted([d for d in os.listdir(themes_dir) 
                     if os.path.isdir(os.path.join(themes_dir, d))])
        
        if not all_themes:
            print(f"No themes found in {themes_dir}")
            return None
            
        print("\nAvailable themes:")
        for i, theme in enumerate(all_themes):
            print(f"{i+1}. {theme}")
        print("0. Cancel")
        
        while True:
            choice = input("\nYour choice [0-{}]: ".format(len(all_themes)))
            if choice == "0":
                return None
            if choice.isdigit() and 1 <= int(choice) <= len(all_themes):
                return all_themes[int(choice)-1]
            print("Invalid choice, try again.")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing themes directory: {e}")
        return None

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Libadwaita Theme Changer")
    parser.add_argument("--reset", action="store_true", help="Reset theme to default")
    parser.add_argument("--list", action="store_true", help="List available themes")
    args = parser.parse_args()
    
    home_dir = os.getenv('HOME')
    config_dir = os.path.join(home_dir, ".config")
    
    if args.reset:
        print("\n*** Resetting theme to default ***")
        remove_current_theme(config_dir)
        print("Theme reset complete.")
        return
        
    themes_rel_path = select_theme_location()
    themes_dir = os.path.join(home_dir, themes_rel_path)
    
    if args.list:
        print(f"\nThemes in {themes_dir}:")
        try:
            for theme in sorted(os.listdir(themes_dir)):
                if os.path.isdir(os.path.join(themes_dir, theme)):
                    print(f"- {theme}")
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
        return
    
    theme = select_theme(themes_dir)
    if theme:
        print(f"\n*** Applying theme: {theme} ***")
        print("Removing previous theme...")
        remove_current_theme(config_dir)
        
        print("Installing new theme...")
        set_new_theme(os.path.join(themes_dir, theme), config_dir)
        
        print("\nTheme applied successfully!")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")