class AJVYRAWebGameplayTemplates {
    static get supportedModes() {
        return [
            "action",
            "racing",
            "fighting",
            "rpg",
            "survival",
            "shooter",
            "adventure",
            "strategy",
            "horror",
            "puzzle",
            "boss"
        ];
    }

    static validate(game) {
        if (!game?.id) {
            throw new Error(
                "Game ID is missing."
            );
        }

        if (
            !this.supportedModes.includes(
                game.mode
            )
        ) {
            throw new Error(
                `Unsupported game mode: ${game.mode}`
            );
        }

        if (
            !Number.isFinite(
                game.objectiveTotal
            ) ||
            game.objectiveTotal <= 0
        ) {
            throw new Error(
                `Invalid objective count: ${game.id}`
            );
        }

        return true;
    }

    static validateAll(games) {
        for (const game of games) {
            this.validate(game);
        }

        return {
            valid: true,
            count: games.length
        };
    }
}

window.AJVYRAWebGameplayTemplates =
    AJVYRAWebGameplayTemplates;
