import math
CSS = "@font-face{font-family:FilmSans;src:url('assets/FilmSans-Bold.ttf');font-weight:700}@font-face{font-family:FilmSans;src:url('assets/FilmSans-Regular.ttf');font-weight:400}*{box-sizing:border-box}#root{position:absolute;inset:0;font-family:FilmSans;color:#f5f3ed}.clip{position:absolute;inset:0;pointer-events:none}.panel{position:absolute;background:rgba(5,17,29,.91);border:1.5px solid #e89b48;border-radius:14px;padding:24px;box-shadow:0 10px 24px rgba(0,0,0,.2)}.label{font-size:28px;font-weight:700;line-height:1.25;letter-spacing:2px;color:#d3dadd}.value{font-size:80px;font-weight:700;line-height:1.1;letter-spacing:-2px;font-variant-numeric:tabular-nums}.unit{font-size:28px;line-height:1.2;letter-spacing:0;color:#d6dadd}.track{position:absolute;left:24px;right:24px;bottom:21px;height:7px;background:#344652;border-radius:3px;overflow:hidden}.fill{height:100%;background:#f7a34c;transform-origin:left center}.gauge .value{position:absolute;left:24px;top:69px}.gauge .unit{position:absolute;right:24px;top:114px}.gauge svg{position:absolute;left:35px;top:132px;width:340px;height:239px}.clock .value{font-size:56px;margin-top:10px;letter-spacing:-1px}.clock .unit{position:absolute;right:24px;bottom:26px}.compact .value{margin-top:8px}.compact .unit{position:absolute;right:24px;top:100px}.caption{position:absolute;left:108px;top:1610px;width:864px;text-align:center;font-size:52px;font-weight:700;line-height:1.25;letter-spacing:-1px}.caption-body{display:inline-block;background:rgba(4,14,24,.91);padding:10px 18px 14px;border-radius:9px}.caption-word{display:inline-block}.emphasis{color:#ffb15b}.rule{position:absolute;height:3px;background:#f4a14b;left:24px;right:24px;top:0;transform-origin:left center}.demo-title{position:absolute;left:108px;top:190px;font-size:38px;font-weight:700;letter-spacing:1px} .caption em{font-style:normal;color:#ffb15b}"

def dial(id, maxi):
    out = '<svg viewBox="0 0 340 260" aria-label="calibrated instrument">'
    for j in range(29):
        th = math.radians(140 + 260 * j / 28)
        major = j % 7 == 0
        ro = 110
        ri = 96 if major else 104
        out += f'<path d="M{170 + ro * math.cos(th):.3f} {144 + ro * math.sin(th):.3f} L{170 + ri * math.cos(th):.3f} {144 + ri * math.sin(th):.3f}" stroke="' + ('#f6a64f' if j > 23 else '#b9cbd1') + f'" stroke-width="{(3 if major else 1.5)}"/>'
    for j, val in [(0, 0), (14, maxi / 2), (28, maxi)]:
        th = math.radians(140 + 260 * j / 28)
        out += f'<text x="{170 + 120 * math.cos(th):.2f}" y="{152 + 120 * math.sin(th):.2f}" fill="#d4dce0" font-size="32" font-family="FilmSans" text-anchor="middle">{val:g}</text>'
    out += f'<g id="{id}"><circle cx="170" cy="144" r="110" fill="transparent"/><path d="M151 144 L269 144" stroke="#ffb15b" stroke-width="5" stroke-linecap="round"/></g><circle cx="170" cy="144" r="8" fill="#f2d1a0"/></svg>'
    return out

def gauge(id, label, x, y, maximum, unit):
    return f'''<section id="{id}-panel" class="panel gauge" style="left:{x}px;top:{y}px;width:410px;height:410px"><div id="{id}-rule" class="rule"></div><div class="label">{label}</div><div id="{id}-value" class="value">0</div><div class="unit">{unit}</div>{dial(id + '-needle', maximum)}<div class="track"><div id="{id}-bar" class="fill"></div></div></section>'''

def clip(id, start, end, inside):
    return f'<div id="{id}" class="clip" data-start="{start}" data-duration="{end - start}">{inside}</div>'

def template(id, body, js):
    return f'<template><style>{CSS}</style><div id="root" data-composition-id="{id}" data-width="1080" data-height="1920">{body}</div><script>{js}</script></template>'
