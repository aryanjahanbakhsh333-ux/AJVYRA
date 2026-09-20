function sanitizeNumber(
    value,
    fallback = 0,
    minimum = 0,
    maximum = Number.MAX_SAFE_INTEGER
) {

    const number =
        Number(value);

    if (!Number.isFinite(number)) {
        return fallback;
    }

    return Math.min(
        maximum,
        Math.max(
            minimum,
            number
        )
    );
}


function sanitizeSaveData(data) {

    if (
        !data ||
        typeof data !== "object"
    ) {
        return null;
    }

    return {

        version:
            sanitizeNumber(
                data.version,
                1,
                1,
                100
            ),

        level:
            sanitizeNumber(
                data.level,
                1,
                1,
                70
            ),

        score:
            sanitizeNumber(
                data.score,
                0,
                0,
                999999999
            ),

        unlockedLevels:
            Array.isArray(
                data.unlockedLevels
            )
                ? data.unlockedLevels
                    .filter(
                        level =>
                            Number.isInteger(
                                level
                            ) &&
                            level >= 1 &&
                            level <= 70
                    )
                : [1]
    };
}
