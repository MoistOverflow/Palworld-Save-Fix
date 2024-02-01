# Palworld Save Fix 

> ### No UESAVE
> ### No melee bug

> ### Be careful of data loss and *always* make a backup.

Dependencies:
- Python 3

Command:    
`python fix-savs.py <old_guid> <new_guid>`

`<new_guid>` - GUID of the player on the new server    
`<old_guid>` - GUID of the player from the old server

Example:    
`python fix-savs.py 00000000000000000000000000000001 6A80B1A6000000000000000000000000`

## migrate a co-op save to a Linux dedicated server

Prerequisites:
- Install the dependencies [above].
- The dedicated server is installed, running, and you're able to join it.
- No viewing cage support. (not tested)

Steps:
1. Copy your desired save's folder from `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames\<random_numbers>` to your dedicated server.
2. In the `PalServer\Pal\Saved\Config\LinuxServer\GameUserSettings.ini` file, change the `DedicatedServerName` to match your save's folder name. For example, if your save's folder name is `2E85FD38BAA792EB1D4C09386F3A3CDA`, the `DedicatedServerName` changes to `DedicatedServerName=2E85FD38BAA792EB1D4C09386F3A3CDA`.
3. Delete `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\WorldOption.sav` to allow modification of `PalWorldSettings.ini`. Players will have to choose their respawn point again, but nothing else is affected as far as I can tell.
4. Confirm you can connect to your save on the dedicated server and that the world is the one in the save. You can check the world with a character that belongs to a regular player from the co-op.
5. Afterwards, the co-op host must create a new character on the dedicated server. A new `.sav` file should appear in `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players`.
6. The name of that new `.sav` file is the co-op host's new GUID. We will need the co-op host's new GUID for the script to work.
7. Shut the server down and then copy `PalServer\Pal\Saved\SaveGames\0\<your_save_here>/Level.sav` and `PalServer\Pal\Saved\SaveGames\0\<your_save_here>/Players/<co-op_sav_file>` to the `sav/` folder in the tool
8. **Make a backup of your save!** This is an experimental script and has known bugs so always keep a backup copy of your save.
9. Run the script using the command in the [Usage section](#usage) with the information you've gathered and using `00000000000000000000000000000001` as the co-op host's old GUID.
10. Copy the save from the temporary folder back to the dedicated server. Move the save you had in the dedicated server somewhere else or rename it to something different.
11. Start the server back up and have the co-op host join the server with their fixed character.




This uses cheahjs https://github.com/cheahjs/palworld-save-tools for converting sav to json and back.

Steps from xNul https://github.com/xNul/palworld-host-save-fix
