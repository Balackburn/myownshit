#!/usr/bin/env python3
"""Score a French "ce mec" script: python3 score_fr.py draft.txt [more.txt ...]

The viral-video-writing checker (scripts/score.py of that skill) adapted to French and to the ce-mec format:
one spoken line per line, the last line is the dry tag (no CTA in the voice: the CTA goes in the post caption).
Hard fails cost 15, soft flags 5. Rewrite until 90+ with zero hard fails.
"""
import re, sys

HARD = [
    (r'—', 'tiret long (personne ne le prononce)'),
    (r';', 'point-virgule'),
    (r"(?i)\b(pas seulement|non seulement)\b.*\bmais\b", '« pas seulement X mais Y »'),
    (r"(?i)\bce n'est pas\b[^.]*?, c'est\b", '« ce n\'est pas X, c\'est Y »'),
    (r"(?i)le truc,? c'est que|la vérité,? c'est que|laissez ça|accrochez-vous|imaginez|force est de constater|il est important de noter|dans un monde où|au final|en fin de compte|que vous soyez", 'didascalie / remplissage'),
    (r"(?i)\b(spoiler|rebondissement)\s*:|c'est là que ça devient|le (meilleur|pire) dans tout ça", 'faux suspense'),
    (r"(?i)\b(plonger dans|plongeons|révolutionnaire|incontournable|ultime|booster|dévoile[rz]?|fascinant|captivant|époustouflant|game.?changer|next level|sublimer)\b", 'mot d\'IA'),
    (r"(?i)\b(mine d'or|sauce secrète|bouton panique)\b", 'métaphore-chute'),
]
NUM = (r"\d|\b(?:deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente|"
       r"quarante|cinquante|soixante|cent|cents|mille|million|millions|milliard)\b")
REHOOK = re.compile(r'(?i)' + NUM + r"|\b(mais|puis|alors|ensuite|sauf que|plus tard|le lendemain|depuis|soudain|"
                    r"finalement|enfin|maintenant|au bout de|un jour|quand)\b")
INSTIT = r"(?i)\b(flics?|police|gendarmes?|plainte|juge|tribunal|avocat|pompiers|préfecture|mairie|huissier|fisc|samu|gign|raid|douane|syndic|sécu|contractuel)\b"
STOP = set("ce cette ces mec il elle ils elles une des les le la un de du a au aux et est pour que qui par sur dans avec son sa ses lui leur plus pas ne".split())

def sentences(t): return [s.strip() for s in re.split(r'(?<=[.?!»])\s+|\n+', t) if s.strip()]
def words(s): return re.findall(r"[\wÀ-ÿ'-]+", s.lower())

def score(text):
    hard, soft = [], []
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    n = len(text.split()); secs = round(n / 3.9)
    if not 55 <= n <= 140: soft.append(f'longueur {n} mots ≈ {secs}s (viser 60-125, soit 15-32 s)')
    S = sentences(text); hook = S[0] if S else ''
    if not re.match(r'(?i)ce mec\b', hook): hard.append('B1 ne commence pas par « Ce mec »')
    if len(hook.split()) > 22: soft.append(f'accroche de {len(hook.split())} mots (22 max)')
    if not re.search(NUM, ' '.join(S[:2]), re.I) and not re.search(r'\b[A-ZÀ-Ý][a-zà-ÿ]+\b', hook[3:]):
        soft.append('ni nombre ni nom propre dans les 2 premières phrases')
    for rx, why in HARD:
        if re.search(rx, text): hard.append(why)
    one = [s for s in S if len(s.split()) == 1]
    if len(one) > 1: hard.append(f'{len(one)} phrases d\'un seul mot : {one[:3]}')
    long_ = [s for s in S if len(s.split()) > 26]
    if long_: soft.append(f'{len(long_)} phrase(s) de plus de 26 mots')
    q = [s for s in S[1:-1] if s.endswith('?')]
    if len(q) > 1: soft.append(f'{len(q)} questions rhétoriques dans le corps')
    gap = worst = 0
    for s in S[1:-1]:
        gap = 0 if REHOOK.search(s) else gap + len(s.split()); worst = max(worst, gap)
    if worst > 28: soft.append(f'{worst} mots (≈{round(worst / 3.9)} s) sans relance (nombre, « puis », « alors », saut dans le temps)')
    low = text.lower()
    if 'ce con' not in low: soft.append('pas de « ce con »')
    if 'putain' not in low: soft.append('pas de « putain »')
    if low.count('putain') > 1: hard.append('« putain » plus d\'une fois')
    if not re.search(INSTIT, text): soft.append('aucune institution (flics, plainte, juge, préfecture...)')
    tag = lines[-1] if lines else ''
    if len(tag.split()) > 7: soft.append(f'chute de {len(tag.split())} mots (7 max)')
    first = {w for s in S[:2] for w in words(s) if len(w) >= 4 and w not in STOP}
    last = {w for s in S[-2:] for w in words(s) if len(w) >= 4 and w not in STOP}
    if not first & last: soft.append('la fin ne rappelle pas le début (callback / boucle)')
    total = max(0, 100 - 15 * len(hard) - 5 * len(soft))
    return total, hard, soft, n, secs

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit('usage: python3 score_fr.py draft.txt [...]')
    for f in sys.argv[1:]:
        total, hard, soft, n, secs = score(open(f).read())
        print(f'{f}: SCORE {total}/100 · {n} mots ≈ {secs}s ' + ('PASS' if not hard and total >= 90 else 'REWRITE'))
        for h in hard: print('   HARD ', h)
        for s in soft: print('   soft ', s)
