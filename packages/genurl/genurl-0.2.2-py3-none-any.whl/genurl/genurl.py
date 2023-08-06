import argparse
import random
import uuid

from tqdm import tqdm
from faker import Faker
from random_word import RandomWords


fake = Faker()
r = RandomWords()
with open("/usr/share/dict/words") as f:
    usr_words = [l.strip() for l in f]


NAME_CACHE_SIZE = 100
VERB_CACHE_SIZE = 100
NOUN_CACHE_SIZE = 100
ADJ_CACHE_SIZE = 100
ADV_CACHE_SIZE = 100

name_c = []
verb_c = []
noun_c = []
adj_c = []
adv_c = []


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

CHARS = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"


def random_word():
    return random.choice(usr_words)


def random_name():
    if len(name_c) > NAME_CACHE_SIZE:
        return random.choice(name_c)
    return fake.name()


# build a cache, once over 1000 just use cache


def random_verb():
    if len(verb_c) > VERB_CACHE_SIZE:
        return random.choice(verb_c)
    maybe = ""
    while (not isinstance(maybe, str)) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="verb",
            excludePartOfSpeech="noun,adjective,adverb",
        )
    verb_c.append(maybe)
    return maybe


def random_noun():
    if len(noun_c) > NOUN_CACHE_SIZE:
        return random.choice(noun_c)
    maybe = ""
    while not isinstance(maybe, str) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="noun",
            excludePartOfSpeech="verb,adjective,adverb",
        )
    noun_c.append(maybe)
    return maybe


def random_adjective():
    if len(adj_c) > ADJ_CACHE_SIZE:
        return random.choice(adj_c)
    maybe = ""
    while not isinstance(maybe, str) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="adjective",
            excludePartOfSpeech="verb,noun,adverb",
        )
    adj_c.append(maybe)
    return maybe


def random_adverb():
    if len(adv_c) > ADV_CACHE_SIZE:
        return random.choice(adv_c)
    maybe = ""
    while not isinstance(maybe, str) or len(maybe) == 0:
        # it sometimes returns None? or empty?
        maybe = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="adverb",
            excludePartOfSpeech="verb,adjective,noun",
        )
    adv_c.append(maybe)
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
        if random.random() > 0.5:
            u = str(uuid.uuid4())
        else:
            u = []
            for _ in range(l):
                u.append(random.choice(CHARS))
            u = "".join(u)
        return u[:l]


def random_url():
    root = None
    while root is None:
        root = random_word()
    root = root.lower()
    subdomain = ""
    if random.random() < 0.8:
        subdomain = random.choice(
            [
                "www",
                random_word(),
                random_word(),
                random_word() + random_word(),
            ]
        )
        while subdomain is None:
            subdomain = random.choice(
                [
                    "www",
                    random_word(),
                    random_word(),
                    random_word() + random_word(),
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
    global NAME_CACHE_SIZE
    global VERB_CACHE_SIZE
    global NOUN_CACHE_SIZE
    global ADJ_CACHE_SIZE
    global ADV_CACHE_SIZE

    parser = argparse.ArgumentParser(description="Generate a file of URLs.")
    parser.add_argument("--number", "-n", type=int, default=1000, help="How many URLs to generate")
    parser.add_argument("--outfile", "-o", type=str, default="urls.txt", help="Output path")
    parser.add_argument("--slow", "-s", action="store_true", help="Run slower but get more diversity of words")
    args = parser.parse_args()
    if args.slow:
        print("running in slow mode, URLs will have more diversity")
        NAME_CACHE_SIZE = 10000
        VERB_CACHE_SIZE = 2000
        NOUN_CACHE_SIZE = 5000
        ADJ_CACHE_SIZE = 1000
        ADV_CACHE_SIZE = 500

    NUM = int(args.number)
    OUT = args.outfile
    print(f"Generating {NUM} URLs, saving in {OUT}...\n")
    with open(OUT, "w+") as f:
        for _ in tqdm(range(NUM), total=NUM):
            url = random_url()
            f.write(url + "\n")