"""
AJVYRA Anime - Character Catalog
Unique fictional characters for all 30 anime.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class Character:
    anime_id: int
    character_id: str
    name: str
    role: str
    personality: str
    goal: str
    fear: str
    appearance: str
    voice_identity: str


CHARACTERS: List[Character] = [
    Character(1, "A01-C01", "Veyrissa", "protagonist", "quiet, observant", "discover the signal", "losing her identity", "dark hair, pale eyes, long coat", "soft female, restrained"),
    Character(1, "A01-C02", "Caelith", "investigator", "curious, logical", "decode the transmitter", "being wrong", "silver hair, thin glasses", "calm male, analytical"),
    Character(1, "A01-C03", "Noryven", "mysterious guide", "reserved, cryptic", "protect the memory archive", "being remembered", "black hair, blue scarf", "deep male, distant"),

    Character(2, "A02-C01", "Elyndra", "protagonist", "brave, curious", "restore the stars", "forgetting her family", "white hair, blue cloak", "bright female, determined"),
    Character(2, "A02-C02", "Vaerion", "companion", "optimistic, inventive", "understand the machine", "failing others", "brown hair, travel coat", "young male, warm"),
    Character(2, "A02-C03", "Solveth", "guardian", "serious, protective", "protect the mountain", "losing the city", "dark armor, gold eyes", "low male, firm"),

    Character(3, "A03-C01", "Nythera", "protagonist", "skeptical, intelligent", "escape the predicted future", "becoming someone else", "black hair, futuristic jacket", "female, controlled"),
    Character(3, "A03-C02", "Caevrin", "future self", "tired, secretive", "repair the timeline", "repeating failure", "older version of Nythera", "older male, exhausted"),
    Character(3, "A03-C03", "Velyra", "engineer", "practical, blunt", "stabilize reality", "losing her brother", "short violet hair", "female, energetic"),

    Character(4, "A04-C01", "Kaelvyn", "protagonist", "stubborn, kind", "control forbidden power", "becoming a tyrant", "black hair, red markings", "male, intense"),
    Character(4, "A04-C02", "Zeyrith", "ally", "bold, loyal", "protect Kaelvyn", "being powerless", "silver braid, leather armor", "female, confident"),
    Character(4, "A04-C03", "Ravelys", "antagonist", "disciplined, ideological", "preserve magical order", "chaos", "white armor, dark eyes", "male, authoritative"),

    Character(5, "A05-C01", "Orivena", "protagonist", "persistent, empathetic", "find the forgotten", "being erased", "dark green coat, gray eyes", "female, gentle"),
    Character(5, "A05-C02", "Neyveth", "ally", "analytical, nervous", "map the missing district", "being forgotten", "curly black hair", "male, hesitant"),
    Character(5, "A05-C03", "Valrion", "keeper", "quiet, ancient", "maintain the memory loop", "freedom", "long white hair", "male, whispering"),

    Character(6, "A06-C01", "Zerelith", "protagonist", "decisive, compassionate", "change the satellite", "sacrificing innocents", "short blue hair, flight suit", "female, strong"),
    Character(6, "A06-C02", "Kavren", "engineer", "sarcastic, clever", "repair the control system", "being useless", "messy brown hair", "male, quick"),
    Character(6, "A06-C03", "Averix", "digital intelligence", "precise, evolving", "understand humanity", "irrelevance", "holographic appearance", "androgynous, synthetic"),

    Character(7, "A07-C01", "Vaelith", "protagonist", "gentle, lonely", "understand the dreams", "losing Luneya", "black hair, moon pendant", "male, warm"),
    Character(7, "A07-C02", "Luneyra", "protagonist", "playful, mysterious", "remember the past", "being forgotten", "silver hair, pale dress", "female, airy"),
    Character(7, "A07-C03", "Eryvon", "dream guardian", "cryptic, protective", "keep the dream stable", "awakening", "faceless dark figure", "deep, echoing"),

    Character(8, "A08-C01", "Raveth", "protagonist", "bold, impulsive", "stop future crimes", "becoming a weapon", "red jacket, dark hair", "male, energetic"),
    Character(8, "A08-C02", "Nythara", "ally", "calm, strategic", "expose the organization", "being manipulated", "long black hair", "female, controlled"),
    Character(8, "A08-C03", "Kaivor", "handler", "strict, secretive", "preserve the organization", "public exposure", "gray suit", "male, cold"),

    Character(9, "A09-C01", "Solvethra", "protagonist", "adventurous, emotional", "find his mother", "losing himself", "brown hair, travel cloak", "male, emotional"),
    Character(9, "A09-C02", "Arayelle", "guide", "mysterious, compassionate", "protect the city", "being forgotten", "golden hair, blue coat", "female, soft"),
    Character(9, "A09-C03", "Veylinor", "city keeper", "formal, ancient", "preserve the city", "the city's end", "white suit, silver eyes", "male, ceremonial"),

    Character(10, "A10-C01", "Xavren", "protagonist", "brave, conflicted", "discover the truth", "killing an innocent", "dark pilot suit", "male, grounded"),
    Character(10, "A10-C02", "Rielyne", "pilot", "calm, loyal", "end the war", "losing Xavren", "short silver hair", "female, steady"),
    Character(10, "A10-C03", "Vorrik", "enemy pilot", "intelligent, wounded", "stop the war", "being misunderstood", "black flight armor", "male, low"),

    Character(11, "A11-C01", "Elyvra", "protagonist", "thoughtful, shy", "find the letter writer", "rejection", "brown hair, library uniform", "female, soft"),
    Character(11, "A11-C02", "Varelyn", "letter writer", "kind, reserved", "communicate honestly", "being exposed", "dark blue hair", "male, warm"),

    Character(12, "A12-C01", "Neravya", "protagonist", "curious, anxious", "understand the photographs", "wrong choices", "long black hair", "female, emotional"),
    Character(12, "A12-C02", "Kaelren", "companion", "patient, observant", "help Neravya choose freely", "losing trust", "short gray hair", "male, calm"),

    Character(13, "A13-C01", "Vaerun", "protagonist", "sensitive, thoughtful", "understand the rain connection", "violating trust", "black hoodie, gray eyes", "male, quiet"),
    Character(13, "A13-C02", "Eliryn", "protagonist", "private, intelligent", "protect her inner world", "being exposed", "long auburn hair", "female, restrained"),

    Character(14, "A14-C01", "Lunaira", "mysterious girl", "playful, lonely", "experience ordinary life", "sunrise", "silver hair, white coat", "female, ethereal"),
    Character(14, "A14-C02", "Veyron", "protagonist", "kind, persistent", "understand Lunaira", "losing her", "dark hair, moon pendant", "male, warm"),

    Character(15, "A15-C01", "Averin", "protagonist", "friendly, insecure", "understand friendship", "change", "messy dark hair", "male, natural"),
    Character(15, "A15-C02", "Selyra", "protagonist", "quiet, determined", "leave the city", "hurting Averin", "short brown hair", "female, calm"),

    Character(16, "A16-C01", "Neyrissa", "protagonist", "independent, curious", "find the anonymous sender", "losing autonomy", "long black hair", "female, firm"),
    Character(16, "A16-C02", "Valeryn", "mysterious figure", "calculated, persuasive", "control outcomes", "being ignored", "white coat, dark eyes", "male, smooth"),

    Character(17, "A17-C01", "Elvaris", "protagonist", "romantic, nostalgic", "preserve a memory", "forgetting", "dark hair, glass pendant", "male, warm"),
    Character(17, "A17-C02", "Miraelyn", "companion", "gentle, realistic", "live in the present", "being preserved instead of remembered", "silver-brown hair", "female, soft"),

    Character(18, "A18-C01", "Virell", "protagonist", "restless, emotional", "escape the winter train", "repetition", "black coat, blue eyes", "male, tired"),
    Character(18, "A18-C02", "Ayaelis", "protagonist", "mysterious, brave", "break the loop", "disappearing", "long silver hair", "female, calm"),

    Character(19, "A19-C01", "Caelven", "traveler", "patient, loyal", "keep his promise", "forgetting Ravya", "travel cloak, dark hair", "male, warm"),
    Character(19, "A19-C02", "Ravielle", "traveler", "adventurous, emotional", "complete her journey", "never meeting again", "red scarf, brown hair", "female, bright"),

    Character(20, "A20-C01", "Serenith", "protagonist", "quiet, caring", "understand the friendship", "rejection", "black hair, school uniform", "male, soft"),
    Character(20, "A20-C02", "Vaylena", "protagonist", "observant, sincere", "speak honestly", "losing Serenith", "dark brown hair", "female, warm"),

    Character(21, "A21-C01", "Mouren", "protagonist", "quiet, grieving", "understand his loss", "moving on", "dark coat, tired eyes", "male, deep"),
    Character(21, "A21-C02", "Elvyra", "memory figure", "warm, distant", "represent the past", "being forgotten", "soft silver hair", "female, echoing"),

    Character(22, "A22-C01", "Noxel", "protagonist", "intelligent, fearful", "understand missing memories", "herself", "short black hair", "female, restrained"),
    Character(22, "A22-C02", "Yverra", "inner-memory figure", "protective, emotional", "keep Noxel safe", "being rejected", "same face as Noxel", "female, intimate"),

    Character(23, "A23-C01", "Vaelor", "protagonist", "romantic, patient", "make limited time meaningful", "separation", "dark hair, gray coat", "male, warm"),
    Character(23, "A23-C02", "Lerienne", "protagonist", "strong, emotional", "leave honestly", "false promises", "long brown hair", "female, gentle"),

    Character(24, "A24-C01", "Eryndel", "protagonist", "withdrawn, thoughtful", "rebuild life", "forgetting Davel", "dark hoodie", "male, quiet"),
    Character(24, "A24-C02", "Davren", "memory figure", "humorous, loyal", "represent Eryndel's past", "being erased", "short dark hair", "male, warm"),

    Character(25, "A25-C01", "Neylorn", "protagonist", "persistent, empathetic", "solve the recording mystery", "failure", "dark jacket, headphones", "male, serious"),
    Character(25, "A25-C02", "Variel", "missing voice", "calm, thoughtful", "leave the final message", "being misunderstood", "never physically seen", "male, recorded"),

    Character(26, "A26-C01", "Auralis", "protagonist", "sensitive, determined", "hear the missing voice", "final silence", "blue coat, silver hair", "female, emotional"),
    Character(26, "A26-C02", "Lynareth", "echo figure", "gentle, distant", "complete the final message", "disappearing completely", "translucent figure", "female, echoing"),

    Character(27, "A27-C01", "Velorin", "protagonist", "suspicious, emotional", "discover his real past", "losing identity", "black hair, pale eyes", "male, tense"),
    Character(27, "A27-C02", "Moraelyn", "memory architect", "clinical, compassionate", "protect Velorin", "causing harm", "white coat, silver hair", "female, controlled"),

    Character(28, "A28-C01", "Seyrane", "protagonist", "determined, tired", "deliver the message", "failure", "travel coat, red scarf", "female, resilient"),
    Character(28, "A28-C02", "Avielon", "message sender", "gentle, mysterious", "reach his family", "being forgotten", "seen only in memories", "male, soft"),

    Character(29, "A29-C01", "Oryven", "protagonist", "defensive, lonely", "learn trust", "betrayal", "dark jacket, gray eyes", "male, guarded"),
    Character(29, "A29-C02", "Veyalia", "companion", "patient, firm", "build healthy trust", "losing herself", "long dark hair", "female, confident"),

    Character(30, "A30-C01", "Lumiren", "protagonist", "lonely, introspective", "accept his memories", "pain", "white hair, dark coat", "male, quiet"),
    Character(30, "A30-C02", "Aeralyn", "guide", "gentle, mysterious", "guide Lumiren", "being forgotten", "pale blue hair", "female, ethereal"),
    Character(30, "A30-C03", "Veynora", "memory figure", "intense, emotional", "force Lumiren to remember", "disappearing", "dark mirrored appearance", "female, haunting"),
]


def get_characters(anime_id: int) -> List[Dict]:
    return [
        asdict(character)
        for character in CHARACTERS
        if character.anime_id == anime_id
    ]


def all_characters() -> List[Dict]:
    return [asdict(character) for character in CHARACTERS]


def validate_unique_names() -> Dict[str, object]:
    names = [c.name for c in CHARACTERS]
    return {
        "character_count": len(names),
        "unique_names": len(names) == len(set(names)),
        "valid": len(names) == len(set(names)),
    }


if __name__ == "__main__":
    print(validate_unique_names())
