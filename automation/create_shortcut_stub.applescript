-- Create a new shortcut in Apple's Shortcuts app via UI scripting.
-- This is best-effort automation and may break across macOS/language versions.

on run argv
	set shortcutName to "Clipboard Helfer (Auto)"
	if (count of argv) > 0 then
		set shortcutName to item 1 of argv
	end if

	tell application "Shortcuts" to activate
	delay 1.0

	tell application "System Events"
		if UI elements enabled is false then
			error "Accessibility access is disabled. Enable it in System Settings > Privacy & Security > Accessibility."
		end if
	end tell

	tell application "System Events"
		tell process "Shortcuts"
			set frontmost to true
			delay 0.3

			-- Try Command+N to create a new shortcut.
			keystroke "n" using command down
			delay 0.8

			-- Rename shortcut via title field or fallback to search/title area.
			set renamedOk to false
			try
				set value of text field 1 of group 1 of window 1 to shortcutName
				set renamedOk to true
			on error
				-- no-op
			end try

			if renamedOk is false then
				try
					keystroke "a" using {command down, shift down}
					delay 0.1
					keystroke shortcutName
					set renamedOk to true
				on error
					-- no-op
				end try
			end if

			-- Open action search and insert a basic action to make the stub visible.
			try
				keystroke "f" using command down
				delay 0.2
				keystroke "Text"
				delay 0.4
				key code 125
				key code 36
			on error
				-- Ignore if insertion path differs; shortcut is still created.
			end try
		end tell
	end tell
end run
