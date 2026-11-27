"""Make an AI voiceover (same voice as the Shorts) plus word timings for each script.
Usage: python scripts/voice.py jobs/<name>/voice.json assets/voice/<name>
voice.json: {"voice": "en-US-ChristopherNeural", "rate": "+10%", "volume": "+40%",
             "items": [{"id": "p02_lost_ticket", "text": "..."}]}
Writes <id>.mp3 and <id>.words.json ([{"w": word, "start": s, "end": s}]).
"""
import asyncio, json, os, sys
import edge_tts

async def one(item, cfg, out):
    c = edge_tts.Communicate(item["text"], cfg.get("voice", "en-US-ChristopherNeural"),
                             rate=cfg.get("rate", "+10%"), volume=cfg.get("volume", "+40%"),
                             boundary="WordBoundary")
    words, audio = [], bytearray()
    async for ch in c.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            s = ch["offset"] / 1e7
            words.append({"w": ch["text"], "start": round(s, 3), "end": round(s + ch["duration"] / 1e7, 3)})
    open(os.path.join(out, item["id"] + ".mp3"), "wb").write(audio)
    json.dump(words, open(os.path.join(out, item["id"] + ".words.json"), "w"), indent=0)
    print(item["id"], len(words), "words", words[-1]["end"] if words else 0, "s")

async def main():
    cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for it in cfg["items"]:
        await one(it, cfg, out)

asyncio.run(main())
