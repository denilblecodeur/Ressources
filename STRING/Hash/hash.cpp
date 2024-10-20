/*
https://stackoverflow.com/questions/664014/what-integer-hash-function-are-good-that-accepts-an-integer-hash-key

In python don't forget to take every result modulo 2^32 or 2^64
*/

// 32-bit
unsigned int hash(unsigned int x) {
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = (x >> 16) ^ x;
    return x;
}
unsigned int unhash(unsigned int x) {
    x = ((x >> 16) ^ x) * 0x119de1f3;
    x = ((x >> 16) ^ x) * 0x119de1f3;
    x = (x >> 16) ^ x;
    return x;
}

// 64-bit
uint64_t hash(uint64_t x) {
    x = (x ^ (x >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
    x = (x ^ (x >> 27)) * UINT64_C(0x94d049bb133111eb);
    x = x ^ (x >> 31);
    return x;
}
uint64_t unhash(uint64_t x) {
    x = (x ^ (x >> 31) ^ (x >> 62)) * UINT64_C(0x319642b2d24d8ec3);
    x = (x ^ (x >> 27) ^ (x >> 54)) * UINT64_C(0x96de1b173f119089);
    x = x ^ (x >> 30) ^ (x >> 60);
    return x;
}

/*

MOD = 1 << 64

def hash(x):
    x = ((x ^ (x >> 30)) * 0xbf58476d1ce4e5b9) % MOD
    x = ((x ^ (x >> 27)) * 0x94d049bb133111eb) % MOD
    x = (x ^ (x >> 31)) % MOD
    return x

def unhash(x):
    x = ((x ^ (x >> 31) ^ (x >> 62)) * 0x319642b2d24d8ec3) % MOD
    x = ((x ^ (x >> 27) ^ (x >> 54)) * 0x96de1b173f119089) % MOD
    x = (x ^ (x >> 30) ^ (x >> 60)) % MOD
    return x

def hash2(x):
    x = ((x ^ (x >> 33)) * 0xff51afd7ed558ccd) % MOD
    x = ((x ^ (x >> 33)) * 0xc4ceb9fe1a85ec53) % MOD
    x = ((x ^ (x >> 33))) % MOD
    return x

def unhash2(x):
    x = ((x ^ (x >> 33)) * 0x9cb4b2f8129337db) % MOD
    x = ((x ^ (x >> 33)) * 0x4f74430c22a54005) % MOD
    x = (x ^ (x >> 33)) % MOD
    return x

*/