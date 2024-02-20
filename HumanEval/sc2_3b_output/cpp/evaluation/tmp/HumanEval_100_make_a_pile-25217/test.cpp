#include<stdlib.h>
#include<algorithm>
#include<math.h>
#include<stdio.h>
#include<vector>
#include<string>
#include<climits>
#include<cstring>
#include<iostream>
#include<cassert>

#include<assert.h>
#include<bits/stdc++.h>
// Given a positive integer n, you have to make a pile of n levels of stones.
// The first level has n stones.
// The number of stones in the next level is:
// - the next odd number if n is odd.
// - the next even number if n is even.
// Return the number of stones in each level in a vector, where element at index
// i represents the number of stones in the level (i+1).
// Examples:
// >>> make_a_pile((3))
// (std::vector<long>({(long)3, (long)5, (long)7}))
std::vector<long> make_a_pile(long n) {
    std::vector<long> result;
    long current = n;
    while (current > 0) {
        result.push_back(current);
        if (current % 2 == 0) {
            current = current / 2;
        } else {
            current = current * 3 + 1;
        }
    }
    return result;

}
int main() {
    auto candidate = make_a_pile;
    assert(candidate((3)) == (std::vector<long>({(long)3, (long)5, (long)7})));
    assert(candidate((4)) == (std::vector<long>({(long)4, (long)6, (long)8, (long)10})));
    assert(candidate((5)) == (std::vector<long>({(long)5, (long)7, (long)9, (long)11, (long)13})));
    assert(candidate((6)) == (std::vector<long>({(long)6, (long)8, (long)10, (long)12, (long)14, (long)16})));
    assert(candidate((8)) == (std::vector<long>({(long)8, (long)10, (long)12, (long)14, (long)16, (long)18, (long)20, (long)22})));
}
