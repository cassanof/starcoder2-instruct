//Given a positive integer n, return an array that has the number of even and odd
// integer palindromes that fall within the range(1, n), inclusive.
// Example 1:
// >>> even_odd_palindrome(3)
// [1, 2]
// Explanation:
// Integer palindrome are 1, 2, 3. one of them is even, and two of them are odd.
// Example 2:
// >>> even_odd_palindrome(12)
// [4, 6]
// Explanation:
// Integer palindrome are 1, 2, 3, 4, 5, 6, 7, 8, 9, 11. four of them are even, and 6 of them are odd.
// Note:
// 1. 1 <= n <= 10^3
// 2. returned array has the number of even and odd integer palindromes respectively.
function even_odd_palindrome(n: number): [number, number] {
    const arr: number[] = [];
    for (let i = 1; i <= n; i++) {
        let isPalindrome = true;
        let reverse = 0;
        while (i > 0) {
            if (i % 10!== reverse % 10) {
                isPalindrome = false;
                break;
            }
            reverse = reverse * 10 + i % 10;
            i = Math.floor(i / 10);
        }
        if (isPalindrome) {
            arr.push(i);
        }
    }
    return [arr.length, arr.filter(x => x % 2 === 0).length];
}

declare var require: any;
const assert = require('node:assert');


function test() {
  let candidate = even_odd_palindrome;
  assert.deepEqual(candidate(123),[8, 13]);
  assert.deepEqual(candidate(12),[4, 6]);
  assert.deepEqual(candidate(3),[1, 2]);
  assert.deepEqual(candidate(63),[6, 8]);
  assert.deepEqual(candidate(25),[5, 6]);
  assert.deepEqual(candidate(19),[4, 6]);
  assert.deepEqual(candidate(9),[4, 5]);
  assert.deepEqual(candidate(1),[0, 1]);
}

test();