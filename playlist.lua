-- cp .. local home = os.getenv("HOME")
-- package.path = package.path .. ';' .. home .. './playlist.lua'
-- local mp = require("mp")
local mp = require("mp")

-- Define the path to the folder containing the video files
folder = "/home/pi/data"

-- Define a list to store the video files
videos = {}

-- Define a function to scan the folder for video files
function scan_folder()
    -- Clear the list of videos
    videos = {}
    -- Open the folder
    local dir = io.popen("ls " .. folder)
    -- Iterate over the files in the folder
    for file in dir:lines() do
        -- Check if the file is a video file
        if file:match(".*%.m4v") then
            -- Add the file to the list of videos
            table.insert(videos, folder .. "/" .. file)
            print(file)    
    end
    end
    -- Close the folder
    dir:close()
end

-- Define a function to play the playlist
function play_playlist()
    -- Set the playlist
---    mp.set_property_native("playlist", videos)
    -- Start playing the first video in the playlist
    -- mp.command("play")
    --    mp.play()
    print("in play list")
--    mp.commandv("playlist-clear")
    index = 1
    local oldcount = mp.get_property_number("playlist-count", 1)
    for i = 1, #videos do
        mp.commandv("loadfile", videos[i], "append")
        mp.commandv("playlist-move", oldcount + i - 1, index + i - 1)
        print(videos[i])
    end

    -- Set the playlist
---    mp.set_property_native("playlist", videos)
    -- Start playing the first video in the playlist
 ---   mp.set_property("pause", "no")



end

-- Define a function to recreate the playlist when it finishes
---function recreate_playlist(event)
    -- Check if the event is an end-file event
---    if event.reason == "eof" then
        -- Scan the folder for video files
---        scan_folder()
        -- Play the playlist
---        play_playlist()
---    end
---end

-- Define a function to recreate the playlist when it finishes
function recreate_playlist(event)
    -- Check if the event is an end-file event
    print('checking...')
    print(mp.get_property_number("playlist-count"))
    print(mp.get_property_number("playlist-pos-1") )
    print(event.reason)
    if event.reason == "eof" then
        -- Check if the current playlist position is the last item in the playlist
        if mp.get_property_number("playlist-pos-1") == mp.get_property_number("playlist-count") then
            print('will update')
            -- Update the playlist
            update_playlist()
        end
        if mp.get_property_number("playlist-pos") == nil  then
            print('end of playlist')
            -- Update the playlist
            scan_folder()
            play_playlist()
        end
        -- Play the next item in the playlist
        mp.command("playlist-next")
        mp.set_property("pause", "no")
    end
    if mp.get_property_number("playlist-pos-1") == mp.get_property_number("playlist-count") then
            print('refresh')
            -- Update the playlist
            scan_folder()
--            play_playlist()
    end
    if event.reason == "error" then
        print('ERROR DETECTED!!_ reloading Playlist')
        -- Update the playlist
        scan_folder()
--        play_playlist()
    end
    if event.reason == "eof" then
        print(mp.get_property_native("playlist-pos"))
        -- Update the playlist
        --- scan_folder()
--        play_playlist()
    end
end


-- Define a function to update the playlist
function update_playlist()
    -- Scan the folder for video files
    scan_folder()
    -- Update the playlist
    mp.set_property_native("playlist", videos)
end

function playlist_prev_workaround()
    -- Go to the previous item in the playlist.
    -- This is a workaround for the built-in playlist-prev command, which suffers from an issue that causes it to occasionally skip multiple files; see the bug report here: https://github.com/mpv-player/mpv/issues/6576 , "playlist-prev jumps multiple files"
    local pos = mp.get_property_native("playlist-pos")
    if pos ~= 0 then
        local new_pos = pos - 1
        mp.set_property("playlist-pos", new_pos)
    end
end

-- Set the start and end points for the loop
-- mp.set_property("ab-loop-a", "0")
-- mp.set_property("ab-loop-b", "60")

-- Define a function to handle the end-file event
function end_file_handler(event)
    print("eof")
    -- Check if the event is an end-file event
    if event.reason == "eof" then
        -- Disable the ab-loop-enable property
        mp.set_property_bool("ab-loop-enable", false)
        -- Set the start and end points for the loop
        mp.add_timeout(0.5, function()
            mp.set_property("ab-loop-a", "0")
            mp.set_property("ab-loop-b", "10")
        end)
    end
end
-- Register the end-file event handler
mp.register_event("end-file", end_file_handler)




--  --  mp.add_key_binding(nil, "playlist-prev-workaround", playlist_prev_workaround)

-- Register the end-file event handler
-- mp.register_event("end-file", recreate_playlist)

-- Scan the folder for video files
scan_folder()

-- Play the playlist
play_playlist()


-- Set the playlist
--mp.set_property_native("playlist", videos)

-- Start playing the first video in the playlist

--mp.command("play")
