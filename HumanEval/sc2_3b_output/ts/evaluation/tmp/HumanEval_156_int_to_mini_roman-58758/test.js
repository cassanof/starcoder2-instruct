//Given a positive integer, obtain its roman numeral equivalent as a string,
// and return it in lowercase.
// Restrictions: 1 <= num <= 1000
// Examples:
// >>> int_to_mini_roman(19)
// "xix"
// >>> int_to_mini_roman(152)
// "clii"
// >>> int_to_mini_roman(426)
// "cdxxvi"
function int_to_mini_roman(number) {
    var romanNumerals = {
        1: "I", 4: "IV", 5: "V", 9: "IX",
        10: "X", 40: "XL", 50: "L", 90: "XC",
        100: "C", 400: "CD", 500: "D", 900: "CM",
        1000: "M"
    };
    var result = "";
    var num = number;
    while (num > 0) {
        var key = Math.floor(num % 10);
        if (key > 0 && key <= 4) {
            result += romanNumerals[key];
            num -= key;
        }
        else if (key > 4 && key <= 9) {
            result += romanNumerals[key - 5];
            num -= key - 5;
        }
        else if (key > 9) {
            result += romanNumerals[key - 10];
            num -= key - 10;
        }
    }
    return result.toLowerCase();
}
var assert = require('node:assert');
function test() {
    var candidate = int_to_mini_roman;
    assert.deepEqual(candidate(19), "xix");
    assert.deepEqual(candidate(152), "clii");
    assert.deepEqual(candidate(251), "ccli");
    assert.deepEqual(candidate(426), "cdxxvi");
    assert.deepEqual(candidate(500), "d");
    assert.deepEqual(candidate(1), "i");
    assert.deepEqual(candidate(4), "iv");
    assert.deepEqual(candidate(43), "xliii");
    assert.deepEqual(candidate(90), "xc");
    assert.deepEqual(candidate(94), "xciv");
    assert.deepEqual(candidate(532), "dxxxii");
    assert.deepEqual(candidate(900), "cm");
    assert.deepEqual(candidate(994), "cmxciv");
    assert.deepEqual(candidate(1000), "m");
}
test();
