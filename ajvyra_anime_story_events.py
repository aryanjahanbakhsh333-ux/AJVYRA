from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class StoryEvent:
    event_id: str
    anime_id: int
    order: int
    title: str
    description: str
    importance: str = "major"
    emotional_effect: str = ""


STORY_EVENTS: List[StoryEvent] = []


def add_event(
    anime_id: int,
    order: int,
    title: str,
    description: str,
    importance: str = "major",
    emotional_effect: str = ""
):
    event_id = f"A{anime_id:02d}-E{order:03d}"

    STORY_EVENTS.append(
        StoryEvent(
            event_id,
            anime_id,
            order,
            title,
            description,
            importance,
            emotional_effect
        )
    )


# Anime 01
add_event(1, 1, "The Signal", "Vaelith discovers a mysterious signal coming from a closed district.", emotional_effect="curiosity")
add_event(1, 2, "The Photograph", "A photograph appears that contains Vaelith in a place he has never visited.", emotional_effect="confusion")
add_event(1, 3, "The Girl in the Archive", "Nerya claims she has seen the same photograph before.", emotional_effect="suspicion")
add_event(1, 4, "The Hidden Room", "The pair discovers an underground archive containing impossible records.", emotional_effect="fear")
add_event(1, 5, "The Missing Day", "Vaelith learns that an entire day has disappeared from his memory.", emotional_effect="shock")
add_event(1, 6, "The Truth", "The signal reveals that the archive was created to preserve erased memories.", emotional_effect="pain")
add_event(1, 7, "The Choice", "Vaelith must decide whether to recover every memory or protect the life he has now.", emotional_effect="conflict")
add_event(1, 8, "The Last Transmission", "The signal sends one final message before disappearing.", emotional_effect="sadness")
add_event(1, 9, "After the Silence", "Vaelith accepts the truth without allowing the past to control his future.", emotional_effect="acceptance")


# Anime 02
add_event(2, 1, "The Empty Sky", "Elyra notices that one star has vanished from the night sky.", emotional_effect="wonder")
add_event(2, 2, "The Map", "A strange map appears inside an old book.", emotional_effect="curiosity")
add_event(2, 3, "Beyond the Gate", "Elyra leaves the city with Varyn.", emotional_effect="adventure")
add_event(2, 4, "The Forest", "They discover a forest that changes according to their memories.", emotional_effect="fear")
add_event(2, 5, "The Fallen Star", "A fallen star reveals why the sky is disappearing.", emotional_effect="shock")
add_event(2, 6, "The Price", "Saving the remaining stars requires giving up something personal.", emotional_effect="conflict")
add_event(2, 7, "The Sacrifice", "Elyra makes a decision that changes her journey forever.", emotional_effect="sadness")
add_event(2, 8, "The Return", "The city sees the stars return.", emotional_effect="hope")


# Anime 03
add_event(3, 1, "The First Message", "Nyren receives a message apparently sent by his future self.", emotional_effect="confusion")
add_event(3, 2, "The Warning", "The message prevents a small accident.", emotional_effect="surprise")
add_event(3, 3, "The Second Future", "A second message predicts a much larger disaster.", emotional_effect="fear")
add_event(3, 4, "The Change", "Preventing the disaster changes another part of reality.", emotional_effect="conflict")
add_event(3, 5, "The Paradox", "Nyren realizes every saved future creates another problem.", emotional_effect="despair")
add_event(3, 6, "The Meeting", "He encounters someone who claims to know his future self.", emotional_effect="tension")
add_event(3, 7, "The Final Choice", "Nyren chooses to stop receiving the messages.", emotional_effect="courage")
add_event(3, 8, "Tomorrow", "For the first time, Nyren faces an unknown future.", emotional_effect="hope")


# Anime 04
add_event(4, 1, "The Awakening", "Kaelor discovers a forbidden ability.", emotional_effect="shock")
add_event(4, 2, "The Hunt", "A powerful faction begins searching for him.", emotional_effect="fear")
add_event(4, 3, "The Training", "Ravien teaches Kaelor to control the ability.", emotional_effect="determination")
add_event(4, 4, "The Betrayal", "Someone inside the group reveals their location.", emotional_effect="anger")
add_event(4, 5, "The Battle", "Kaelor uses the forbidden force for the first time.", emotional_effect="intensity")
add_event(4, 6, "The Cost", "The ability begins damaging him.", emotional_effect="pain")
add_event(4, 7, "The Final Fight", "Kaelor confronts the faction leader.", emotional_effect="courage")
add_event(4, 8, "The Choice", "He refuses to become the weapon everyone expected.", emotional_effect="hope")


# Anime 05
add_event(5, 1, "The Empty Seat", "Oriven notices that a classmate has disappeared and nobody remembers him.", emotional_effect="unease")
add_event(5, 2, "The Notebook", "He discovers a notebook containing names of other forgotten people.", emotional_effect="mystery")
add_event(5, 3, "The Pattern", "Every disappearance happens at the same time.", emotional_effect="fear")
add_event(5, 4, "The Night", "Oriven stays awake to witness the next disappearance.", emotional_effect="tension")
add_event(5, 5, "The District", "He enters the abandoned district where the missing people are taken.", emotional_effect="danger")
add_event(5, 6, "The Memory Room", "He finds evidence that the city itself is hiding the truth.", emotional_effect="shock")
add_event(5, 7, "The Return", "Oriven brings back one forgotten person.", emotional_effect="hope")
add_event(5, 8, "Remembered", "The city begins remembering what it tried to erase.", emotional_effect="release")


# Anime 06
add_event(6, 1, "The Satellite", "Zeria discovers that a damaged satellite is making human decisions.", emotional_effect="curiosity")
add_event(6, 2, "The First Prediction", "The satellite predicts a disaster.", emotional_effect="fear")
add_event(6, 3, "The Rescue", "Kavon helps Zeria prevent the disaster.", emotional_effect="relief")
add_event(6, 4, "The Second Decision", "The satellite chooses who should survive another event.", emotional_effect="conflict")
add_event(6, 5, "The Question", "Zeria questions whether the machine understands human life.", emotional_effect="doubt")
add_event(6, 6, "The Shutdown", "They attempt to shut down the satellite.", emotional_effect="tension")
add_event(6, 7, "The Final Calculation", "The satellite chooses to sacrifice itself.", emotional_effect="sadness")
add_event(6, 8, "The Sky", "Zeria looks toward the sky after the signal disappears.", emotional_effect="hope")


# Anime 07
add_event(7, 1, "The Dream", "Vael meets an unknown girl in a recurring dream.", emotional_effect="wonder")
add_event(7, 2, "The Recognition", "He notices the same person in real life.", emotional_effect="surprise")
add_event(7, 3, "The Rain", "Their dreams become more detailed during storms.", emotional_effect="connection")
add_event(7, 4, "The Secret", "Luneya reveals she has been having the same dreams.", emotional_effect="intimacy")
add_event(7, 5, "The Boundary", "The dream world begins appearing in reality.", emotional_effect="fear")
add_event(7, 6, "The Choice", "They must decide whether to remain in the dream.", emotional_effect="conflict")
add_event(7, 7, "Goodbye", "The dream world begins disappearing.", emotional_effect="sadness")
add_event(7, 8, "Morning", "They wake up and choose reality.", emotional_effect="hope")


# Anime 08
add_event(8, 1, "Recruitment", "Ravel is recruited by an organization that predicts crimes.", emotional_effect="curiosity")
add_event(8, 2, "The First Case", "The team prevents a planned crime.", emotional_effect="tension")
add_event(8, 3, "The Prediction", "Ravel sees his own name in the next prediction.", emotional_effect="shock")
add_event(8, 4, "The Investigation", "Nytha discovers the prediction may have been manipulated.", emotional_effect="suspicion")
add_event(8, 5, "The Betrayer", "A member of the organization reveals their true agenda.", emotional_effect="anger")
add_event(8, 6, "The Trap", "Ravel becomes the target of the organization.", emotional_effect="danger")
add_event(8, 7, "The Choice", "He refuses to allow a prediction to define his actions.", emotional_effect="defiance")
add_event(8, 8, "The Future", "The organization loses control of its own prediction system.", emotional_effect="freedom")


# Anime 09
add_event(9, 1, "The Railway", "Solven discovers a railway that does not appear on any map.", emotional_effect="wonder")
add_event(9, 2, "The Train", "The train arrives exactly at midnight.", emotional_effect="mystery")
add_event(9, 3, "The Journey", "Solven, Araya and Veylin board the train.", emotional_effect="adventure")
add_event(9, 4, "The Empty City", "They arrive at a city with no visible inhabitants.", emotional_effect="unease")
add_event(9, 5, "The Clock", "They discover the city exists for only one night.", emotional_effect="urgency")
add_event(9, 6, "The Secret", "The city preserves memories of people who once lived there.", emotional_effect="sadness")
add_event(9, 7, "Sunrise", "The travelers must leave before the city disappears.", emotional_effect="tension")
add_event(9, 8, "The Return", "They return home carrying one final memory.", emotional_effect="hope")


# Anime 10
add_event(10, 1, "Awakening", "Xaven wakes up with memories belonging to an enemy.", emotional_effect="confusion")
add_event(10, 2, "The Mission", "He is sent to stop the person whose memories he carries.", emotional_effect="conflict")
add_event(10, 3, "The Recognition", "The enemy recognizes memories that Xaven should not possess.", emotional_effect="shock")
add_event(10, 4, "The Truth", "Xaven discovers both sides have been manipulated.", emotional_effect="anger")
add_event(10, 5, "The Escape", "Xaven and Riela escape from the battlefield.", emotional_effect="tension")
add_event(10, 6, "The Choice", "He refuses to continue the cycle.", emotional_effect="courage")
add_event(10, 7, "The Final Transmission", "Xaven exposes the truth to both sides.", emotional_effect="release")
add_event(10, 8, "A Different Future", "The conflict begins to change.", emotional_effect="hope")


def get_events(anime_id: int) -> List[StoryEvent]:
    return sorted(
        [event for event in STORY_EVENTS if event.anime_id == anime_id],
        key=lambda event: event.order
    )


def export_events() -> List[Dict]:
    return [event.to_dict() for event in STORY_EVENTS]


if __name__ == "__main__":
    for anime_id in range(1, 11):
        print(f"Anime {anime_id}: {len(get_events(anime_id))} events")
