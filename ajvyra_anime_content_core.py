from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class AnimeContent:
    anime_id: int
    title: str
    genre: List[str]
    tone: str
    logline: str
    premise: str
    themes: List[str] = field(default_factory=list)
    characters: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


ANIME_CONTENT: List[AnimeContent] = [

    AnimeContent(
        1,
        "Veylora",
        ["Mystery", "Psychological", "Drama"],
        "dark and mysterious",
        "A forgotten signal begins revealing memories that should not exist.",
        "A quiet student discovers an impossible transmission coming from an abandoned district.",
        ["memory", "identity", "truth"],
        ["Vaelith", "Nerya", "Kaelor"]
    ),

    AnimeContent(
        2,
        "Aelvryn",
        ["Fantasy", "Adventure", "Drama"],
        "epic and emotional",
        "A girl discovers that the stars above her city are disappearing one by one.",
        "She follows a strange map that leads beyond the borders of her known world.",
        ["freedom", "sacrifice", "hope"],
        ["Elyra", "Varyn", "Solven"]
    ),

    AnimeContent(
        3,
        "Nyxara",
        ["Sci-Fi", "Thriller", "Mystery"],
        "cold and futuristic",
        "A teenager receives messages from a version of himself living ten years ahead.",
        "Each message prevents a disaster but slowly changes reality.",
        ["time", "choice", "consequences"],
        ["Nyren", "Caelis", "Veyra"]
    ),

    AnimeContent(
        4,
        "Kaelith",
        ["Action", "Fantasy", "Adventure"],
        "fast and cinematic",
        "A powerless boy becomes the only person capable of controlling a forbidden force.",
        "He must master it before rival factions discover what he can do.",
        ["power", "responsibility", "trust"],
        ["Kaelor", "Ravien", "Zeyla"]
    ),

    AnimeContent(
        5,
        "Orivane",
        ["Thriller", "Psychological", "Mystery"],
        "tense and unsettling",
        "A city begins forgetting people who disappear during the night.",
        "One teenager records every disappearing person before the city forgets them.",
        ["memory", "loss", "truth"],
        ["Oriven", "Neyra", "Valen"]
    ),

    AnimeContent(
        6,
        "Zeravia",
        ["Sci-Fi", "Action", "Drama"],
        "intense and futuristic",
        "A damaged artificial satellite starts choosing human lives to save.",
        "Its final decision may destroy the city it was created to protect.",
        ["humanity", "sacrifice", "technology"],
        ["Zeria", "Kavon", "Averin"]
    ),

    AnimeContent(
        7,
        "Vaelune",
        ["Fantasy", "Romance", "Drama"],
        "soft and magical",
        "Two strangers repeatedly meet in dreams but never recognize each other awake.",
        "Their dreams begin affecting their real lives.",
        ["connection", "dreams", "choice"],
        ["Vael", "Luneya", "Eron"]
    ),

    AnimeContent(
        8,
        "Ravelyth",
        ["Action", "Thriller", "Mystery"],
        "dark and aggressive",
        "A hidden organization recruits teenagers who can see future crimes.",
        "One recruit discovers that his own future is the crime they are trying to stop.",
        ["fate", "justice", "identity"],
        ["Ravel", "Nytha", "Kaiven"]
    ),

    AnimeContent(
        9,
        "Solvarya",
        ["Adventure", "Fantasy", "Drama"],
        "warm and adventurous",
        "A forgotten railway leads to a city that exists only once every century.",
        "Three travelers race to reach it before sunrise.",
        ["friendship", "time", "journey"],
        ["Solven", "Araya", "Veylin"]
    ),

    AnimeContent(
        10,
        "Xaveren",
        ["Action", "Sci-Fi", "Drama"],
        "epic and emotional",
        "A pilot wakes up with memories belonging to an enemy.",
        "He must decide which identity is truly his.",
        ["identity", "war", "choice"],
        ["Xaven", "Riela", "Vorren"]
    ),

    AnimeContent(
        11,
        "Elyvara",
        ["Romance", "Drama"],
        "gentle and emotional",
        "Two people become close through letters without knowing who is writing them.",
        "A final letter reveals a connection neither expected.",
        ["love", "distance", "truth"],
        ["Elyra", "Varen"]
    ),

    AnimeContent(
        12,
        "Neravelle",
        ["Romance", "Mystery", "Drama"],
        "melancholic and mysterious",
        "A girl finds photographs of moments that have not happened yet.",
        "Every photograph brings her closer to someone she has never met.",
        ["future", "love", "choice"],
        ["Nerava", "Kaelin"]
    ),

    AnimeContent(
        13,
        "Vaerith",
        ["Romance", "Psychological", "Drama"],
        "intimate and emotional",
        "A boy begins hearing the thoughts of one person whenever it rains.",
        "The ability disappears whenever he tries to tell her.",
        ["communication", "fear", "love"],
        ["Vaer", "Elira"]
    ),

    AnimeContent(
        14,
        "Lunavyr",
        ["Romance", "Fantasy"],
        "dreamlike and warm",
        "A mysterious girl appears only during moonlit nights.",
        "A lonely boy tries to discover why she cannot exist during daylight.",
        ["loneliness", "connection", "hope"],
        ["Lunai", "Veyren"]
    ),

    AnimeContent(
        15,
        "Averlyn",
        ["Romance", "Drama", "Slice of Life"],
        "realistic and heartfelt",
        "Two students slowly become friends while hiding their biggest fears.",
        "Their relationship changes when one decides to leave the city.",
        ["friendship", "change", "goodbye"],
        ["Averin", "Selya"]
    ),

    AnimeContent(
        16,
        "Neyvara",
        ["Romance", "Mystery", "Thriller"],
        "dark and emotional",
        "A girl receives anonymous messages describing her future relationships.",
        "The final message contains the name of someone she has never met.",
        ["trust", "fear", "love"],
        ["Neyra", "Valen"]
    ),

    AnimeContent(
        17,
        "Elvaria",
        ["Romance", "Fantasy", "Drama"],
        "magical and bittersweet",
        "A boy can preserve one memory inside a glass pendant.",
        "He must choose between keeping his happiest memory and saving someone he loves.",
        ["memory", "sacrifice", "love"],
        ["Elvar", "Mirael"]
    ),

    AnimeContent(
        18,
        "Virelya",
        ["Romance", "Psychological"],
        "quiet and introspective",
        "Two people keep meeting in the same empty train every winter.",
        "Neither knows why the train remembers them.",
        ["memory", "connection", "time"],
        ["Virel", "Ayaen"]
    ),

    AnimeContent(
        19,
        "Caelora",
        ["Romance", "Drama", "Adventure"],
        "hopeful and cinematic",
        "Two travelers promise to meet again after taking separate paths.",
        "Years later, a forgotten photograph brings them together.",
        ["distance", "growth", "reunion"],
        ["Caelor", "Ravya"]
    ),

    AnimeContent(
        20,
        "Seravyn",
        ["Romance", "Drama"],
        "emotional and hopeful",
        "A quiet friendship becomes something neither character knows how to name.",
        "When everything changes, they finally understand what they meant to each other.",
        ["friendship", "love", "maturity"],
        ["Seren", "Vayla"]
    ),

    AnimeContent(
        21,
        "Mouravia",
        ["Drama", "Psychological", "Sad"],
        "heavy and emotional",
        "A boy keeps visiting a place where someone important used to wait for him.",
        "He slowly learns that remembering someone does not mean living in the past.",
        ["grief", "memory", "acceptance"],
        ["Mouren", "Elvya"]
    ),

    AnimeContent(
        22,
        "Noxelya",
        ["Psychological", "Drama", "Mystery"],
        "dark and lonely",
        "A girl begins finding notes written by herself on days she cannot remember.",
        "The notes lead her toward a painful truth.",
        ["identity", "memory", "healing"],
        ["Noxel", "Yvera"]
    ),

    AnimeContent(
        23,
        "Vaelora",
        ["Drama", "Romance", "Sad"],
        "melancholic",
        "Two people become important to each other at exactly the wrong time.",
        "Their final conversation changes how both understand goodbye.",
        ["timing", "loss", "acceptance"],
        ["Vaelor", "Leria"]
    ),

    AnimeContent(
        24,
        "Eryndra",
        ["Psychological", "Drama"],
        "quiet and dark",
        "A teenager tries to rebuild his life after losing his closest friend.",
        "Small memories gradually become the reason he starts moving forward.",
        ["grief", "friendship", "recovery"],
        ["Eryn", "Davel"]
    ),

    AnimeContent(
        25,
        "Neylith",
        ["Drama", "Mystery", "Sad"],
        "mysterious and sorrowful",
        "A forgotten voice recording contains the final words of someone missing.",
        "Finding the truth forces the protagonist to confront his own guilt.",
        ["guilt", "truth", "loss"],
        ["Neyl", "Varis"]
    ),

    AnimeContent(
        26,
        "Auralyne",
        ["Drama", "Fantasy", "Sad"],
        "poetic and emotional",
        "A city hears the voice of someone who disappeared years ago.",
        "One person follows the voice into a place where memories become real.",
        ["memory", "loss", "hope"],
        ["Aural", "Lynae"]
    ),

    AnimeContent(
        27,
        "Velmora",
        ["Psychological", "Drama", "Thriller"],
        "dark and tense",
        "A boy discovers that his happiest memories may have been created artificially.",
        "He must decide whether truth is more important than happiness.",
        ["truth", "identity", "memory"],
        ["Vel", "Morai"]
    ),

    AnimeContent(
        28,
        "Seyravia",
        ["Drama", "Adventure", "Sad"],
        "emotional and cinematic",
        "A girl travels across several cities carrying a final message.",
        "Every stop reveals another part of the person who wrote it.",
        ["journey", "goodbye", "love"],
        ["Seyra", "Avien"]
    ),

    AnimeContent(
        29,
        "Oryvane",
        ["Drama", "Psychological", "Romance"],
        "dark but hopeful",
        "A person who has stopped trusting people meets someone who refuses to leave.",
        "Their relationship becomes a slow battle against isolation.",
        ["trust", "healing", "connection"],
        ["Oryn", "Veya"]
    ),

    AnimeContent(
        30,
        "Luminarae",
        ["Drama", "Fantasy", "Psychological"],
        "dark-to-light",
        "A lonely character enters a strange world where every painful memory becomes visible.",
        "Instead of destroying the memories, they learn how to live beside them.",
        ["healing", "acceptance", "hope"],
        ["Lumir", "Aera", "Veyn"]
    ),
]


def get_anime(anime_id: int) -> AnimeContent:
    for anime in ANIME_CONTENT:
        if anime.anime_id == anime_id:
            return anime

    raise KeyError(f"Anime {anime_id} does not exist.")


def search_anime(query: str) -> List[AnimeContent]:
    query = query.lower().strip()

    return [
        anime
        for anime in ANIME_CONTENT
        if query in anime.title.lower()
        or query in anime.logline.lower()
        or any(query in genre.lower() for genre in anime.genre)
    ]


def all_anime() -> List[AnimeContent]:
    return list(ANIME_CONTENT)


if __name__ == "__main__":
    print(f"AJVYRA anime count: {len(ANIME_CONTENT)}")

    for anime in ANIME_CONTENT:
        print(
            f"{anime.anime_id:02d} | "
            f"{anime.title} | "
            f"{', '.join(anime.genre)}"
        )
