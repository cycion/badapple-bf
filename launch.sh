if [[ ! -f "badapple.mp4" ]]; then
    [ -x "$(command -v yt-dlp)" ] || (echo "Command yt-dlp not found, please install youtube-dl" && exit 1)
    yt-dlp -f 396 https://www.youtube.com/watch\?v\=FtutLA63Cp8 -o "badapple.mp4"
fi
[ "$(ls -A res/text/ori)" ] || python vid2txt.py
[ "$(ls -A res/bfcode/bf)" ] || python txt2bf.py
python analysis.py
python txtplayer.py

