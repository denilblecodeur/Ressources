mint refhash = 0;
for (int i = 0; i < hp; i++) {
    for (int j = 0; j < wp; j++) {
        refhash += mint(pattern[i][j]) * (mint(A) ^ (wp * i + j));
    }
}
vector<vector<mint>> hash1d(hm, vector<mint>());
for (int i = 0; i < hm; i++) {
    mint current_hash = 0;
    for (int j = 0; j < wp; j++) {
        current_hash += mint(masterpiece[i][j]) * (mint(A) ^ j);
    }
    hash1d[i].push_back(current_hash);
    for (int j = wp; j < wm; j++) {
        current_hash = (current_hash - mint(masterpiece[i][j - wp])) * invA + mint(masterpiece[i][j]) * (mint(A) ^ (wp - 1));
        hash1d[i].push_back(current_hash);
    }
}
vector<vector<mint>> hash2d(hm - hp + 1, vector<mint>(wm - wp + 1, mint(0)));
for (int j = wp; j <= wm; j++) {
    mint current_hash = 0;
    for (int i = 0; i < hp; i++) {
        current_hash += hash1d[i][j - wp] * (mint(A) ^ (i * wp));
    }
    hash2d[0][j - wp] = current_hash;
}
for (int i = hp; i < hm; i++) {
    for (int j = wp; j <= wm; j++) {
        hash2d[i - hp + 1][j - wp] = (hash2d[i - hp][j - wp] - hash1d[i - hp][j - wp]) * (mint(invA) ^ wp)
                                        + hash1d[i][j - wp] * (mint(A) ^ (wp * (hp - 1)));
    }
}
int matches = 0;
for (int i = 0; i <= hm - hp; i++) {
    for (int j = 0; j <= wm - wp; j++) {
        if (hash2d[i][j] == refhash) {
            matches++;
        }
    }
}
cout << matches << endl;