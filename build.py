#!/usr/bin/env python3
"""Builds the SRoolsKing site from one data set:
  srk.html               -> artifact preview (no doctype, per the Artifact page contract)
  index.html             -> standalone page for any static host
  squarespace-block.html -> body of a Squarespace Code Block
  squarespace-custom.css -> paste into Squarespace Design > Custom CSS
"""
import json, html, pathlib

SNAPSHOT = "Oct 7, 2026"
CDN = "https://tr.rbxcdn.com/180DAY-{}/768/432/Image/Png/noFilter"
AVATAR = "https://tr.rbxcdn.com/30DAY-Avatar-CC8985CFD7EEB4635B4D148C707DAB35-Png/420/420/Avatar/Png/noFilter"

# status: live | beta | retired
GAMES = [
  dict(u=10767645246, p=127633247396147, name="Get Rich Building Stairs", status="beta", year="2026", date="Sep 2026", visits=4060, favs=21, by="Golden Eagle Studios", code="", plat="Xbox · Mobile · PC", grad="#1E6B43,#C99412", thumb="f32416710bb299697873431640a18a31",
       blurb="Chop trees, mine rocks, and build a staircase that never ends. Pets gather for you, and it earns money offline."),
  dict(u=10345791932, p=107417157677118, name="Build Your Soccer Empire", status="beta", year="2026", date="Jun 2026", visits=6392, favs=24, by="Peregrine Falcon Studios", code="", plat="Xbox · Mobile · PC", grad="#0F766E,#84CC16", thumb="e68203bfe14724788c30bd7074b59fe5",
       blurb="Draw a card against another player, then split it or steal it all. Boost your luck for Pros, World Class and GOATs, rebirth, fuse duplicates, get revenge."),
  dict(u=2101240674, p=5880489517, name="Ultimate Modern House Tycoon", status="retired", year="2020", date="Oct 2020", visits=8157809, favs=30667, by="SRoolsKing", code="", plat="Xbox · Mobile · PC", grad="#334155,#94A3B8", thumb="efa622fac2320cb9485915efe359c41e",
       blurb="The original. Claim a plot, build a modern house, drive cars. Retired, with players and gamepass credit carried into the sequel."),
  dict(u=4592957519, p=13160412552, name="Ultimate Mansion Tycoon", status="live", year="2023", date="Apr 2023", visits=7428276, favs=19374, by="Golden Eagle Studios", code="4444LIKES", plat="Xbox · Mobile · PC · VR", grad="#6D28D9,#F472B6", thumb="fe48b235000c5b4472f66fc670d1eaaa",
       blurb="Claim a plot and build the best-looking mansion tycoon on Roblox. Unlock and drive cars, throw a house party, rebirth and do it bigger."),
  dict(u=3482493471, p=9305786774, name="Ultimate Modern House Tycoon 2", status="live", year="2022", date="Apr 2022", visits=4852173, favs=11396, by="SRoolsKing", code="Ultimat3", plat="Xbox · Mobile · PC", grad="#0369A1,#38BDF8", thumb="921903f01e18529a354933243a9cad7a",
       blurb="Rebirths, a revamped GUI, new gamepasses and a rebirth leaderboard. Claim a plot, build a modern house, drive cars."),
  dict(u=4201850178, p=11874434852, name="Ultimate Modern House Tycoon (2022)", status="retired", year="2022", date="Dec 2022", visits=2379385, favs=7744, by="SRoolsKing", code="", plat="Xbox · Mobile · PC", grad="#475569,#CBD5E1", thumb="9ae596d05e8982d944ab2d2001c12a10",
       blurb="The 2022 remake of the original, with gamepass credit for returning players. Retired."),
  dict(u=2533980161, p=6709868855, name="Ultimate House Tycoon", status="live", year="2021", date="Apr 2021", visits=1055311, favs=10397, by="SRoolsKing", code="", plat="Xbox · Mobile · PC", grad="#B45309,#FBBF24", thumb="d9cc1e87629430c2babab3be50d016da",
       blurb="Claim a plot to build a house and roleplay with friends. Rebirth once you've bought every non-Robux button."),
  dict(u=9530317138, p=119069636768315, name="Billionaire House Tycoon", status="beta", year="2026", date="Jan 2026", visits=1017135, favs=7533, by="Golden Eagle Studios", code="REL3ASE", plat="Xbox · Mobile · PC · VR", grad="#1D4ED8,#22D3EE", thumb="30f3e26e1ceeaf3ed893636b27b4b35a",
       blurb="Claim multiple plots and build a billionaire real estate portfolio. Start businesses, unlock cars. Yachts and mansions on the way."),
  dict(u=2838525435, p=7274429037, name="Youtuber Tycoon", status="live", year="2021", date="Aug 2021", visits=109430, favs=706, by="SRoolsKing", code="", plat="PC · Mobile", grad="#991B1B,#F87171", thumb="5b160190a73c6e36955becc3c3042db6",
       blurb="Every plot is a YouTuber who's played tycoons. Build your base and climb to rebirth."),
  dict(u=1863305565, p=5320150722, name="Haitians Hangout", status="live", year="2020", date="Jul 2020", visits=22855, favs=339, by="Haitians", code="", plat="PC · Mobile", grad="#1E3A8A,#DC2626", thumb="43c9d916c9703e3d0e6784ac11984594",
       blurb="A hangout for the Haitians group. Not a game, just a place to meet people."),
  dict(u=3250974283, p=8516882838, name="Beat The Time!", status="live", year="2022", date="Jan 2022", visits=9650, favs=198, by="Top Notch Obbies", code="", plat="PC · Mobile", grad="#0F766E,#2DD4BF", thumb="547b16bfc4df033def001b5342b59fa7",
       blurb="An easy obby with a twist: 100 stages before the clock runs out. Later stages are harder but give back more time."),
  dict(u=3291101795, p=8650152585, name="Celebrities Hangout", status="live", year="2022", date="Jan 2022", visits=786, favs=18, by="SRoolsKing", code="", plat="PC · Mobile", grad="#7E22CE,#C084FC", thumb="321a327a9647fe47601f21ea477224c5",
       blurb="A spatial-voice hangout."),
]
WORKED_ON = [
  dict(u=3746418487, p=10224049386, name="House Tycoon 2", by="Haza Games", year="2022", date="Jul 2022", visits=336096741, favs=414643, playing=1998, grad="#0E7490,#67E8F9", thumb="ebfea0a757a60f8188be4dec9fc937d2",
       blurb="Haza Games' house tycoon. I'm part of the team behind it."),
]
YT = dict(url="https://www.youtube.com/@sroolsking", handle="@sroolsking", channel_id="UCxVNuXOtvIn214EDRwgAgPQ", subs=986, videos=151, views=349226, since="Jan 2020")
TW = dict(url="https://www.twitch.tv/sroolsking", handle="twitch.tv/sroolsking", login="sroolsking", followers=159)
FTB = dict(url="https://www.youtube.com/@FTBVision", handle="@FTBVision", channel_id="UC8OVbnfqSap98PcS69iWfgg", subs=125, videos=34, role="Founder, director and manager")
CONTACT = [
  ("Discord", "discord.gg/WewVqAu", "https://discord.gg/WewVqAu"),
  ("Instagram", "@sroolsking_", "https://www.instagram.com/sroolsking_"),
  ("X", "@sroolsking", "https://twitter.com/sroolsking"),
  ("Roblox", "@SRoolsKing", "https://www.roblox.com/users/1074781327/profile"),
  ("Golden Eagle Studios", "Roblox group · in-game rewards for members", "https://www.roblox.com/groups/11451117/Golden-Eagle-Studios"),
  ("Honneur", "shophonneur.com", "https://shophonneur.com/"),
]

def n(x): return f"{x:,}"
def compact(x):
    if x >= 1e9: return f"{x/1e9:.1f}B"
    if x >= 1e6: return f"{x/1e6:.1f}M".replace(".0M","M")
    if x >= 1e3: return f"{x/1e3:.1f}K".replace(".0K","K")
    return str(x)
def esc(s): return html.escape(s, quote=True)

# Private / unlisted projects (test places, unreleased games) as of the snapshot date. Counted in the totals, not listed.
UNLISTED_VISITS = 78900
UNLISTED_FAVS = 5908
own_visits = sum(g["visits"] for g in GAMES) + UNLISTED_VISITS
own_favs = sum(g["favs"] for g in GAMES) + UNLISTED_FAVS
all_visits = own_visits + sum(g["visits"] for g in WORKED_ON)
all_favs = own_favs + sum(g["favs"] for g in WORKED_ON)

STATUS = {"live":("Live","live"), "beta":("Beta","beta"), "retired":("Retired","retired")}

def shot(g, cls="shot"):
    return (f'<span class="{cls}" style="background:linear-gradient(135deg,{g["grad"]})">'
            f'<span class="fb">{esc(g["name"])}</span>'
            f'<img src="{CDN.format(g["thumb"])}" alt="" data-thumb="{g["u"]}" onerror="this.remove()" loading="lazy" decoding="async"></span>')

def card(g):
    label, cls = STATUS[g["status"]]
    url = f'https://www.roblox.com/games/{g["p"]}'
    chips = f'<span class="chip {cls}">{label}</span><span class="chip">{esc(g["by"])}</span>'
    if g["code"]: chips += f'<span class="chip code">Code {esc(g["code"])}</span>'
    play = "" if g["status"] == "retired" else f'<a class="btn sm" href="{url}" target="_blank" rel="noopener">Play <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg></a>'
    link_open = f'<a href="{url}" target="_blank" rel="noopener" class="shot-link" aria-label="Play {esc(g["name"])}">' if g["status"] != "retired" else '<span class="shot-link">'
    link_close = "</a>" if g["status"] != "retired" else "</span>"
    return f'''<article class="card" data-u="{g["u"]}">
  {link_open}{shot(g)}{link_close}
  <div class="cap">
    <div class="cap-top"><h3>{esc(g["name"])}</h3><span class="year">{g["year"]}</span></div>
    <p>{esc(g["blurb"])}</p>
    <div class="chips">{chips}</div>
    <dl class="kv">
      <div><dd data-k="visits">{n(g["visits"])}</dd><dt>visits</dt></div>
      <div><dd data-k="favs">{n(g["favs"])}</dd><dt>favorites</dt></div>
      <div class="playing" hidden><dd data-k="playing">0</dd><dt>playing now</dt></div>
    </dl>
    {play}
  </div>
</article>'''

def row(g):
    label, cls = STATUS[g["status"]]
    url = f'https://www.roblox.com/games/{g["p"]}'
    return f'''<a class="rowg" href="{url}" target="_blank" rel="noopener" data-u="{g["u"]}">
  {shot(g, "mini")}
  <span class="rowg-main"><b>{esc(g["name"])}</b><span>{esc(g["blurb"])}</span></span>
  <span class="rowg-meta"><span class="chip {cls}">{label}</span><span class="year">{g["year"]}</span></span>
  <span class="rowg-n"><b data-k="visits">{n(g["visits"])}</b> visits</span>
  <span class="arrow" aria-hidden="true">→</span>
</a>'''

new_games = [g for g in GAMES if g["year"] == "2026" and g["visits"] < 100000]
big = sorted([g for g in GAMES if g not in new_games and g["visits"] >= 1000000], key=lambda g: -g["visits"])
rest = sorted([g for g in GAMES if g not in new_games and g not in big], key=lambda g: -g["visits"])
w = WORKED_ON[0]
wurl = f'https://www.roblox.com/games/{w["p"]}'

CSS = r"""
/* Builder's project sheet: one 1080px column, hairline-ruled sections, 16:9 shots with a caption under each. */
:root{
  --bg:#F5F6F7; --fg:#141517; --muted:#696D74; --line:#E0E2E6; --panel:#FFFFFF;
  --accent:#F2B705; --live:#17A34A;
  --display:"Bricolage Grotesque","Arial Narrow",system-ui,sans-serif;
  --body:"Schibsted Grotesk","Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0F1012; --fg:#F2F2F0; --muted:#9A9EA6; --line:#26282D; --panel:#17181B;
  --accent:#F7C32E; --live:#3DDC6A; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0F1012; --fg:#F2F2F0; --muted:#9A9EA6; --line:#26282D; --panel:#17181B;
  --accent:#F7C32E; --live:#3DDC6A; color-scheme:dark}
body{background:var(--bg)}
#srk{background:var(--bg);color:var(--fg);font:400 17px/1.5 var(--body);max-width:1080px;margin:0 auto;padding-inline:20px;padding-block:0 40px;box-sizing:border-box}
#srk *{box-sizing:border-box}
#srk a{color:inherit;text-decoration:none}
#srk a:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:8px}
#srk ::selection{background:var(--accent);color:#141517}
#srk h1,#srk h2,#srk h3{margin:0;font-family:var(--display);text-wrap:balance;letter-spacing:-.02em;color:var(--fg)}
#srk p{margin:0}
#srk .eyebrow{font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
#srk .mono{font-family:var(--mono);font-size:12.5px;letter-spacing:.02em}
#srk .muted{color:var(--muted)}

/* Nav */
#srk .nav{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-block:22px}
#srk .mark{font:700 20px/1 var(--display);letter-spacing:-.02em}
#srk .mark b{color:var(--accent)}
#srk .nav ul{display:flex;gap:22px;list-style:none;margin:0;padding:0;font-size:15px;font-weight:500;color:var(--muted)}
#srk .nav ul a:hover{color:var(--fg)}

/* Hero */
#srk .hero{display:grid;grid-template-columns:1fr 300px;gap:40px;align-items:end;padding-block:48px 44px}
#srk .hero-copy{display:flex;flex-direction:column;gap:22px;min-width:0}
#srk h1{font-size:clamp(46px,8vw,100px);font-weight:800;line-height:.94;font-variation-settings:"opsz" 96}
#srk .lede{font-size:19px;color:var(--muted);max-width:46ch}
#srk .lede b{color:var(--fg);font-weight:600}
#srk .cta{display:flex;flex-wrap:wrap;gap:10px}
#srk .btn{display:inline-flex;align-items:center;gap:8px;font:600 15px var(--body);padding:12px 20px;border-radius:999px;border:1.5px solid var(--fg);background:var(--fg);color:var(--bg);transition:transform .12s;cursor:pointer}
#srk .btn:hover{transform:translateY(-1px)}
#srk .btn.ghost{background:transparent;color:var(--fg)}
#srk .btn.sm{padding:9px 16px;font-size:14px}
#srk .btn svg{width:14px;height:14px;fill:currentColor}
#srk .avatar{position:relative;aspect-ratio:1;max-width:100%;border-radius:24px;background:var(--panel);border:1px solid var(--line);overflow:hidden}
#srk .avatar img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
#srk .avatar .fb{position:absolute;inset:0;display:grid;place-items:center;font:800 72px var(--display);color:var(--line)}
#srk .avatar .tag{position:absolute;left:14px;bottom:12px;color:var(--muted);z-index:1}

/* Stats strip */
#srk .strip{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:0}
#srk .strip>div{padding:18px 0;display:flex;flex-direction:column;gap:2px;min-width:0}
#srk .strip>div+div{padding-left:24px;border-left:1px solid var(--line)}
#srk .strip dd{margin:0;font:600 clamp(22px,2.8vw,32px)/1.1 var(--display);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
#srk .strip dt{font-size:13px;color:var(--muted)}
#srk .split{display:flex;flex-wrap:wrap;gap:6px 24px;padding-top:14px;font-size:14px;color:var(--muted)}
#srk .split b{color:var(--fg);font-weight:600;font-variant-numeric:tabular-nums}

/* Sections */
#srk section{padding-block:64px 0}
#srk .sec{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:24px}
#srk .sec h2{font-size:clamp(28px,3.6vw,40px);font-weight:700}
#srk .sec .note{font-size:14px;color:var(--muted)}
#srk .dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--muted);margin-right:6px;vertical-align:1px}
#srk .dot.on{background:var(--live)}

/* Cards */
#srk .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:40px 28px}
#srk .card{display:flex;flex-direction:column;gap:16px;min-width:0}
#srk .shot-link{display:block}
#srk .shot{position:relative;display:block;aspect-ratio:16/9;max-width:100%;border-radius:18px;overflow:hidden;background:var(--panel);transition:transform .18s}
#srk a.shot-link:hover .shot{transform:scale(1.01)}
#srk .shot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
#srk .shot .fb{position:absolute;inset:0;display:flex;align-items:flex-end;padding:clamp(14px,3vw,26px);color:#fff;font:800 clamp(22px,3.4vw,38px)/.95 var(--display);letter-spacing:-.03em;text-shadow:0 2px 20px rgba(0,0,0,.25)}
#srk .cap{display:flex;flex-direction:column;gap:12px;min-width:0}
#srk .cap-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
#srk .cap h3{font-size:clamp(21px,2.4vw,26px);font-weight:700}
#srk .year{font-family:var(--mono);font-size:13px;color:var(--muted);flex:none}
#srk .cap p{color:var(--muted);font-size:15.5px;max-width:52ch}
#srk .chips{display:flex;flex-wrap:wrap;gap:8px}
#srk .chip{font-size:12.5px;font-weight:500;padding:4px 9px;border-radius:7px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
#srk .chip.live{color:var(--live);border-color:color-mix(in srgb,var(--live) 40%,var(--line))}
#srk .chip.beta{color:var(--fg)}
#srk .chip.retired{border-style:dashed}
#srk .chip.code{font-family:var(--mono);font-size:12px}
#srk .kv{display:flex;flex-wrap:wrap;gap:10px 24px;margin:0}
#srk .kv>div{display:flex;align-items:baseline;gap:6px;min-width:0}
#srk .kv dd{margin:0;font:600 19px/1.15 var(--display);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
#srk .kv dt{font-size:13px;color:var(--muted)}
#srk .kv .playing dd{color:var(--live)}
#srk .card .btn{align-self:flex-start}

/* Compact rows */
#srk .rows{display:flex;flex-direction:column;border-top:1px solid var(--line)}
#srk .rowg{display:grid;grid-template-columns:120px minmax(0,1.6fr) auto auto 20px;gap:18px;align-items:center;padding:14px 2px;border-bottom:1px solid var(--line)}
#srk .mini{position:relative;display:block;aspect-ratio:16/9;width:120px;max-width:100%;border-radius:10px;overflow:hidden}
#srk .mini img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
#srk .mini .fb{position:absolute;inset:0;display:flex;align-items:flex-end;padding:6px 8px;color:#fff;font:800 11px/1.05 var(--display);letter-spacing:-.02em}
#srk .rowg-main{display:flex;flex-direction:column;gap:2px;min-width:0}
#srk .rowg-main b{font-weight:600}
#srk .rowg-main span{font-size:14px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#srk .rowg-meta{display:flex;align-items:center;gap:10px}
#srk .rowg-n{font-size:14px;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}
#srk .rowg-n b{color:var(--fg);font-weight:600}
#srk .arrow{color:var(--muted);transition:transform .15s}
#srk .rowg:hover .arrow,#srk .row:hover .arrow{transform:translateX(4px);color:var(--fg)}

/* Worked on */
#srk .worked{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:28px;align-items:center;padding:24px;border-radius:22px;background:var(--panel);border:1px solid var(--line)}
#srk .worked .cap{gap:10px}
#srk .worked .big{font:700 clamp(36px,5vw,56px)/1 var(--display);font-variant-numeric:tabular-nums;letter-spacing:-.03em}
#srk .worked .big small{display:block;font:400 14px/1.4 var(--body);color:var(--muted);letter-spacing:0;margin-top:6px}

/* Watch */
#srk .tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
#srk .tile{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:center;padding:22px 24px;border-radius:18px;background:var(--panel);border:1px solid var(--line);transition:transform .15s}
#srk a.tile:hover{transform:translateY(-2px)}
#srk .tile .ic{width:48px;height:48px;border-radius:12px;display:grid;place-items:center}
#srk .tile .ic svg{width:24px;height:24px;fill:#fff}
#srk .tile .t{display:flex;flex-direction:column;gap:2px;min-width:0}
#srk .tile .t b{font-weight:600;font-size:17px}
#srk .tile .t span{font-size:14px;color:var(--muted);overflow-wrap:anywhere}
#srk .tile .stats{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:6px;font-size:14px;color:var(--muted)}
#srk .tile .stats b{color:var(--fg);font-weight:600;font-variant-numeric:tabular-nums}
#srk .tile .arrow{font-size:20px}
#srk .liv{display:none;font-size:11px;font-weight:700;letter-spacing:.08em;padding:3px 7px;border-radius:5px;background:#E11D48;color:#fff;vertical-align:2px;margin-left:8px}
#srk .liv.on{display:inline-block}

/* Contact */
#srk .row{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 2px;border-bottom:1px solid var(--line)}
#srk .row .l{display:flex;flex-direction:column;gap:2px;min-width:0}
#srk .row .l b{font-weight:600}
#srk .row .l span{font-size:14px;color:var(--muted);overflow-wrap:anywhere}

#srk footer{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;padding-block:56px 0;font-size:14px;color:var(--muted)}

@media (max-width:820px){
  #srk .hero{grid-template-columns:1fr;gap:28px;align-items:start}
  #srk .avatar{width:180px}
  #srk .strip{grid-template-columns:1fr 1fr}
  #srk .strip>div:nth-child(3){padding-left:0;border-left:0}
  #srk .strip>div:nth-child(n+3){border-top:1px solid var(--line)}
  #srk .grid{grid-template-columns:1fr;gap:36px}
  #srk .worked{grid-template-columns:1fr}
  #srk .tiles{grid-template-columns:1fr}
  #srk .rowg{grid-template-columns:96px minmax(0,1fr) 20px;grid-template-areas:"img main arrow" "img meta arrow" "img n arrow";row-gap:6px}
  #srk .mini{width:96px;grid-area:img}
  #srk .rowg-main{grid-area:main} #srk .rowg-meta{grid-area:meta} #srk .rowg-n{grid-area:n} #srk .rowg .arrow{grid-area:arrow}
}
@media (max-width:520px){
  #srk .nav ul{gap:16px;font-size:14px}
  #srk section{padding-block:52px 0}
  #srk .shot{border-radius:14px}
}
@media (prefers-reduced-motion:reduce){#srk *{transition:none!important}}
"""

YT_SVG = '<path d="M23 7.5a3 3 0 00-2.1-2.1C19 5 12 5 12 5s-7 0-8.9.4A3 3 0 001 7.5 31 31 0 00.6 12a31 31 0 00.4 4.5 3 3 0 002.1 2.1C5 19 12 19 12 19s7 0 8.9-.4a3 3 0 002.1-2.1 31 31 0 00.4-4.5 31 31 0 00-.4-4.5zM9.8 15.1V8.9l5.4 3.1z"/>'
TW_SVG = '<path d="M4.3 2L2.5 6.4v15.2h5.2V24h3l2.6-2.4h4.2L23 15.9V2zm16.6 13l-3.1 3h-5.2l-2.6 2.4V18H5.6V4.1h15.3zM17.6 7.9h-2.1v5.5h2.1zm-5.5 0H10v5.5h2.1z"/>'

BODY = f'''<div id="srk">
  <nav class="nav" aria-label="Main">
    <a class="mark" href="#top">SRools<b>King</b></a>
    <ul><li><a href="#games">Games</a></li><li><a href="#watch">Watch</a></li><li><a href="#contact">Contact</a></li></ul>
  </nav>

  <header class="hero" id="top">
    <div class="hero-copy">
      <span class="eyebrow">Roblox builder · Brooklyn, NY</span>
      <h1>I build Roblox tycoons.</h1>
      <p class="lede">Founder of <b>Golden Eagle Studios</b> and <b>Peregrine Falcon Studios</b>. Twelve games of my own since 2020, from <b>Ultimate Modern House Tycoon</b> to <b>Ultimate Mansion Tycoon</b>, and part of the team behind <b>House Tycoon 2</b>.</p>
      <div class="cta">
        <a class="btn" href="https://www.roblox.com/games/127633247396147" target="_blank" rel="noopener">Play the latest <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg></a>
        <a class="btn ghost" href="#watch">Watch</a>
      </div>
    </div>
    <div class="avatar">
      <span class="fb" aria-hidden="true">SR</span>
      <img src="{AVATAR}" alt="SRoolsKing's Roblox avatar" data-avatar onerror="this.remove()">
      <span class="tag mono">@SRoolsKing</span>
    </div>
  </header>

  <dl class="strip" aria-label="Totals across every game">
    <div><dd id="t-visits">{n(all_visits)}</dd><dt>Total visits</dt></div>
    <div><dd id="t-favs">{n(all_favs)}</dd><dt>Favorites</dt></div>
    <div><dd>{len(GAMES) + len(WORKED_ON)}</dd><dt>Games</dt></div>
    <div><dd>2020</dd><dt>Building since</dt></div>
  </dl>
  <div class="split"><span><b id="t-own">{n(own_visits)}</b> on my own games, incl. unlisted projects</span><span><b id="t-worked">{n(w["visits"])}</b> on House Tycoon 2</span><span><span class="dot" id="dot"></span><span id="live-text">Stats as of {SNAPSHOT}</span></span></div>

  <section id="games">
    <div class="sec"><h2>New</h2><span class="note">In beta, updated often</span></div>
    <div class="grid">
{chr(10).join(card(g) for g in new_games)}
    </div>
  </section>

  <section>
    <div class="sec"><h2>Most played</h2><span class="note">Over a million visits each</span></div>
    <div class="grid">
{chr(10).join(card(g) for g in big)}
    </div>
  </section>

  <section>
    <div class="sec"><h2>More</h2><span class="note">Smaller builds and hangouts</span></div>
    <div class="rows">
{chr(10).join(row(g) for g in rest)}
    </div>
  </section>

  <section id="worked">
    <div class="sec"><h2>Worked on</h2><span class="note">Other teams' games I've built for</span></div>
    <div class="worked" data-u="{w["u"]}">
      <a href="{wurl}" target="_blank" rel="noopener" class="shot-link" aria-label="Play House Tycoon 2">{shot(w)}</a>
      <div class="cap">
        <div class="cap-top"><h3>{esc(w["name"])}</h3><span class="year">{w["year"]}</span></div>
        <p>{esc(w["blurb"])}</p>
        <div class="chips"><span class="chip live">Live</span><span class="chip">{esc(w["by"])}</span></div>
        <div class="big"><span data-k="visits">{n(w["visits"])}</span><small><span data-k="favs">{n(w["favs"])}</span> favorites · <span data-k="playing">{n(w["playing"])}</span> playing now</small></div>
        <a class="btn sm" href="{wurl}" target="_blank" rel="noopener">Play <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg></a>
      </div>
    </div>
  </section>

  <section id="watch">
    <div class="sec"><h2>Watch</h2><span class="note">Dev logs, builds, live sessions and FTB</span></div>
    <div class="tiles">
      <a class="tile" href="{YT["url"]}" target="_blank" rel="noopener">
        <span class="ic" style="background:#FF0033"><svg viewBox="0 0 24 24" aria-hidden="true">{YT_SVG}</svg></span>
        <span class="t"><b>YouTube</b><span>{YT["handle"]} · since {YT["since"]}</span>
          <span class="stats"><span><b id="yt-subs">{n(YT["subs"])}</b> subscribers</span><span><b id="yt-videos">{n(YT["videos"])}</b> videos</span><span><b id="yt-views">{n(YT["views"])}</b> views</span></span></span>
        <span class="arrow" aria-hidden="true">↗</span>
      </a>
      <a class="tile" href="{FTB["url"]}" target="_blank" rel="noopener">
        <span class="ic" style="background:#FF0033"><svg viewBox="0 0 24 24" aria-hidden="true">{YT_SVG}</svg></span>
        <span class="t"><b>FTB</b><span>{FTB["handle"]} · {FTB["role"]}</span>
          <span class="stats"><span><b id="ftb-subs">{n(FTB["subs"])}</b> subscribers</span><span><b id="ftb-videos">{n(FTB["videos"])}</b> videos</span><span id="ftb-views-wrap" hidden><b id="ftb-views">0</b> views</span></span></span>
        <span class="arrow" aria-hidden="true">↗</span>
      </a>
      <a class="tile" href="{TW["url"]}" target="_blank" rel="noopener">
        <span class="ic" style="background:#9146FF"><svg viewBox="0 0 24 24" aria-hidden="true">{TW_SVG}</svg></span>
        <span class="t"><b>Twitch<span class="liv" id="tw-live">LIVE</span></b><span>{TW["handle"]}</span>
          <span class="stats"><span><b id="tw-followers">{n(TW["followers"])}</b> followers</span><span id="tw-uptime" hidden></span></span></span>
        <span class="arrow" aria-hidden="true">↗</span>
      </a>
    </div>
  </section>

  <section id="contact">
    <div class="sec"><h2>Contact</h2><span class="note">Business, collabs, commissions</span></div>
    <div class="rows">
{chr(10).join(f'      <a class="row" href="{u}" target="_blank" rel="noopener"><span class="l"><b>{esc(a)}</b><span>{esc(b)}</span></span><span class="arrow" aria-hidden="true">→</span></a>' for a,b,u in CONTACT)}
    </div>
  </section>

  <footer><span>© 2026 SRoolsKing</span><span>sroolsking.com</span></footer>
</div>'''

UNIVERSES = [g["u"] for g in GAMES] + [g["u"] for g in WORKED_ON]
JS = r"""
<script>
(function(){
  var root = document.getElementById("srk");
  var OWN = %s, WORKED = %s;
  var YT_ID = %s, FTB_ID = %s, YT_API_KEY = "";   /* optional: a YouTube Data API key makes the YouTube numbers official */
  var TW_LOGIN = %s;
  var UNLISTED_VISITS = %s, UNLISTED_FAVS = %s;   /* private and test projects, counted but not listed */
  var fmt = function(x){ return Number(x).toLocaleString("en-US"); };
  var get = function(u, asText){ return fetch(u).then(function(r){ return r.ok ? (asText ? r.text() : r.json()) : null; }).catch(function(){ return null; }); };
  function set(sel, v){ var el = root.querySelector(sel); if (el && v != null) el.textContent = fmt(v); }

  /* Roblox: live visits, favorites, playing-now and fresh thumbnails through the public RoProxy mirror. */
  var ids = OWN.concat(WORKED).join(",");
  Promise.all([
    get("https://games.roproxy.com/v1/games?universeIds=" + ids),
    get("https://thumbnails.roproxy.com/v1/games/multiget/thumbnails?universeIds=" + ids + "&countPerUniverse=1&size=768x432&format=Png&isCircular=false"),
    get("https://thumbnails.roproxy.com/v1/users/avatar?userIds=1074781327&size=420x420&format=Png&isCircular=false")
  ]).then(function(res){
    var gr = res[0], th = res[1], av = res[2];
    if (!gr || !gr.data) return;
    var own = 0, worked = 0, favs = 0;
    gr.data.forEach(function(d){
      var box = root.querySelector('[data-u="' + d.id + '"]'); if (!box) return;
      set('[data-u="' + d.id + '"] [data-k="visits"]', d.visits);
      set('[data-u="' + d.id + '"] [data-k="favs"]', d.favoritedCount);
      var p = box.querySelector(".playing"); if (p){ p.hidden = !d.playing; } set('[data-u="' + d.id + '"] [data-k="playing"]', d.playing);
      if (WORKED.indexOf(d.id) >= 0) worked += d.visits; else own += d.visits;
      favs += d.favoritedCount;
    });
    if (gr.data.length === OWN.length + WORKED.length){
      own += UNLISTED_VISITS; favs += UNLISTED_FAVS;
      set("#t-visits", own + worked); set("#t-favs", favs); set("#t-own", own); set("#t-worked", worked);
    }
    if (th && th.data) th.data.forEach(function(t){
      var u = t.thumbnails && t.thumbnails[0] && t.thumbnails[0].imageUrl;
      var img = root.querySelector('img[data-thumb="' + t.universeId + '"]');
      if (u && img && img.src !== u) img.src = u;
    });
    var a = av && av.data && av.data[0] && av.data[0].imageUrl, ai = root.querySelector("img[data-avatar]");
    if (a && ai && ai.src !== a) ai.src = a;
    root.querySelector("#dot").classList.add("on");
    root.querySelector("#live-text").textContent = "Live from Roblox";
  });

  /* YouTube: official API when a key is set, otherwise a public counter; the numbers in the page are the fallback. */
  [["yt", YT_ID], ["ftb", FTB_ID]].forEach(function(ch){
    var p = ch[0], id = ch[1];
    if (YT_API_KEY){
      get("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + id + "&key=" + YT_API_KEY).then(function(j){
        var s = j && j.items && j.items[0] && j.items[0].statistics; if (!s) return;
        set("#" + p + "-subs", s.subscriberCount); set("#" + p + "-videos", s.videoCount); set("#" + p + "-views", s.viewCount);
        var w = root.querySelector("#" + p + "-views-wrap"); if (w) w.hidden = false;
      });
    } else {
      get("https://api.socialcounts.org/youtube-live-subscriber-count/" + id).then(function(j){
        if (!j) return;
        if (j.est_sub) set("#" + p + "-subs", j.est_sub);
        (j.table || []).forEach(function(r){
          if (/view/i.test(r.name)){ set("#" + p + "-views", r.count); var w = root.querySelector("#" + p + "-views-wrap"); if (w) w.hidden = false; }
          if (/video/i.test(r.name)) set("#" + p + "-videos", r.count);
        });
      });
    }
  });

  /* Twitch: follower count and live status via DecAPI. */
  get("https://decapi.me/twitch/followcount/" + TW_LOGIN, true).then(function(t){ if (t && /^\d+$/.test(t.trim())) set("#tw-followers", t.trim()); });
  get("https://decapi.me/twitch/uptime/" + TW_LOGIN, true).then(function(t){
    if (!t || /offline|error|not found/i.test(t)) return;
    root.querySelector("#tw-live").classList.add("on");
    var up = root.querySelector("#tw-uptime"); up.hidden = false; up.textContent = "live for " + t.trim();
  });
})();
</script>
""" % (json.dumps([g["u"] for g in GAMES]), json.dumps([g["u"] for g in WORKED_ON]), json.dumps(YT["channel_id"]), json.dumps(FTB["channel_id"]), json.dumps(TW["login"]), UNLISTED_VISITS, UNLISTED_FAVS)

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Schibsted+Grotesk:wght@400;500;600&display=swap">'
HEAD = f'<title>SRoolsKing</title>\n<meta name="description" content="SRoolsKing, Roblox builder at Golden Eagle Studios. {compact(all_visits)} visits across tycoons like Ultimate Mansion Tycoon and House Tycoon 2. Games, YouTube, Twitch and contact.">\n{FONTS}\n<style>{CSS}</style>'

out = pathlib.Path(__file__).parent
(out / "srk.html").write_text(HEAD + "\n\n" + BODY + "\n" + JS)
(out / "index.html").write_text('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n' + HEAD + '\n</head>\n<body>\n' + BODY + "\n" + JS + '</body>\n</html>\n')
(out / "squarespace-block.html").write_text(FONTS + "\n<style>" + CSS + "</style>\n" + BODY + "\n" + JS)
(out / "squarespace-custom.css").write_text("""/* SRoolsKing.com: let the Code Block page run edge to edge and hide the Squarespace chrome around it. */
#header, #footer-sections, .header, .site-footer, .sqs-announcement-bar-dropzone { display: none !important; }
.page-section .content-wrapper, .sqs-layout .sqs-row, .sqs-block, .sqs-block-code { padding: 0 !important; margin: 0 !important; max-width: none !important; }
.page-section { padding: 0 !important; min-height: 0 !important; }
.sqs-block-code .sqs-block-content { padding: 0 !important; }
""")
print("own", own_visits, "all", all_visits, "favs", all_favs)
