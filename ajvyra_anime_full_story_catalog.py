"""
AJVYRA Anime - Full Story Catalog
---------------------------------
Central narrative arcs for all 30 AJVYRA anime.

This file does NOT generate video/audio.
It defines what happens in each anime so other production systems
can consume the story data.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class StoryArc:
    anime_id: int
    title: str
    genre: str

    opening: str
    inciting_incident: str
    rising_action: str
    midpoint: str
    major_reversal: str
    crisis: str
    climax: str
    ending: str

    protagonist_goal: str
    central_conflict: str
    emotional_arc: str
    final_message: str


STORIES: List[StoryArc] = [
    StoryArc(
        1, "Veylora", "Psychological / Mystery / Drama",
        "A quiet coastal city begins receiving a radio signal that nobody remembers creating.",
        "Veyra finds a recording containing her own voice describing a memory she has never lived.",
        "She and Caelor investigate abandoned transmitters beneath the old observatory.",
        "The recordings reveal fragments of people's forgotten memories.",
        "Veyra discovers that the signal reacts whenever someone suppresses a painful truth.",
        "The city begins losing recent memories, including names and relationships.",
        "Veyra enters the transmitter chamber and broadcasts her own most painful memory.",
        "The signal disappears after the city collectively remembers what it tried to forget.",
        "Veyra wants to understand why the impossible recordings know her.",
        "Memory versus denial.",
        "Fear becomes acceptance.",
        "Pain does not become harmless by being forgotten."
    ),

    StoryArc(
        2, "Aelvryn", "Fantasy / Adventure / Drama",
        "Aelvryn is a mountain city beneath a sky filled with unnatural stars.",
        "Elyra notices that one star disappears after every midnight.",
        "She travels toward the northern observatory with Varyn and Solven.",
        "They discover an ancient machine beneath the mountains controlling the sky.",
        "The machine is not destroying stars; it is storing them.",
        "The stored stars contain memories of civilizations erased from history.",
        "Elyra must choose between restoring the stars and releasing the memories.",
        "She activates the machine and returns the lost light to the sky.",
        "Elyra wants to discover why the stars are disappearing.",
        "Truth versus protection.",
        "Curiosity becomes responsibility.",
        "Some truths deserve to be remembered."
    ),

    StoryArc(
        3, "Nyxara", "Sci-Fi / Thriller / Mystery",
        "Nyren receives messages from a version of himself ten years older.",
        "The future version warns him not to enter a particular subway station.",
        "Nyren investigates why the warning exists.",
        "He learns that the future messages are being sent from a failed timeline.",
        "The future Nyren admits that every warning he sent created another disaster.",
        "The present begins changing around Nyren as timelines collide.",
        "Nyren deliberately ignores the final message and makes a decision without future guidance.",
        "The timeline stabilizes because his choice was genuinely his own.",
        "Nyren wants to prevent the future disaster.",
        "Free will versus predetermined knowledge.",
        "Fear becomes independence.",
        "Knowing the future does not mean you must obey it."
    ),

    StoryArc(
        4, "Kaelith", "Action / Fantasy / Adventure",
        "Kaelor lives in a kingdom where magical power determines social status.",
        "A forbidden force awakens inside him during an attack.",
        "He escapes with Zeyla and searches for the origin of the power.",
        "They discover that the kingdom secretly created the forbidden force.",
        "Kaelor learns his power was designed to destroy magical rulers.",
        "The kingdom's elite hunt him through several districts.",
        "Kaelor refuses revenge and uses the force to destroy the system controlling ordinary people.",
        "He disappears before becoming the new ruler.",
        "Kaelor wants control over his own power.",
        "Power versus responsibility.",
        "Anger becomes restraint.",
        "Having power does not justify becoming powerful over others."
    ),

    StoryArc(
        5, "Orivane", "Thriller / Psychological / Mystery",
        "People disappear from Orivane every night, and by morning nobody remembers them.",
        "Oriven discovers an old photograph containing a person everyone has forgotten.",
        "He searches for others who still remember the missing.",
        "The group finds a hidden district outside normal city maps.",
        "The missing people are alive but trapped inside a memory loop.",
        "Oriven discovers his own name written among the missing.",
        "He enters the loop to bring the forgotten people back.",
        "The city remembers them, but Oriven loses one personal memory in exchange.",
        "Oriven wants to understand the disappearances.",
        "Identity versus collective memory.",
        "Obsession becomes sacrifice.",
        "A person can disappear from records without becoming meaningless."
    ),

    StoryArc(
        6, "Zeravia", "Sci-Fi / Action / Drama",
        "A damaged orbital satellite begins making independent decisions about human survival.",
        "Zeria receives a message from the satellite naming three people it intends to save.",
        "She travels to an abandoned control facility.",
        "The satellite reveals that its original survival protocol has failed.",
        "Its calculations show that saving everyone is impossible.",
        "Zeria discovers the satellite is secretly protecting someone considered statistically insignificant.",
        "She changes the system from probability-based decisions to human choice.",
        "The satellite shuts down peacefully after transmitting its final data.",
        "Zeria wants to know why the machine chose certain lives.",
        "Calculation versus humanity.",
        "Detachment becomes empathy.",
        "A human life cannot be reduced to a number."
    ),

    StoryArc(
        7, "Vaelune", "Fantasy / Romance / Drama",
        "Vael and Luneya repeatedly meet inside the same dream.",
        "They recognize each other in dreams but pass like strangers during daylight.",
        "They begin leaving clues for their waking selves.",
        "The dreams reveal that they knew each other years earlier.",
        "One of them remembers a promise the other forgot.",
        "The dream world begins collapsing as their memories return.",
        "They finally remember their shared past and accept what happened.",
        "The final dream ends with them meeting awake without needing magic.",
        "Vael wants to discover who Luneya really is.",
        "Memory versus present identity.",
        "Longing becomes acceptance.",
        "Some connections matter even when their original form disappears."
    ),

    StoryArc(
        8, "Ravelyth", "Action / Thriller / Mystery",
        "Teenagers with visions of future crimes are secretly recruited by an organization.",
        "Ravel predicts a crime that the organization refuses to investigate.",
        "Ravel and Nytha investigate independently.",
        "They discover that some predicted crimes are being deliberately caused.",
        "The organization has been manipulating predictions to justify its authority.",
        "Ravel becomes the target of the organization.",
        "He exposes the system instead of using his visions to control people.",
        "The gifted teenagers become independent investigators.",
        "Ravel wants to stop future crimes.",
        "Prediction versus manipulation.",
        "Fear becomes moral courage.",
        "Seeing a possible future does not give anyone ownership of it."
    ),

    StoryArc(
        9, "Solvarya", "Adventure / Fantasy / Drama",
        "An abandoned railway appears once every hundred years.",
        "Solven boards the train after hearing his missing mother's name announced.",
        "He reaches a city that exists outside normal time.",
        "Every resident has arrived from a different century.",
        "Solven learns the city survives by taking one memory from every visitor.",
        "He must choose between recovering his mother and losing his own identity.",
        "He refuses the city's bargain and finds another way to leave.",
        "The city disappears, but Solven keeps the memory he came for.",
        "Solven wants answers about his mother.",
        "Loss versus identity.",
        "Attachment becomes courage.",
        "Remembering someone does not require losing yourself."
    ),

    StoryArc(
        10, "Xaveren", "Action / Sci-Fi / Drama",
        "A pilot wakes after an accident carrying memories that belong to an enemy.",
        "Xaven remembers battles he never fought.",
        "He searches for the owner of the memories.",
        "He discovers the enemy pilot was once his childhood friend.",
        "The war was built on a manufactured historical event.",
        "Both sides prepare for one final battle.",
        "Xaven broadcasts the truth instead of firing.",
        "The battle stops long enough for the truth to be heard.",
        "Xaven wants to understand his enemy.",
        "Propaganda versus personal memory.",
        "Hatred becomes recognition.",
        "Knowing someone's story can change what an enemy means."
    ),

    StoryArc(
        11, "Elyvara", "Romance / Drama",
        "Two strangers exchange anonymous letters through an old library box.",
        "Elyra discovers a letter addressed to her.",
        "The correspondence becomes a daily ritual.",
        "They realize their lives are connected through the same neighborhood.",
        "Both suspect the other person but fear revealing themselves.",
        "The letters suddenly stop.",
        "Elyra searches for the writer and discovers Varen has been writing them.",
        "They meet without pretending to be anonymous.",
        "Elyra wants to know the person behind the letters.",
        "Anonymity versus vulnerability.",
        "Curiosity becomes trust.",
        "Real connection begins when hiding becomes unnecessary."
    ),

    StoryArc(
        12, "Neravelle", "Romance / Mystery / Drama",
        "Nerava discovers photographs showing moments that have not happened yet.",
        "One photograph shows her meeting Kaelin at a place she has never visited.",
        "She follows the photographs one by one.",
        "The images begin predicting emotionally difficult moments.",
        "She realizes the photographs are not fixed futures.",
        "Changing one image causes later images to become unclear.",
        "Nerava stops chasing the photographs and chooses her own future.",
        "The final photograph is blank.",
        "Nerava wants to understand her future.",
        "Prediction versus choice.",
        "Anxiety becomes freedom.",
        "A future is not meaningful if you never choose it."
    ),

    StoryArc(
        13, "Vaerith", "Romance / Psychological / Drama",
        "Vaer begins hearing Elira's thoughts whenever rain falls.",
        "He accidentally hears a thought she never says aloud.",
        "Their relationship becomes complicated because Vaer knows things she has not shared.",
        "Elira discovers his secret.",
        "She feels betrayed even though he never intended to invade her privacy.",
        "The rain begins every day, making silence impossible.",
        "Vaer learns to respect silence and stops listening for hidden answers.",
        "The rain eventually stops, but their trust remains.",
        "Vaer wants to understand Elira.",
        "Intimacy versus privacy.",
        "Possession becomes respect.",
        "Knowing everything about someone is not the same as understanding them."
    ),

    StoryArc(
        14, "Lunavyr", "Romance / Fantasy",
        "A mysterious girl appears only beneath moonlight.",
        "Lunai meets Veyren on an empty street after midnight.",
        "They spend several nights talking.",
        "Veyren discovers Lunai disappears whenever sunrise arrives.",
        "She reveals she is connected to an old lunar phenomenon.",
        "One night the moon does not rise.",
        "Veyren searches for Lunai before she disappears forever.",
        "They meet again years later under an ordinary moon.",
        "Veyren wants to understand Lunai's existence.",
        "Temporary life versus lasting memory.",
        "Wonder becomes acceptance.",
        "A short connection can still change a lifetime."
    ),

    StoryArc(
        15, "Averlyn", "Romance / Slice of Life / Drama",
        "Two students become friends while hiding their deepest fears.",
        "Averin notices Selya always leaves school before sunset.",
        "They gradually share small pieces of their lives.",
        "A school project forces them to work together.",
        "Selya admits she plans to leave the city.",
        "Their friendship becomes threatened by the approaching departure.",
        "Averin stops trying to convince her to stay.",
        "They promise to remain part of each other's lives from different places.",
        "Averin wants to understand his growing attachment.",
        "Fear of change versus friendship.",
        "Attachment becomes maturity.",
        "Caring for someone does not mean controlling their path."
    ),

    StoryArc(
        16, "Neyvara", "Romance / Mystery / Thriller",
        "Neyra receives anonymous messages describing future relationships.",
        "The first message predicts someone she has never met.",
        "More messages arrive and become increasingly personal.",
        "Valen appears exactly as predicted.",
        "The messages begin telling Neyra what she should feel.",
        "She realizes the sender has been manipulating her choices.",
        "Neyra confronts the sender and destroys the message archive.",
        "She chooses relationships without instructions.",
        "Neyra wants to discover who controls the messages.",
        "Guidance versus autonomy.",
        "Dependency becomes independence.",
        "Love cannot be scripted by someone else."
    ),

    StoryArc(
        17, "Elvaria", "Romance / Fantasy / Drama",
        "Elvar discovers a glass pendant capable of preserving one memory.",
        "He stores a memory of Mirael inside it.",
        "The pendant becomes the center of their relationship.",
        "He learns every preserved memory slowly removes another memory from its owner.",
        "Elvar must choose which memory to protect.",
        "The pendant begins cracking.",
        "He releases the memory instead of keeping it forever.",
        "The memory disappears from the pendant but remains meaningful to both.",
        "Elvar wants to preserve something precious.",
        "Preservation versus living.",
        "Fear of loss becomes acceptance.",
        "A memory does not need to be trapped to remain valuable."
    ),

    StoryArc(
        18, "Virelya", "Romance / Psychological",
        "Two people repeatedly meet on an empty winter train.",
        "Virel recognizes Ayaen despite never meeting her elsewhere.",
        "Their conversations repeat with strange variations.",
        "They realize each meeting occurs on a different version of the same winter.",
        "One version ends with one of them disappearing.",
        "Virel tries to change the final train journey.",
        "Ayaen chooses to leave the train before the loop closes.",
        "The next winter they meet in an ordinary station.",
        "Virel wants to escape the repeating train.",
        "Repetition versus change.",
        "Fear becomes action.",
        "Life begins where repetition ends."
    ),

    StoryArc(
        19, "Caelora", "Romance / Drama / Adventure",
        "Two travelers promise to meet again after choosing separate paths.",
        "Caelor and Ravya part at a mountain crossroads.",
        "Both travel through different regions.",
        "Each finds clues suggesting the other is nearby.",
        "A storm destroys the route connecting their destinations.",
        "They consider abandoning the promise.",
        "They continue separately until their paths unexpectedly cross.",
        "Their reunion is quiet rather than dramatic.",
        "Caelor wants to keep a promise without forcing the future.",
        "Distance versus commitment.",
        "Longing becomes patience.",
        "Some promises survive because they are not forced."
    ),

    StoryArc(
        20, "Seravyn", "Romance / Drama",
        "Seren and Vayla develop a quiet friendship.",
        "They begin meeting after school without calling it a routine.",
        "Small gestures slowly become emotionally important.",
        "Both realize their friendship has changed.",
        "Neither wants to risk destroying it with a confession.",
        "A misunderstanding separates them.",
        "They finally speak honestly without demanding an outcome.",
        "Their relationship continues with greater honesty.",
        "Seren wants to understand what their bond means.",
        "Silence versus honesty.",
        "Uncertainty becomes courage.",
        "Not every meaningful relationship needs an immediate label."
    ),

    StoryArc(
        21, "Mouravia", "Drama / Psychological / Sad",
        "Mouren keeps visiting a place where someone important once waited.",
        "He finds an old object that reminds him of Elvya.",
        "He reconstructs memories of their final days.",
        "He discovers he has been remembering one event incorrectly.",
        "The corrected memory is more painful than the one he preferred.",
        "Mouren must decide whether to keep living inside the old version.",
        "He returns one final time and leaves the object behind.",
        "He visits the place later without expecting anyone to return.",
        "Mouren wants to understand his grief.",
        "Memory versus acceptance.",
        "Grief becomes movement.",
        "Moving forward does not erase the person you lost."
    ),

    StoryArc(
        22, "Noxelya", "Psychological / Drama / Mystery",
        "Noxel finds notes written in her handwriting about days she cannot remember.",
        "One note warns her not to trust herself tomorrow.",
        "She follows the instructions.",
        "The notes reveal a hidden pattern in her missing memories.",
        "She discovers she wrote the notes during moments of extreme fear.",
        "The final note asks her to forgive herself.",
        "Noxel stops treating her forgotten self as an enemy.",
        "She begins recording her present life openly.",
        "Noxel wants to understand the missing days.",
        "Self-protection versus self-acceptance.",
        "Fear becomes compassion.",
        "Sometimes the person we need to forgive is ourselves."
    ),

    StoryArc(
        23, "Vaelora", "Drama / Romance / Sad",
        "Vaelor and Leria become important to each other at the wrong moment in life.",
        "They meet shortly before Leria must leave.",
        "Their connection grows quickly.",
        "Both know the relationship has a deadline.",
        "They avoid discussing the future.",
        "The departure date arrives.",
        "They choose honesty rather than pretending distance will be easy.",
        "Years later, their memories remain warm instead of painful.",
        "Vaelor wants to make the most of limited time.",
        "Love versus timing.",
        "Fear becomes gratitude.",
        "Not every meaningful relationship is meant to last forever."
    ),

    StoryArc(
        24, "Eryndra", "Psychological / Drama",
        "Eryn tries to rebuild life after losing his closest friend Davel.",
        "A familiar song triggers an old memory.",
        "Eryn starts returning to places they visited together.",
        "He realizes grief has made him isolate himself.",
        "A friend confronts him about living only inside the past.",
        "Eryn finally visits the place where Davel's final memory remains.",
        "He speaks aloud about everything he never said.",
        "He begins creating new memories without feeling guilty.",
        "Eryn wants to learn how to live after loss.",
        "Grief versus renewal.",
        "Guilt becomes gratitude.",
        "Continuing to live is not betrayal."
    ),

    StoryArc(
        25, "Neylith", "Drama / Mystery / Sad",
        "Neyl discovers a forgotten voice recording belonging to someone missing.",
        "The recording contains a warning and a name.",
        "Neyl searches for the person connected to the voice.",
        "Each recording reveals another part of the disappearance.",
        "The final recording suggests the missing person chose to disappear.",
        "Neyl struggles with the difference between saving someone and respecting their choice.",
        "He follows the final clue and learns the truth.",
        "He keeps the recordings but stops searching.",
        "Neyl wants to know what happened.",
        "Truth versus rescue.",
        "Obsession becomes respect.",
        "Finding the truth does not always mean changing the past."
    ),

    StoryArc(
        26, "Auralyne", "Drama / Fantasy / Sad",
        "A city hears the voice of someone who disappeared years earlier.",
        "Aural recognizes the voice immediately.",
        "The voice appears through old speakers around the city.",
        "The messages describe places that no longer exist.",
        "Aural discovers the voice is coming from a magical echo beneath the city.",
        "The echo begins fading.",
        "Aural reaches the source and hears one final message.",
        "The city falls silent, but the memory remains.",
        "Aural wants to hear the voice one last time.",
        "Presence versus absence.",
        "Longing becomes farewell.",
        "Sometimes goodbye is the final form of love."
    ),

    StoryArc(
        27, "Velmora", "Psychological / Drama / Thriller",
        "Vel discovers that his happiest memories may have been artificially created.",
        "A familiar scene suddenly changes when he revisits it.",
        "He investigates his childhood memories.",
        "He finds evidence that several memories were implanted.",
        "Vel learns the memories were created to protect him from a traumatic event.",
        "Removing them would restore the truth but destroy parts of his current identity.",
        "He chooses to remember both the artificial comfort and the painful truth.",
        "Vel accepts that his identity includes imperfect memories.",
        "Vel wants to know what really happened.",
        "Truth versus psychological protection.",
        "Suspicion becomes self-acceptance.",
        "A painful truth can coexist with the person you became."
    ),

    StoryArc(
        28, "Seyravia", "Drama / Adventure / Sad",
        "Seyra crosses several cities carrying a final message.",
        "She receives the message from someone who cannot deliver it.",
        "She travels through trains, streets and remote towns.",
        "Every city reveals another part of the sender's story.",
        "Seyra learns the recipient may no longer be alive.",
        "She considers destroying the message.",
        "She continues because the meaning matters even without an answer.",
        "The message is delivered to the recipient's family.",
        "Seyra wants to complete her promise.",
        "Duty versus emotional exhaustion.",
        "Burden becomes meaning.",
        "A message can matter even when no reply comes."
    ),

    StoryArc(
        29, "Oryvane", "Drama / Psychological / Romance",
        "Oryn has stopped trusting people after repeated betrayal.",
        "Veya refuses to leave after seeing how isolated he has become.",
        "She slowly earns his trust through ordinary actions.",
        "Oryn deliberately pushes her away.",
        "Veya leaves rather than allowing herself to be treated unfairly.",
        "Oryn realizes trust is not something another person can force into existence.",
        "He finds Veya and apologizes without asking for immediate forgiveness.",
        "She chooses to begin again slowly.",
        "Oryn wants to learn whether trust is possible again.",
        "Protection versus connection.",
        "Defensiveness becomes vulnerability.",
        "Trust is built through repeated choices."
    ),

    StoryArc(
        30, "Luminarae", "Drama / Fantasy / Psychological",
        "Lumir enters a strange world where painful memories become visible objects.",
        "Aera shows him a landscape built from his childhood memories.",
        "Each memory becomes a physical place he must cross.",
        "Lumir encounters Veyn, a figure representing everything he refuses to remember.",
        "The world reveals that his happiest memories are also connected to his pain.",
        "The landscape begins collapsing.",
        "Lumir stops running and accepts every memory instead of destroying them.",
        "He wakes in the real world with no magical answers, but with peace.",
        "Lumir wants to escape his painful memories.",
        "Escape versus integration.",
        "Pain becomes understanding.",
        "Healing does not require deleting the past."
    ),
]


def get_story(anime_id: int) -> StoryArc:
    for story in STORIES:
        if story.anime_id == anime_id:
            return story
    raise KeyError("Anime not found: {}".format(anime_id))


def story_as_dict(anime_id: int) -> Dict:
    return asdict(get_story(anime_id))


def all_stories() -> List[Dict]:
    return [asdict(item) for item in STORIES]


def validate_story_catalog() -> Dict[str, object]:
    ids = [item.anime_id for item in STORIES]
    titles = [item.title for item in STORIES]

    return {
        "anime_count": len(STORIES),
        "ids_are_unique": len(ids) == len(set(ids)),
        "titles_are_unique": len(titles) == len(set(titles)),
        "has_all_30": ids == list(range(1, 31)),
        "valid": (
            len(STORIES) == 30
            and len(ids) == len(set(ids))
            and len(titles) == len(set(titles))
            and ids == list(range(1, 31))
        ),
    }


if __name__ == "__main__":
    print(validate_story_catalog())
