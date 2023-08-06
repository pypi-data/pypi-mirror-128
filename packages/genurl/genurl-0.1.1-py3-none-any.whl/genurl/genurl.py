import argparse
import random
import uuid

from tqdm import tqdm
from faker import Faker
from random_word import RandomWords


fake = Faker()
r = RandomWords()


# https://www.hayksaakian.com/most-popular-tlds/
TLDS_WEIGHTS = [
    ("com", 328427),
    ("org", 23269),
    ("ru", 1132),
    ("net", 22400),
    ("de", 3400),
    ("com.br", 1000),
    ("co.uk", 5, 144),
    ("pl", 1125),
    ("it", 1125),
    ("ai", 3000),
    ("ly", 3000),
    ("fr", 1000),
]
TLDS, WEIGHTS = list(zip(*TLDS_WEIGHTS))


def random_name():
    return fake.name()


# build a cache, once over 1000 just use cache
verbc = []


def random_verb():
    if len(verbc) > 700:
        return random.choice(verbc)
    maybe = ""
    while (not isinstance(maybe, str)) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="verb",
            excludePartOfSpeech="noun,adjective,adverb",
        )
    verbc.append(maybe)
    return maybe


nounc = []


def random_noun():
    if len(nounc) > 1000:
        return random.choice(nounc)
    maybe = ""
    while not isinstance(maybe, str) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="noun",
            excludePartOfSpeech="verb,adjective,adverb",
        )
    nounc.append(maybe)
    return maybe


adjc = []


def random_adjective():
    if len(adjc) > 200:
        return random.choice(adjc)
    maybe = ""
    while not isinstance(maybe, str) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="adjective",
            excludePartOfSpeech="verb,noun,adverb",
        )
    adjc.append(maybe)
    return maybe


advc = []


def random_adverb():
    if len(advc) > 100:
        return random.choice(advc)
    maybe = ""
    while not isinstance(maybe, str) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="adverb",
            excludePartOfSpeech="verb,adjective,noun",
        )
    advc.append(maybe)
    return maybe


def random_preposition():
    return random.choice(
        ["with", "to", "in", "while", "on", "to", "on way to", "despite"]
    )


def random_clause():
    story = []
    story.append(random.choice(["a", "two", "several", "both", "an original", "the"]))
    if random.random() < 0.5:
        story.append(random_adjective())
        if random.random() < 0.08:
            story.append(random_adjective())
    story.append(random_noun())
    return story


def random_story() -> str:
    story = []
    story.append(random_name())
    if random.random() < 0.2:
        story.append("and")
        story.append(random_name())
    if random.random() < 0.1:
        story.append(random_adverb())
    story.append(random_verb())
    story.append(random_preposition())
    story += random_clause()
    if random.random() < 0.25:
        story.append(random_preposition())
        story += random_clause()
    return " ".join(story)


def random_tech_blog():
    story = []
    story.append(
        random.choice(
            [
                "Google",
                "Apple",
                "Microsoft",
                "Intel",
                "Zoom",
                "OnePice",
                "LegalZoom",
                "ZenBusiness",
                "MetroPlus",
                "RocketLawyer",
                "Fundbox",
                "Cricket Health",
                "HealthJoy",
                "UnitedHealth Group",
            ]
        )
    )
    story.append(
        random.choice(
            [
                "announces",
                "releases",
                "presents",
                "make headlines with",
                "deny reports of",
            ]
        )
    )
    story += random_clause()
    return " ".join(story)


def random_subpath():
    if random.random() < 0.333:
        top = random.choice(["blog", "stories", "latest"])
        path = random_story().replace(" ", "-")
        return top + "/" + path
    elif random.random() > 0.6666:
        return random_tech_blog().replace(" ", "-")
    else:
        l = random.randrange(6, 30)
        u = str(uuid.uuid4())
        return u[:l]


def random_url():
    root = None
    while root is None:
        root = r.get_random_word()
    root = root.lower()
    subdomain = ""
    if random.random() < 0.8:
        subdomain = random.choice(
            [
                "www",
                r.get_random_word(),
                r.get_random_word(),
                r.get_random_word() + r.get_random_word(),
            ]
        )
        while subdomain is None:
            subdomain = random.choice(
                [
                    "www",
                    r.get_random_word(),
                    r.get_random_word(),
                    r.get_random_word(),
                ]
            )
        subdomain = subdomain.replace(" ", "-")
        subdomain += "."
    tld = random.choices(TLDS, weights=WEIGHTS, k=1)[0]
    main = subdomain + root + "." + tld
    if random.random() > 0.2:
        main += "/"
        if random.random() > 0.2:
            main += random_subpath()
    if random.random() < 0.1:
        protocol = "http://"
    elif random.random() < 0.5:
        protocol = ""
    else:
        protocol = "https://"
    return protocol + main

def main():
    parser = argparse.ArgumentParser(description='Generate a file of URLs.')
    parser.add_argument('number', type=int, help='How many URLs to generate')
    parser.add_argument('outfile', type=str, help='Output path')
    args = parser.parse_args()
    NUM = int(args.number)
    OUT = args.outfile
    with open(OUT, "w+") as f:
        for _ in tqdm(range(NUM), total=NUM):
            url = random_url()
            f.write(url + "\n")