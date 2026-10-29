#!/usr/bin/env bash
# Renders both ads (60 fps), muxes the soundtracks and copies the finals to deliverables/.
# Run `npm run audio` first so build/mix_v.wav and build/mix_h.wav exist.
set -e
mkdir -p build deliverables
node render.mjs v916/index.html build/v916_video.mp4 --w 1080 --h 1920 --fps 60 --dur 18.5 > build/render_v.log 2>&1
ffmpeg -hide_banner -loglevel error -y -i build/v916_video.mp4 -i build/mix_v.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "build/FlightDeals_9x16_Reels.mp4"
echo "V DONE"
node render.mjs h169/index.html build/h169_video.mp4 --w 1920 --h 1080 --fps 60 --dur 25.5 > build/render_h.log 2>&1
ffmpeg -hide_banner -loglevel error -y -i build/h169_video.mp4 -i build/mix_h.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "build/FlightDeals_16x9_YouTube.mp4"
echo "H DONE"
cp build/FlightDeals_9x16_Reels.mp4 build/FlightDeals_16x9_YouTube.mp4 deliverables/
echo "Copied finals to deliverables/"
