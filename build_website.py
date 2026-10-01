"""
Therapy Anonymous Bila AI - website builder (Python, standard library only).

What it does
  1. Holds all the text from the business plan (sections 1-24) as Python data.
  2. Builds the website: index, about, services, community, online, agency, pricing, contact (.html),
     plus style.css, script.js and robots.txt, into a folder called "website".
  3. Opens the finished site in your browser.

How to run (PyCharm): right-click this file > Run 'build_website'.
Options:   python build_website.py --no-serve    (build only, do not open the browser)

To change the website: edit the text in the N[...] = sec(...) lines below, or the placeholders
(search for "[") in OLD, then run again.
"""
import re, os, sys

OUT = 'website/'
os.makedirs(OUT, exist_ok=True)

# ---- Page pieces that are not in the plan text (header strip, footer, styles, form script) ----
FONTS = r'''<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Young+Serif&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">'''

FAVICON = r'''<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>&#128330;</text></svg>">'''

CRISIS = r'''<div class="crisis" id="crisis"><div class="wrap">
<strong>If you or someone else is in immediate danger, get help now.</strong>
<p>Kenya Red Cross: <a href="tel:1199">1199</a> &nbsp;|&nbsp; Gender violence helpline: <a href="tel:1195">1195</a> &nbsp;|&nbsp; Befrienders Kenya: <a href="tel:+254722178177">+254 722 178 177</a></p>
</div></div>'''

FOOTER = r'''<footer><div class="wrap"><span>&copy; Therapy Anonymous Bila AI. A safe space to talk. A safe space to heal.</span><span>Services are provided by qualified professionals. Not a substitute for emergency care.</span></div></footer>'''

CSS = r''':root{--bg:#f2f6f4;--surface:#fff;--ink:#14303a;--muted:#48626a;--accent:#1f6f6a;--accent-ink:#fff;--soft:#d5e7e3;--glow:#e8b567;--line:#c5d6d2;
--serif:'Young Serif',Georgia,serif;--sans:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;
box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e1c21;--surface:#152a31;--ink:#e6f0ee;--muted:#a3bbb7;--accent:#6fc2b8;--accent-ink:#0e1c21;--soft:#1c3a40;--glow:#e8b567;--line:#2a464d}}
:root[data-theme="dark"]{--bg:#0e1c21;--surface:#152a31;--ink:#e6f0ee;--muted:#a3bbb7;--accent:#6fc2b8;--accent-ink:#0e1c21;--soft:#1c3a40;--glow:#e8b567;--line:#2a464d}
html{scroll-behavior:smooth;scroll-padding-top:calc(72px + env(safe-area-inset-top,0px))}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 1.06rem/1.65 var(--sans)}
a{color:var(--accent)}
:focus-visible{outline:3px solid var(--glow);outline-offset:3px;border-radius:4px}
h1,h2,h3{font-family:var(--serif);font-weight:400;line-height:1.15;margin:0}
h2{font-size:clamp(1.8rem,4vw,2.5rem);margin-bottom:.6em}
h3{font-size:1.25rem}
p{margin:0 0 1em;max-width:62ch}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
section{padding:72px 0}
header{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:var(--bg);border-bottom:1px solid var(--line)}
nav{display:flex;align-items:center;justify-content:space-between;gap:16px;height:64px}
.logo{font-family:var(--serif);text-decoration:none;color:var(--ink);font-size:1.05rem}
nav ul{display:flex;gap:22px;list-style:none;margin:0;padding:0}
nav ul a{text-decoration:none;color:var(--muted);font-weight:500;font-size:.95rem}
nav ul a:hover{color:var(--ink)}
.btn{display:inline-block;background:var(--accent);color:var(--accent-ink);padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:600;border:0;font:inherit;font-weight:600;cursor:pointer}
.btn.ghost{background:transparent;color:var(--ink);border:1.5px solid var(--line)}
@media(max-width:760px){nav{flex-wrap:wrap;height:auto;padding:10px 0}nav ul{order:3;width:100%;overflow-x:auto;gap:18px;padding-bottom:4px}nav ul a{white-space:nowrap}}
section[hidden]{display:none}
nav ul a[aria-current="page"]{color:var(--ink);border-bottom:2px solid var(--glow);padding-bottom:4px}
.mp{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
@media(max-width:820px){.mp{grid-template-columns:1fr}}
.paybox{background:var(--surface);border:1.5px solid var(--line);border-radius:20px;padding:24px;box-shadow:0 0 0 6px var(--soft)}
.paybox dl{margin:0}.paybox dt{color:var(--muted);font-size:.9rem;margin-top:12px}.paybox dd{margin:0;font-family:var(--serif);font-size:1.4rem}
.mps{margin:0;padding-left:20px}.mps li{padding:4px 0}
/* hero */
.hero{padding:64px 0 80px}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.hero h1{font-family:var(--serif);font-size:clamp(2.4rem,6vw,4.2rem);line-height:1.05;margin-bottom:.4em}
.lead{font-size:1.2rem;color:var(--muted)}
.pad{display:flex;flex-direction:column;background:var(--surface);border:1.5px solid var(--line);border-radius:28px 28px 28px 6px;padding:22px;box-shadow:0 0 0 8px var(--soft)}
.pad label{font-family:var(--serif);font-size:1.15rem;margin-bottom:10px}
.pad textarea{width:100%;min-height:150px;resize:vertical;border:0;background:transparent;color:var(--ink);font:inherit;padding:0}
.pad textarea:focus{outline:none}
.pad .note{display:flex;align-items:center;gap:8px;font-size:.88rem;color:var(--muted);border-top:1px solid var(--line);padding-top:12px;margin-top:10px}
.dot{width:9px;height:9px;border-radius:50%;background:var(--glow);flex:none}
.pad .reply{margin:12px 0 0;color:var(--ink);min-height:1.5em;font-size:.98rem}
.actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px}
@media(max-width:860px){.hero .wrap{grid-template-columns:1fr}}
/* crisis */
.crisis{background:var(--ink);color:var(--bg);padding:26px 0}
.crisis .wrap{display:flex;flex-wrap:wrap;gap:12px 32px;align-items:center}
.crisis strong{font-family:var(--serif);font-weight:400;font-size:1.15rem}
.crisis a{color:var(--bg);font-weight:600}
.crisis p{margin:0;max-width:none}
/* about */
.two{display:grid;grid-template-columns:1fr 1fr;gap:48px}
@media(max-width:820px){.two{grid-template-columns:1fr}}
.values{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}
.values span{background:var(--soft);padding:6px 16px;border-radius:999px;font-weight:500;font-size:.95rem}
/* services */
.svc{border-top:1px solid var(--line)}
.svc details{border-bottom:1px solid var(--line)}
.svc summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;padding:20px 4px;font-family:var(--serif);font-size:1.3rem}
.svc summary::-webkit-details-marker{display:none}
.svc summary::after{content:'+';font-family:var(--sans);color:var(--accent);font-size:1.6rem;line-height:1}
.svc details[open] summary::after{content:'\2212'}
.svc .body{padding:0 4px 24px;display:grid;grid-template-columns:1fr 1fr;gap:4px 32px;color:var(--muted)}
.svc .body p{grid-column:1/-1;color:var(--ink)}
.svc .body span{padding-left:16px;position:relative}
.svc .body span::before{content:'';position:absolute;left:0;top:.7em;width:6px;height:6px;border-radius:50%;background:var(--accent)}
@media(max-width:600px){.svc .body{grid-template-columns:1fr}}
.band{background:var(--soft)}
.support{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:36px}
.support div{border-left:3px solid var(--glow);padding-left:18px}
.support p{color:var(--muted);margin:.5em 0 0}
.list2{columns:2;column-gap:36px;padding:0;list-style:none;margin:0}
.list2 li{break-inside:avoid;padding:5px 0}
@media(max-width:600px){.list2{columns:1}}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:32px}
.tiles p{color:var(--muted)}
/* contact */
.contact{display:grid;grid-template-columns:1fr 1fr;gap:48px}
@media(max-width:820px){.contact{grid-template-columns:1fr}}
.contact input,.contact select,.contact textarea{width:100%;padding:12px 14px;margin:6px 0 16px;border:1.5px solid var(--line);border-radius:12px;background:var(--surface);color:var(--ink);font:inherit}
.contact label{font-weight:500;font-size:.95rem}
.confirm{margin-top:14px;font-weight:600;color:var(--accent)}
footer{border-top:1px solid var(--line);padding:32px 0 40px;color:var(--muted);font-size:.92rem}
footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}
.steps{list-style:none;counter-reset:s;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:28px}
.steps li{counter-increment:s;position:relative;padding-top:52px}
.steps li::before{content:counter(s);position:absolute;top:0;left:0;width:38px;height:38px;border-radius:50%;background:var(--accent);color:var(--accent-ink);display:grid;place-items:center;font-family:var(--serif)}
.steps p{color:var(--muted);margin:.4em 0 0}
.team{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:32px}
.person p{color:var(--muted)}
.person .role{color:var(--accent);font-weight:600;font-size:.92rem;margin:.2em 0 .6em}
.av{width:84px;height:84px;border-radius:50% 50% 50% 12px;background:var(--soft);border:2px solid var(--glow);display:grid;place-items:center;font-family:var(--serif);font-size:1.4rem;margin-bottom:14px}
.price{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}
.price>div{background:var(--surface);border:1.5px solid var(--line);border-radius:18px;padding:24px}
.price .best{border-color:var(--accent);box-shadow:0 0 0 4px var(--soft)}
.price p{color:var(--muted);margin:0}
.price .amt{font-family:var(--serif);font-size:1.6rem;color:var(--ink);margin:8px 0}
.eps{display:grid;gap:12px;margin-top:8px}
.ep{display:flex;gap:14px;align-items:center;background:var(--surface);border:1.5px solid var(--line);border-radius:16px;padding:14px 16px}
.ep small{color:var(--muted)}
.play{flex:none;width:40px;height:40px;border-radius:50%;background:var(--accent);color:var(--accent-ink);display:grid;place-items:center;font-size:.85rem;padding-left:3px}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chips a{text-decoration:none;color:var(--ink);background:var(--soft);padding:10px 18px;border-radius:999px;font-weight:500}
.chips a:hover{background:var(--accent);color:var(--accent-ink)}
main>section h1{font-size:clamp(1.8rem,4vw,2.5rem);margin-bottom:.6em}
.skip{position:absolute;left:-999px;top:0;background:var(--accent);color:var(--accent-ink);padding:10px 16px;z-index:20}.skip:focus{left:8px;top:8px}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
.num{display:inline-block;font:600 .8rem var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:10px}
.num::before{content:"Section ";opacity:.7}
.eyebrow{font:600 .85rem var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 14px}
.plain{list-style:none;padding:0;margin:.6em 0 0;color:var(--muted)}
.plain li{padding:3px 0 3px 16px;position:relative}
.plain li::before{content:"";position:absolute;left:0;top:.8em;width:6px;height:6px;border-radius:50%;background:var(--accent)}
.tag{font-family:var(--serif);font-size:clamp(1.5rem,3.5vw,2.2rem);line-height:1.25;margin:0 0 16px}
.tiles+p,.two+p,.price+p,.list2+p{margin-top:22px}
'''

JS = r'''/* Fill these in, then the booking form opens WhatsApp or email with the request ready to send. */
var CONTACT={whatsapp:"", /* e.g. "2547XXXXXXXX" (country code, no + or spaces) */ email:"" /* e.g. "hello@yourdomain.co.ke" */};
(function(){
var t=document.getElementById('say'),r=document.getElementById('reply'),timer;
if(t&&r){t.addEventListener('input',function(){
clearTimeout(timer);
if(!t.value.trim()){r.textContent='';return}
timer=setTimeout(function(){r.textContent='Thank you for putting that into words. Whenever you are ready, a therapist can listen.'},1400);
});}
var s=document.getElementById('send');
if(s){s.addEventListener('click',function(){
var g=function(i){return document.getElementById(i).value.trim()};
var o=document.getElementById('ok');
if(!g('c')){o.textContent='Add a phone number or email so we can reach you.';return}
var msg='Session request%0AName/nickname: '+encodeURIComponent(g('n')||'Not given')+'%0AContact: '+encodeURIComponent(g('c'))+'%0ASession: '+encodeURIComponent(g('m'))+'%0AMeeting: '+encodeURIComponent(g('w'));
if(CONTACT.whatsapp){window.open('https://wa.me/'+CONTACT.whatsapp+'?text='+msg,'_blank');o.textContent='Opening WhatsApp so you can send your request.';}
else if(CONTACT.email){location.href='mailto:'+CONTACT.email+'?subject='+encodeURIComponent('Session request')+'&body='+msg;o.textContent='Opening your email app so you can send your request.';}
else{o.textContent='Preview only: add a WhatsApp number or email in script.js to receive requests.';}
});}
})();
'''

# ---- Ready-made sections: hero, how it works, team, pricing, M-Pesa, FAQ, booking form ----
OLD = {
    'home': r'''<section class="hero" id="home"><div class="wrap">
<div>
<p class="eyebrow">Mental-health counselling, therapy &amp; advocacy agency</p><h1>A safe space to talk. A safe space to heal.</h1>
<p class="lead">Confidential counselling, therapy and advocacy with real, qualified people. Meet us in person or online, without fear of judgment, stigma or discrimination.</p>
<div class="actions"><a class="btn" href="#book">Book a private session</a><a class="btn ghost" href="#services">See what we help with</a></div>
</div>
<div class="pad">
<label for="say">What's on your mind today?</label>
<textarea id="say" placeholder="Write it here. Just for you."></textarea>
<p class="reply" id="reply" aria-live="polite"></p>
<div class="note"><span class="dot"></span>Nothing typed here is saved or sent anywhere.</div>
</div>
</div></section>''',
    'how': r'''<section id="how" class="band"><div class="wrap">
<h2>Getting started is simple</h2>
<ol class="steps">
<li><h3>Reach out</h3><p>Send a request with a nickname if you prefer. Nothing more is needed.</p></li>
<li><h3>Get matched</h3><p>We pair you with a therapist suited to what you are facing.</p></li>
<li><h3>Your first session</h3><p>Meet in person or online. Go at your own pace, and share only what you want to.</p></li>
<li><h3>Keep going, or pause</h3><p>Continue with regular sessions, add family or group support, or come back when you need us.</p></li>
</ol>
</div></section>''',
    'digital': r'''<section id="digital"><div class="wrap">
<h2>Support that fits your life</h2>
<div class="tiles">
<div><h3>In person</h3><p>Sit down with a therapist in a private, comfortable setting.</p></div>
<div><h3>Online counselling</h3><p>Talk from home, with private, secure sessions and easy appointment booking.</p></div>
<div><h3>Mobile app, coming soon</h3><p>Book appointments, message your therapist, and reach resources and crisis information on Android and iOS.</p></div>
<div><h3>For teams and organisations</h3><p>Corporate mental-health programmes, employee wellbeing activities and team-building experiences, including "Adventures Together".</p></div>
</div>
</div></section>''',
    'team': r'''<section id="team" class="band"><div class="wrap">
<h2>Meet the team</h2>
<p>Our therapists and counsellors each specialise in different areas of mental health, backed by a small team that looks after bookings, records and your privacy.</p>
<div class="team">
<div class="person"><div class="av">T1</div><h3>[Therapist name]</h3><p class="role">[Qualification and registration]</p><p>[Specialities, e.g. trauma, grief, couples]. Add a short, warm introduction here.</p></div>
<div class="person"><div class="av">T2</div><h3>[Therapist name]</h3><p class="role">[Qualification and registration]</p><p>[Specialities, e.g. childhood trauma, family counselling]. Add a short, warm introduction here.</p></div>
<div class="person"><div class="av">T3</div><h3>[Counsellor name]</h3><p class="role">[Qualification and registration]</p><p>[Specialities, e.g. substance abuse, suicide prevention]. Add a short, warm introduction here.</p></div>
</div>
</div></section>''',
    'listen': r'''<section id="listen" class="band"><div class="wrap two">
<div>
<h2>Listen in</h2>
<p>Short, honest conversations you can play in private, any time. New episodes will appear here.</p>
<div class="eps">
<div class="ep"><span class="play" aria-hidden="true">&#9654;</span><div><strong>[Episode title]</strong><br><small>Grief and healing</small></div></div>
<div class="ep"><span class="play" aria-hidden="true">&#9654;</span><div><strong>[Episode title]</strong><br><small>Relationships and breakups</small></div></div>
<div class="ep"><span class="play" aria-hidden="true">&#9654;</span><div><strong>[Episode title]</strong><br><small>Talking about suicide prevention</small></div></div>
</div>
</div>
<div>
<h2>When you are unsure</h2>
<p>Not sure which service you need? Pick what sounds closest, and we will help you from there.</p>
<div class="chips">
<a href="#services">I feel low or anxious</a><a href="#services">My relationship is struggling</a><a href="#support">I have experienced abuse</a><a href="#services">I lost someone</a><a href="#services">I lost my job</a><a href="#support">I am worried about someone's life</a><a href="#services">Someone I love struggles with addiction</a>
</div>
</div>
</div></section>''',
    'pricing': r'''<section id="pricing"><div class="wrap">
<h1>Fees and packages</h1>
<p>Clear pricing, so cost is never a surprise. Fill in your rates below.</p>
<div class="price">
<div><h3>Single session</h3><p class="amt">KSh [____]</p><p>One-on-one, in person or online.</p></div>
<div class="best"><h3>Online therapy package</h3><p class="amt">KSh [____]</p><p>A bundle of sessions at a reduced rate.</p></div>
<div><h3>Couples or family</h3><p class="amt">KSh [____]</p><p>Per session, for two or more people.</p></div>
<div><h3>Group sessions</h3><p class="amt">KSh [____]</p><p>Support groups, per person.</p></div>
</div>
<p style="margin-top:20px;color:var(--muted)">Corporate programmes and workshops are quoted individually. Get in touch to discuss your team.</p>
</div></section>''',
    'mpesa': r'''<section id="mpesa" class="band"><div class="wrap mp">
<div>
<h1>Pay with M-Pesa</h1>
<p>Pay for a session or package privately from your phone. You can use your nickname as the account name, so your payment never needs to carry your full name.</p>
<ol class="mps">
<li>Open M-Pesa and choose <strong>Lipa na M-Pesa</strong>.</li>
<li>Choose <strong>Paybill</strong> and enter the business number.</li>
<li>Enter your booking nickname as the account number.</li>
<li>Enter the amount for your session or package.</li>
<li>Enter your M-Pesa PIN and send. Keep the confirmation message.</li>
</ol>
</div>
<div class="paybox">
<h3>Payment details</h3>
<dl><dt>Paybill number</dt><dd>[add number]</dd><dt>Account number</dt><dd>Your booking nickname</dd><dt>Business name</dt><dd>[add name shown on M-Pesa]</dd></dl>
<p style="margin:16px 0 0;color:var(--muted);font-size:.92rem">After paying, send the confirmation message when you book so we can confirm your session.</p>
</div>
</div></section>''',
    'faq': r'''<section id="faq"><div class="wrap">
<h1>Common questions</h1>
<div class="svc">
<details><summary>Is it really anonymous?</summary><div class="body"><p>You can start with a nickname, and we keep records secure and share nothing without your consent. The exceptions are where the law requires it or where your safety, or someone else's, is at serious risk.</p></div></details>
<details><summary>Are your therapists qualified?</summary><div class="body"><p>Yes. All counselling and clinical services are delivered by appropriately qualified and authorised professionals.</p></div></details>
<details><summary>How private are online sessions?</summary><div class="body"><p>We use private, secure sessions and ask you to find a quiet space where you feel comfortable. Details of how we protect your data are shared when you book.</p></div></details>
<details><summary>What if I am in danger or thinking of ending my life?</summary><div class="body"><p>Please call 1199, 1195 or Befrienders Kenya on +254 722 178 177 now, or go to the nearest hospital. Where there is immediate risk, we connect you with emergency and specialised services.</p></div></details>
<details><summary>Can I bring my partner or family?</summary><div class="body"><p>Yes. We offer couples, family and group sessions, and you can also start on your own and involve others later.</p></div></details>
<details><summary>What if I need more than counselling?</summary><div class="body"><p>We make referrals to specialised treatment, child services or emergency services whenever that is the safest and best route for you.</p></div></details>
</div>
</div></section>''',
    'book': r'''<section id="book" class="band"><div class="wrap contact">
<div>
<h1>Book a private session</h1>
<p>Tell us how you would like to meet and we will get back to you. You can use a first name or a nickname.</p>
<p><strong>Email:</strong> [add email address]<br><strong>Phone / WhatsApp:</strong> [add phone number]<br><strong>Location:</strong> [add physical address]</p>
</div>
<div>
<label for="n">Name or nickname</label><input id="n" autocomplete="off">
<label for="c">How should we reach you?</label><input id="c" placeholder="Phone or email" autocomplete="off">
<label for="m">Session type</label>
<select id="m"><option>Individual</option><option>Couples</option><option>Family</option><option>Group</option></select>
<label for="w">Preferred way to meet</label>
<select id="w"><option>Online</option><option>In person</option></select>
<button class="btn" id="send" type="button">Request a session</button>
<p class="confirm" id="ok" role="status"></p>
</div>
</div></section>''',
}

S=lambda s:s.split('|')
def ul(s):return '<ul class="list2">'+''.join('<li>%s</li>'%x for x in S(s))+'</ul>'
def pl(s):return '<ul class="plain">'+''.join('<li>%s</li>'%x for x in S(s))+'</ul>'
def sec(i,n,t,body,lead=''):
    return '<section id="%s"><div class="wrap">%s<h2>%s</h2>%s%s</div></section>'%(i,('<span class="num">%s</span>'%n if n else ''),t,('<p>'+lead+'</p>' if lead else ''),body)
def cards(items):return '<div class="tiles">'+''.join('<div><h3>%s</h3>%s</div>'%(h,b) for h,b in items)+'</div>'
def two(a,b):return '<div class="two"><div>%s</div><div>%s</div></div>'%(a,b)
def acc(items):
    o=''
    for k,(t,l,b) in enumerate(items):
        o+='<details%s><summary>%s</summary><div class="body">%s%s</div></details>'%(' open' if k==0 else '',t,'<p>'+l+'</p>' if l else '',''.join('<span>%s</span>'%x for x in S(b)))
    return '<div class="svc">'+o+'</div>'
N={}
N['about']=sec('about','1 &middot; Introduction',"Therapy Anonymous Bila AI",two('<p>Therapy Anonymous Bila AI is a mental-health counselling, therapy and advocacy agency created to provide a safe, confidential and accessible environment where individuals can seek professional emotional and psychological support.</p><p>The agency provides both physical and online services, allowing clients to access counselling in a setting that is comfortable and convenient for them. The concept is built around confidentiality, accessibility, human connection and professional support.</p>','<h3>Our philosophy</h3><p class="tag">&ldquo;Therapy Anonymous Bila AI&rdquo;</p><p>The idea is to provide a space where people can speak openly, be heard and receive human therapeutic support while maintaining their privacy and dignity.</p>'))
N['vision']=sec('vision','2 &amp; 3 &middot; Vision and mission','What we are here to do',cards([('Our vision','<p>To create a trusted and accessible mental-health agency where people can seek support without fear of judgment, stigma or discrimination.</p>'),('Our mission','<p>To provide confidential, professional and accessible counselling, therapy, mental-health education and advocacy services to individuals, couples, families, groups and communities.</p>')]))
N['core']=sec('core','4 &middot; Core areas','Two divisions, one purpose','<p>The agency operates through two major divisions.</p>'+cards([('A. Administration &amp; Operations','<p>Responsible for the business and operational side of the agency.</p>'),('B. Counselling &amp; Mental Health Services','<p>Responsible for professional counselling, therapy, mental-health programmes and client support.</p>')]))
N['brand']=sec('brand','23 &middot; Brand identity','A safe space to talk. A safe space to heal.','<p>Our core values guide everything we do.</p><div class="values"><span>Confidentiality</span><span>Humanity</span><span>Professionalism</span><span>Accessibility</span><span>Compassion</span><span>Healing</span></div>')
N['longterm']=sec('longterm','24 &middot; Long-term goal','Where we are heading','<p>Therapy Anonymous Bila AI aims to grow from a counselling agency into a broader mental-health advocacy and support platform, combining professional therapy, digital services, education, community outreach and mental-health awareness.</p><p>The long-term vision is to make professional mental-health support more accessible, less intimidating and easier to reach, both physically and digitally.</p>')
N['services']=sec('services','7 &middot; Counselling &amp; therapy services','How we can help',acc([
('A. Individual / one-on-one therapy','Offered both physically and online. We support clients experiencing:','Depression|Anxiety|Stress|Emotional difficulties|Mental-health challenges|Relationship problems|Parenting challenges|Childhood trauma|Sexual abuse|Physical abuse|Emotional abuse|Domestic violence|Grief and loss|Job loss|Financial stress|Bankruptcy|Retirement|Pregnancy-related emotional challenges|Single parenthood|Support for new mothers|School-related challenges|Workplace challenges|Special-needs-related challenges|Post-accident psychological difficulties'),
('B. Family counselling','Family counselling addresses:','Family conflict|Communication problems|Parenting challenges|Separation|Divorce|Pre-divorce counselling|Post-divorce counselling|Family trauma|Family emotional support'),
('C. Couples &amp; relationship therapy','','Relationship counselling|Breakup support|Pre-marital counselling|Post-marital counselling|Communication support|Trust-related issues|Romantic relationships|Non-romantic relationships|Platonic relationships|Relationship transitions'),
('D. Group therapy','Possible groups include:','Families|Couples|Friends|Partners|People experiencing grief|People experiencing addiction|Trauma-support groups|Mental-health support groups|Parents and caregivers'),
('E. Grief counselling','Support for:','Loss of a loved one|Bereavement|Emotional trauma following loss|Major life changes|Adjustment after loss'),
('F. Trauma therapy','Support for:','Childhood trauma|Sexual abuse|Physical abuse|Emotional abuse|Domestic violence|Accidents|Relationship trauma|Other traumatic experiences'),
('G. Substance-abuse counselling','Support may include:','Family counselling|Emotional support|Relapse-prevention support|Mental-health education|Appropriate referrals where specialised treatment is required')]),'One-on-one therapy is offered both physically and online.')
N['support']=sec('support','8 &middot; Sexual-abuse &amp; gender-based violence support','Confidential support after abuse','<p>We provide confidential counselling for people affected by sexual abuse and gender-based violence, including people who have experienced:</p>'+ul('Sexual abuse|Physical abuse|Emotional abuse|Domestic violence|Gender-based violence')+'<p>Appropriate professional and emergency referrals are made where necessary.</p>')
N['childhood']=sec('childhood','9 &middot; Childhood trauma','Healing the effects of childhood trauma','<p>A specialised programme addresses the psychological and emotional effects of childhood trauma. We may provide:</p>'+ul('Individual counselling|Family support|Trauma-focused therapy|Parenting guidance|Referral to specialised child services where necessary'))
N['jobloss']=sec('jobloss','10 &middot; Job loss &amp; career-related therapy','When work and money feel uncertain','<p>We support individuals experiencing emotional difficulties following:</p>'+ul('Job loss|Unemployment|Career changes|Workplace stress|Retirement|Financial pressure|Bankruptcy'))
N['specialised']=sec('specialised','11 &middot; Specialised mental-health support','Programmes for specific needs','<p>Programmes may include:</p>'+ul('Depression and mental illness|Anxiety|Single parenthood|Pregnancy|New mothers|Special-needs individuals|Post-accident survivors|School-related challenges|Workplace-related challenges'))
N['suicide']=sec('suicide','12 &middot; Suicide prevention &amp; post-suicide support','Suicide prevention is one of our key advocacy areas','<p>Our programme may include:</p>'+ul('Suicide-prevention awareness|Mental-health education|Crisis support|Risk identification|Emotional support|Post-suicide support|Support for affected families|Community awareness|Professional referrals')+'<p>Where there is an immediate risk of harm, we connect clients with emergency and specialised services. If you are in danger now, call the numbers at the top of this page.</p>')
N['advocacy']=sec('advocacy','13 &middot; Mental-health advocacy','Advocacy beyond individual therapy','<p>We go beyond individual therapy by creating awareness around mental health. Our advocacy activities include:</p>'+ul('Mental-health awareness campaigns|Community education|School programmes|Workplace programmes|Suicide-prevention awareness|Mental-health workshops|Anti-stigma campaigns|Educational content|Community outreach'))
N['social']=sec('social','15 &middot; Social media &amp; marketing','Where to find us',two('<h3>Platforms</h3>'+pl('Instagram|TikTok|YouTube|Podcast platforms|Website|Mobile application'),'<h3>Content</h3>'+pl('Mental-health education|Short educational videos|Therapy discussions|Relationship topics|Parenting topics|Trauma awareness|Suicide-prevention information|Grief and healing discussions|Mental-health campaigns')))
N['podcast']=sec('podcast','16 &middot; Podcast','The mental-health podcast','<p>Our dedicated mental-health podcast serves as both an educational and advocacy platform. Topics include:</p>'+ul('Mental health|Relationships|Breakups|Trauma|Childhood experiences|Parenting|Grief|Addiction|Emotional wellbeing|Suicide prevention|Abuse|Personal growth'))
N['marketing']=sec('marketing','17 &middot; Marketing strategy','Trust and awareness first','<p>Our marketing focuses on building trust and awareness rather than simply advertising therapy. Strategies include:</p>'+ul('Social-media campaigns|Educational content|Podcasts|YouTube videos|Community outreach|Partnerships with organisations|School programmes|Workplace programmes|Mental-health events|Website visibility|Referral networks'))
N['website']=sec('website','14 &middot; Digital services &middot; Website','Our website','<p>The agency has an online presence through a website and mobile application. The website offers:</p>'+ul('Information about the agency|Counselling services|Therapist profiles|Appointment booking|Online counselling|Mental-health resources|Contact information|Referral information'))
N['app']=sec('app','14 &middot; Digital services &middot; Mobile app','Our mobile application','<p>The application is planned for Android and iOS and will offer:</p>'+ul('Appointment booking|Online counselling|Therapist access|Messaging|Mental-health resources|Educational materials|Crisis information|Client accounts|Service information'))
N['admin']=sec('admin','5 &middot; Administration &amp; operations','Running the agency day to day','<p>The administration department coordinates the day-to-day running of the agency. Key responsibilities:</p>'+ul('General administration|Client registration|Appointment scheduling|Records management|Finance and accounting|Human-resource management|Marketing|Social-media management|Website management|Mobile-app management|Partnerships|Community outreach|Staff coordination|Legal and licensing requirements|Data protection and confidentiality procedures'))
N['staff']=sec('staff','6 &middot; Proposed staff structure','A multidisciplinary team','<p>The agency requires a multidisciplinary team.</p>'+cards([('Therapists &amp; counsellors','<p>Therapists specialising in different areas of mental health.</p>'),('Accountant',pl('Financial records|Budgeting|Payments|Financial reporting|Tax-related matters')),('Human resources',pl('Recruitment|Staff welfare|Employee records|Staff policies|Performance management')),('Designer',pl('Branding|Posters|Graphics|Website visuals|Marketing materials')),('Social media manager',pl('Instagram|TikTok|YouTube|Podcast promotion|Content management|Online engagement|Digital campaigns'))]))
N['structure']=sec('structure','22 &middot; Agency structure','How the agency is organised',cards([('Administration &amp; Operations',pl('Management|Finance|HR|Marketing|Social media|Digital platforms|Client administration|Legal/compliance|Partnerships')),('Counselling &amp; Mental Health Department',pl('Individual therapy|Couples therapy|Family counselling|Group therapy|Trauma therapy|Grief counselling|Substance-abuse support|Suicide prevention|Mental-health advocacy|Specialised programmes|Online therapy'))]))
N['legal']=sec('legal','20 &middot; Professional, legal &amp; compliance requirements','Doing things properly','<p>Before launching, the agency establishes the appropriate legal and professional framework. Areas to address:</p>'+ul('Business registration|Relevant licences|Professional counselling requirements|Professional practising requirements|Tax compliance|KRA PIN and tax obligations|Data protection|Client confidentiality|Consent procedures|Record keeping|Professional ethics|Clinical referral procedures|Appropriate insurance where required')+'<p>All counselling and clinical services are delivered by appropriately qualified and authorised professionals.</p>')
N['privacy']=sec('privacy','21 &middot; Confidentiality &amp; client privacy','Privacy is central to everything','<p>Because our core promise is anonymity and confidentiality, privacy is a central part of our operations. We establish clear procedures for:</p>'+ul('Client confidentiality|Secure client records|Consent|Online-session privacy|Data protection|Therapist-client boundaries|Information sharing|Emergency situations')+'<p>Our use of &ldquo;Anonymous&rdquo; is a commitment to a private, non-judgmental environment, not a promise that confidentiality has no legal or safety exceptions.</p>')
N['ideas']=sec('ideas','19 &middot; Additional business ideas','What comes next',two('<h3>Possible future services</h3>'+pl('Premium mental-health resources|Medication/mental-health information resources|Online therapy packages|Educational programmes|Team-building programmes|Community programmes|Corporate mental-health programmes'),'<h3>Team building</h3>'+pl('Team-building events|Staff retreats|&ldquo;Adventures Together&rdquo;|Employee wellbeing activities')))
N['budget']=sec('budget','18 &middot; Budget &amp; digital development','Budget for digital development','<p>Initial areas of expenditure: website development, mobile application development, website hosting, registration, marketing, branding, social-media management and content creation.</p><div class="price"><div><h3>Website, hosting &amp; registration</h3><p class="amt">KSh 30,000</p></div><div><h3>Website</h3><p class="amt">KSh 30,000</p></div><div><h3>Application</h3><p class="amt">KSh 56,000</p></div><div><h3>Marketing</h3><p class="amt">~ KSh 25,000</p></div></div><p>These figures are preliminary estimates and should be confirmed with actual quotations before implementation.</p>')
for k in OLD: N[k] = OLD[k]
pages=[('index','Home','home',['home','how','digital'],'Confidential counselling, therapy and advocacy with qualified professionals, in person or online.'),
('about','About','about',['about','vision','core','brand','longterm','team'],'About Therapy Anonymous Bila AI: our introduction, vision, mission, values and long-term goal.'),
('services','Services','services',['services','support','childhood','jobloss','specialised','suicide'],'Counselling and therapy services, abuse and trauma support, job-loss therapy and suicide prevention.'),
('community','Advocacy','advocacy',['advocacy','social','podcast','listen','marketing'],'Mental-health advocacy, social media, our podcast and marketing strategy.'),
('online','Online','website',['website','app'],'Our website and mobile application: booking, online counselling, resources and crisis information.'),
('agency','Agency','admin',['admin','staff','structure','legal','privacy','ideas','budget'],'How the agency runs: operations, staff, structure, compliance, privacy, future ideas and budget.'),
('pricing','Pricing','pricing',['pricing','mpesa'],'Session fees, packages and private M-Pesa payment.'),
('contact','Contact','faq',['faq','book'],'Common questions and booking a private session.')]
where={'top':'index'};firsts={}
for f,l,fi,ids,d in pages:
    firsts[f]=ids[0]
    for i in ids: where[i]=f
def fix(h,cur):
    def r(m):
        i=m.group(1)
        if i=='crisis' or i not in where: return m.group(0)
        f=where[i];t=f+'.html'
        if firsts[f]!=i and i!='top':t+='#'+i
        if f==cur and firsts[f]!=i:t='#'+i
        return 'href="'+t+'"'
    return re.sub(r'href="#(\w+)"',r,h)
def body_of(ids):
    o=[]
    for k,i in enumerate(ids):
        s=N[i]
        if i!='home':
            s=s.replace(' class="band"','',1)
            if k%2==1: s=s.replace('<section id="%s"'%i,'<section id="%s" class="band"'%i,1)
        o.append(s)
    return '\n\n'.join(o)
def header(cur):
    li=''.join('<li><a href="#%s"%s>%s</a></li>'%(fi,' aria-current="page"' if f==cur else '',l) for f,l,fi,ids,d in pages)
    return '<header><div class="wrap"><nav aria-label="Main"><a class="logo" href="#home">Therapy Anonymous Bila AI</a><ul>'+li+'</ul><a class="btn" href="#book">Book a session</a></nav></div></header>'
for f,l,fi,ids,d in pages:
    b=body_of(ids)
    if f!='index': b=b.replace('<h2>','<h1>',1).replace('</h2>','</h1>',1)
    t='Therapy Anonymous Bila AI' if f=='index' else l+' | Therapy Anonymous Bila AI'
    h=fix(header(f),f).replace('aria-current="page"','aria-current="page"')
    page='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<title>%s</title>\n<meta name="description" content="%s">\n<meta name="theme-color" content="#1f6f6a">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n%s\n%s\n<link rel="stylesheet" href="style.css">\n</head>\n<body>\n<a class="skip" href="#main">Skip to content</a>\n%s\n%s\n<main id="main">\n%s\n</main>\n%s\n<script src="script.js"></script>\n</body>\n</html>'%(t,d,t,d,FAVICON,FONTS,h,CRISIS,fix(b,f),fix(FOOTER,f))
    open(OUT+f+'.html','w',encoding='utf-8').write(page)
open(OUT+'style.css','w',encoding='utf-8').write(CSS)
open(OUT+'script.js','w',encoding='utf-8').write(JS)
open(OUT+'robots.txt','w').write('User-agent: *\nAllow: /\n')

print('Built', len(pages), 'pages into', os.path.abspath(OUT))

if '--no-serve' not in sys.argv:
    import http.server, socketserver, webbrowser, functools
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=OUT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('', 8000), handler) as server:
        print('Website running at http://localhost:8000/index.html  (press the red Stop button to quit)')
        webbrowser.open('http://localhost:8000/index.html')
        server.serve_forever()
