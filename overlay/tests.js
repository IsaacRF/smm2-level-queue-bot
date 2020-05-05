var testUsers = ['clickandslash', 'ggpalma', 'sirteclas', 'tomatefey', 'zeroretr0', 'steyb'];
var testWins = 0;
var testSkips = 0;
var testLevels = [];
var testCurrentLevelPosition = 0;
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
function testGenerateRandomLevelCode() {
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
 * Test initialization
 * @param {int} levelsNumber Number of levels to generate
 */
function testInit(levelsNumber) {
    testLevels = [];
    testAddLevel(levelsNumber);
    testUpdateUI();
}

/**
 * Simulates a level win
 */
function testWinLevel() {
    if (testLevels.length > 0) {
        testWins += 1;
        testLevels.shift();
        testUpdateUI();
        console.log(testLevels.length + " niveles más en la lista");
    } else {
        console.log("No hay niveles, no se han modificado los contadores ni la UI");
    }
}

/**
 * Simulates a level skip
 */
function testSkipLevel() {
    if (testLevels.length > 0) {
        testSkips += 1;
        testLevels.shift();
        testUpdateUI();
        console.log(testLevels.length + " niveles más en la lista");
    } else {
        console.log("No hay niveles, no se han modificado los contadores ni la UI");
    }
}

/**
 * Generates specified number of random levels and adds them to list. Updates UI only
 * if there are 1 or less levels remaining in list.
 * @param {int} levelsNumber Number of levels to add to list. Default is 1.
 */
function testAddLevel(levelsNumber=1) {
    var isUpdateUIRequired = (testLevels.length <= 1);

    for (let i = 0; i < levelsNumber; i++) {
        testLevels.push(new TestLevel());
    }

    if (isUpdateUIRequired) {
        testUpdateUI();
    }
}

/**
 * Updates UI with next levels in list
 */
function testUpdateUI() {
    var testJsonData = '{"currentLevelCode": "' + (testLevels.length >= 1 ? testLevels[0].code : "") + '", ' +
                        '"currentLevelUser": "' + (testLevels.length >= 1 ? testLevels[0].user : "") + '", ' +
                        '"nextLevelCode": "' + (testLevels.length >= 2 ? testLevels[1].code : "") + '", ' +
                        '"nextLevelUser": "' + (testLevels.length >= 2 ? testLevels[1].user : "") + '", ' +
                        '"wins": ' + testWins +', ' +
                        '"skips": ' + testSkips + '}';

    updateUI(testJsonData);
}

/**
 * Forces UI update with random data depending on levelsReturned specified
 * @param {int} levelsReturned 0 for empty - 1 for current level only - 2 for both current and next levels
 */
function testUpdateUIRandom(levelsReturned) {
    var testJsonData = '{"currentLevelCode": "' + ((levelsReturned >= 1) ? testGenerateRandomLevelCode() : "") + '", ' +
                        '"currentLevelUser": "' + ((levelsReturned >= 1) ? testGetRandomUserName() : "") + '", ' +
                        '"nextLevelCode": "' + ((levelsReturned >= 2) ? testGenerateRandomLevelCode() : "") + '", ' +
                        '"nextLevelUser": "' + ((levelsReturned >= 2) ? testGetRandomUserName() : "") + '", ' +
                        '"wins": ' + testWins +', ' +
                        '"skips": ' + testSkips + '}';

    updateUI(testJsonData);
}

class TestLevel {
    constructor() {
        this.code = testGenerateRandomLevelCode();
        this.user = testGetRandomUserName();
    }
}