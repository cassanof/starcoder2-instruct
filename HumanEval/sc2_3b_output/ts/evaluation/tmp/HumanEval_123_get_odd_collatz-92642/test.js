//Given a positive integer n, return a sorted array that has the odd numbers in collatz sequence.
// The Collatz conjecture is a conjecture in mathematics that concerns a sequence defined
// as follows: start with any positive integer n. Then each term is obtained from the 
// previous term as follows: if the previous term is even, the next term is one half of 
// the previous term. If the previous term is odd, the next term is 3 times the previous
// term plus 1. The conjecture is that no matter what value of n, the sequence will always reach 1.
// Note: 
// 1. Collatz(1) is [1].
// 2. returned array sorted in increasing order.
// For example:
// get_odd_collatz(5) returns [1, 5] # The collatz sequence for 5 is [5, 16, 8, 4, 2, 1], so the odd numbers are only 1, and 5.
// >>> get_odd_collatz(5)
// [1, 5]
function get_odd_collatz(n) {
    var collatz = [1];
    var current = 1;
    while (current <= n) {
        if (current % 2 === 0) {
            current = current / 2;
        }
        else {
            current = 3 * current + 1;
        }
        collatz.push(current);
    }
    return collatz.sort(function (a, b) { return a - b; });
}
var assert = require('node:assert');
function test() {
    var candidate = get_odd_collatz;
    assert.deepEqual(candidate(14), [1, 5, 7, 11, 13, 17]);
    assert.deepEqual(candidate(5), [1, 5]);
    assert.deepEqual(candidate(12), [1, 3, 5]);
    assert.deepEqual(candidate(1), [1]);
}
test();
