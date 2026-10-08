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
    return f'''<article class="card" data-u="{g["u"]}">
  <a href="{url}" target="_blank" rel="noopener" class="shot-link" aria-label="Play {esc(g["name"])}">{shot(g)}</a>
  <div class="cap">
    <div class="cap-top"><h3>{esc(g["name"])}</h3><span class="year">{g["year"]}</span></div>
    <p>{esc(g["blurb"])}</p>
    <div class="chips">{chips}</div>
    <dl class="kv">
      <div><dd data-k="visits">{n(g["visits"])}</dd><dt>visits</dt></div>
      <div><dd data-k="favs">{n(g["favs"])}</dd><dt>favorites</dt></div>
      <div class="playing" hidden><dd data-k="playing">0</dd><dt>playing now</dt></div>
    </dl>
    <a class="btn sm" href="{url}" target="_blank" rel="noopener">Play<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg></a>
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

SHOWN = [g for g in GAMES if g["status"] != "retired"]          # retired/private games count in the totals but are not displayed
new_games = [g for g in SHOWN if g["year"] == "2026" and g["visits"] < 100000]
big = sorted([g for g in SHOWN if g not in new_games and g["visits"] >= 1000000], key=lambda g: -g["visits"])
rest = sorted([g for g in SHOWN if g not in new_games and g not in big], key=lambda g: -g["visits"])
w = WORKED_ON[0]

CSS = r"""
/* Dark luxury: one 1120px column on near-black, gold hairlines, cream text, Bodoni numerals. Single committed dark look. */
:root{
  --bg:#0A0A0B; --bg2:#111113; --panel:#151517; --fg:#F3ECDC; --muted:#9A9283; --dim:#5E5A52;
  --line:#26241F; --gold:#D4AF37; --gold-2:#F3D985; --gold-3:#8A6B1E; --gold-line:rgba(212,175,55,.38); --gold-soft:rgba(212,175,55,.10);
  --cash:#43C46F;
  --display:"Bodoni Moda","Didot","Bodoni 72","Times New Roman",serif;
  --body:"Manrope","Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color-scheme:dark;
}
html{background:var(--bg)}
body{background:var(--bg);color:var(--fg)}
#srk{background:var(--bg);color:var(--fg);font:400 16.5px/1.6 var(--body);max-width:1120px;margin:0 auto;padding-inline:22px;padding-block:0 48px;box-sizing:border-box;position:relative}
#srk *{box-sizing:border-box}
#srk a{color:inherit;text-decoration:none}
#srk a:focus-visible,#srk button:focus-visible{outline:2px solid var(--gold);outline-offset:4px}
#srk ::selection{background:var(--gold);color:#0A0A0B}
#srk h1,#srk h2,#srk h3{margin:0;font-family:var(--display);font-weight:600;letter-spacing:-.01em;text-wrap:balance;color:var(--fg)}
#srk p{margin:0}
#srk .eyebrow{font:600 11.5px/1.4 var(--body);letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}
#srk .mono{font-family:var(--mono);font-size:12px;letter-spacing:.06em}
#srk .gold{background:linear-gradient(100deg,var(--gold-2) 0%,var(--gold) 45%,var(--gold-3) 100%);-webkit-background-clip:text;background-clip:text;color:transparent}

/* Nav */
#srk .nav{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-block:26px;border-bottom:1px solid var(--line)}
#srk .mark{display:inline-flex;align-items:center;gap:10px;font:600 21px/1 var(--display);letter-spacing:.02em}
#srk .mark svg{width:26px;height:26px;fill:none;stroke:var(--gold);stroke-width:1.4;stroke-linejoin:round}
#srk .nav ul{display:flex;gap:28px;list-style:none;margin:0;padding:0;font:600 11.5px var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
#srk .nav ul a{padding-bottom:4px;border-bottom:1px solid transparent}
#srk .nav ul a:hover{color:var(--gold);border-bottom-color:var(--gold-line)}

/* Hero */
#srk .hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:48px;align-items:center;padding-block:64px 56px}
#srk .hero-copy{display:flex;flex-direction:column;gap:26px;min-width:0}
#srk h1{font-size:clamp(54px,8.6vw,118px);font-weight:600;line-height:.96;letter-spacing:-.015em}
#srk h1 em{font-style:italic;font-weight:500}
#srk .lede{font-size:18px;line-height:1.65;color:var(--muted);max-width:50ch}
#srk .lede b{color:var(--fg);font-weight:600}
#srk .cta{display:flex;flex-wrap:wrap;gap:12px}
#srk .btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font:700 12px var(--body);letter-spacing:.18em;text-transform:uppercase;padding:16px 26px;border:1px solid var(--gold);background:linear-gradient(100deg,var(--gold-2),var(--gold) 55%,var(--gold-3));color:#0A0A0B;transition:transform .15s,box-shadow .15s}
#srk .btn:hover{transform:translateY(-1px);box-shadow:0 10px 30px rgba(212,175,55,.18)}
#srk .btn.ghost{background:transparent;color:var(--gold)}
#srk .btn.ghost:hover{background:var(--gold-soft)}
#srk .btn.sm{padding:12px 18px;font-size:11px}
#srk .btn svg{width:12px;height:12px;fill:currentColor}
#srk .portrait{position:relative;aspect-ratio:4/5;max-width:100%;border:1px solid var(--gold-line);background:var(--bg2);overflow:hidden}
#srk .portrait::before{content:"";position:absolute;inset:10px;border:1px solid var(--gold-line);pointer-events:none;z-index:2}
#srk .portrait img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 20%;display:block;filter:saturate(.92)}
#srk .portrait .fb{position:absolute;inset:0;display:grid;place-items:center;font:600 120px var(--display);color:var(--line)}
#srk .portrait .tag{position:absolute;left:24px;bottom:20px;z-index:3;color:var(--gold);background:rgba(10,10,11,.7);padding:6px 10px;border:1px solid var(--gold-line)}

/* Ledger */
#srk .strip{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--gold-line);border-bottom:1px solid var(--gold-line);margin:0}
#srk .strip>div{padding:24px 0;display:flex;flex-direction:column;gap:6px;min-width:0}
#srk .strip>div+div{padding-left:28px;border-left:1px solid var(--line)}
#srk .strip dd{margin:0;font:600 clamp(28px,3.4vw,44px)/1 var(--display);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
#srk .strip dt{font:600 11px/1.4 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
#srk .split{display:flex;flex-wrap:wrap;gap:8px 28px;padding-top:16px;font-size:13.5px;color:var(--muted)}
#srk .split b{color:var(--fg);font-weight:600;font-variant-numeric:tabular-nums}
#srk .dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--dim);margin-right:8px;vertical-align:1px}
#srk .dot.on{background:var(--cash);box-shadow:0 0 0 3px rgba(67,196,111,.18)}

/* Sections */
#srk section{padding-block:72px 0}
#srk .sec{display:flex;align-items:baseline;gap:20px;margin-bottom:30px}
#srk .sec h2{font-size:clamp(32px,4vw,46px);white-space:nowrap}
#srk .sec .rule{flex:1;height:1px;background:linear-gradient(90deg,var(--gold-line),transparent)}
#srk .sec .note{font:600 11px/1.4 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--muted);white-space:nowrap}

/* Cards */
#srk .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:48px 32px}
#srk .card{display:flex;flex-direction:column;gap:18px;min-width:0}
#srk .shot-link{display:block}
#srk .shot{position:relative;display:block;aspect-ratio:16/9;max-width:100%;overflow:hidden;background:var(--bg2);border:1px solid var(--line);transition:border-color .2s,transform .25s}
#srk a.shot-link:hover .shot{border-color:var(--gold);transform:translateY(-3px)}
#srk .shot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
#srk .shot .fb{position:absolute;inset:0;display:flex;align-items:flex-end;padding:clamp(14px,3vw,26px);color:#fff;font:600 clamp(22px,3.2vw,36px)/1 var(--display);letter-spacing:-.01em;text-shadow:0 2px 20px rgba(0,0,0,.4)}
#srk .cap{display:flex;flex-direction:column;gap:12px;min-width:0}
#srk .cap-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
#srk .cap h3{font-size:clamp(24px,2.6vw,30px)}
#srk .year{font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:var(--gold);flex:none}
#srk .cap p{color:var(--muted);font-size:15px;max-width:52ch}
#srk .chips{display:flex;flex-wrap:wrap;gap:8px}
#srk .chip{font:600 10.5px/1 var(--body);letter-spacing:.16em;text-transform:uppercase;padding:7px 10px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
#srk .chip.live{color:var(--cash);border-color:rgba(67,196,111,.35)}
#srk .chip.beta{color:var(--gold);border-color:var(--gold-line)}
#srk .chip.code{font-family:var(--mono);text-transform:none;letter-spacing:.06em;font-size:11.5px}
#srk .kv{display:flex;flex-wrap:wrap;gap:10px 26px;margin:0}
#srk .kv>div{display:flex;align-items:baseline;gap:7px;min-width:0}
#srk .kv dd{margin:0;font:600 22px/1 var(--display);font-variant-numeric:tabular-nums}
#srk .kv dt{font-size:12.5px;letter-spacing:.04em;color:var(--muted)}
#srk .kv .playing dd{color:var(--cash)}
#srk .card .btn{align-self:flex-start}

/* Compact rows */
#srk .rows{display:flex;flex-direction:column;border-top:1px solid var(--line)}
#srk .rowg{display:grid;grid-template-columns:128px minmax(0,1.6fr) auto auto 24px;gap:20px;align-items:center;padding:16px 4px;border-bottom:1px solid var(--line);transition:background .15s}
#srk .rowg:hover{background:var(--bg2)}
#srk .mini{position:relative;display:block;aspect-ratio:16/9;width:128px;max-width:100%;overflow:hidden;border:1px solid var(--line)}
#srk .mini img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
#srk .mini .fb{position:absolute;inset:0;display:flex;align-items:flex-end;padding:6px 8px;color:#fff;font:600 11px/1.05 var(--display)}
#srk .rowg-main{display:flex;flex-direction:column;gap:3px;min-width:0}
#srk .rowg-main b{font:600 18px/1.2 var(--display)}
#srk .rowg-main span{font-size:13.5px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#srk .rowg-meta{display:flex;align-items:center;gap:12px}
#srk .rowg-n{font-size:13.5px;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}
#srk .rowg-n b{color:var(--fg);font:600 18px/1 var(--display)}
#srk .arrow{color:var(--dim);transition:transform .15s,color .15s;font-size:18px}
#srk .rowg:hover .arrow,#srk .row:hover .arrow{transform:translateX(5px);color:var(--gold)}

/* Watch */
#srk .tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}
#srk .tile{display:grid;grid-template-columns:auto 1fr auto;gap:18px;align-items:center;padding:24px;background:var(--panel);border:1px solid var(--line);transition:border-color .2s,transform .15s}
#srk a.tile:hover{border-color:var(--gold-line);transform:translateY(-2px)}
#srk .tile .ic{width:48px;height:48px;display:grid;place-items:center;background:linear-gradient(135deg,var(--gold-2),var(--gold) 55%,var(--gold-3));color:#0A0A0B}
#srk .tile .ic svg{width:22px;height:22px;fill:currentColor}
#srk .tile .t{display:flex;flex-direction:column;gap:3px;min-width:0}
#srk .tile .t b{font:600 20px/1.2 var(--display)}
#srk .tile .t span{font-size:13.5px;color:var(--muted);overflow-wrap:anywhere}
#srk .tile .stats{display:flex;flex-wrap:wrap;gap:4px 16px;margin-top:8px;font-size:13px;color:var(--muted)}
#srk .tile .stats b{color:var(--fg);font:600 17px/1 var(--display);font-variant-numeric:tabular-nums}
#srk .tile .arrow{font-size:20px}
#srk .liv{display:none;font:700 10px/1 var(--body);letter-spacing:.14em;padding:4px 7px;background:#C8102E;color:#fff;vertical-align:3px;margin-left:10px}
#srk .liv.on{display:inline-block}

/* Contact */
#srk .row{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:18px 4px;border-bottom:1px solid var(--line);transition:background .15s}
#srk .row:hover{background:var(--bg2)}
#srk .row .l{display:flex;flex-direction:column;gap:3px;min-width:0}
#srk .row .l b{font:600 19px/1.2 var(--display)}
#srk .row .l span{font-size:13.5px;color:var(--muted);overflow-wrap:anywhere}

#srk footer{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;padding-block:64px 0;font:600 11px/1.4 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--dim)}
#srk footer .mark{font-size:16px;color:var(--muted)}

@media (max-width:860px){
  #srk .hero{grid-template-columns:1fr;gap:34px;padding-block:44px 40px}
  #srk .portrait{width:min(100%,280px)}
  #srk .cta{flex-direction:column}
  #srk .btn{width:100%}
  #srk .card .btn{width:auto}
  #srk .strip{grid-template-columns:1fr 1fr}
  #srk .strip>div:nth-child(3){padding-left:0;border-left:0}
  #srk .strip>div:nth-child(n+3){border-top:1px solid var(--line)}
  #srk .grid{grid-template-columns:1fr;gap:40px}
  #srk .rowg{grid-template-columns:100px minmax(0,1fr) 24px;grid-template-areas:"img main arrow" "img meta arrow" "img n arrow";row-gap:6px}
  #srk .mini{width:100px;grid-area:img}
  #srk .rowg-main{grid-area:main} #srk .rowg-meta{grid-area:meta} #srk .rowg-n{grid-area:n} #srk .rowg .arrow{grid-area:arrow}
  #srk .sec{flex-wrap:wrap;gap:12px}
  #srk .sec .rule{display:none}
}
@media (max-width:520px){
  #srk .nav ul{gap:18px;font-size:10.5px;letter-spacing:.14em}
  #srk section{padding-block:56px 0}
}
@media (prefers-reduced-motion:reduce){#srk *{transition:none!important}}
"""

HAT = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M9 21.5 L10.2 9.5 Q10.4 7.5 12.4 7.5 L19.6 7.5 Q21.6 7.5 21.8 9.5 L23 21.5"/><path d="M10 16.5 L22 16.5"/><ellipse cx="16" cy="22.5" rx="12" ry="3.2"/></svg>'
YT_SVG = '<path d="M23 7.5a3 3 0 00-2.1-2.1C19 5 12 5 12 5s-7 0-8.9.4A3 3 0 001 7.5 31 31 0 00.6 12a31 31 0 00.4 4.5 3 3 0 002.1 2.1C5 19 12 19 12 19s7 0 8.9-.4a3 3 0 002.1-2.1 31 31 0 00.4-4.5 31 31 0 00-.4-4.5zM9.8 15.1V8.9l5.4 3.1z"/>'
TW_SVG = '<path d="M4.3 2L2.5 6.4v15.2h5.2V24h3l2.6-2.4h4.2L23 15.9V2zm16.6 13l-3.1 3h-5.2l-2.6 2.4V18H5.6V4.1h15.3zM17.6 7.9h-2.1v5.5h2.1zm-5.5 0H10v5.5h2.1z"/>'

def sec(title, note):
    return f'<div class="sec"><h2>{title}</h2><span class="rule"></span><span class="note">{note}</span></div>'

BODY = f'''<div id="srk">
  <nav class="nav" aria-label="Main">
    <a class="mark" href="#top">{HAT}SRoolsKing</a>
    <ul><li><a href="#games">Games</a></li><li><a href="#watch">Watch</a></li><li><a href="#contact">Contact</a></li></ul>
  </nav>

  <header class="hero" id="top">
    <div class="hero-copy">
      <span class="eyebrow">Founder · Golden Eagle Studios · Peregrine Falcon Studios</span>
      <h1>I build <em class="gold">video games.</em></h1>
      <p class="lede">Roblox tycoons since 2020, from <b>Ultimate Modern House Tycoon</b> to <b>Ultimate Mansion Tycoon</b> and <b>Billionaire House Tycoon</b>, plus builds for other studios. Based in Brooklyn, NY.</p>
      <div class="cta">
        <a class="btn" href="https://www.roblox.com/games/127633247396147" target="_blank" rel="noopener">Play the latest<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg></a>
        <a class="btn ghost" href="#watch">Watch</a>
      </div>
    </div>
    <div class="portrait">
      <span class="fb" aria-hidden="true">S</span>
      <img src="{AVATAR}" alt="SRoolsKing's Roblox avatar" data-avatar onerror="this.remove()">
      <span class="tag mono">@SRoolsKing</span>
    </div>
  </header>

  <dl class="strip" aria-label="Totals across every game">
    <div><dd class="gold" id="t-visits">{n(all_visits)}</dd><dt>Total visits</dt></div>
    <div><dd id="t-favs">{n(all_favs)}</dd><dt>Favorites</dt></div>
    <div><dd>{len(GAMES) + len(WORKED_ON)}</dd><dt>Games shipped</dt></div>
    <div><dd>2020</dd><dt>Building since</dt></div>
  </dl>
  <div class="split"><span><b id="t-own">{n(own_visits)}</b> on my own games</span><span><b id="t-worked">{n(w["visits"])}</b> on games built for other studios</span><span><span class="dot" id="dot"></span><span id="live-text">Stats as of {SNAPSHOT}</span></span></div>

  <section id="games">
    {sec("New", "In beta, updated often")}
    <div class="grid">
{chr(10).join(card(g) for g in new_games)}
    </div>
  </section>

  <section>
    {sec("Most played", "Over a million visits each")}
    <div class="grid">
{chr(10).join(card(g) for g in big)}
    </div>
  </section>

  <section>
    {sec("More", "Smaller builds and hangouts")}
    <div class="rows">
{chr(10).join(row(g) for g in rest)}
    </div>
  </section>

  <section id="watch">
    {sec("Watch", "Dev logs, builds, live sessions and FTB")}
    <div class="tiles">
      <a class="tile" href="{YT["url"]}" target="_blank" rel="noopener">
        <span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">{YT_SVG}</svg></span>
        <span class="t"><b>YouTube</b><span>{YT["handle"]} · since {YT["since"]}</span>
          <span class="stats"><span><b id="yt-subs">{n(YT["subs"])}</b> subscribers</span><span><b id="yt-videos">{n(YT["videos"])}</b> videos</span><span><b id="yt-views">{n(YT["views"])}</b> views</span></span></span>
        <span class="arrow" aria-hidden="true">↗</span>
      </a>
      <a class="tile" href="{FTB["url"]}" target="_blank" rel="noopener">
        <span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">{YT_SVG}</svg></span>
        <span class="t"><b>FTB</b><span>{FTB["handle"]} · {FTB["role"]}</span>
          <span class="stats"><span><b id="ftb-subs">{n(FTB["subs"])}</b> subscribers</span><span><b id="ftb-videos">{n(FTB["videos"])}</b> videos</span><span id="ftb-views-wrap" hidden><b id="ftb-views">0</b> views</span></span></span>
        <span class="arrow" aria-hidden="true">↗</span>
      </a>
      <a class="tile" href="{TW["url"]}" target="_blank" rel="noopener">
        <span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">{TW_SVG}</svg></span>
        <span class="t"><b>Twitch<span class="liv" id="tw-live">LIVE</span></b><span>{TW["handle"]}</span>
          <span class="stats"><span><b id="tw-followers">{n(TW["followers"])}</b> followers</span><span id="tw-uptime" hidden></span></span></span>
        <span class="arrow" aria-hidden="true">↗</span>
      </a>
    </div>
  </section>

  <section id="contact">
    {sec("Contact", "Business, collabs, commissions")}
    <div class="rows">
{chr(10).join(f'      <a class="row" href="{u}" target="_blank" rel="noopener"><span class="l"><b>{esc(a)}</b><span>{esc(b)}</span></span><span class="arrow" aria-hidden="true">→</span></a>' for a,b,u in CONTACT)}
    </div>
  </section>

  <footer><span class="mark">{HAT}SRoolsKing</span><span>© 2026 · sroolsking.com</span></footer>
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
      if (WORKED.indexOf(d.id) >= 0) worked += d.visits; else own += d.visits;
      favs += d.favoritedCount;
      var box = root.querySelector('[data-u="' + d.id + '"]'); if (!box) return;
      set('[data-u="' + d.id + '"] [data-k="visits"]', d.visits);
      set('[data-u="' + d.id + '"] [data-k="favs"]', d.favoritedCount);
      var p = box.querySelector(".playing"); if (p){ p.hidden = !d.playing; } set('[data-u="' + d.id + '"] [data-k="playing"]', d.playing);
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

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;0,6..96,600;1,6..96,500&family=Manrope:wght@400;600;700&display=swap">'
HEAD = f'<title>SRoolsKing</title>\n<meta name="description" content="SRoolsKing, founder of Golden Eagle Studios and Peregrine Falcon Studios. {compact(all_visits)} visits across Roblox tycoons like Ultimate Mansion Tycoon. Games, YouTube, Twitch and contact.">\n{FONTS}\n<style>{CSS}</style>'

out = pathlib.Path(__file__).parent
(out / "srk.html").write_text(HEAD + "\n\n" + BODY + "\n" + JS)
(out / "index.html").write_text('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="theme-color" content="#0A0A0B">\n' + HEAD + '\n</head>\n<body>\n' + BODY + "\n" + JS + '</body>\n</html>\n')
print("own", own_visits, "all", all_visits, "favs", all_favs)
