from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass(frozen=True)
class FilmStory:
    film_id: str
    title: str
    genre: str
    logline: str
    protagonist: str
    antagonist: str
    world: str
    emotional_core: str
    visual_style: str
    ending_type: str


class AJVYRACinematic30FilmStoryBible:
    """
    The canonical story identity for the 30 cinematic anime films.

    This is intentionally separate from rendering.
    A film must have a defined narrative identity before media generation.
    """

    STORIES = (
        FilmStory(
            "anime_01",
            "Veylora",
            "Dark Fantasy",
            "A silent girl discovers that every shadow in her city remembers a forgotten death.",
            "Veylora",
            "The Hollow King",
            "A rain-soaked city built around a dead moon.",
            "Grief, memory, and letting go.",
            "Dark blue-gray anime cinema, rain, moonlight, deep shadows.",
            "Bittersweet",
        ),
        FilmStory(
            "anime_02",
            "Aelvryn",
            "Fantasy Romance",
            "A young guardian falls in love with a mysterious traveler who disappears whenever dawn arrives.",
            "Aelvryn",
            "The Dawn Keeper",
            "A floating forest above an endless cloud ocean.",
            "Love versus possession.",
            "Dreamlike skies, glowing forests, soft cinematic light.",
            "Melancholic",
        ),
        FilmStory(
            "anime_03",
            "Nyxara",
            "Psychological Horror",
            "A girl begins receiving messages from a version of herself that died years ago.",
            "Nyxara",
            "The Other Nyxara",
            "An abandoned coastal town where clocks never move.",
            "Identity and fear.",
            "Cold coastal horror, fog, muted colors, oppressive silence.",
            "Ambiguous",
        ),
        FilmStory(
            "anime_04",
            "Kaelith",
            "Action Fantasy",
            "A disgraced swordsman must protect the child carrying the last fragment of a destroyed kingdom.",
            "Kaelith",
            "Lord Vaeron",
            "A fractured kingdom surrounded by enormous black mountains.",
            "Redemption.",
            "High-energy sword choreography with dramatic skies.",
            "Triumphant",
        ),
        FilmStory(
            "anime_05",
            "Orivane",
            "Science Fantasy",
            "A boy living inside a dying artificial world discovers that its final sunrise is only hours away.",
            "Orivane",
            "The Architect",
            "A gigantic artificial city orbiting a dead star.",
            "Mortality and meaning.",
            "Futuristic anime architecture, neon rain, cosmic vistas.",
            "Bittersweet",
        ),
        FilmStory(
            "anime_06",
            "Zeravia",
            "Dark Romance",
            "Two strangers share the same recurring dream but wake up with memories of different lives.",
            "Zeravia",
            "The Dream Weaver",
            "A city connected through sleeping minds.",
            "Longing and impossible love.",
            "Nighttime neon, dream transitions, intimate close-ups.",
            "Tragic",
        ),
        FilmStory(
            "anime_07",
            "Vaelune",
            "Fantasy",
            "A moon priestess learns that the moon she worships is actually a sleeping ancient being.",
            "Vaelune",
            "The Moon Below",
            "An ocean kingdom illuminated by enormous moon crystals.",
            "Faith and truth.",
            "Silver-blue fantasy landscapes and luminous water.",
            "Revelatory",
        ),
        FilmStory(
            "anime_08",
            "Ravelyth",
            "Action Horror",
            "A hunter enters a city where monsters imitate the voices of people he once loved.",
            "Ravelyth",
            "The Choir",
            "A ruined city hidden inside perpetual midnight.",
            "Trauma and courage.",
            "Violent shadows, rain, ruined architecture.",
            "Dark Triumph",
        ),
        FilmStory(
            "anime_09",
            "Solvarya",
            "Adventure Fantasy",
            "A young explorer searches for a legendary sun buried beneath an eternal winter.",
            "Solvarya",
            "The Frost Queen",
            "A frozen continent beneath a permanent eclipse.",
            "Hope.",
            "Grand landscapes, snow, warm light against cold environments.",
            "Hopeful",
        ),
        FilmStory(
            "anime_10",
            "Xaveren",
            "Cyberpunk Action",
            "A memory thief steals one memory too many and accidentally discovers the truth behind his own identity.",
            "Xaveren",
            "The Memory Corporation",
            "A vertical cyberpunk metropolis.",
            "Identity and freedom.",
            "Neon streets, rain, kinetic camera movement.",
            "Open",
        ),
        FilmStory(
            "anime_11",
            "Elyvara",
            "Romance Drama",
            "Two childhood friends meet again after one of them has forgotten everything.",
            "Elyvara",
            "Time itself",
            "A quiet seaside town where memories fade unusually quickly.",
            "Memory and love.",
            "Warm sunset photography, intimate emotional framing.",
            "Bittersweet",
        ),
        FilmStory(
            "anime_12",
            "Neravelle",
            "Mystery Fantasy",
            "A detective investigates a village where nobody casts a shadow.",
            "Neravelle",
            "The Shadowless",
            "A secluded mountain village.",
            "Truth and sacrifice.",
            "Fog, lanterns, dark forests.",
            "Revelation",
        ),
        FilmStory(
            "anime_13",
            "Vaerith",
            "Epic Fantasy",
            "A fallen prince returns to a kingdom that believes he died twenty years earlier.",
            "Vaerith",
            "The False King",
            "A vast medieval kingdom divided by magical borders.",
            "Betrayal and responsibility.",
            "Epic castles, storms, battlefield cinematography.",
            "Sacrificial",
        ),
        FilmStory(
            "anime_14",
            "Lunavyr",
            "Dark Fantasy",
            "A girl follows a white fox into a forest that contains every version of her future.",
            "Lunavyr",
            "The Forest Oracle",
            "An impossible forest existing outside normal time.",
            "Choice and regret.",
            "Mystical forests, moonlight, surreal transitions.",
            "Hopeful",
        ),
        FilmStory(
            "anime_15",
            "Averlyn",
            "Romance Fantasy",
            "A young musician discovers that every song he writes brings someone from the past back for one night.",
            "Averlyn",
            "The Last Song",
            "A rain-covered old European-inspired city.",
            "Love and farewell.",
            "Piano, rain, warm interiors, cinematic night scenes.",
            "Emotional",
        ),
        FilmStory(
            "anime_16",
            "Neyvara",
            "Psychological Drama",
            "A teenager wakes every morning with memories belonging to another person.",
            "Neyvara",
            "The Forgotten Self",
            "A modern city with recurring impossible events.",
            "Selfhood.",
            "Naturalistic anime cinematography with surreal interruptions.",
            "Ambiguous",
        ),
        FilmStory(
            "anime_17",
            "Elvaria",
            "Adventure",
            "Three young travelers cross a dying magical continent searching for a place untouched by war.",
            "Elvaria",
            "The War Machine",
            "A vast fantasy continent.",
            "Friendship and survival.",
            "Large-scale landscapes and traveling sequences.",
            "Hopeful",
        ),
        FilmStory(
            "anime_18",
            "Virelya",
            "Horror Mystery",
            "A village hears a bell every midnight, and every person who investigates disappears.",
            "Virelya",
            "The Bell",
            "A remote mountain settlement.",
            "Curiosity and fear.",
            "Heavy fog, darkness, candlelight.",
            "Dark",
        ),
        FilmStory(
            "anime_19",
            "Caelora",
            "Science Fantasy",
            "A girl aboard a generation ship discovers that Earth was never actually destroyed.",
            "Caelora",
            "The Ship Intelligence",
            "A generation ship drifting between stars.",
            "Truth and home.",
            "Space interiors, stars, restrained futuristic design.",
            "Revelatory",
        ),
        FilmStory(
            "anime_20",
            "Seravyn",
            "Romantic Drama",
            "A boy keeps meeting the same girl on the same rainy street even though they live in different years.",
            "Seravyn",
            "Time",
            "A timeless rain-soaked city street.",
            "Missed chances.",
            "Rain, umbrellas, warm streetlights, emotional close-ups.",
            "Bittersweet",
        ),
        FilmStory(
            "anime_21",
            "Mouravia",
            "Dark Fantasy",
            "A kingdom hires a girl who can speak to the dead to investigate a royal murder.",
            "Mouravia",
            "The Dead King",
            "A gothic kingdom surrounded by mist.",
            "Grief and justice.",
            "Gothic castles, candles, fog.",
            "Dark Revelation",
        ),
        FilmStory(
            "anime_22",
            "Noxelya",
            "Horror Fantasy",
            "Every night the city loses one street, until a girl realizes the missing streets lead somewhere.",
            "Noxelya",
            "The City Beneath",
            "A gigantic city slowly disappearing.",
            "Fear of the unknown.",
            "Black skies, distorted architecture, eerie silence.",
            "Nightmarish",
        ),
        FilmStory(
            "anime_23",
            "Vaelora",
            "Epic Romance",
            "A warrior and a healer from opposing kingdoms must cross a battlefield that never ends.",
            "Vaelora",
            "The Endless War",
            "Two kingdoms trapped in an eternal battlefield.",
            "Love during conflict.",
            "Large-scale war scenes contrasted with quiet intimacy.",
            "Tragic",
        ),
        FilmStory(
            "anime_24",
            "Eryndra",
            "Mystery",
            "A girl finds photographs showing events that have not happened yet.",
            "Eryndra",
            "The Photographer",
            "A modern city surrounded by mountains.",
            "Fate and choice.",
            "Photographic compositions, rain, subdued colors.",
            "Open",
        ),
        FilmStory(
            "anime_25",
            "Neylith",
            "Action Fantasy",
            "A young warrior discovers that the monster hunting him is actually protecting him.",
            "Neylith",
            "The Hunter",
            "A wilderness filled with ancient ruins.",
            "Trust.",
            "Dynamic combat and huge natural environments.",
            "Redemptive",
        ),
        FilmStory(
            "anime_26",
            "Auralyne",
            "Musical Fantasy",
            "A girl whose voice can change reality must sing one final song to stop the world from collapsing.",
            "Auralyne",
            "The Silence",
            "A world where music physically shapes reality.",
            "Expression and sacrifice.",
            "Colorful magical soundscapes with cinematic performance scenes.",
            "Sacrificial",
        ),
        FilmStory(
            "anime_27",
            "Velmora",
            "Dark Adventure",
            "A courier carrying a mysterious black letter is hunted across a kingdom.",
            "Velmora",
            "The Letter",
            "A vast kingdom connected by dangerous roads.",
            "Truth and consequence.",
            "Night travel, forests, storms, horseback sequences.",
            "Revelatory",
        ),
        FilmStory(
            "anime_28",
            "Seyravia",
            "Fantasy Romance",
            "A princess secretly leaves her kingdom and falls for the stranger who is supposed to capture her.",
            "Seyravia",
            "The Royal Guard",
            "A colorful fantasy kingdom.",
            "Freedom and love.",
            "Romantic fantasy landscapes and intimate dialogue.",
            "Hopeful",
        ),
        FilmStory(
            "anime_29",
            "Oryvane",
            "Science Fiction",
            "A lonely astronaut receives a transmission from Earth dated fifty years in the future.",
            "Oryvane",
            "Future Earth",
            "A remote space station beyond the solar system.",
            "Isolation and hope.",
            "Deep-space cinematography, minimal interiors.",
            "Emotional",
        ),
        FilmStory(
            "anime_30",
            "Luminarae",
            "Epic Dark Fantasy",
            "A girl carrying the last light in existence walks into a world where darkness has become alive.",
            "Luminarae",
            "The Living Darkness",
            "A dying world without sunlight.",
            "Hope against despair.",
            "Massive dark landscapes, luminous character design, cinematic finale.",
            "Cathartic",
        ),
    )

    @classmethod
    def all(cls) -> tuple[FilmStory, ...]:
        return cls.STORIES

    @classmethod
    def get(cls, film_id: str) -> FilmStory:
        for story in cls.STORIES:
            if story.film_id == film_id:
                return story

        raise KeyError(
            f"Unknown cinematic film: {film_id}"
        )

    @classmethod
    def save(cls, output: str | Path) -> Path:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = [
            asdict(story)
            for story in cls.STORIES
        ]

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
