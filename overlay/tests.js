var testUsers = ['clickandslash', 'ggpalma', 'sirteclas', 'tomatefey', 'zeroretr0', 'steyb'];
var testWins = 0;
var testSkips = 0;
var testsEnabled = true;

/**
 * Return a random user from testUsers list
 */
function testGetRandomUserName() {
    return testUsers[Math.floor(Math.random() * testUsers.length)];
}

/**
 * Returns a randomly generated SMM2 legal level code
 */
function testCreateLevelCode() {
    var result           = '';
    var characters       = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < 11; i++ ) {
        if ((i + 1) % 4 == 0 && i != 0) {
            result += "-";
        } else {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
    }
    return result;
}

/**
 * Simulates a level win
 * @param {int} levelsReturned 0 for empty - 1 for current level only - 2 for both current and next levels
 */
function testWinLevel(levelsReturned) {
    testWins += 1;
    testUpdateUIRandom(levelsReturned);
}

/**
 * Simulates a level skip
 * @param {int} levelsReturned 0 for empty - 1 for current level only - 2 for both current and next levels
 */
function testSkipLevel(levelsReturned) {
    testSkips += 1;
    testUpdateUIRandom(levelsReturned);
}

/**
 * Forces UI update with random data depending on levelsReturned specified
 * @param {int} levelsReturned 0 for empty - 1 for current level only - 2 for both current and next levels
 */
function testUpdateUIRandom(levelsReturned) {
    var testJsonData = '{"currentLevelCode": "' + ((levelsReturned >= 1) ? testCreateLevelCode() : "") + '", ' +
                        '"currentLevelUser": "' + ((levelsReturned >= 1) ? testGetRandomUserName() : "") + '", ' +
                        '"nextLevelCode": "' + ((levelsReturned >= 2) ? testCreateLevelCode() : "") + '", ' +
                        '"nextLevelUser": "' + ((levelsReturned >= 2) ? testGetRandomUserName() : "") + '", ' +
                        '"wins": ' + testWins +', ' +
                        '"skips": ' + testSkips + '}';

    updateUI(testJsonData);
}